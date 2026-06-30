"use client";

import { useEffect, useRef, useState, useCallback } from "react";
import {
  X, Send, Sparkles, RotateCcw, Loader2,
} from "lucide-react";

// ── Types ─────────────────────────────────────────────────────────────────────

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  actions?: string[];
  timestamp: number;
}

interface ChatWidgetProps {
  open: boolean;
  onClose: () => void;
  /** Optional – name shown in the header */
  title?: string;
}

// ── Constants ─────────────────────────────────────────────────────────────────

const AI_SERVICE_URL =
  process.env.NEXT_PUBLIC_AI_URL || "http://localhost:9000";

const QUICK_PROMPTS = [
  "I'm in Class 12 PCM. Which career should I choose?",
  "Compare engineering vs data science for me",
  "Which colleges are best for Computer Science?",
  "How to prepare for JEE in 6 months?",
  "Find scholarships for OBC students",
];

const WELCOME: Message = {
  id: "welcome",
  role: "assistant",
  content:
    "Hi! I'm Career Brownie AI 👋\n\nI'm your personal career counsellor for Indian students. Ask me anything about careers, colleges, entrance exams, scholarships, or skill development.",
  actions: [
    "Get career recommendations",
    "Best colleges for my score",
    "Find scholarships",
  ],
  timestamp: Date.now(),
};

// ── Helpers ───────────────────────────────────────────────────────────────────

function uid() {
  return Math.random().toString(36).slice(2, 10);
}

function getSessionId() {
  if (typeof window === "undefined") return uid();
  let sid = sessionStorage.getItem("cb_session_id");
  if (!sid) {
    sid = uid();
    sessionStorage.setItem("cb_session_id", sid);
  }
  return sid;
}

// ── TypingIndicator ───────────────────────────────────────────────────────────

function TypingDots() {
  return (
    <div className="flex items-center gap-1 px-4 py-3">
      {[0, 1, 2].map((i) => (
        <span
          key={i}
          className="w-2 h-2 rounded-full bg-violet-400 animate-bounce"
          style={{ animationDelay: `${i * 0.15}s` }}
        />
      ))}
    </div>
  );
}

// ── MessageBubble ─────────────────────────────────────────────────────────────

