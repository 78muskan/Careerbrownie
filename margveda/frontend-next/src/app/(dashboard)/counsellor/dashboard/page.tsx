"use client";
import { useEffect, useState } from "react";
import { Calendar, Users, Star } from "lucide-react";
import api from "@/lib/api";

interface Session {
  id: string;
  session_type: string;
  status: string;
  scheduled_at: string;
  duration_minutes: number;
  student_name: string | null;
  student_rating: number | null;
}

export default function CounsellorDashboardPage() {
  const [sessions, setSessions] = useState<Session[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get("/sessions/counsellor/")
      .then((r) => setSessions(r.data))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const upcoming = sessions.filter((s) => ["pending", "confirmed"].includes(s.status));
  const avgRating = (() => {
    const rated = sessions.filter((s) => s.student_rating);
    if (!rated.length) return 0;
    return (rated.reduce((acc, s) => acc + (s.student_rating ?? 0), 0) / rated.length).toFixed(1);
  })();

  return (
    <div className="max-w-5xl space-y-6">
      <h1 className="text-2xl font-display font-bold text-gray-900">Counsellor Dashboard</h1>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        {[
          { label: "Total Sessions", value: sessions.length, icon: <Calendar className="w-5 h-5 text-primary-600" />, bg: "bg-primary-50" },
          { label: "Upcoming", value: upcoming.length, icon: <Users className="w-5 h-5 text-violet-600" />, bg: "bg-violet-50" },
          { label: "Avg. Rating", value: avgRating || "—", icon: <Star className="w-5 h-5 text-yellow-500" />, bg: "bg-yellow-50" },
        ].map((s) => (
          <div key={s.label} className="bg-white rounded-2xl p-5 shadow-sm border border-gray-100">
            <div className={`w-10 h-10 ${s.bg} rounded-xl flex items-center justify-center mb-3`}>{s.icon}</div>
            <div className="text-2xl font-bold text-gray-900">{s.value}</div>
            <div className="text-sm text-gray-500 mt-0.5">{s.label}</div>
          </div>
        ))}
      </div>

      <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
        <h3 className="font-semibold text-gray-900 mb-4">My Sessions</h3>
        {loading ? (
          <div className="text-center py-8 text-gray-400">Loading…</div>
        ) : sessions.length === 0 ? (
          <div className="text-center py-8 text-gray-400">No sessions yet.</div>
        ) : (
          <div className="space-y-3">
            {sessions.slice(0, 10).map((s) => (
              <div key={s.id} className="flex items-center gap-4 p-3 bg-gray-50 rounded-xl text-sm">
                <div className="flex-1">
                  <p className="font-medium text-gray-900">{s.session_type.replace(/_/g, " ")}</p>
                  <p className="text-gray-500">{s.student_name} · {new Date(s.scheduled_at).toLocaleDateString("en-IN")}</p>
                </div>
                <span className={`text-xs px-2.5 py-1 rounded-full font-medium ${s.status === "confirmed" ? "bg-green-100 text-green-700" : "bg-gray-100 text-gray-600"}`}>
                  {s.status}
                </span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
