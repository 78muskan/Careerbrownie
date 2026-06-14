"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import { Calendar, Clock, Video, Loader2, Plus } from "lucide-react";
import api from "@/lib/api";

interface Session {
  id: string;
  session_type: string;
  status: string;
  scheduled_at: string;
  duration_minutes: number;
  meeting_link: string | null;
  counsellor_name: string | null;
}

const STATUS_COLORS: Record<string, string> = {
  confirmed: "bg-green-100 text-green-700",
  pending: "bg-yellow-100 text-yellow-700",
  completed: "bg-gray-100 text-gray-600",
  cancelled_student: "bg-red-100 text-red-600",
  cancelled_counsellor: "bg-red-100 text-red-600",
  in_progress: "bg-blue-100 text-blue-700",
};

export default function SessionsPage() {
  const [sessions, setSessions] = useState<Session[]>([]);
  const [loading, setLoading] = useState(true);
  const [tab, setTab] = useState<"upcoming" | "past">("upcoming");

  useEffect(() => {
    api.get("/sessions/my/")
      .then((r) => setSessions(r.data))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const upcoming = sessions.filter((s) => ["pending", "confirmed", "in_progress"].includes(s.status));
  const past = sessions.filter((s) => ["completed", "cancelled_student", "cancelled_counsellor"].includes(s.status));
  const shown = tab === "upcoming" ? upcoming : past;

  return (
    <div className="max-w-3xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-display font-bold text-gray-900">My Sessions</h1>
          <p className="text-sm text-gray-500 mt-1">All your career counselling sessions.</p>
        </div>
        <Link href="/book-consultation" className="btn-primary flex items-center gap-2 text-sm">
          <Plus className="w-4 h-4" />
          Book session
        </Link>
      </div>

      <div className="flex gap-1 bg-gray-100 p-1 rounded-xl w-fit">
        {(["upcoming", "past"] as const).map((t) => (
          <button
            key={t}
            onClick={() => setTab(t)}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${tab === t ? "bg-white shadow-sm text-gray-900" : "text-gray-500 hover:text-gray-700"}`}
          >
            {t.charAt(0).toUpperCase() + t.slice(1)} ({t === "upcoming" ? upcoming.length : past.length})
          </button>
        ))}
      </div>

      {loading ? (
        <div className="flex justify-center p-12"><Loader2 className="w-8 h-8 animate-spin text-primary-600" /></div>
      ) : shown.length === 0 ? (
        <div className="text-center bg-white rounded-2xl p-12 border border-gray-100">
          <Calendar className="w-12 h-12 text-gray-200 mx-auto mb-3" />
          <p className="text-gray-500">No {tab} sessions.</p>
          {tab === "upcoming" && (
            <Link href="/book-consultation" className="mt-4 inline-block text-primary-600 text-sm hover:underline">
              Book your first free session →
            </Link>
          )}
        </div>
      ) : (
        <div className="space-y-3">
          {shown.map((s) => (
            <div key={s.id} className="bg-white rounded-2xl p-5 shadow-sm border border-gray-100 flex gap-4">
              <div className="w-12 h-12 bg-primary-50 rounded-xl flex items-center justify-center shrink-0">
                <Calendar className="w-6 h-6 text-primary-600" />
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-start justify-between gap-2">
                  <div>
                    <p className="font-medium text-gray-900">{s.session_type.replace(/_/g, " ")}</p>
                    {s.counsellor_name && <p className="text-sm text-gray-500">with {s.counsellor_name}</p>}
                  </div>
                  <span className={`text-xs font-medium px-2.5 py-1 rounded-full shrink-0 ${STATUS_COLORS[s.status] ?? "bg-gray-100 text-gray-600"}`}>
                    {s.status.replace(/_/g, " ")}
                  </span>
                </div>
                <div className="flex items-center gap-4 mt-2 text-xs text-gray-500">
                  <span className="flex items-center gap-1">
                    <Clock className="w-3.5 h-3.5" />
                    {new Date(s.scheduled_at).toLocaleDateString("en-IN", { day: "numeric", month: "short", year: "numeric", hour: "2-digit", minute: "2-digit" })}
                  </span>
                  <span>{s.duration_minutes} min</span>
                </div>
                {s.meeting_link && (
                  <a href={s.meeting_link} target="_blank" rel="noopener noreferrer" className="mt-2 inline-flex items-center gap-1.5 text-xs text-blue-600 hover:underline">
                    <Video className="w-3.5 h-3.5" />
                    Join meeting
                  </a>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
