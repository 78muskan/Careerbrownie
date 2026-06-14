"use client";
import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { Sparkles, TrendingUp, BookOpen, Target, Zap, ArrowRight, Loader2, ExternalLink } from "lucide-react";
import Link from "next/link";
import api from "@/lib/api";

interface CareerMatch {
  key: string;
  title: string;
  domain: string;
  match_pct: number;
  avg_salary_india: string;
  growth_rate: string;
  key_skills: string[];
  demand: string;
}

interface Trend { domain: string; trend: string; impact: string; }
interface Resource { title: string; url: string; type: string; free: boolean; }
interface Insight { type: string; title: string; content: string; data: Record<string, unknown>; }

interface AdvisorData {
  insights: Insight[];
  career_matches: CareerMatch[];
  skill_gaps: string[];
  market_trends: Trend[];
  learning_resources: Resource[];
  assessments_completed: string[];
}

const DEMAND_COLOR: Record<string, string> = {
  very_high: "bg-green-100 text-green-700",
  high: "bg-blue-100 text-blue-700",
  medium: "bg-yellow-100 text-yellow-700",
  stable: "bg-gray-100 text-gray-600",
};

export default function AIAdvisorPage() {
  const [data, setData] = useState<AdvisorData | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<"matches" | "gaps" | "trends" | "resources">("matches");

  useEffect(() => {
    api.get("/ai/advisor/")
      .then((r) => setData(r.data))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="flex justify-center p-16"><Loader2 className="w-8 h-8 animate-spin text-primary-600" /></div>;

  const assessed = data?.assessments_completed.length ?? 0;

  return (
    <div className="max-w-5xl space-y-6">
      <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }}>
        <div className="flex items-start justify-between gap-4">
          <div>
            <h1 className="text-2xl font-display font-bold text-gray-900 flex items-center gap-2">
              <Sparkles className="w-6 h-6 text-violet-500" />
              AI Career Advisor
            </h1>
            <p className="text-gray-500 mt-1">Personalised career intelligence powered by your profile and assessments.</p>
          </div>
          {assessed < 4 && (
            <Link href="/student/assessment" className="btn-secondary text-sm shrink-0">
              {assessed}/4 Assessments done →
            </Link>
          )}
        </div>
      </motion.div>

      {/* Insights strip */}
      {data?.insights && data.insights.length > 0 && (
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {data.insights.slice(0, 4).map((ins, i) => (
            <motion.div key={i} initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.08 }}
              className="bg-gradient-to-br from-violet-50 to-primary-50 rounded-2xl p-5 border border-violet-100"
            >
              <div className="flex items-start gap-3">
                <div className="w-8 h-8 bg-violet-100 rounded-lg flex items-center justify-center shrink-0">
                  <Sparkles className="w-4 h-4 text-violet-600" />
                </div>
                <div>
                  <p className="text-sm font-semibold text-gray-900">{ins.title}</p>
                  <p className="text-xs text-gray-600 mt-1 leading-relaxed">{ins.content}</p>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      )}

      {/* Tabs */}
      <div className="flex gap-1 bg-gray-100 p-1 rounded-xl w-fit">
        {([
          { key: "matches", label: "Career Matches", icon: <Target className="w-4 h-4" /> },
          { key: "gaps", label: "Skill Gaps", icon: <Zap className="w-4 h-4" /> },
          { key: "trends", label: "Market Trends", icon: <TrendingUp className="w-4 h-4" /> },
          { key: "resources", label: "Learn", icon: <BookOpen className="w-4 h-4" /> },
        ] as const).map((t) => (
          <button key={t.key} onClick={() => setActiveTab(t.key)}
            className={`flex items-center gap-1.5 px-4 py-2 rounded-lg text-sm font-medium transition-all ${
              activeTab === t.key ? "bg-white shadow-sm text-gray-900" : "text-gray-500 hover:text-gray-700"
            }`}
          >
            {t.icon}{t.label}
          </button>
        ))}
      </div>

      {/* Career Matches */}
      {activeTab === "matches" && (
        <div className="space-y-3">
          {!data?.career_matches?.length ? (
            <div className="text-center bg-white rounded-2xl p-12 border border-gray-100">
              <Target className="w-12 h-12 text-gray-200 mx-auto mb-3" />
              <p className="text-gray-500">Complete your profile and assessments to get career matches.</p>
              <Link href="/student/assessment" className="mt-4 inline-block btn-primary">Take Assessments →</Link>
            </div>
          ) : data.career_matches.map((c, i) => (
            <motion.div key={c.key} initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.05 }}
              className="bg-white rounded-2xl p-5 shadow-sm border border-gray-100 hover:border-primary-200 hover:shadow-md transition-all"
            >
              <div className="flex items-start justify-between gap-4">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <h3 className="font-semibold text-gray-900">{c.title}</h3>
                    <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${DEMAND_COLOR[c.demand] ?? "bg-gray-100 text-gray-600"}`}>
                      {c.demand?.replace("_", " ")} demand
                    </span>
                  </div>
                  <p className="text-sm text-gray-500">{c.domain} · {c.avg_salary_india} · {c.growth_rate} growth</p>
                  <div className="flex flex-wrap gap-1.5 mt-2">
                    {c.key_skills?.slice(0, 4).map((s) => (
                      <span key={s} className="text-xs bg-gray-100 text-gray-600 px-2 py-0.5 rounded-md">{s}</span>
                    ))}
                  </div>
                </div>
                <div className="text-right shrink-0">
                  <div className="text-2xl font-bold text-primary-600">{c.match_pct}%</div>
                  <div className="text-xs text-gray-400">match</div>
                  <div className="mt-2 w-16 bg-gray-100 rounded-full h-1.5">
                    <div className="bg-primary-500 h-1.5 rounded-full" style={{ width: `${c.match_pct}%` }} />
                  </div>
                </div>
              </div>
              <div className="flex items-center gap-2 mt-3 pt-3 border-t border-gray-50">
                <Link href={`/student/career/${c.key}`} className="text-sm text-primary-600 hover:underline flex items-center gap-1">
                  Explore career <ArrowRight className="w-3.5 h-3.5" />
                </Link>
                <Link href="/student/career-roadmap" className="text-sm text-gray-500 hover:underline flex items-center gap-1">
                  Generate roadmap
                </Link>
              </div>
            </motion.div>
          ))}
        </div>
      )}

      {/* Skill Gaps */}
      {activeTab === "gaps" && (
        <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
          <h3 className="font-semibold text-gray-900 mb-4">Skills to develop for your target career</h3>
          {!data?.skill_gaps?.length ? (
            <p className="text-gray-500 text-sm">Complete your profile with target roles to see skill gaps.</p>
          ) : (
            <div className="space-y-3">
              {data.skill_gaps.map((gap, i) => (
                <div key={i} className="flex items-center gap-4 p-3 bg-orange-50 rounded-xl">
                  <div className="w-2 h-2 bg-orange-400 rounded-full shrink-0" />
                  <div className="flex-1">
                    <span className="text-sm font-medium text-gray-800">{gap}</span>
                  </div>
                  <span className="text-xs text-orange-600 font-medium">To develop</span>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Market Trends */}
      {activeTab === "trends" && (
        <div className="space-y-3">
          {data?.market_trends?.map((t, i) => (
            <motion.div key={i} initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.06 }}
              className="bg-white rounded-2xl p-5 shadow-sm border border-gray-100"
            >
              <div className="flex items-start gap-3">
                <TrendingUp className={`w-5 h-5 mt-0.5 shrink-0 ${t.impact === "positive" ? "text-green-500" : "text-gray-400"}`} />
                <div>
                  <span className="text-xs font-semibold text-gray-400 uppercase tracking-wide">{t.domain}</span>
                  <p className="text-sm text-gray-800 mt-0.5 leading-relaxed">{t.trend}</p>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      )}

      {/* Learning Resources */}
      {activeTab === "resources" && (
        <div className="space-y-3">
          {!data?.learning_resources?.length ? (
            <div className="text-center bg-white rounded-2xl p-12 border border-gray-100">
              <BookOpen className="w-12 h-12 text-gray-200 mx-auto mb-3" />
              <p className="text-gray-500">Complete your profile to get personalised learning recommendations.</p>
            </div>
          ) : data.learning_resources.map((r, i) => (
            <div key={i} className="bg-white rounded-2xl p-4 shadow-sm border border-gray-100 flex items-center gap-4">
              <div className="w-10 h-10 bg-blue-50 rounded-xl flex items-center justify-center shrink-0">
                <BookOpen className="w-5 h-5 text-blue-600" />
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-gray-900 truncate">{r.title}</p>
                <div className="flex items-center gap-2 mt-0.5">
                  <span className="text-xs text-gray-400">{r.type}</span>
                  {r.free && <span className="text-xs bg-green-100 text-green-700 px-1.5 py-0.5 rounded">Free</span>}
                </div>
              </div>
              <a href={r.url} target="_blank" rel="noopener noreferrer"
                className="shrink-0 p-2 rounded-lg text-gray-400 hover:text-primary-600 hover:bg-primary-50 transition-colors">
                <ExternalLink className="w-4 h-4" />
              </a>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
