"use client";
import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { Target, Calendar, TrendingUp, CheckCircle2, ChevronRight, Sparkles, BookOpen } from "lucide-react";
import Link from "next/link";
import api from "@/lib/api";

interface DashboardData {
  profile: {
    full_name: string;
    avatar: string | null;
    is_verified: boolean;
    profile_score: number;
    career_score: number;
    onboarding_completed: boolean;
  };
  career_recommendations: string[];
  skill_gaps: string[];
  upcoming_sessions: Array<{
    id: string;
    type: string;
    status: string;
    scheduled_at: string;
    counsellor: string | null;
    duration_minutes: number;
    meeting_link: string | null;
  }>;
  past_sessions: Array<{ id: string; type: string }>;
  total_sessions: number;
  unread_notifications: number;
  goals: Array<{ id: number; title: string; status: string; target_date: string | null }>;
}

const card = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0 },
};

export default function StudentDashboardPage() {
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get("/student/dashboard/")
      .then((r) => setData(r.data))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="w-8 h-8 border-4 border-primary-600 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  if (!data) return <p className="text-gray-500">Could not load dashboard data.</p>;

  const { profile, upcoming_sessions, career_recommendations, skill_gaps, goals } = data;

  return (
    <motion.div
      initial="hidden"
      animate="show"
      variants={{ show: { transition: { staggerChildren: 0.08 } } }}
      className="space-y-6 max-w-6xl"
    >
      {/* Header */}
      <motion.div variants={card}>
        <h1 className="text-2xl font-display font-bold text-gray-900">Your Career Dashboard</h1>
        <p className="text-gray-500 text-sm mt-1">Track your progress and take the next step.</p>
      </motion.div>

      {/* Score cards */}
      <motion.div variants={card} className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {[
          { label: "Profile Score", value: `${profile.profile_score}%`, color: "text-primary-600", bg: "bg-primary-50", icon: <Target className="w-5 h-5 text-primary-600" />, sub: "Complete your profile" },
          { label: "Career Score", value: `${profile.career_score}%`, color: "text-violet-600", bg: "bg-violet-50", icon: <TrendingUp className="w-5 h-5 text-violet-600" />, sub: "AI-powered score" },
          { label: "Total Sessions", value: String(data.total_sessions), color: "text-blue-600", bg: "bg-blue-50", icon: <Calendar className="w-5 h-5 text-blue-600" />, sub: "Counselling sessions" },
          { label: "Active Goals", value: String(goals.length), color: "text-green-600", bg: "bg-green-50", icon: <CheckCircle2 className="w-5 h-5 text-green-600" />, sub: "In progress" },
        ].map((s) => (
          <div key={s.label} className="bg-white rounded-2xl p-5 shadow-sm border border-gray-100">
            <div className={`w-10 h-10 ${s.bg} rounded-xl flex items-center justify-center mb-3`}>
              {s.icon}
            </div>
            <div className={`text-2xl font-bold ${s.color}`}>{s.value}</div>
            <div className="text-sm font-medium text-gray-700 mt-0.5">{s.label}</div>
            <div className="text-xs text-gray-400 mt-0.5">{s.sub}</div>
          </div>
        ))}
      </motion.div>

      {/* Profile completion */}
      {!profile.onboarding_completed && (
        <motion.div variants={card} className="bg-gradient-to-r from-primary-600 to-violet-600 rounded-2xl p-6 text-white">
          <div className="flex items-start justify-between gap-4">
            <div className="flex-1">
              <h3 className="font-semibold text-lg">Complete your profile</h3>
              <p className="text-white/80 text-sm mt-1">Get personalised AI career recommendations by completing your profile.</p>
              <div className="mt-3 bg-white/20 rounded-full h-2">
                <div className="bg-white h-2 rounded-full transition-all" style={{ width: `${profile.profile_score}%` }} />
              </div>
              <p className="text-xs text-white/70 mt-1">{profile.profile_score}% complete</p>
            </div>
            <Link href="/student/profile/build" className="shrink-0 bg-white text-primary-700 font-semibold text-sm px-4 py-2 rounded-xl hover:bg-primary-50 transition-colors">
              Complete now
            </Link>
          </div>
        </motion.div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Upcoming sessions */}
        <motion.div variants={card} className="lg:col-span-2 bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-semibold text-gray-900 flex items-center gap-2">
              <Calendar className="w-5 h-5 text-primary-600" />
              Upcoming Sessions
            </h3>
            <Link href="/student/sessions" className="text-sm text-primary-600 hover:underline flex items-center gap-1">
              View all <ChevronRight className="w-4 h-4" />
            </Link>
          </div>
          {upcoming_sessions.length === 0 ? (
            <div className="text-center py-8">
              <Calendar className="w-12 h-12 text-gray-200 mx-auto mb-3" />
              <p className="text-gray-500 text-sm">No upcoming sessions</p>
              <Link href="/book-consultation" className="mt-3 inline-block text-sm text-primary-600 hover:underline">
                Book a free session →
              </Link>
            </div>
          ) : (
            <div className="space-y-3">
              {upcoming_sessions.map((s) => (
                <div key={s.id} className="flex items-center gap-4 p-3 bg-gray-50 rounded-xl">
                  <div className="w-10 h-10 bg-primary-100 rounded-xl flex items-center justify-center shrink-0">
                    <Calendar className="w-5 h-5 text-primary-600" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-900 truncate">{s.type}</p>
                    <p className="text-xs text-gray-500">
                      {new Date(s.scheduled_at).toLocaleDateString("en-IN", { day: "numeric", month: "short", hour: "2-digit", minute: "2-digit" })}
                      {s.counsellor && ` · ${s.counsellor}`}
                    </p>
                  </div>
                  <span className={`text-xs font-medium px-2.5 py-1 rounded-full ${s.status === "confirmed" ? "bg-green-100 text-green-700" : "bg-yellow-100 text-yellow-700"}`}>
                    {s.status}
                  </span>
                </div>
              ))}
            </div>
          )}
        </motion.div>

        {/* AI Recommendations */}
        <motion.div variants={card} className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
          <h3 className="font-semibold text-gray-900 flex items-center gap-2 mb-4">
            <Sparkles className="w-5 h-5 text-violet-600" />
            AI Career Picks
          </h3>
          {career_recommendations.length === 0 ? (
            <div className="text-center py-6">
              <Sparkles className="w-10 h-10 text-gray-200 mx-auto mb-2" />
              <p className="text-xs text-gray-500">Complete your profile to get AI recommendations</p>
            </div>
          ) : (
            <div className="space-y-2">
              {career_recommendations.map((rec, i) => (
                <div key={i} className="flex items-center gap-3 p-2.5 rounded-lg hover:bg-gray-50 transition-colors">
                  <span className="w-6 h-6 bg-violet-100 rounded-full flex items-center justify-center text-xs font-bold text-violet-700 shrink-0">
                    {i + 1}
                  </span>
                  <span className="text-sm text-gray-700">{rec}</span>
                </div>
              ))}
            </div>
          )}
        </motion.div>
      </div>

      {/* Goals + Skill Gaps */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <motion.div variants={card} className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-semibold text-gray-900 flex items-center gap-2">
              <Target className="w-5 h-5 text-green-600" />
              Active Goals
            </h3>
            <Link href="/student/goals" className="text-sm text-primary-600 hover:underline">Add goal</Link>
          </div>
          {goals.length === 0 ? (
            <p className="text-sm text-gray-500 py-4 text-center">No goals yet. Set your first career goal!</p>
          ) : (
            <div className="space-y-2">
              {goals.map((g) => (
                <div key={g.id} className="flex items-start gap-3 p-2.5 rounded-lg hover:bg-gray-50">
                  <div className={`mt-0.5 w-4 h-4 rounded-full border-2 shrink-0 ${g.status === "in_progress" ? "border-primary-500 bg-primary-100" : "border-gray-300"}`} />
                  <div>
                    <p className="text-sm text-gray-800 font-medium">{g.title}</p>
                    {g.target_date && (
                      <p className="text-xs text-gray-400">Due {new Date(g.target_date).toLocaleDateString("en-IN")}</p>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </motion.div>

        <motion.div variants={card} className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
          <h3 className="font-semibold text-gray-900 flex items-center gap-2 mb-4">
            <BookOpen className="w-5 h-5 text-blue-600" />
            Skill Gaps to Bridge
          </h3>
          {skill_gaps.length === 0 ? (
            <p className="text-sm text-gray-500 py-4 text-center">Complete AI assessment to discover skill gaps.</p>
          ) : (
            <div className="space-y-2">
              {skill_gaps.map((skill, i) => (
                <div key={i} className="flex items-center gap-3 p-2.5 bg-orange-50 rounded-lg">
                  <span className="w-2 h-2 bg-orange-400 rounded-full shrink-0" />
                  <span className="text-sm text-gray-700">{skill}</span>
                </div>
              ))}
            </div>
          )}
        </motion.div>
      </div>
    </motion.div>
  );
}
