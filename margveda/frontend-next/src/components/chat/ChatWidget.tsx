"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  X, Send, Sparkles, RotateCcw, Loader2,
  BookOpen, Calendar, ChevronDown, BadgeCheck, ExternalLink,
} from "lucide-react";
import Link from "next/link";

// ── Types ─────────────────────────────────────────────────────────────────────

interface Citation { index: number; title: string; domain: string; score: number; }

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  suggestions?: string[];
  citations?: Citation[];
  needs_counselor?: boolean;
  counselor_reason?: string;
  from_cache?: boolean;
  latency_ms?: number;
  timestamp: number;
}

interface ChatWidgetProps {
  open: boolean;
  onClose: () => void;
  title?: string;
}

// ── Constants ─────────────────────────────────────────────────────────────────

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

const DOMAIN_COLORS: Record<string, string> = {
  career:     "bg-violet-100 text-violet-700 border-violet-200",
  college:    "bg-blue-100 text-blue-700 border-blue-200",
  exam:       "bg-amber-100 text-amber-700 border-amber-200",
  scholarship:"bg-green-100 text-green-700 border-green-200",
  salary:     "bg-emerald-100 text-emerald-700 border-emerald-200",
  skills:     "bg-cyan-100 text-cyan-700 border-cyan-200",
  timeline:   "bg-orange-100 text-orange-700 border-orange-200",
  faq:        "bg-gray-100 text-gray-700 border-gray-200",
  counsellor: "bg-pink-100 text-pink-700 border-pink-200",
  govt_jobs:  "bg-indigo-100 text-indigo-700 border-indigo-200",
};

const QUICK_PROMPTS = [
  "Which career suits me after Class 12 PCM?",
  "Compare IIT vs NIT — which should I target?",
  "How do I prepare for UPSC Civil Services?",
  "Best government jobs after graduation?",
  "Scholarships available for OBC students?",
  "Software engineer salary in India 2025?",
];

const WELCOME: Message = {
  id: "welcome",
  role: "assistant",
  content: `**Hello! I'm CareerVeda**, your AI career counsellor from CareerBrownie.\n\nI can help you with:\n- **Careers** — engineering, medicine, law, civil services, design & more\n- **Colleges** — IITs, NITs, IIMs, medical colleges, state universities\n- **Entrance Exams** — JEE, NEET, CAT, UPSC, SSC, NDA, GATE & more\n- **Scholarships** — central, state, and international funding\n- **Government Jobs** — UPSC, SSC, Banking, Defence, Railways, Teaching\n- **Salary & Skills** — market rates, skill roadmaps, certifications\n\nWhat would you like to explore today?`,
  timestamp: Date.now(),
};

// ── Helpers ───────────────────────────────────────────────────────────────────

function uid() { return Math.random().toString(36).slice(2, 10); }

function getSessionId() {
  if (typeof window === "undefined") return uid();
  let sid = sessionStorage.getItem("cb_session_id");
  if (!sid) { sid = uid(); sessionStorage.setItem("cb_session_id", sid); }
  return sid;
}

// ── Simple markdown renderer ──────────────────────────────────────────────────

