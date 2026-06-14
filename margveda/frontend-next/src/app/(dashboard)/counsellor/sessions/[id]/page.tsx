"use client";
import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { Loader2, Save, ChevronLeft } from "lucide-react";
import api from "@/lib/api";

interface Appointment {
  id: string;
  scheduled_date: string;
  start_time: string;
  end_time: string;
  status: string;
  session_type: string;
  meeting_link: string;
  student_name: string | null;
  student_notes: string;
}

interface SessionNote {
  key_points: string;
  action_items: Array<{ task: string; deadline: string }>;
  resources_shared: string[];
  student_feedback: string;
  student_rating: number | null;
  next_session_notes: string;
  is_private: boolean;
}

const inputCls = "w-full px-4 py-3 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary-500";

export default function SessionDetailPage() {
  const params = useParams();
  const router = useRouter();
  const id = params.id as string;

  const [appt, setAppt] = useState<Appointment | null>(null);
  const [note, setNote] = useState<Partial<SessionNote>>({
    key_points: "", action_items: [], resources_shared: [], student_feedback: "",
    student_rating: null, next_session_notes: "", is_private: false,
  });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [meetingLink, setMeetingLink] = useState("");

  useEffect(() => {
    api.get(`/portal/appointments/${id}/`)
      .then((r) => {
        setAppt(r.data);
        setMeetingLink(r.data.meeting_link || "");
        if (r.data.session_note) setNote(r.data.session_note);
      })
      .catch(() => router.push("/counsellor/dashboard"))
      .finally(() => setLoading(false));
  }, [id, router]);

  const updateStatus = async (newStatus: string) => {
    const { data } = await api.patch(`/portal/appointments/${id}/`, { status: newStatus, meeting_link: meetingLink });
    setAppt(data);
  };

  const saveNote = async () => {
    setSaving(true);
    try {
      await api.post(`/portal/appointments/${id}/notes/`, note);
    } catch {
      alert("Save failed.");
    } finally {
      setSaving(false);
    }
  };

  const addActionItem = () => {
    setNote((n) => ({ ...n, action_items: [...(n.action_items || []), { task: "", deadline: "" }] }));
  };

  if (loading) return <div className="flex justify-center p-16"><Loader2 className="w-8 h-8 animate-spin text-primary-600" /></div>;

  return (
    <div className="max-w-3xl space-y-6">
      <button onClick={() => router.back()} className="flex items-center gap-2 text-sm text-gray-500 hover:text-gray-900">
        <ChevronLeft className="w-4 h-4" />Back
      </button>

      {appt && (
        <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
          <div className="flex items-start justify-between gap-4">
            <div>
              <h1 className="text-xl font-display font-bold text-gray-900">{appt.session_type.replace(/_/g, " ")}</h1>
              <p className="text-gray-500 text-sm mt-1">
                Student: <span className="font-medium text-gray-800">{appt.student_name ?? "Open"}</span>
              </p>
              <p className="text-gray-500 text-sm">
                {new Date(appt.scheduled_date).toLocaleDateString("en-IN", { weekday: "long", day: "numeric", month: "long" })} · {appt.start_time} – {appt.end_time}
              </p>
            </div>
            <span className={`text-sm font-medium px-3 py-1.5 rounded-full ${
              appt.status === "confirmed" ? "bg-green-100 text-green-700" :
              appt.status === "completed" ? "bg-gray-100 text-gray-600" :
              "bg-yellow-100 text-yellow-700"
            }`}>{appt.status}</span>
          </div>

          {appt.student_notes && (
            <div className="mt-4 p-3 bg-blue-50 rounded-xl text-sm text-blue-800">
              <span className="font-medium">Student notes: </span>{appt.student_notes}
            </div>
          )}

          <div className="mt-4 flex flex-wrap gap-2">
            {appt.status === "requested" && (
              <button onClick={() => updateStatus("confirmed")} className="btn-primary text-sm">Confirm Session</button>
            )}
            {appt.status === "confirmed" && (
              <button onClick={() => updateStatus("completed")} className="bg-green-600 text-white px-4 py-2 rounded-xl text-sm font-medium hover:bg-green-700">Mark Complete</button>
            )}
            {["requested", "confirmed"].includes(appt.status) && (
              <button onClick={() => updateStatus("cancelled")} className="btn-secondary text-sm text-red-600">Cancel</button>
            )}
          </div>
        </div>
      )}

      {/* Meeting Link */}
      <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
        <h3 className="font-semibold text-gray-900 mb-3">Meeting Link</h3>
        <div className="flex gap-3">
          <input type="url" value={meetingLink} onChange={(e) => setMeetingLink(e.target.value)}
            className={`${inputCls} flex-1`} placeholder="https://meet.google.com/..." />
          <button onClick={() => updateStatus(appt?.status || "confirmed")} className="btn-secondary text-sm">Update</button>
        </div>
      </div>

      {/* Session Notes */}
      <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 space-y-5">
        <div className="flex items-center justify-between">
          <h3 className="font-semibold text-gray-900">Session Notes</h3>
          <button onClick={saveNote} disabled={saving} className="btn-primary text-sm flex items-center gap-2 disabled:opacity-60">
            {saving && <Loader2 className="w-4 h-4 animate-spin" />}
            <Save className="w-4 h-4" />{saving ? "Saving…" : "Save Notes"}
          </button>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1.5">Key Discussion Points</label>
          <textarea rows={4} value={note.key_points || ""} onChange={(e) => setNote({ ...note, key_points: e.target.value })}
            className={`${inputCls} resize-none`} placeholder="Main topics covered in the session…" />
        </div>
        <div>
          <div className="flex items-center justify-between mb-1.5">
            <label className="text-sm font-medium text-gray-700">Action Items</label>
            <button onClick={addActionItem} className="text-xs text-primary-600 hover:underline">+ Add item</button>
          </div>
          {(note.action_items || []).map((item, i) => (
            <div key={i} className="grid grid-cols-2 gap-3 mb-2">
              <input type="text" value={item.task} onChange={(e) => {
                const ai = [...(note.action_items || [])];
                ai[i] = { ...ai[i], task: e.target.value };
                setNote({ ...note, action_items: ai });
              }} className={inputCls} placeholder="Task description" />
              <input type="date" value={item.deadline} onChange={(e) => {
                const ai = [...(note.action_items || [])];
                ai[i] = { ...ai[i], deadline: e.target.value };
                setNote({ ...note, action_items: ai });
              }} className={inputCls} />
            </div>
          ))}
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1.5">Notes for Next Session</label>
          <textarea rows={2} value={note.next_session_notes || ""} onChange={(e) => setNote({ ...note, next_session_notes: e.target.value })}
            className={`${inputCls} resize-none`} placeholder="What to cover next time…" />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1.5">Student Rating (1–5)</label>
          <div className="flex gap-2">
            {[1, 2, 3, 4, 5].map((r) => (
              <button key={r} onClick={() => setNote({ ...note, student_rating: r })}
                className={`w-10 h-10 rounded-xl font-bold text-sm border transition-all ${
                  note.student_rating === r ? "bg-yellow-400 text-white border-yellow-400" : "border-gray-200 text-gray-500 hover:border-yellow-300"
                }`}>{r}</button>
            ))}
          </div>
        </div>
        <div className="flex items-center gap-3">
          <input type="checkbox" id="private" checked={note.is_private || false}
            onChange={(e) => setNote({ ...note, is_private: e.target.checked })}
            className="w-4 h-4 rounded" />
          <label htmlFor="private" className="text-sm text-gray-700">Keep notes private (not visible to student)</label>
        </div>
      </div>
    </div>
  );
}