function MessageBubble({
  msg,
  onAction,
}: {
  msg: Message;
  onAction: (text: string) => void;
}) {
  const isUser = msg.role === "user";
  return (
    <div className={`flex gap-2 ${isUser ? "flex-row-reverse" : "flex-row"}`}>
      {/* Avatar */}
      {!isUser && (
        <div className="w-7 h-7 rounded-full bg-gradient-to-br from-violet-500 to-purple-600 flex items-center justify-center flex-shrink-0 mt-1">
          <Sparkles className="w-3.5 h-3.5 text-white" />
        </div>
      )}

      <div className={`max-w-[80%] ${isUser ? "items-end" : "items-start"} flex flex-col gap-1.5`}>
        {/* Text bubble */}
        <div
          className={`px-4 py-3 rounded-2xl text-sm leading-relaxed whitespace-pre-wrap ${
            isUser
              ? "bg-violet-600 text-white rounded-tr-sm"
              : "bg-white border border-gray-100 text-gray-800 shadow-sm rounded-tl-sm"
          }`}
        >
          {msg.content}
        </div>

        {/* Action chips */}
        {!isUser && msg.actions && msg.actions.length > 0 && (
          <div className="flex flex-wrap gap-1.5 mt-0.5">
            {msg.actions.map((a) => (
              <button
                key={a}
                onClick={() => onAction(a)}
                className="text-xs bg-violet-50 hover:bg-violet-100 text-violet-700 border border-violet-200 px-2.5 py-1 rounded-full transition-colors font-medium"
              >
                {a}
              </button>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

// ── ChatWidget ────────────────────────────────────────────────────────────────

export default function ChatWidget({ open, onClose, title = "Career Brownie AI" }: ChatWidgetProps) {
  const [messages, setMessages] = useState<Message[]>([WELCOME]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const bottomRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);
  const sessionId = useRef(getSessionId());

  // Auto-scroll to bottom on new message
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  // Focus input when opened
  useEffect(() => {
    if (open) {
      setTimeout(() => inputRef.current?.focus(), 100);
    }
  }, [open]);

  const sendMessage = useCallback(
    async (text: string) => {
      const trimmed = text.trim();
      if (!trimmed || loading) return;

      setInput("");
      setError(null);

      const userMsg: Message = {
        id: uid(),
        role: "user",
        content: trimmed,
        timestamp: Date.now(),
      };
      setMessages((prev) => [...prev, userMsg]);
      setLoading(true);

      try {
        const res = await fetch(`${AI_SERVICE_URL}/api/v2/chat/`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            message: trimmed,
            session_id: sessionId.current,
          }),
        });

        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();

        const aiMsg: Message = {
          id: uid(),
          role: "assistant",
          content: data.reply || "I'm here to help! Please ask me anything about careers.",
          actions: data.suggested_actions ?? [],
          timestamp: Date.now(),
        };
        setMessages((prev) => [...prev, aiMsg]);
      } catch {
        setError("Couldn't reach the AI. Please check your connection and try again.");
      } finally {
        setLoading(false);
      }
    },
    [loading]
  );

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage(input);
    }
  };

  const reset = () => {
    sessionId.current = uid();
    sessionStorage.setItem("cb_session_id", sessionId.current);
    setMessages([WELCOME]);
    setError(null);
  };

  if (!open) return null;

  return (
    <>
      {/* Mobile overlay */}
      <div
        className="fixed inset-0 bg-black/40 z-40 md:hidden"
        onClick={onClose}
        aria-hidden
      />

      {/* Chat panel */}
      <div
        role="dialog"
        aria-label="Career Brownie AI Chat"
        className={`
          fixed z-50 flex flex-col bg-gray-50 shadow-2xl
          /* Mobile: full screen slide up */
          inset-0 md:inset-auto
          /* Desktop: bottom-right panel */
          md:bottom-6 md:right-6 md:w-[400px] md:h-[600px]
          md:rounded-2xl overflow-hidden
          /* Animation */
          animate-in slide-in-from-bottom-4 duration-200
        `}
      >
        {/* Header */}
        <div className="flex items-center gap-3 px-4 py-3 bg-gradient-to-r from-violet-600 to-purple-700 text-white flex-shrink-0">
          <div className="w-8 h-8 rounded-full bg-white/20 flex items-center justify-center">
            <Sparkles className="w-4 h-4" />
          </div>
          <div className="flex-1 min-w-0">
            <p className="font-semibold text-sm truncate">{title}</p>
            <p className="text-xs text-white/70">AI Career Counsellor · Available 24/7</p>
          </div>
          <div className="flex items-center gap-1">
            <button
              onClick={reset}
              title="New conversation"
              className="p-1.5 rounded-lg hover:bg-white/20 transition-colors"
            >
              <RotateCcw className="w-4 h-4" />
            </button>
            <button
              onClick={onClose}
              title="Close"
              className="p-1.5 rounded-lg hover:bg-white/20 transition-colors"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4 scroll-smooth">
          {/* Quick prompts — only when just welcome message */}
          {messages.length === 1 && (
            <div className="pb-2">
              <p className="text-xs text-gray-400 font-medium mb-2 uppercase tracking-wide">Try asking</p>
              <div className="flex flex-col gap-1.5">
                {QUICK_PROMPTS.map((p) => (
                  <button
                    key={p}
                    onClick={() => sendMessage(p)}
                    className="text-left text-xs text-gray-700 bg-white border border-gray-200 hover:border-violet-300 hover:bg-violet-50 px-3 py-2 rounded-xl transition-colors"
                  >
                    {p}
                  </button>
                ))}
              </div>
            </div>
          )}

          {messages.map((msg) => (
            <MessageBubble key={msg.id} msg={msg} onAction={sendMessage} />
          ))}

          {loading && (
            <div className="flex gap-2">
              <div className="w-7 h-7 rounded-full bg-gradient-to-br from-violet-500 to-purple-600 flex items-center justify-center flex-shrink-0">
                <Sparkles className="w-3.5 h-3.5 text-white" />
              </div>
              <div className="bg-white border border-gray-100 rounded-2xl rounded-tl-sm shadow-sm">
                <TypingDots />
              </div>
            </div>
          )}

          {error && (
            <div className="text-xs text-red-600 bg-red-50 border border-red-200 rounded-xl px-3 py-2">
              {error}
            </div>
          )}

          <div ref={bottomRef} />
        </div>

        {/* Input */}
        <div className="flex-shrink-0 border-t border-gray-200 bg-white p-3">
          <div className="flex items-end gap-2 bg-gray-50 border border-gray-200 rounded-2xl px-3 py-2 focus-within:border-violet-400 focus-within:ring-2 focus-within:ring-violet-100 transition-all">
            <textarea
              ref={inputRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask about careers, colleges, exams…"
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
              className="w-8 h-8 rounded-xl bg-violet-600 hover:bg-violet-700 disabled:bg-gray-200 disabled:cursor-not-allowed flex items-center justify-center transition-colors flex-shrink-0 mb-0.5"
            >
              {loading ? (
                <Loader2 className="w-4 h-4 text-white animate-spin" />
              ) : (
                <Send className="w-4 h-4 text-white" />
              )}
            </button>
          </div>
          <p className="text-center text-xs text-gray-400 mt-2">
            Press <kbd className="bg-gray-100 px-1 py-0.5 rounded text-[10px]">Enter</kbd> to send
            · <kbd className="bg-gray-100 px-1 py-0.5 rounded text-[10px]">Shift+Enter</kbd> for newline
          </p>
        </div>
      </div>
    </>
  );
}