function renderMarkdown(text: string): React.ReactNode[] {
  const lines = text.split("\n");
  const nodes: React.ReactNode[] = [];
  let i = 0;

  while (i < lines.length) {
    const line = lines[i];

    // H3
    if (line.startsWith("### ")) {
      nodes.push(<h3 key={i} className="font-bold text-gray-900 text-sm mt-3 mb-1">{inlineFormat(line.slice(4))}</h3>);
      i++; continue;
    }
    // H2
    if (line.startsWith("## ")) {
      nodes.push(<h2 key={i} className="font-bold text-gray-900 text-sm mt-3 mb-1">{inlineFormat(line.slice(3))}</h2>);
      i++; continue;
    }
    // Horizontal rule
    if (line === "---") {
      nodes.push(<hr key={i} className="my-2 border-gray-200" />);
      i++; continue;
    }
    // Numbered list
    const numMatch = line.match(/^(\d+)\.\s+(.+)/);
    if (numMatch) {
      const items: React.ReactNode[] = [];
      while (i < lines.length && lines[i].match(/^\d+\.\s+/)) {
        const m = lines[i].match(/^\d+\.\s+(.+)/);
        items.push(<li key={i} className="ml-1">{inlineFormat(m![1])}</li>);
        i++;
      }
      nodes.push(<ol key={`ol-${i}`} className="list-decimal list-inside space-y-0.5 my-1 text-sm text-gray-800">{items}</ol>);
      continue;
    }
    // Bullet list
    if (line.match(/^[-•]\s+/)) {
      const items: React.ReactNode[] = [];
      while (i < lines.length && lines[i].match(/^[-•]\s+/)) {
        const content = lines[i].replace(/^[-•]\s+/, "");
        items.push(<li key={i} className="ml-1">{inlineFormat(content)}</li>);
        i++;
      }
      nodes.push(<ul key={`ul-${i}`} className="list-disc list-inside space-y-0.5 my-1 text-sm text-gray-800">{items}</ul>);
      continue;
    }
    // Empty line → spacer
    if (line.trim() === "") {
      nodes.push(<div key={i} className="h-1" />);
      i++; continue;
    }
    // Regular paragraph
    nodes.push(<p key={i} className="text-sm text-gray-800 leading-relaxed">{inlineFormat(line)}</p>);
    i++;
  }
  return nodes;
}

