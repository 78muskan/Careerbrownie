"use client";
import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Target, CheckCircle, AlertCircle, XCircle, Info } from "lucide-react";
import api from "@/lib/api";

const EXAMS = [
  { key: "JEE Main", label: "JEE Main", desc: "NITs, IIITs, GFTIs" },
  { key: "JEE Advanced", label: "JEE Advanced", desc: "IITs" },
  { key: "NEET-UG", label: "NEET-UG", desc: "MBBS/BDS" },
  { key: "CAT", label: "CAT", desc: "IIMs & B-schools" },
  { key: "CUET", label: "CUET", desc: "Central Universities" },
  { key: "GATE", label: "GATE", desc: "M.Tech / PSU Jobs" },
];

const CATEGORIES = [
  { key: "general", label: "General" },
  { key: "obc", label: "OBC" },
  { key: "sc", label: "SC" },
  { key: "st", label: "ST" },
  { key: "ews", label: "EWS" },
];

interface PredictedCollege {
  college: string;
  cutoff: number;
  student_score: number;
  qualifies: boolean;
  margin: number;
  admission_chance: "High" | "Moderate" | "Low";
}

const CHANCE_STYLE: Record<string, { color: string; icon: React.ReactNode }> = {
  High: { color: "bg-green-100 text-green-700 border-green-200", icon: <CheckCircle className="w-4 h-4" /> },
  Moderate: { color: "bg-yellow-100 text-yellow-700 border-yellow-200", icon: <AlertCircle className="w-4 h-4" /> },
  Low: { color: "bg-red-100 text-red-700 border-red-200", icon: <XCircle className="w-4 h-4" /> },
};

export default function CollegePredictorPage() {
  const [exam, setExam] = useState("JEE Main");
  const [score, setScore] = useState("");
  const [category, setCategory] = useState("general");
  const [results, setResults] = useState<PredictedCollege[]>([]);
  const [loading, setLoading] = useState(false);
  const [submitted, setSubmitted] = useState(false);

  async function predict() {
    if (!score) return;
    setLoading(true);
    try {
      const res = await api.post("/predictor/predict/", { exam_type: exam, score: parseFloat(score), category });
      setResults(res.data.predicted_colleges);
      setSubmitted(true);
    } finally {
      setLoading(false);
    }
  }

  const EXAM_INFO: Record<string, { placeholder: string; note: string }> = {
    "JEE Main": { placeholder: "Percentile (e.g. 98.5)", note: "Enter overall percentile score" },
    "JEE Advanced": { placeholder: "AIR Rank (e.g. 500)", note: "Enter your All India Rank (lower = better)" },
    "NEET-UG": { placeholder: "Score out of 720 (e.g. 620)", note: "Enter your raw score out of 720" },
    CAT: { placeholder: "Percentile (e.g. 98.5)", note: "Enter overall percentile" },
    CUET: { placeholder: "Normalised score out of 100 (e.g. 92)", note: "Enter normalised score" },
    GATE: { placeholder: "Score (e.g. 750)", note: "Enter GATE score (out of 1000)" },
  };

  return (
    <div className="p-6 max-w-3xl mx-auto">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
          <Target className="w-6 h-6 text-indigo-600" /> College Predictor
        </h1>
        <p className="text-gray-500 mt-1">Enter your exam score to see which colleges you qualify for.</p>
      </div>

      {/* Exam selector */}
      <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 mb-6">
        {EXAMS.map(e => (
          <button key={e.key} onClick={() => { setExam(e.key); setSubmitted(false); setResults([]); }}
            className={`p-3 rounded-xl border text-left transition ${exam === e.key ? "border-indigo-400 bg-indigo-50" : "border-gray-200 bg-white hover:border-indigo-200"}`}>
            <p className="font-semibold text-sm text-gray-900">{e.label}</p>
            <p className="text-xs text-gray-500">{e.desc}</p>
          </button>
        ))}
      </div>

      {/* Input form */}
      <div className="bg-white rounded-2xl border border-gray-200 p-6 mb-6">
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
          <div>
            <label className="text-sm text-gray-600 block mb-2">Your {exam} Score</label>
            <input type="number" value={score} onChange={e => setScore(e.target.value)}
              placeholder={EXAM_INFO[exam]?.placeholder}
              className="w-full border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-300" />
            <p className="text-xs text-gray-400 mt-1 flex items-center gap-1">
              <Info className="w-3 h-3" /> {EXAM_INFO[exam]?.note}
            </p>
          </div>
          <div>
            <label className="text-sm text-gray-600 block mb-2">Category</label>
            <select value={category} onChange={e => setCategory(e.target.value)}
              className="w-full border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-300">
              {CATEGORIES.map(c => <option key={c.key} value={c.key}>{c.label}</option>)}
            </select>
          </div>
        </div>
        <button onClick={predict} disabled={loading || !score}
          className="flex items-center gap-2 bg-indigo-600 text-white px-6 py-3 rounded-xl hover:bg-indigo-700 disabled:opacity-50 transition">
          {loading ? <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white" /> : <Target className="w-4 h-4" />}
          Predict Colleges
        </button>
      </div>

      {/* Results */}
      <AnimatePresence>
        {submitted && (
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
            <div className="flex items-center justify-between mb-4">
              <h2 className="font-semibold text-gray-800">{results.length} College{results.length !== 1 ? "s" : ""} Found</h2>
              <button onClick={() => setSubmitted(false)} className="text-sm text-gray-500 hover:text-gray-700">Clear</button>
            </div>

            {results.length === 0 ? (
              <div className="text-center py-12 bg-gray-50 rounded-2xl border border-gray-200">
                <XCircle className="w-12 h-12 text-gray-400 mx-auto mb-3" />
                <p className="text-gray-600 font-medium">No matches found for this score and category.</p>
                <p className="text-sm text-gray-400 mt-1">Try a different exam or check if your score is correct.</p>
              </div>
            ) : (
              <div className="space-y-3">
                {results.map((r, i) => (
                  <motion.div key={i} initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: i * 0.07 }}
                    className="bg-white rounded-2xl border border-gray-200 p-4">
                    <div className="flex items-start justify-between">
                      <div>
                        <p className="font-semibold text-gray-900">{r.college}</p>
                        <p className="text-xs text-gray-500 mt-0.5">
                          Cutoff: {r.cutoff} • Your Score: {r.student_score}
                          {r.qualifies ? ` • ${r.margin.toFixed(1)} above cutoff` : ` • ${r.margin.toFixed(1)} below cutoff`}
                        </p>
                      </div>
                      <span className={`flex items-center gap-1 text-xs px-3 py-1 rounded-full border font-medium ${CHANCE_STYLE[r.admission_chance].color}`}>
                        {CHANCE_STYLE[r.admission_chance].icon}
                        {r.admission_chance}
                      </span>
                    </div>
                  </motion.div>
                ))}
              </div>
            )}

            <div className="mt-6 p-4 bg-amber-50 rounded-xl border border-amber-100">
              <p className="text-xs text-amber-700 flex items-start gap-2">
                <Info className="w-3 h-3 mt-0.5 shrink-0" />
                Predictions are based on historical cutoff data. Actual cutoffs vary yearly. Always check the official counselling website for confirmed cutoffs.
              </p>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
