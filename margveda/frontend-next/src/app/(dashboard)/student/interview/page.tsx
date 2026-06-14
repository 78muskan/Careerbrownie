"use client";
import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { Mic, Award, TrendingUp, Clock, ChevronRight } from "lucide-react";
import Link from "next/link";
import api from "@/lib/api";

const INTERVIEW_TYPES = [
  { type: "hr", label: "HR Interview", icon: "👤", desc: "Salary, motivation, culture fit — the essential HR questions.", color: "bg-blue-50 border-blue-100", badge: "bg-blue-100 text-blue-800" },
  { type: "behavioural", label: "Behavioural Interview", icon: "🧠", desc: "STAR-method questions: leadership, conflict, teamwork, adaptability.", color: "bg-purple-50 border-purple-100", badge: "bg-purple-100 text-purple-800" },
  { type: "technical", label: "Technical Interview", icon: "💻", desc: "Domain-specific technical questions (CS, Finance, Marketing, Data Science).", color: "bg-indigo-50 border-indigo-100", badge: "bg-indigo-100 text-indigo-800" },
  { type: "mock", label: "Mock Interview", icon: "🎯", desc: "Full end-to-end mock: HR + Behavioural + Technical in one session.", color: "bg-green-50 border-green-100", badge: "bg-green-100 text-green-800" },
];

interface Stats {
  total_sessions: number;
  overall_average: number;
  by_type: Record<string, number>;
}

export default function InterviewPage() {
  const [stats, setStats] = useState<Stats | null>(null);
  const [sessions, setSessions] = useState<any[]>([]);

  useEffect(() => {
    api.get("/interview/stats/").then(r => setStats(r.data)).catch(() => {});
    api.get("/interview/sessions/").then(r => setSessions(r.data)).catch(() => {});
  }, []);

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
          <Mic className="w-6 h-6 text-purple-600" /> Interview Coach
        </h1>
        <p className="text-gray-500 mt-1">Practice interviews. Get instant AI feedback. Build confidence.</p>
      </div>

      {/* Stats */}
      {stats && stats.total_sessions > 0 && (
        <div className="grid grid-cols-3 gap-4 mb-8">
          {[
            { label: "Sessions Done", value: stats.total_sessions, icon: <Clock className="w-5 h-5" />, color: "text-purple-600 bg-purple-50" },
            { label: "Avg Score", value: `${stats.overall_average}/100`, icon: <TrendingUp className="w-5 h-5" />, color: "text-green-600 bg-green-50" },
            { label: "Types Practiced", value: Object.keys(stats.by_type).length, icon: <Award className="w-5 h-5" />, color: "text-blue-600 bg-blue-50" },
          ].map((s, i) => (
            <motion.div key={i} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.1 }}
              className="bg-white rounded-2xl border border-gray-200 p-4 flex items-center gap-3">
              <div className={`w-10 h-10 rounded-xl flex items-center justify-center ${s.color}`}>{s.icon}</div>
              <div>
                <p className="text-xl font-bold text-gray-900">{s.value}</p>
                <p className="text-xs text-gray-500">{s.label}</p>
              </div>
            </motion.div>
          ))}
        </div>
      )}

      {/* Interview Type Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-8">
        {INTERVIEW_TYPES.map((t, i) => (
          <motion.div key={t.type} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.1 }}
            className={`rounded-2xl border p-5 ${t.color} hover:shadow-md transition`}>
            <div className="flex items-start justify-between mb-3">
              <div className="flex items-center gap-3">
                <span className="text-2xl">{t.icon}</span>
                <div>
                  <h3 className="font-semibold text-gray-900">{t.label}</h3>
                  {stats?.by_type[t.type] && (
                    <span className={`text-xs px-2 py-0.5 rounded-full ${t.badge}`}>Last: {stats.by_type[t.type]}/100</span>
                  )}
                </div>
              </div>
            </div>
            <p className="text-sm text-gray-600 mb-4">{t.desc}</p>
            <Link href={`/student/interview/${t.type}`}
              className="flex items-center gap-1 text-sm font-medium text-indigo-700 hover:text-indigo-900">
              Start Practice <ChevronRight className="w-4 h-4" />
            </Link>
          </motion.div>
        ))}
      </div>

      {/* Recent Sessions */}
      {sessions.length > 0 && (
        <div className="bg-white rounded-2xl border border-gray-200 p-6">
          <h3 className="font-semibold text-gray-800 mb-4">Recent Sessions</h3>
          <div className="space-y-3">
            {sessions.slice(0, 5).map((s: any) => (
              <div key={s.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-xl">
                <div>
                  <p className="text-sm font-medium text-gray-700 capitalize">{s.interview_type} • {s.domain}</p>
                  <p className="text-xs text-gray-400">{s.questions_answered}/{s.total_questions} questions • {new Date(s.started_at).toLocaleDateString()}</p>
                </div>
                <div className="flex items-center gap-2">
                  <span className={`text-sm font-bold ${s.overall_score >= 70 ? "text-green-600" : s.overall_score >= 50 ? "text-yellow-600" : "text-red-500"}`}>
                    {s.overall_score}/100
                  </span>
                  <span className={`text-xs px-2 py-0.5 rounded-full ${s.is_completed ? "bg-green-100 text-green-700" : "bg-yellow-100 text-yellow-700"}`}>
                    {s.is_completed ? "Done" : "In Progress"}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