function inlineFormat(text: string): React.ReactNode {
  // Process **bold**, *italic*, `code`, and [N] citations
  const parts = text.split(/(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`|\[\d+\])/g);
  return parts.map((part, i) => {
    if (part.startsWith("**") && part.endsWith("**"))
      return <strong key={i} className="font-semibold text-gray-900">{part.slice(2, -2)}</strong>;
    if (part.startsWith("*") && part.endsWith("*"))
      return <em key={i}>{part.slice(1, -1)}</em>;
    if (part.startsWith("`") && part.endsWith("`"))
      return <code key={i} className="bg-gray-100 text-violet-700 px-1 rounded text-xs font-mono">{part.slice(1, -1)}</code>;
    if (/^\[\d+\]$/.test(part))
      return <sup key={i} className="inline-flex items-center justify-center w-4 h-4 bg-violet-100 text-violet-700 text-[10px] font-bold rounded-full ml-0.5 cursor-default">{part}</sup>;
    return part;
  });
}

// ── Sub-components ────────────────────────────────────────────────────────────

function TypingDots() {
  return (
    <div className="flex items-center gap-1 px-4 py-3">
      {[0, 1, 2].map((i) => (
        <span key={i} className="w-2 h-2 rounded-full bg-violet-400 animate-bounce"
          style={{ animationDelay: `${i * 0.15}s` }} />
      ))}
    </div>
  );
}

function CitationBar({ citations }: { citations: Citation[] }) {
  const [expanded, setExpanded] = useState(false);
  if (!citations?.length) return null;
  const shown = expanded ? citations : citations.slice(0, 2);

  return (
    <div className="mt-2 pt-2 border-t border-gray-100">
      <button onClick={() => setExpanded(!expanded)}
        className="flex items-center gap-1 text-xs text-gray-400 hover:text-gray-600 mb-1.5 transition-colors">
        <BookOpen className="w-3 h-3" />
        <span>{citations.length} source{citations.length > 1 ? "s" : ""} used</span>
        <ChevronDown className={`w-3 h-3 transition-transform ${expanded ? "rotate-180" : ""}`} />
      </button>
      <div className="flex flex-wrap gap-1">
        {shown.map((c) => (
          <span key={c.index}
            className={`inline-flex items-center gap-1 text-[10px] font-medium px-2 py-0.5 rounded-full border ${DOMAIN_COLORS[c.domain] ?? "bg-gray-100 text-gray-600 border-gray-200"}`}>
            <span className="opacity-60">[{c.index}]</span>
            {c.title.length > 22 ? c.title.slice(0, 22) + "…" : c.title}
            <span className="opacity-50">{Math.round(c.score * 100)}%</span>
          </span>
        ))}
        {!expanded && citations.length > 2 && (
          <span className="text-[10px] text-gray-400 self-center">+{citations.length - 2} more</span>
        )}
      </div>
    </div>
  );
}

function CounselorCard({ reason }: { reason?: string }) {
  return (
    <motion.div initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }}
      className="mt-3 bg-gradient-to-r from-violet-50 to-purple-50 border border-violet-200 rounded-xl p-3">
      <div className="flex items-start gap-2">
        <div className="w-7 h-7 rounded-lg bg-violet-100 flex items-center justify-center shrink-0">
          <BadgeCheck className="w-4 h-4 text-violet-600" />
        </div>
        <div className="flex-1 min-w-0">
          <p className="text-xs font-semibold text-violet-900">
            Talk to a Human Counsellor
          </p>
          <p className="text-xs text-violet-700 mt-0.5 leading-relaxed">
            {reason || "This question may benefit from personalised 1-on-1 expert guidance."}
          </p>
          <div className="flex gap-2 mt-2">
            <Link href="/student/sessions/book"
              className="inline-flex items-center gap-1 text-xs font-medium bg-violet-600 hover:bg-violet-700 text-white px-2.5 py-1 rounded-lg transition-colors">
              <Calendar className="w-3 h-3" />
              Book Session
            </Link>
            <Link href="/counsellors"
              className="inline-flex items-center gap-1 text-xs font-medium text-violet-600 hover:text-violet-800 border border-violet-300 px-2.5 py-1 rounded-lg transition-colors">
              <ExternalLink className="w-3 h-3" />
              Browse Counsellors
            </Link>
          </div>
        </div>
      </div>
    </motion.div>
  );
}

function MessageBubble({ msg, onAction }: { msg: Message; onAction: (t: string) => void }) {
  const isUser = msg.role === "user";

  if (isUser) {
    return (
      <div className="flex justify-end">
        <div className="max-w-[82%] px-4 py-2.5 bg-violet-600 text-white rounded-2xl rounded-tr-sm text-sm leading-relaxed">
          {msg.content}
        </div>
      </div>
    );
  }

  return (
    <div className="flex gap-2.5">
      <div className="w-7 h-7 rounded-full bg-gradient-to-br from-violet-500 to-purple-700 flex items-center justify-center flex-shrink-0 mt-0.5 shadow-sm">
        <Sparkles className="w-3.5 h-3.5 text-white" />
      </div>
      <div className="max-w-[85%] flex flex-col gap-1">
        <div className="bg-white border border-gray-100 shadow-sm rounded-2xl rounded-tl-sm px-4 py-3">
          <div className="space-y-1">
            {renderMarkdown(msg.content)}
          </div>

          {/* Citations */}
          {msg.citations && msg.citations.length > 0 && (
            <CitationBar citations={msg.citations} />
          )}
        </div>

        {/* Counselor escalation card */}
        {msg.needs_counselor && (
          <CounselorCard reason={msg.counselor_reason} />
        )}

        {/* Suggested follow-ups */}
        {msg.suggestions && msg.suggestions.length > 0 && (
          <div className="flex flex-wrap gap-1.5 mt-0.5">
            {msg.suggestions.map((s, i) => (
              <button key={i} onClick={() => onAction(s)}
                className="text-[11px] bg-violet-50 hover:bg-violet-100 text-violet-700 border border-violet-200 px-2.5 py-1 rounded-full transition-colors font-medium text-left leading-tight">
                {s.length > 55 ? s.slice(0, 55) + "…" : s}
              </button>
            ))}
          </div>
        )}

        {/* Latency badge */}
        {msg.latency_ms !== undefined && msg.latency_ms > 0 && (
          <div className="flex items-center gap-1.5">
            {msg.from_cache && (
              <span className="text-[9px] text-gray-300 font-medium uppercase tracking-wide">cached</span>
            )}
            <span className="text-[9px] text-gray-300">{msg.latency_ms < 1000 ? `${msg.latency_ms}ms` : `${(msg.latency_ms / 1000).toFixed(1)}s`}</span>
          </div>
        )}
      </div>
    </div>
  );
}

// ── ChatWidget (main) ─────────────────────────────────────────────────────────

export default function ChatWidget({ open, onClose, title = "CareerVeda AI" }: ChatWidgetProps) {
  const [messages, setMessages] = useState<Message[]>([WELCOME]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [domain, setDomain] = useState<string | null>(null);
  const bottomRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);
  const sessionId = useRef(getSessionId());

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  useEffect(() => {
    if (open) setTimeout(() => inputRef.current?.focus(), 120);
  }, [open]);

  const sendMessage = useCallback(async (text: string) => {
    const trimmed = text.trim();
    if (!trimmed || loading) return;

    setInput("");
    setError(null);
    const userMsg: Message = { id: uid(), role: "user", content: trimmed, timestamp: Date.now() };
    setMessages((prev) => [...prev, userMsg]);
    setLoading(true);

    const history = messages
      .filter((m) => m.id !== "welcome")
      .map((m) => ({ role: m.role, content: m.content }));

    const MAX_RETRIES = 3;
    const RETRY_DELAY_MS = 3000;

    for (let attempt = 0; attempt < MAX_RETRIES; attempt++) {
      try {
        if (attempt > 0) {
          await new Promise((resolve) => setTimeout(resolve, RETRY_DELAY_MS));
        }

        const res = await fetch(`${API_URL}/chatbot/public-chat`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ message: trimmed, history, domain }),
        });

        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();

        const aiMsg: Message = {
          id: uid(),
          role: "assistant",
          content: data.reply || "I'm not sure about that. You can book a free counselling session for personalised guidance.",
          suggestions: data.suggested_actions ?? [],
          citations: data.citations ?? [],
          needs_counselor: data.needs_counselor ?? false,
          counselor_reason: data.counselor_reason ?? "",
          from_cache: data.from_cache ?? false,
          latency_ms: data.latency_ms ?? 0,
          timestamp: Date.now(),
        };
        setMessages((prev) => [...prev, aiMsg]);
        setLoading(false);
        return;
      } catch {
        // Network error — will retry after delay
      }
    }

    // All retries exhausted — show helpful message
    setError("I'm having trouble connecting to the AI service. Please try again in a moment. You can also book a free counselling session.");
    setLoading(false);
  }, [loading, messages, domain]);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); sendMessage(input); }
  };

  const reset = () => {
    sessionId.current = uid();
    sessionStorage.setItem("cb_session_id", sessionId.current);
    setMessages([WELCOME]);
    setError(null);
    setDomain(null);
  };

  if (!open) return null;

  const DOMAIN_FILTERS = [
    { label: "All", value: null },
    { label: "Careers", value: "career" },
    { label: "Colleges", value: "college" },
    { label: "Exams", value: "exam" },
    { label: "Govt Jobs", value: "govt_jobs" },
    { label: "Scholarships", value: "scholarship" },
    { label: "Salary", value: "salary" },
  ];

  return (
    <>
      {/* Mobile overlay */}
      <div className="fixed inset-0 bg-black/50 z-40 md:hidden" onClick={onClose} aria-hidden />

      {/* Chat panel */}
      <motion.div
        role="dialog"
        aria-label="CareerVeda AI Chat"
        initial={{ opacity: 0, y: 20, scale: 0.97 }}
        animate={{ opacity: 1, y: 0, scale: 1 }}
        exit={{ opacity: 0, y: 20, scale: 0.97 }}
        transition={{ duration: 0.2, ease: "easeOut" }}
        className="fixed z-50 flex flex-col bg-gray-50
          inset-0 md:inset-auto
          md:bottom-6 md:right-6 md:w-[420px] md:h-[650px]
          md:rounded-2xl overflow-hidden shadow-2xl border border-gray-200"
      >
        {/* ── Header ── */}
        <div className="flex items-center gap-3 px-4 py-3 bg-gradient-to-r from-violet-700 to-purple-800 text-white flex-shrink-0">
          <div className="w-9 h-9 rounded-xl bg-white/15 flex items-center justify-center border border-white/20">
            <Sparkles className="w-4.5 h-4.5" />
          </div>
          <div className="flex-1 min-w-0">
            <p className="font-semibold text-sm">{title}</p>
            <div className="flex items-center gap-1.5 mt-0.5">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
              <p className="text-[11px] text-white/70">AI Career Counsellor · Available 24/7</p>
            </div>
          </div>
          <div className="flex items-center gap-1">
            <button onClick={reset} title="New conversation"
              className="p-1.5 rounded-lg hover:bg-white/15 transition-colors">
              <RotateCcw className="w-4 h-4" />
            </button>
            <button onClick={onClose} title="Close"
              className="p-1.5 rounded-lg hover:bg-white/15 transition-colors">
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* ── Domain filter ── */}
        <div className="flex gap-1.5 px-3 py-2 bg-white border-b border-gray-100 overflow-x-auto scrollbar-hide flex-shrink-0">
          {DOMAIN_FILTERS.map((f) => (
            <button key={String(f.value)} onClick={() => setDomain(f.value)}
              className={`text-[11px] font-medium px-2.5 py-1 rounded-full border whitespace-nowrap transition-all flex-shrink-0 ${
                domain === f.value
                  ? "bg-violet-600 text-white border-violet-600 shadow-sm"
                  : "bg-gray-50 text-gray-600 border-gray-200 hover:border-violet-300 hover:text-violet-600"
              }`}>
              {f.label}
            </button>
          ))}
        </div>

        {/* ── Messages ── */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {/* Quick prompts */}
          {messages.length === 1 && (
            <div>
              <p className="text-[10px] text-gray-400 font-semibold uppercase tracking-wider mb-2">
                Try asking
              </p>
              <div className="grid grid-cols-1 gap-1.5">
                {QUICK_PROMPTS.map((p) => (
                  <button key={p} onClick={() => sendMessage(p)}
                    className="text-left text-xs text-gray-700 bg-white border border-gray-200 hover:border-violet-300 hover:bg-violet-50 hover:text-violet-700 px-3 py-2 rounded-xl transition-all">
                    {p}
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Message list */}
          <AnimatePresence initial={false}>
            {messages.map((msg) => (
              <motion.div key={msg.id}
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.18 }}>
                <MessageBubble msg={msg} onAction={sendMessage} />
              </motion.div>
            ))}
          </AnimatePresence>

          {/* Typing indicator */}
          {loading && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex gap-2.5">
              <div className="w-7 h-7 rounded-full bg-gradient-to-br from-violet-500 to-purple-700 flex items-center justify-center flex-shrink-0 shadow-sm">
                <Sparkles className="w-3.5 h-3.5 text-white" />
              </div>
              <div className="bg-white border border-gray-100 rounded-2xl rounded-tl-sm shadow-sm">
                <TypingDots />
              </div>
            </motion.div>
          )}

          {/* Error */}
          {error && (
            <div className="text-xs text-red-600 bg-red-50 border border-red-200 rounded-xl px-3 py-2">
              {error}
            </div>
          )}

          <div ref={bottomRef} />
        </div>

        {/* ── Input ── */}
        <div className="flex-shrink-0 bg-white border-t border-gray-200 p-3">
          <div className="flex items-end gap-2 bg-gray-50 border border-gray-200 rounded-2xl px-3 py-2
            focus-within:border-violet-400 focus-within:ring-2 focus-within:ring-violet-100 transition-all">
            <textarea
              ref={inputRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder={domain
                ? `Ask about ${domain.replace("_", " ")}…`
                : "Ask about careers, colleges, exams, govt jobs…"}
              rows={1}
              disabled={loading}
              className="flex-1 resize-none bg-transparent text-sm text-gray-800 placeholder-gray-400 outline-none max-h-32 leading-relaxed disabled:opacity-50"
              style={{ minHeight: "24px" }}
              onInput={(e) => {
                const el = e.currentTarget;
                el.style.height = "auto";
                el.style.height = Math.min(el.scrollHeight, 128) + "px";
              }}
            />
            <button
              onClick={() => sendMessage(input)}
              disabled={!input.trim() || loading}
              className="w-8 h-8 rounded-xl bg-violet-600 hover:bg-violet-700 disabled:bg-gray-200 disabled:cursor-not-allowed flex items-center justify-center transition-colors flex-shrink-0 mb-0.5 shadow-sm">
              {loading
                ? <Loader2 className="w-4 h-4 text-white animate-spin" />
                : <Send className="w-4 h-4 text-white" />
              }
            </button>
          </div>
          <p className="text-center text-[10px] text-gray-400 mt-1.5">
            <kbd className="bg-gray-100 px-1 py-0.5 rounded text-[9px]">Enter</kbd> send ·{" "}
            <kbd className="bg-gray-100 px-1 py-0.5 rounded text-[9px]">Shift+Enter</kbd> newline
          </p>
        </div>
      </motion.div>
    </>
  );
}
