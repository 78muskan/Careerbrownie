"use client";
import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { BarChart2, Users, CheckCircle } from "lucide-react";
import api from "@/lib/api";

interface Analytics {
  total_students: number;
  profile_score_distribution: Record<string, number>;
  top_career_aspirations: { career: string; count: number }[];
  assessments_by_type: Record<string, number>;
}

const ASSESSMENT_LABELS: Record<string, string> = {
  interest: "Interest (RIASEC)",
  personality: "Personality (Big 5)",
  aptitude: "Aptitude",
  readiness: "Career Readiness",
};

export default function SchoolAnalyticsPage() {
  const [data, setData] = useState<Analytics | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get("/school/analytics/").then(r => { setData(r.data); setLoading(false); });
  }, []);

  if (loading) return <div className="flex items-center justify-center h-64"><div className="animate-spin w-8 h-8 border-4 border-indigo-600 border-t-transparent rounded-full" /></div>;
  if (!data) return null;

  const maxCareer = Math.max(...data.top_career_aspirations.map(c => c.count), 1);

  return (
    <div className="p-6 space-y-6">
      <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }}>
        <h1 className="text-2xl font-bold text-gray-900">Student Analytics</h1>
        <p className="text-gray-500 mt-1">{data.total_students} students tracked across all batches</p>
      </motion.div>

      <div className="grid md:grid-cols-3 gap-6">
        {/* Profile Score Distribution */}
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}
          className="md:col-span-1 bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
          <h2 className="font-semibold text-gray-900 mb-4 flex items-center gap-2">
            <BarChart2 className="w-5 h-5 text-indigo-600" /> Profile Score Distribution
          </h2>
          <div className="space-y-4">
            {Object.entries(data.profile_score_distribution).map(([range, count]) => (
              <div key={range}>
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-gray-600">{range}%</span>
                  <span className="font-medium">{count} students</span>
                </div>
                <div className="w-full bg-gray-100 rounded-full h-3">
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: `${Math.min((count / (data.total_students || 1)) * 100, 100)}%` }}
                    transition={{ delay: 0.4 }}
                    className="h-3 bg-indigo-500 rounded-full" />
                </div>
              </div>
            ))}
          </div>
        </motion.div>

        {/* Top Career Aspirations */}
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}
          className="md:col-span-2 bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
          <h2 className="font-semibold text-gray-900 mb-4 flex items-center gap-2">
            <Users className="w-5 h-5 text-purple-600" /> Top Career Aspirations
          </h2>
          <div className="space-y-3">
            {data.top_career_aspirations.map((item, i) => (
              <div key={item.career}>
                <div className="flex justify-between text-sm mb-1">
                  <span className="capitalize text-gray-700">{item.career.replace(/_/g, " ")}</span>
                  <span className="text-gray-500">{item.count}</span>
                </div>
                <div className="w-full bg-gray-100 rounded-full h-2.5">
                  <motion.div
                    initial={{ width: 0 }} animate={{ width: `${(item.count / maxCareer) * 100}%` }}
                    transition={{ delay: 0.5 + i * 0.06 }}
                    className="h-2.5 rounded-full bg-gradient-to-r from-purple-500 to-indigo-500" />
                </div>
              </div>
            ))}
          </div>
        </motion.div>
      </div>

      {/* Assessment Completion */}
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }}
        className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
        <h2 className="font-semibold text-gray-900 mb-5 flex items-center gap-2">
          <CheckCircle className="w-5 h-5 text-green-600" /> Assessment Completion
        </h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {Object.entries(data.assessments_by_type).map(([type, count]) => (
            <div key={type} className="text-center p-4 bg-gray-50 rounded-xl">
              <div className="text-3xl font-bold text-indigo-600">{count}</div>
              <div className="text-sm text-gray-500 mt-1">{ASSESSMENT_LABELS[type] || type}</div>
              <div className="text-xs text-gray-400 mt-0.5">
                {data.total_students > 0 ? Math.round((count / data.total_students) * 100) : 0}% completion
              </div>
            </div>
          ))}
        </div>
      </motion.div>
    </div>
  );
}
