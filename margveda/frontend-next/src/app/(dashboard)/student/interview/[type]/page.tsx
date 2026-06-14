"use client";
import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import { ChevronRight, Send, RotateCcw, Trophy, AlertCircle } from "lucide-react";
import api from "@/lib/api";

const DOMAIN_OPTIONS = ["general", "technology", "data_science", "finance", "marketing"];

const TYPE_LABELS: Record<string, string> = {
  hr: "HR Interview", behavioural: "Behavioural Interview",
  technical: "Technical Interview", mock: "Mock Interview",
};

interface Question {
  id: string;
  question: string;
  category: string;
  tips?: string;
  competency?: string;
}

interface ResponseFeedback {
  score: number;
  feedback: string[];
  word_count: number;
}

export default function InterviewTypePage() {
  const { type } = useParams<{ type: string }>();
  const router = useRouter();

  const [domain, setDomain] = useState("general");
  const [questions, setQuestions] = useState<Question[]>([]);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answer, setAnswer] = useState("");
  const [feedback, setFeedback] = useState<ResponseFeedback | null>(null);
  const [allFeedback, setAllFeedback] = useState<Record<string, ResponseFeedback>>({});
  const [submitting, setSubmitting] = useState(false);
  const [sessionComplete, setSessionComplete] = useState(false);
  const [overallScore, setOverallScore] = useState(0);
  const [showTip, setShowTip] = useState(false);

  useEffect(() => {
    if (type) loadQuestions();
  }, [type, domain]);

  async function loadQuestions() {
    const res = await api.get(`/interview/questions/?type=${type}&domain=${domain}`);
    setQuestions(res.data.questions);
  }

  async function startSession() {
    const res = await api.post("/interview/sessions/", { interview_type: type, domain });
    setSessionId(res.data.id);
    setQuestions(res.data.questions);
    setCurrentIndex(0);
    setAllFeedback({});
    setFeedback(null);
    setAnswer("");
    setSessionComplete(false);
  }

  async function submitAnswer() {
    if (!sessionId || !answer.trim()) return;
    setSubmitting(true);
    try {
      const q = questions[currentIndex];
      const res = await api.post(`/interview/sessions/${sessionId}/`, {
        question_id: q.id,
        question_text: q.question,
        response_text: answer,
      });
      const fb: ResponseFeedback = res.data.response;
      setFeedback(fb);
      setAllFeedback(prev => ({ ...prev, [q.id]: fb }));
      if (res.data.session.is_completed) {
        setSessionComplete(true);
        setOverallScore(res.data.session.overall_score);
      }
    } finally {
      setSubmitting(false);
    }
  }

  function nextQuestion() {
    if (currentIndex < questions.length - 1) {
      setCurrentIndex(prev => prev + 1);
      setAnswer("");
      setFeedback(null);
      setShowTip(false);
    } else {
      // Complete session
      api.patch(`/interview/sessions/${sessionId}/`).then(r => {
        setSessionComplete(true);
        setOverallScore(r.data.overall_score);
      });
    }
  }

  const currentQ = questions[currentIndex];
  const progress = questions.length > 0 ? ((currentIndex + (feedback ? 1 : 0)) / questions.length) * 100 : 0;

  if (sessionComplete) {
    return (
      <div className="p-6 max-w-2xl mx-auto">
        <motion.div initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }}
          className="text-center bg-white rounded-3xl border border-gray-200 p-10">
          <Trophy className="w-16 h-16 text-yellow-500 mx-auto mb-4" />
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Interview Complete!</h1>
          <p className="text-gray-500 mb-6">You finished {questions.length} questions.</p>
          <div className={`text-6xl font-bold mb-2 ${overallScore >= 70 ? "text-green-600" : overallScore >= 50 ? "text-yellow-600" : "text-red-500"}`}>
            {overallScore}<span className="text-2xl text-gray-400">/100</span>
          </div>
          <p className="text-sm text-gray-500 mb-8">
            {overallScore >= 80 ? "Excellent! You are very well prepared." :
             overallScore >= 60 ? "Good effort. Review the feedback and practice more." :
             "Keep practising. Use the STAR method and add more specific examples."}
          </p>
          <div className="grid grid-cols-2 gap-3">
            <button onClick={() => { setSessionId(null); setCurrentIndex(0); setAllFeedback({}); setFeedback(null); setSessionComplete(false); setAnswer(""); }}
              className="flex items-center justify-center gap-2 border border-gray-200 text-gray-700 px-4 py-3 rounded-xl hover:bg-gray-50">
              <RotateCcw className="w-4 h-4" /> Try Again
            </button>
            <button onClick={() => router.push("/student/interview")}
              className="bg-indigo-600 text-white px-4 py-3 rounded-xl hover:bg-indigo-700">
              Back to Coach
            </button>
          </div>
        </motion.div>
      </div>
    );
  }

  if (!sessionId) {
    return (
      <div className="p-6 max-w-2xl mx-auto">
        <h1 className="text-2xl font-bold text-gray-900 mb-2">{TYPE_LABELS[type] || type}</h1>
        <p className="text-gray-500 mb-6">Practise answering real interview questions with instant AI feedback.</p>

        {(type === "technical" || type === "mock") && (
          <div className="mb-6">
            <label htmlFor="domain-select" className="text-sm text-gray-600 block mb-2">Your Domain</label>
            <select id="domain-select" value={domain} onChange={e => setDomain(e.target.value)}
              className="w-full sm:w-64 border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-300">
              {DOMAIN_OPTIONS.map(d => <option key={d} value={d}>{d.replace("_", " ").replace(/\b\w/g, l => l.toUpperCase())}</option>)}
            </select>
          </div>
        )}

        <div className="bg-indigo-50 rounded-2xl p-6 mb-6">
          <p className="text-indigo-800 font-medium mb-2">How it works</p>
          <ul className="text-sm text-indigo-700 space-y-1">
            <li>• You will get {questions.length || "10–12"} questions one at a time</li>
            <li>• Type your answer (aim for 150–350 words)</li>
            <li>• Get instant score + feedback after each answer</li>
            <li>• See your overall score at the end</li>
          </ul>
        </div>

        <button onClick={startSession} className="bg-indigo-600 text-white px-8 py-3 rounded-xl hover:bg-indigo-700 text-lg">
          Start Interview →
        </button>
      </div>
    );
  }

  return (
    <div className="p-6 max-w-2xl mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <h1 className="text-lg font-semibold text-gray-800">{TYPE_LABELS[type]}</h1>
        <span className="text-sm text-gray-500">{currentIndex + 1} / {questions.length}</span>
      </div>

      {/* Progress bar */}
      <div className="w-full bg-gray-200 rounded-full h-1.5 mb-8">
        <motion.div className="bg-indigo-600 h-1.5 rounded-full" animate={{ width: `${progress}%` }} />
      </div>

      {currentQ && (
        <AnimatePresence mode="wait">
          <motion.div key={currentQ.id} initial={{ opacity: 0, x: 30 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -30 }}>
            {/* Question */}
            <div className="bg-white rounded-2xl border border-gray-200 p-6 mb-4">
              <div className="flex items-start justify-between mb-2">
                <span className="text-xs bg-gray-100 text-gray-600 px-2 py-0.5 rounded-full capitalize">{currentQ.category}</span>
                {currentQ.competency && <span className="text-xs bg-indigo-100 text-indigo-700 px-2 py-0.5 rounded-full">{currentQ.competency?.replace("_", " ")}</span>}
              </div>
              <p className="text-lg text-gray-800 font-medium mt-3">{currentQ.question}</p>

              {currentQ.tips && (
                <div className="mt-4">
                  <button onClick={() => setShowTip(!showTip)} className="text-xs text-indigo-600 hover:text-indigo-800 flex items-center gap-1">
                    <AlertCircle className="w-3 h-3" /> {showTip ? "Hide" : "Show"} Tip
                  </button>
                  {showTip && (
                    <motion.p initial={{ opacity: 0 }} animate={{ opacity: 1 }}
                      className="text-sm text-indigo-700 bg-indigo-50 p-3 rounded-xl mt-2">{currentQ.tips}</motion.p>
                  )}
                </div>
              )}
            </div>

            {/* Answer input */}
            {!feedback && (
              <div className="mb-4">
                <textarea value={answer} onChange={e => setAnswer(e.target.value)} rows={8}
                  placeholder="Type your answer here… (Tip: use specific examples, numbers, and action verbs)"
                  className="w-full border border-gray-200 rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-300 resize-none" />
                <div className="flex items-center justify-between mt-2">
                  <span className="text-xs text-gray-400">{answer.split(/\s+/).filter(Boolean).length} words</span>
                  <button onClick={submitAnswer} disabled={submitting || answer.trim().length < 20}
                    className="flex items-center gap-2 bg-indigo-600 text-white px-5 py-2 rounded-xl hover:bg-indigo-700 disabled:opacity-50">
                    {submitting ? <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white" /> : <Send className="w-4 h-4" />}
                    Submit
                  </button>
                </div>
              </div>
            )}

            {/* Feedback */}
            {feedback && (
              <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}
                className="bg-white rounded-2xl border border-gray-200 p-6 mb-4">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="font-semibold text-gray-800">Feedback</h3>
                  <span className={`text-2xl font-bold ${feedback.score >= 70 ? "text-green-600" : feedback.score >= 50 ? "text-yellow-600" : "text-red-500"}`}>
                    {feedback.score}/100
                  </span>
                </div>
                <ul className="space-y-2">
                  {feedback.feedback.map((f, i) => (
                    <li key={i} className="flex items-start gap-2 text-sm text-gray-700">
                      <span className="mt-0.5 w-4 h-4 shrink-0 rounded-full bg-indigo-100 text-indigo-700 flex items-center justify-center text-xs">{i + 1}</span>
                      {f}
                    </li>
                  ))}
                </ul>
                <button onClick={nextQuestion}
                  className="mt-5 flex items-center gap-2 bg-indigo-600 text-white px-5 py-2 rounded-xl hover:bg-indigo-700">
                  {currentIndex < questions.length - 1 ? <><ChevronRight className="w-4 h-4" /> Next Question</> : <><Trophy className="w-4 h-4" /> Finish Interview</>}
                </button>
              </motion.div>
            )}
          </motion.div>
        </AnimatePresence>
      )}
    </div>
  );
}
