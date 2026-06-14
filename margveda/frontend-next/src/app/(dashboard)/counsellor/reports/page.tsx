"use client";
import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { TrendingUp, Users, Calendar, DollarSign, Star, Loader2 } from "lucide-react";
import api from "@/lib/api";

interface Summary {
  total_sessions: number;
  completed_sessions: number;
  upcoming_sessions: number;
  total_revenue: number;
  pending_revenue: number;
  avg_rating: number;
  unique_students: number;
}

interface Reports {
  summary: Summary;
  monthly_sessions: Array<{ month: string; count: number }>;
  recent_appointments: Array<{
    id: string; scheduled_date: string; start_time: string;
    status: string; student_name: string | null; session_type: string;
  }>;
}

export default function CounsellorReportsPage() {
  const [data, setData] = useState<Reports | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get("/portal/reports/")
      .then((r) => setData(r.data))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="flex justify-center p-16"><Loader2 className="w-8 h-8 animate-spin text-primary-600" /></div>;

  const s = data?.summary;

  return (
    <div className="max-w-5xl space-y-6">
      <div>
        <h1 className="text-2xl font-display font-bold text-gray-900">Reports & Analytics</h1>
        <p className="text-gray-500 text-sm mt-1">Track your sessions, students, and revenue.</p>
      </div>

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {[
          { label: "Total Sessions", value: s?.total_sessions ?? 0, icon: <Calendar className="w-5 h-5 text-primary-600" />, bg: "bg-primary-50" },
          { label: "Unique Students", value: s?.unique_students ?? 0, icon: <Users className="w-5 h-5 text-violet-600" />, bg: "bg-violet-50" },
          { label: "Total Revenue", value: `₹${(s?.total_revenue ?? 0).toLocaleString()}`, icon: <DollarSign className="w-5 h-5 text-green-600" />, bg: "bg-green-50" },
          { label: "Avg. Rating", value: `${(s?.avg_rating ?? 0).toFixed(1)}★`, icon: <Star className="w-5 h-5 text-yellow-500" />, bg: "bg-yellow-50" },
        ].map((stat, i) => (
          <motion.div key={stat.label} initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.08 }}
            className="bg-white rounded-2xl p-5 shadow-sm border border-gray-100">
            <div className={`w-10 h-10 ${stat.bg} rounded-xl flex items-center justify-center mb-3`}>{stat.icon}</div>
            <div className="text-2xl font-bold text-gray-900">{stat.value}</div>
            <div className="text-sm text-gray-500 mt-0.5">{stat.label}</div>
          </motion.div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Revenue breakdown */}
        <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
          <h3 className="font-semibold text-gray-900 mb-4 flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-green-600" />Revenue Breakdown
          </h3>
          <div className="space-y-3">
            {[
              { label: "Total Earned", value: s?.total_revenue ?? 0, color: "text-green-600" },
              { label: "Pending Payout", value: s?.pending_revenue ?? 0, color: "text-yellow-600" },
              { label: "Completed Sessions", value: s?.completed_sessions ?? 0, color: "text-blue-600", unit: " sessions" },
              { label: "Upcoming Sessions", value: s?.upcoming_sessions ?? 0, color: "text-primary-600", unit: " sessions" },
            ].map((item) => (
              <div key={item.label} className="flex justify-between items-center py-2 border-b border-gray-50 last:border-0">
                <span className="text-sm text-gray-600">{item.label}</span>
                <span className={`font-semibold ${item.color}`}>
                  {item.unit ? item.value + item.unit : `₹${Number(item.value).toLocaleString()}`}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Recent appointments */}
        <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
          <h3 className="font-semibold text-gray-900 mb-4 flex items-center gap-2">
            <Calendar className="w-5 h-5 text-primary-600" />Recent Appointments
          </h3>
          {!data?.recent_appointments?.length ? (
            <p className="text-gray-500 text-sm py-4">No appointments yet.</p>
          ) : (
            <div className="space-y-2">
              {data.recent_appointments.map((a) => (
                <div key={a.id} className="flex items-center gap-3 p-2.5 bg-gray-50 rounded-xl text-sm">
                  <div className="flex-1 min-w-0">
                    <p className="font-medium text-gray-900 truncate">{a.student_name ?? "Open Slot"}</p>
                    <p className="text-xs text-gray-500">
                      {new Date(a.scheduled_date).toLocaleDateString("en-IN")} · {a.session_type?.replace(/_/g, " ")}
                    </p>
                  </div>
                  <span className={`text-xs font-medium px-2 py-1 rounded-full shrink-0 ${
                    a.status === "completed" ? "bg-green-100 text-green-700" :
                    a.status === "confirmed" ? "bg-blue-100 text-blue-700" :
                    "bg-gray-100 text-gray-600"
                  }`}>{a.status}</span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
