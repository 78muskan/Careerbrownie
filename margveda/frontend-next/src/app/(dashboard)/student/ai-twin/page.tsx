"use client";
import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Cpu, RefreshCw, Target, Zap, Calendar, TrendingUp, CheckCircle } from "lucide-react";
import api from "@/lib/api";

interface TwinSession {
  id: string;
  predicted_career_fit: string;
  predicted_placement_score: number;
  recommendations: { type: string; priority: string; title: string; description: string }[];
  action_plan: { week: number; task: string }[];
  career_profile_snapshot: { skills: string[]; interests: string[]; top_careers: string[] };
  session_context: { career_score: number; assessments_done: string[]; skill_gaps: string[] };
  created_at: string;
}

const PRIORITY_COLORS: Record<string, string> = {
  high: "border-red-200 bg-red-50",
  medium: "border-yellow-200 bg-yellow-50",
  low: "border-green-200 bg-green-50",
};
const TYPE_ICONS: Record<string, React.ElementType> = {
  skill: Zap, assessment: CheckCircle, profile: Target, roadmap: TrendingUp,
};

export default function AICareerTwinPage() {
  const [session, setSession] = useState<TwinSession | null>(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState("");

  const fetchTwin = async (refresh = false) => {
    if (refresh) setRefreshing(true);
    try {
      const method = refresh ? api.post : api.get;
      const res = await method("/enterprise/ai-twin/");
      setSession(res.data);
      setError("");
    } catch (e: unknown) {
      const msg = (e as { response?: { data?: { error?: string } } })?.response?.data?.error || "Failed to load AI Twin";
      setError(msg);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => { fetchTwin(); }, []);

  if (loading) return (
    <div className="flex flex-col items-center justify-center h-64 gap-4">
      <div className="relative w-16 h-16">
        <div className="absolute inset-0 rounded-full border-4 border-indigo-200 animate-ping" />
        <div className="absolute inset-2 rounded-full bg-indigo-600 flex items-center justify-center">
          <Cpu className="w-6 h-6 text-white" />
        </div>
      </div>
      <p className="text-gray-500 animate-pulse">Initialising AI Career Twin...</p>
    </div>
  );

  if (error) return (
    <div className="p-6">
      <div className="bg-yellow-50 border border-yellow-200 rounded-2xl p-6 text-center">
        <Cpu className="w-10 h-10 text-yellow-400 mx-auto mb-3" />
        <p className="text-yellow-700 font-medium">{error}</p>
        <a href="/student/profile/build" className="mt-3 inline-block text-sm text-indigo-600 hover:underline">
          Complete your profile →
        </a>
      </div>
    </div>
  );

  if (!session) return null;

  const scoreColor = session.predicted_placement_score >= 70 ? "text-green-600" :
    session.predicted_placement_score >= 40 ? "text-yellow-600" : "text-red-500";

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }}
        className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-12 h-12 bg-gradient-to-br from-indigo-600 to-purple-600 rounded-2xl flex items-center justify-center">
            <Cpu className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-gray-900">AI Career Twin</h1>
            <p className="text-gray-500 text-sm">Your personalised AI career intelligence engine</p>
          </div>
        </div>
        <button onClick={() => fetchTwin(true)} disabled={refreshing}
          className="flex items-center gap-2 text-sm bg-white border border-gray-200 px-4 py-2 rounded-xl hover:bg-gray-50 transition disabled:opacity-50">
          <RefreshCw className={`w-4 h-4 ${refreshing ? "animate-spin" : ""}`} />
          Refresh
        </button>
      </motion.div>

      {/* Hero card */}
      <motion.div initial={{ opacity: 0, scale: 0.97 }} animate={{ opacity: 1, scale: 1 }} transition={{ delay: 0.1 }}
        className="bg-gradient-to-br from-indigo-600 via-purple-600 to-pink-600 rounded-3xl p-8 text-white">
        <div className="grid md:grid-cols-3 gap-6">
          <div className="text-center">
            <div className="text-5xl font-bold">{session.predicted_placement_score}%</div>
            <div className="text-indigo-200 mt-1 text-sm">Placement Readiness</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold">{session.predicted_career_fit}</div>
            <div className="text-indigo-200 mt-1 text-sm">Best Career Fit</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold">{session.session_context.assessments_done.length}/4</div>
            <div className="text-indigo-200 mt-1 text-sm">Assessments Done</div>
          </div>
        </div>
        <div className="mt-6">
          <div className="flex justify-between text-xs text-indigo-200 mb-1">
            <span>Readiness</span><span>{session.predicted_placement_score}%</span>
          </div>
          <div className="w-full bg-white/20 rounded-full h-2">
            <motion.div
              initial={{ width: 0 }} animate={{ width: `${session.predicted_placement_score}%` }}
              transition={{ duration: 1.2, delay: 0.5 }}
              className="h-2 bg-white rounded-full" />
          </div>
        </div>
      </motion.div>

      <div className="grid md:grid-cols-2 gap-6">
        {/* Recommendations */}
        <motion.div initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.25 }}
          className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
          <h2 className="font-semibold text-gray-900 mb-4 flex items-center gap-2">
            <Target className="w-5 h-5 text-indigo-600" /> AI Recommendations
          </h2>
          <div className="space-y-3">
            {session.recommendations.map((rec, i) => {
              const Icon = TYPE_ICONS[rec.type] || Zap;
              return (
                <AnimatePresence key={i}>
                  <motion.div initial={{ opacity: 0, x: -10 }} animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.3 + i * 0.08 }}
                    className={`p-4 rounded-xl border ${PRIORITY_COLORS[rec.priority] || "bg-gray-50 border-gray-200"}`}>
                    <div className="flex items-start gap-3">
                      <Icon className="w-5 h-5 mt-0.5 text-gray-600 flex-shrink-0" />
                      <div>
                        <div className="font-medium text-gray-800 text-sm">{rec.title}</div>
                        <div className="text-xs text-gray-500 mt-0.5">{rec.description}</div>
                      </div>
                      <span className={`ml-auto text-xs px-2 py-0.5 rounded-full font-medium ${rec.priority === "high" ? "bg-red-100 text-red-600" : rec.priority === "medium" ? "bg-yellow-100 text-yellow-600" : "bg-green-100 text-green-600"}`}>
                        {rec.priority}
                      </span>
                    </div>
                  </motion.div>
                </AnimatePresence>
              );
            })}
          </div>
        </motion.div>

        {/* 12-Week Action Plan */}
        <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.25 }}
          className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
          <h2 className="font-semibold text-gray-900 mb-4 flex items-center gap-2">
            <Calendar className="w-5 h-5 text-purple-600" /> 12-Week Action Plan
          </h2>
          <div className="space-y-3">
            {session.action_plan.map((step, i) => (
              <motion.div key={i} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.4 + i * 0.1 }}
                className="flex items-start gap-3">
                <div className="w-8 h-8 bg-purple-100 rounded-full flex items-center justify-center flex-shrink-0 text-xs font-bold text-purple-700">
                  W{step.week}
                </div>
                <div className="flex-1 p-3 bg-gray-50 rounded-xl">
                  <div className="text-sm text-gray-700">{step.task}</div>
                </div>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </div>

      {/* Snapshot */}
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.4 }}
        className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
        <h2 className="font-semibold text-gray-900 mb-4">Your Career Profile Snapshot</h2>
        <div className="grid md:grid-cols-3 gap-4">
          <div>
            <div className="text-xs text-gray-400 mb-2">Top Skills</div>
            <div className="flex flex-wrap gap-1">
              {session.career_profile_snapshot.skills.slice(0, 6).map(s => (
                <span key={s} className="text-xs bg-indigo-50 text-indigo-700 px-2 py-0.5 rounded-full">{s}</span>
              ))}
            </div>
          </div>
          <div>
            <div className="text-xs text-gray-400 mb-2">Interests</div>
            <div className="flex flex-wrap gap-1">
              {session.career_profile_snapshot.interests.map(i => (
                <span key={i} className="text-xs bg-green-50 text-green-700 px-2 py-0.5 rounded-full capitalize">{i}</span>
              ))}
            </div>
          </div>
          <div>
            <div className="text-xs text-gray-400 mb-2">Skill Gaps</div>
            <div className="flex flex-wrap gap-1">
              {session.session_context.skill_gaps.slice(0, 4).map(g => (
                <span key={g} className="text-xs bg-red-50 text-red-600 px-2 py-0.5 rounded-full">{g}</span>
              ))}
            </div>
          </div>
        </div>
        <div className="mt-4 text-xs text-gray-300">
          Generated on {new Date(session.created_at).toLocaleString("en-IN")} · Click Refresh to regenerate
        </div>
      </motion.div>
    </div>
  );
}
