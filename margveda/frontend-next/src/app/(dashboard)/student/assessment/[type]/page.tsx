"use client";
import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import { ChevronLeft, ChevronRight, Loader2, CheckCircle2 } from "lucide-react";
import api from "@/lib/api";

interface Question {
  id: number;
  text: string;
  options: Array<{ text: string; value?: number; riasec?: string }>;
  type?: string;
  correct?: number;
  trait?: string;
  category?: string;
}

const LIKERT = ["Strongly Agree", "Agree", "Neutral", "Disagree", "Strongly Disagree"];
const LABELS: Record<string, string> = {
  interest: "Interest Assessment",
  personality: "Personality Assessment",
  aptitude: "Aptitude Assessment",
  readiness: "Career Readiness",
};

export default function AssessmentPage() {
  const params = useParams();
  const router = useRouter();
  const type = params.type as string;

  const [questions, setQuestions] = useState<Question[]>([]);
  const [current, setCurrent] = useState(0);
  const [responses, setResponses] = useState<Record<string, number>>({});
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [done, setDone] = useState(false);
  const [result, setResult] = useState<Record<string, unknown> | null>(null);

  useEffect(() => {
    api.get(`/ai/assessment/${type}/questions/`)
      .then((r) => setQuestions(r.data.questions))
      .catch(() => router.push("/student/assessment"))
      .finally(() => setLoading(false));
  }, [type, router]);

  const q = questions[current];
  const answered = q ? responses[String(q.id)] !== undefined : false;
  const progress = Math.round((current / Math.max(questions.length, 1)) * 100);

  const select = (optIdx: number) => {
    if (!q) return;
    setResponses((r) => ({ ...r, [String(q.id)]: optIdx }));
  };

  const next = () => {
    if (current < questions.length - 1) setCurrent((c) => c + 1);
  };
  const back = () => setCurrent((c) => Math.max(0, c - 1));

  const submit = async () => {
    setSubmitting(true);
    try {
      const { data } = await api.post(`/ai/assessment/${type}/submit/`, { responses });
      setResult(data.result);
      setDone(true);
    } catch {
      alert("Submission failed. Please try again.");
    } finally {
      setSubmitting(false);
    }
  };

  const isPersonalityOrReadiness = type === "personality" || type === "readiness";

  if (loading) return <div className="flex justify-center p-16"><Loader2 className="w-8 h-8 animate-spin text-primary-600" /></div>;

  if (done && result) {
    return (
      <div className="max-w-2xl mx-auto py-8">
        <div className="text-center mb-8">
          <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <CheckCircle2 className="w-8 h-8 text-green-600" />
          </div>
          <h2 className="text-2xl font-display font-bold text-gray-900">Assessment Complete!</h2>
          <p className="text-gray-500 mt-2">{String(result.result_summary || "")}</p>
        </div>
        {!!result.top_careers && Array.isArray(result.top_careers) && (result.top_careers as Array<{title: string; match_pct: number; domain: string; avg_salary_india: string}>).length > 0 && (
          <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 mb-6">
            <h3 className="font-semibold text-gray-900 mb-4">Your Top Career Matches</h3>
            <div className="space-y-3">
              {(result.top_careers as Array<{title: string; match_pct: number; domain: string; avg_salary_india: string}>).slice(0, 5).map((c, i) => (
                <div key={i} className="flex items-center gap-4">
                  <span className="w-6 h-6 bg-primary-100 rounded-full flex items-center justify-center text-xs font-bold text-primary-700 shrink-0">{i + 1}</span>
                  <div className="flex-1">
                    <div className="flex justify-between items-center mb-1">
                      <span className="text-sm font-medium text-gray-800">{c.title}</span>
                      <span className="text-xs font-bold text-primary-600">{c.match_pct}%</span>
                    </div>
                    <div className="w-full bg-gray-100 rounded-full h-1.5">
                      <div className="bg-primary-500 h-1.5 rounded-full" style={{ width: `${c.match_pct}%` }} />
                    </div>
                    <p className="text-xs text-gray-400 mt-0.5">{c.domain} · {c.avg_salary_india}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
        <div className="flex gap-3 justify-center">
          <button onClick={() => router.push("/student/assessment")} className="btn-secondary">Back to Assessments</button>
          <button onClick={() => router.push("/student/ai-advisor")} className="btn-primary">View AI Insights →</button>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <div>
        <h1 className="text-xl font-display font-bold text-gray-900">{LABELS[type] || type}</h1>
        <div className="mt-3 flex items-center gap-3">
          <div className="flex-1 bg-gray-100 rounded-full h-2">
            <div className="bg-primary-500 h-2 rounded-full transition-all" style={{ width: `${progress}%` }} />
          </div>
          <span className="text-sm text-gray-500 shrink-0">{current + 1} / {questions.length}</span>
        </div>
      </div>

      <AnimatePresence mode="wait">
        <motion.div key={current} initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: -20 }} transition={{ duration: 0.2 }}
          className="bg-white rounded-2xl p-8 shadow-sm border border-gray-100"
        >
          {q && (
            <>
              <p className="text-gray-800 font-medium text-lg leading-relaxed mb-6">{q.text}</p>
              <div className="space-y-3">
                {isPersonalityOrReadiness
                  ? LIKERT.map((label, idx) => (
                    <button key={idx} onClick={() => { select(5 - idx); next(); }}
                      className={`w-full text-left px-4 py-3 rounded-xl border text-sm transition-all ${
                        responses[String(q.id)] === 5 - idx
                          ? "bg-primary-50 border-primary-400 text-primary-700 font-medium"
                          : "border-gray-200 hover:border-primary-300 hover:bg-gray-50"
                      }`}
                    >
                      {label}
                    </button>
                  ))
                  : q.options.map((opt, idx) => (
                    <button key={idx} onClick={() => select(idx)}
                      className={`w-full text-left px-4 py-3 rounded-xl border text-sm transition-all ${
                        responses[String(q.id)] === idx
                          ? "bg-primary-50 border-primary-400 text-primary-700 font-medium"
                          : "border-gray-200 hover:border-primary-300 hover:bg-gray-50"
                      }`}
                    >
                      {typeof opt === "object" && opt !== null ? String((opt as { text?: string }).text ?? "") : String(opt)}
                    </button>
                  ))
                }
              </div>
            </>
          )}
        </motion.div>
      </AnimatePresence>

      <div className="flex items-center justify-between">
        <button onClick={back} disabled={current === 0} className="flex items-center gap-2 text-sm text-gray-600 hover:text-gray-900 disabled:opacity-30 disabled:cursor-not-allowed">
          <ChevronLeft className="w-4 h-4" />Previous
        </button>
        {current < questions.length - 1 ? (
          <button onClick={next} disabled={!answered && !isPersonalityOrReadiness}
            className="flex items-center gap-2 btn-primary disabled:opacity-50">
            Next<ChevronRight className="w-4 h-4" />
          </button>
        ) : (
          <button onClick={submit} disabled={submitting}
            className="flex items-center gap-2 btn-primary disabled:opacity-60">
            {submitting && <Loader2 className="w-4 h-4 animate-spin" />}
            {submitting ? "Submitting…" : "Submit Assessment"}
            {!submitting && <CheckCircle2 className="w-4 h-4" />}
          </button>
        )}
      </div>
    </div>
  );
}
