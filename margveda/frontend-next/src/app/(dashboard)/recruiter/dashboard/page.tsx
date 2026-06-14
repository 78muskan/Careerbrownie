"use client";
import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { Briefcase, Users, TrendingUp, CheckSquare, Plus } from "lucide-react";
import api from "@/lib/api";

interface RecruiterData {
  company: { name: string; industry: string; city: string; employee_size: string; is_verified: boolean };
  stats: { active_jobs: number; active_internships: number; total_applications: number; shortlisted: number };
  recent_jobs: { id: string; title: string; location: string; job_type: string; views_count: number; created_at: string }[];
}

export default function RecruiterDashboardPage() {
  const [data, setData] = useState<RecruiterData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get("/jobs/recruiter/dashboard/").then(r => { setData(r.data); setLoading(false); });
  }, []);

  if (loading) return <div className="flex items-center justify-center h-64"><div className="animate-spin w-8 h-8 border-4 border-indigo-600 border-t-transparent rounded-full" /></div>;
  if (!data) return null;

  const stats = [
    { label: "Active Jobs", value: data.stats.active_jobs, icon: Briefcase, color: "from-blue-500 to-blue-600" },
    { label: "Internships", value: data.stats.active_internships, icon: TrendingUp, color: "from-purple-500 to-purple-600" },
    { label: "Applications", value: data.stats.total_applications, icon: Users, color: "from-green-500 to-green-600" },
    { label: "Shortlisted", value: data.stats.shortlisted, icon: CheckSquare, color: "from-orange-500 to-orange-600" },
  ];

  return (
    <div className="p-6 space-y-6">
      <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }}
        className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">
            {data.company.name}
            {data.company.is_verified && (
              <span className="ml-2 text-xs bg-green-100 text-green-700 px-2 py-0.5 rounded-full font-normal">Verified</span>
            )}
          </h1>
          <p className="text-gray-500 capitalize">{data.company.industry} · {data.company.city} · {data.company.employee_size} employees</p>
        </div>
        <a href="/recruiter/jobs"
          className="flex items-center gap-2 bg-indigo-600 text-white px-4 py-2 rounded-xl hover:bg-indigo-700 transition text-sm font-medium">
          <Plus className="w-4 h-4" /> Post Job
        </a>
      </motion.div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {stats.map((s, i) => (
          <motion.div key={s.label} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.08 }}
            className={`bg-gradient-to-br ${s.color} rounded-2xl p-5 text-white`}>
            <s.icon className="w-6 h-6 mb-3 opacity-80" />
            <div className="text-3xl font-bold">{s.value}</div>
            <div className="text-sm opacity-80 mt-1">{s.label}</div>
          </motion.div>
        ))}
      </div>

      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.35 }}
        className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
        <div className="flex items-center justify-between mb-5">
          <h2 className="font-semibold text-gray-900">Recent Job Postings</h2>
          <a href="/recruiter/jobs" className="text-sm text-indigo-600 hover:underline">Manage all</a>
        </div>
        {data.recent_jobs.length === 0 && (
          <div className="text-center py-8">
            <Briefcase className="w-10 h-10 text-gray-300 mx-auto mb-3" />
            <p className="text-gray-400">No jobs posted yet</p>
            <a href="/recruiter/jobs" className="text-indigo-600 text-sm hover:underline mt-2 inline-block">Post your first job →</a>
          </div>
        )}
        <div className="space-y-3">
          {data.recent_jobs.map(job => (
            <div key={job.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-xl">
              <div>
                <div className="font-medium text-gray-800">{job.title}</div>
                <div className="text-xs text-gray-400 mt-0.5">
                  {job.location} · <span className="capitalize">{job.job_type.replace("_", " ")}</span>
                </div>
              </div>
              <div className="text-right">
                <div className="text-sm font-medium text-gray-700">{job.views_count} views</div>
                <div className="text-xs text-gray-400">{new Date(job.created_at).toLocaleDateString("en-IN")}</div>
              </div>
            </div>
          ))}
        </div>
      </motion.div>
    </div>
  );
}
