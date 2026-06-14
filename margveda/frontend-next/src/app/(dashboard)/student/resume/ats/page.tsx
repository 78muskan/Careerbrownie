"use client";
import { useEffect, useState, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import { motion } from "framer-motion";
import { BarChart2, CheckCircle, XCircle, AlertCircle, Zap } from "lucide-react";
import api from "@/lib/api";

const DOMAINS = ["technology", "data_science", "finance", "marketing", "hr", "design", "general"];

interface ATSResult {
  ats_score: number;
  grade: string;
  breakdown: Record<string, number>;
  matched_keywords: string[];
  missing_keywords: string[];
  suggestions: string[];
  word_count: number;
}

function ATSContent() {
  const params = useSearchParams();
  const resumeId = params.get("id");
  const [result, setResult] = useState<ATSResult | null>(null);
  const [domain, setDomain] = useState("technology");
  const [jd, setJd] = useState("");
  const [analysing, setAnalysing] = useState(false);
  const [history, setHistory] = useState<ATSResult[]>([]);

  useEffect(() => {
    if (resumeId) api.get(`/resume/${resumeId}/ats/`).then(r => setHistory(r.data));
  }, [resumeId]);

  async function runAnalysis() {
    setAnalysing(true);
    try {
      const res = await api.post(`/resume/${resumeId}/ats/`, { domain, job_description: jd });
      setResult(res.data);
    } finally {
      setAnalysing(false);
    }
  }

  const scoreColor = (score: number) =>
    score >= 80 ? "text-green-600" : score >= 65 ? "text-yellow-600" : "text-red-600";

  const gradeBg = (grade: string) =>
    grade === "A" ? "bg-green-100 text-green-800" :
    grade === "B" ? "bg-yellow-100 text-yellow-800" :
    grade === "C" ? "bg-orange-100 text-orange-800" : "bg-red-100 text-red-800";

  return (
    <div className="p-6 max-w-3xl mx-auto">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
          <BarChart2 className="w-6 h-6 text-indigo-600" /> ATS Resume Analyser
        </h1>
        <p className="text-gray-500 mt-1">See how well your resume performs against ATS systems before you apply.</p>
      </div>

      {/* Config */}
      <div className="bg-white rounded-2xl border border-gray-200 p-6 mb-6">
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
          <div>
            <label className="text-sm text-gray-600 block mb-2">Target Domain</label>
            <select value={domain} onChange={e => setDomain(e.target.value)}
              className="w-full border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-300">
              {DOMAINS.map(d => <option key={d} value={d}>{d.replace("_", " ").replace(/\b\w/g, l => l.toUpperCase())}</option>)}
            </select>
          </div>
        </div>
        <div className="mb-4">
          <label className="text-sm text-gray-600 block mb-2">Paste Job Description (optional — improves accuracy)</label>
          <textarea value={jd} onChange={e => setJd(e.target.value)} rows={5}
            placeholder="Paste the job description here for a more targeted analysis…"
            className="w-full border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-300 resize-none" />
        </div>
        <button onClick={runAnalysis} disabled={analysing || !resumeId}
          className="flex items-center gap-2 bg-indigo-600 text-white px-6 py-3 rounded-xl hover:bg-indigo-700 disabled:opacity-50 transition">
          {analysing ? <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white" /> : <Zap className="w-4 h-4" />}
          {analysing ? "Analysing…" : "Analyse Resume"}
        </button>
      </div>

      {/* Results */}
      {result && (
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
          {/* Score Card */}
          <div className="bg-white rounded-2xl border border-gray-200 p-6 mb-4">
            <div className="flex items-center justify-between mb-6">
              <div>
                <p className="text-sm text-gray-500">ATS Score</p>
                <p className={`text-5xl font-bold ${scoreColor(result.ats_score)}`}>{result.ats_score}<span className="text-xl text-gray-400">/100</span></p>
              </div>
              <span className={`text-3xl font-bold px-6 py-3 rounded-2xl ${gradeBg(result.grade)}`}>{result.grade}</span>
            </div>
            <div className="grid grid-cols-2 sm:grid-cols-5 gap-3">
              {Object.entries(result.breakdown).map(([key, val]) => (
                <div key={key} className="text-center p-3 bg-gray-50 rounded-xl">
                  <p className="text-lg font-bold text-gray-800">{val}</p>
                  <p className="text-xs text-gray-500 capitalize">{key.replace("_", " ")}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Keywords */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
            <div className="bg-green-50 rounded-2xl border border-green-100 p-5">
              <h3 className="flex items-center gap-2 font-semibold text-green-800 mb-3">
                <CheckCircle className="w-4 h-4" /> Matched Keywords ({result.matched_keywords.length})
              </h3>
              <div className="flex flex-wrap gap-2">
                {result.matched_keywords.map(kw => (
                  <span key={kw} className="text-xs bg-green-100 text-green-800 px-2 py-1 rounded-full">{kw}</span>
                ))}
              </div>
            </div>
            <div className="bg-red-50 rounded-2xl border border-red-100 p-5">
              <h3 className="flex items-center gap-2 font-semibold text-red-800 mb-3">
                <XCircle className="w-4 h-4" /> Missing Keywords ({result.missing_keywords.length})
              </h3>
              <div className="flex flex-wrap gap-2">
                {result.missing_keywords.map(kw => (
                  <span key={kw} className="text-xs bg-red-100 text-red-800 px-2 py-1 rounded-full">{kw}</span>
                ))}
              </div>
            </div>
          </div>

          {/* Suggestions */}
          {result.suggestions.length > 0 && (
            <div className="bg-amber-50 rounded-2xl border border-amber-100 p-5">
              <h3 className="flex items-center gap-2 font-semibold text-amber-800 mb-3">
                <AlertCircle className="w-4 h-4" /> Improvement Tips
              </h3>
              <ul className="space-y-2">
                {result.suggestions.map((s, i) => (
                  <li key={i} className="flex items-start gap-2 text-sm text-amber-800">
                    <span className="mt-0.5 shrink-0 w-5 h-5 bg-amber-200 rounded-full flex items-center justify-center text-xs font-bold">{i + 1}</span>
                    {s}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </motion.div>
      )}

      {/* History */}
      {history.length > 0 && !result && (
        <div className="bg-white rounded-2xl border border-gray-200 p-6">
          <h3 className="font-semibold text-gray-800 mb-4">Previous Analyses</h3>
          <div className="space-y-3">
            {history.map((h: any, i: number) => (
              <div key={i} className="flex items-center justify-between p-3 bg-gray-50 rounded-xl">
                <div>
                  <p className="text-sm font-medium text-gray-700">{h.domain} — {new Date(h.created_at).toLocaleDateString()}</p>
                  <p className="text-xs text-gray-500">{h.word_count} words</p>
                </div>
                <div className="flex items-center gap-2">
                  <span className={`text-lg font-bold ${scoreColor(h.ats_score)}`}>{h.ats_score}</span>
                  <span className={`text-xs px-2 py-0.5 rounded-full ${gradeBg(h.grade)}`}>{h.grade}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default function ATSPage() {
  return (
    <Suspense fallback={<div className="flex items-center justify-center h-64"><div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600" /></div>}>
      <ATSContent />
    </Suspense>
  );
}
