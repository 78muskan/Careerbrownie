"use client";
import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { TrendingUp, RefreshCw, Building2, AlertCircle, Zap } from "lucide-react";
import api from "@/lib/api";

interface Prediction {
  placement_probability: number;
  predicted_package_min: number;
  predicted_package_max: number;
  top_matching_companies: string[];
  skill_gap_impact: Record<string, string>;
  timeline_to_ready: number;
  model_inputs: { career_score: number; assessments_completed: number; skills_count: number };
}

export default function PlacementPredictorPage() {
  const [data, setData] = useState<Prediction | null>(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const fetch = async (refresh = false) => {
    if (refresh) setRefreshing(true);
    const method = refresh ? api.post : api.get;
    const res = await method("/enterprise/placement-predictor/");
    setData(res.data);
    setLoading(false);
    setRefreshing(false);
  };

  useEffect(() => { fetch(); }, []);

  if (loading) return <div className="flex items-center justify-center h-64"><div className="animate-spin w-8 h-8 border-4 border-indigo-600 border-t-transparent rounded-full" /></div>;
  if (!data) return null;

  const pct = Math.round(data.placement_probability * 100);
  const circumference = 2 * Math.PI * 54;
  const dash = (pct / 100) * circumference;

  return (
    <div className="p-6 space-y-6">
      <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }}
        className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">AI Placement Predictor</h1>
          <p className="text-gray-500 text-sm mt-1">Predicts your placement probability based on your profile</p>
        </div>
        <button onClick={() => fetch(true)} disabled={refreshing}
          className="flex items-center gap-2 text-sm bg-white border border-gray-200 px-4 py-2 rounded-xl hover:bg-gray-50 transition disabled:opacity-50">
          <RefreshCw className={`w-4 h-4 ${refreshing ? "animate-spin" : ""}`} /> Update
        </button>
      </motion.div>

      {/* Main prediction card */}
      <motion.div initial={{ opacity: 0, scale: 0.97 }} animate={{ opacity: 1, scale: 1 }} transition={{ delay: 0.1 }}
        className="bg-white rounded-3xl p-8 shadow-sm border border-gray-100">
        <div className="grid md:grid-cols-3 gap-8 items-center">
          {/* Circular score */}
          <div className="flex flex-col items-center">
            <div className="relative w-32 h-32">
              <svg className="w-32 h-32 -rotate-90" viewBox="0 0 120 120">
                <circle cx="60" cy="60" r="54" fill="none" stroke="#EEF2FF" strokeWidth="12" />
                <motion.circle cx="60" cy="60" r="54" fill="none"
                  stroke={pct >= 60 ? "#22c55e" : pct >= 35 ? "#f59e0b" : "#ef4444"}
                  strokeWidth="12" strokeLinecap="round"
                  strokeDasharray={circumference}
                  initial={{ strokeDashoffset: circumference }}
                  animate={{ strokeDashoffset: circumference - dash }}
                  transition={{ duration: 1.5, ease: "easeOut" }} />
              </svg>
              <div className="absolute inset-0 flex flex-col items-center justify-center">
                <span className="text-3xl font-bold text-gray-900">{pct}%</span>
                <span className="text-xs text-gray-400">probability</span>
              </div>
            </div>
            <p className="text-sm text-gray-500 mt-2 text-center">Ready in ~{data.timeline_to_ready} months</p>
          </div>

          {/* Package prediction */}
          <div className="text-center">
            <div className="text-xs text-gray-400 mb-1">Predicted CTC Range</div>
            <div className="text-2xl font-bold text-gray-900">
              ₹{(data.predicted_package_min / 100000).toFixed(1)}L –
              ₹{(data.predicted_package_max / 100000).toFixed(1)}L
            </div>
            <div className="text-xs text-gray-400 mt-1">per annum</div>
          </div>

          {/* Model inputs */}
          <div className="space-y-3">
            {[
              { label: "Career Score", value: `${data.model_inputs.career_score}%` },
              { label: "Assessments", value: `${data.model_inputs.assessments_completed}/4` },
              { label: "Skills Added", value: data.model_inputs.skills_count },
            ].map(item => (
              <div key={item.label} className="flex justify-between items-center">
                <span className="text-sm text-gray-500">{item.label}</span>
                <span className="font-medium text-gray-800">{item.value}</span>
              </div>
            ))}
          </div>
        </div>
      </motion.div>

      <div className="grid md:grid-cols-2 gap-6">
        {/* Top matching companies */}
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.25 }}
          className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
          <h2 className="font-semibold text-gray-900 mb-4 flex items-center gap-2">
            <Building2 className="w-5 h-5 text-indigo-600" /> Top Matching Companies
          </h2>
          <div className="space-y-2">
            {data.top_matching_companies.map((company, i) => (
              <motion.div key={company} initial={{ opacity: 0, x: -10 }} animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.4 + i * 0.08 }}
                className="flex items-center gap-3 p-3 bg-indigo-50 rounded-xl">
                <div className="w-8 h-8 bg-indigo-600 rounded-lg flex items-center justify-center text-white text-xs font-bold">
                  {company[0]}
                </div>
                <span className="font-medium text-gray-800">{company}</span>
                <span className="ml-auto text-xs text-indigo-600">#{i + 1} match</span>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* Skill gap impact */}
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }}
          className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
          <h2 className="font-semibold text-gray-900 mb-4 flex items-center gap-2">
            <Zap className="w-5 h-5 text-orange-500" /> Skill Gap Impact
          </h2>
          {Object.keys(data.skill_gap_impact).length === 0 ? (
            <div className="text-center py-6">
              <TrendingUp className="w-8 h-8 text-green-400 mx-auto mb-2" />
              <p className="text-sm text-gray-400">Great! No critical skill gaps found</p>
            </div>
          ) : (
            <div className="space-y-3">
              {Object.entries(data.skill_gap_impact).map(([skill, impact]) => (
                <div key={skill} className="p-3 bg-orange-50 border border-orange-100 rounded-xl">
                  <div className="flex items-start gap-2">
                    <AlertCircle className="w-4 h-4 text-orange-500 mt-0.5 flex-shrink-0" />
                    <div>
                      <div className="font-medium text-sm text-gray-800">{skill}</div>
                      <div className="text-xs text-gray-500 mt-0.5">{impact}</div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </motion.div>
      </div>
    </div>
  );
}
