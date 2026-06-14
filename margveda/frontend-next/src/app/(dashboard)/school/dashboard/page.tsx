"use client";
import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { Users, BookOpen, BarChart2, Award, TrendingUp, School } from "lucide-react";
import api from "@/lib/api";

interface DashboardData {
  school: { name: string; city: string; subscription_plan: string; school_type: string };
  stats: {
    total_batches: number;
    total_students: number;
    assessments_completed: number;
    avg_profile_score: number;
  };
  top_career_interests: { interest: string; count: number }[];
  recent_batches: { id: string; name: string; grade: string; student_count: number }[];
}

export default function SchoolDashboardPage() {
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get("/school/dashboard/").then(r => { setData(r.data); setLoading(false); });
  }, []);

  if (loading) return <div className="flex items-center justify-center h-64"><div className="animate-spin w-8 h-8 border-4 border-indigo-600 border-t-transparent rounded-full" /></div>;
  if (!data) return null;

  const stats = [
    { label: "Total Batches", value: data.stats.total_batches, icon: BookOpen, color: "from-blue-500 to-blue-600" },
    { label: "Total Students", value: data.stats.total_students, icon: Users, color: "from-purple-500 to-purple-600" },
    { label: "Assessments Done", value: data.stats.assessments_completed, icon: BarChart2, color: "from-green-500 to-green-600" },
    { label: "Avg Profile Score", value: `${data.stats.avg_profile_score}%`, icon: Award, color: "from-orange-500 to-orange-600" },
  ];

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }}
        className="flex items-center gap-3">
        <div className="p-3 bg-indigo-100 rounded-xl"><School className="w-7 h-7 text-indigo-600" /></div>
        <div>
          <h1 className="text-2xl font-bold text-gray-900">{data.school.name}</h1>
          <p className="text-gray-500">{data.school.city} · {data.school.school_type.toUpperCase()} ·
            <span className="ml-1 text-indigo-600 capitalize font-medium">{data.school.subscription_plan} Plan</span>
          </p>
        </div>
      </motion.div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {stats.map((s, i) => (
          <motion.div key={s.label} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.08 }}
            className={`bg-gradient-to-br ${s.color} rounded-2xl p-5 text-white`}>
            <s.icon className="w-6 h-6 mb-3 opacity-80" />
            <div className="text-2xl font-bold">{s.value}</div>
            <div className="text-sm opacity-80 mt-1">{s.label}</div>
          </motion.div>
        ))}
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        {/* Top Career Interests */}
        <motion.div initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.3 }}
          className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
          <div className="flex items-center gap-2 mb-5">
            <TrendingUp className="w-5 h-5 text-indigo-600" />
            <h2 className="font-semibold text-gray-900">Top Career Interests</h2>
          </div>
          <div className="space-y-3">
            {data.top_career_interests.length === 0 && (
              <p className="text-gray-400 text-sm text-center py-4">No data yet — students need to complete profiles</p>
            )}
            {data.top_career_interests.map((item, i) => (
              <div key={item.interest}>
                <div className="flex justify-between text-sm mb-1">
                  <span className="capitalize text-gray-700">{item.interest.replace(/_/g, " ")}</span>
                  <span className="text-gray-500">{item.count} students</span>
                </div>
                <div className="w-full bg-gray-100 rounded-full h-2">
                  <motion.div
                    initial={{ width: 0 }} animate={{ width: `${Math.min(item.count * 20, 100)}%` }}
                    transition={{ delay: 0.5 + i * 0.1 }}
                    className="h-2 bg-indigo-500 rounded-full" />
                </div>
              </div>
            ))}
          </div>
        </motion.div>

        {/* Recent Batches */}
        <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.3 }}
          className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
          <div className="flex items-center justify-between mb-5">
            <h2 className="font-semibold text-gray-900 flex items-center gap-2">
              <BookOpen className="w-5 h-5 text-indigo-600" /> Recent Batches
            </h2>
            <a href="/school/batches" className="text-sm text-indigo-600 hover:underline">View all</a>
          </div>
          {data.recent_batches.length === 0 && (
            <p className="text-gray-400 text-sm text-center py-4">No batches created yet</p>
          )}
          <div className="space-y-3">
            {data.recent_batches.map(batch => (
              <a key={batch.id} href={`/school/batches`}
                className="flex items-center justify-between p-3 bg-gray-50 hover:bg-indigo-50 rounded-xl transition-colors">
                <div>
                  <div className="font-medium text-gray-800">{batch.name}</div>
                  <div className="text-xs text-gray-400">Grade {batch.grade}</div>
                </div>
                <div className="text-right">
                  <div className="text-sm font-semibold text-indigo-600">{batch.student_count}</div>
                  <div className="text-xs text-gray-400">students</div>
                </div>
              </a>
            ))}
          </div>
        </motion.div>
      </div>
    </div>
  );
}
