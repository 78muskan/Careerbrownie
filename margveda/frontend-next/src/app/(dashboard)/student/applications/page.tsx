"use client";
import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { FileText, CheckCircle, XCircle, Clock, AlertCircle } from "lucide-react";
import api from "@/lib/api";

interface Application {
  id: string;
  job_title: string;
  status: string;
  cover_letter: string;
  applied_at: string;
  updated_at: string;
  job: string | null;
  internship: string | null;
}

const STATUS_CONFIG: Record<string, { label: string; color: string; icon: React.ElementType }> = {
  applied: { label: "Applied", color: "bg-blue-100 text-blue-700", icon: Clock },
  shortlisted: { label: "Shortlisted", color: "bg-yellow-100 text-yellow-700", icon: AlertCircle },
  interview: { label: "Interview", color: "bg-purple-100 text-purple-700", icon: FileText },
  offered: { label: "Offer Received", color: "bg-green-100 text-green-700", icon: CheckCircle },
  rejected: { label: "Rejected", color: "bg-red-100 text-red-600", icon: XCircle },
  withdrawn: { label: "Withdrawn", color: "bg-gray-100 text-gray-500", icon: XCircle },
};

export default function ApplicationsPage() {
  const [apps, setApps] = useState<Application[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get("/jobs/applications/").then(r => { setApps(r.data); setLoading(false); });
  }, []);

  const groupedByStatus = (status: string) => apps.filter(a => a.status === status);

  const stats = {
    total: apps.length,
    shortlisted: groupedByStatus("shortlisted").length + groupedByStatus("interview").length,
    offered: groupedByStatus("offered").length,
    pending: groupedByStatus("applied").length,
  };

  if (loading) return <div className="flex items-center justify-center h-64"><div className="animate-spin w-8 h-8 border-4 border-indigo-600 border-t-transparent rounded-full" /></div>;

  return (
    <div className="p-6 space-y-6">
      <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }}>
        <h1 className="text-2xl font-bold text-gray-900">My Applications</h1>
        <p className="text-gray-500 mt-1">Track all your job and internship applications</p>
      </motion.div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {[
          { label: "Total Applied", value: stats.total, color: "from-blue-500 to-blue-600" },
          { label: "Pending Review", value: stats.pending, color: "from-yellow-500 to-yellow-600" },
          { label: "Shortlisted", value: stats.shortlisted, color: "from-purple-500 to-purple-600" },
          { label: "Offers", value: stats.offered, color: "from-green-500 to-green-600" },
        ].map((s, i) => (
          <motion.div key={s.label} initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.08 }}
            className={`bg-gradient-to-br ${s.color} rounded-2xl p-5 text-white`}>
            <div className="text-3xl font-bold">{s.value}</div>
            <div className="text-sm opacity-80 mt-1">{s.label}</div>
          </motion.div>
        ))}
      </div>

      {apps.length === 0 ? (
        <div className="text-center py-12 bg-white rounded-2xl border border-gray-100">
          <FileText className="w-12 h-12 text-gray-300 mx-auto mb-3" />
          <p className="text-gray-400 font-medium">No applications yet</p>
          <a href="/student/jobs" className="mt-3 inline-block text-sm text-indigo-600 hover:underline">
            Browse matched jobs →
          </a>
        </div>
      ) : (
        <div className="space-y-3">
          {apps.map((app, i) => {
            const config = STATUS_CONFIG[app.status] || STATUS_CONFIG.applied;
            const Icon = config.icon;
            return (
              <motion.div key={app.id} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.06 }}
                className="bg-white rounded-2xl p-5 shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-1">
                      <h3 className="font-semibold text-gray-900">{app.job_title || "Application"}</h3>
                      <span className="text-xs text-gray-400">{app.internship ? "Internship" : "Job"}</span>
                    </div>
                    <div className="text-xs text-gray-400">
                      Applied {new Date(app.applied_at).toLocaleDateString("en-IN")} ·
                      Updated {new Date(app.updated_at).toLocaleDateString("en-IN")}
                    </div>
                  </div>
                  <div className={`flex items-center gap-1.5 text-xs px-3 py-1.5 rounded-full font-medium ${config.color}`}>
                    <Icon className="w-3.5 h-3.5" />
                    {config.label}
                  </div>
                </div>
                {app.cover_letter && (
                  <div className="mt-3 text-xs text-gray-400 bg-gray-50 rounded-lg px-3 py-2 line-clamp-1">
                    {app.cover_letter}
                  </div>
                )}
              </motion.div>
            );
          })}
        </div>
      )}
    </div>
  );
}
