"use client";
import { useEffect, useState } from "react";
import { Loader2, Save, CheckCircle2 } from "lucide-react";
import api from "@/lib/api";

interface Profile {
  bio: string;
  tagline: string;
  experience_years: number;
  specializations: string[];
  languages: string[];
  hourly_rate: string;
  free_session_minutes: number;
  linkedin_url: string;
  is_accepting_students: boolean;
  user_name?: string;
  user_email?: string;
  avg_rating?: number;
  total_sessions_conducted?: number;
}

const inputCls = "w-full px-4 py-3 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary-500";

export default function CounsellorProfilePage() {
  const [profile, setProfile] = useState<Profile | null>(null);
  const [form, setForm] = useState<Partial<Profile>>({});
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    api.get("/portal/profile/")
      .then((r) => { setProfile(r.data); setForm(r.data); })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const save = async () => {
    setSaving(true);
    try {
      const { data } = await api.patch("/portal/profile/", {
        ...form,
        specializations: Array.isArray(form.specializations) ? form.specializations :
          String(form.specializations || "").split(",").map((s) => s.trim()).filter(Boolean),
        languages: Array.isArray(form.languages) ? form.languages :
          String(form.languages || "").split(",").map((s) => s.trim()).filter(Boolean),
      });
      setProfile(data);
      setSaved(true);
      setTimeout(() => setSaved(false), 2000);
    } catch {
      alert("Save failed.");
    } finally {
      setSaving(false);
    }
  };

  const set = (k: keyof Profile, v: unknown) => setForm((f) => ({ ...f, [k]: v }));

  if (loading) return <div className="flex justify-center p-16"><Loader2 className="w-8 h-8 animate-spin text-primary-600" /></div>;

  return (
    <div className="max-w-2xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-display font-bold text-gray-900">Counsellor Profile</h1>
          <p className="text-gray-500 text-sm mt-1">Your public profile shown to students.</p>
        </div>
        <button onClick={save} disabled={saving} className="btn-primary flex items-center gap-2 disabled:opacity-60">
          {saving ? <Loader2 className="w-4 h-4 animate-spin" /> : saved ? <CheckCircle2 className="w-4 h-4" /> : <Save className="w-4 h-4" />}
          {saving ? "Saving…" : saved ? "Saved!" : "Save"}
        </button>
      </div>

      {profile && (
        <div className="grid grid-cols-3 gap-4">
          {[
            { label: "Avg Rating", value: `${profile.avg_rating ?? 5.0}★` },
            { label: "Sessions", value: profile.total_sessions_conducted ?? 0 },
            { label: "Status", value: profile.is_accepting_students ? "Accepting" : "Closed" },
          ].map((s) => (
            <div key={s.label} className="bg-white rounded-xl p-4 text-center shadow-sm border border-gray-100">
              <div className="text-xl font-bold text-primary-600">{s.value}</div>
              <div className="text-xs text-gray-500 mt-0.5">{s.label}</div>
            </div>
          ))}
        </div>
      )}

      <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 space-y-5">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1.5">Tagline</label>
          <input type="text" value={form.tagline || ""} onChange={(e) => set("tagline", e.target.value)}
            className={inputCls} placeholder="Career Counsellor with 5+ years guiding IIT/NIT aspirants" />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1.5">Bio</label>
          <textarea rows={4} value={form.bio || ""} onChange={(e) => set("bio", e.target.value)}
            className={`${inputCls} resize-none`} placeholder="Write about your background, expertise, and how you help students…" />
        </div>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1.5">Years of Experience</label>
            <input type="number" value={form.experience_years || 0} onChange={(e) => set("experience_years", parseInt(e.target.value))}
              className={inputCls} min={0} />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1.5">Hourly Rate (₹)</label>
            <input type="number" value={form.hourly_rate || 0} onChange={(e) => set("hourly_rate", e.target.value)}
              className={inputCls} min={0} />
          </div>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1.5">Specializations (comma-separated)</label>
          <input type="text" value={Array.isArray(form.specializations) ? form.specializations.join(", ") : form.specializations || ""}
            onChange={(e) => set("specializations", e.target.value)}
            className={inputCls} placeholder="Career Counselling, Study Abroad, UPSC Preparation" />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1.5">Languages</label>
          <input type="text" value={Array.isArray(form.languages) ? form.languages.join(", ") : form.languages || ""}
            onChange={(e) => set("languages", e.target.value)}
            className={inputCls} placeholder="English, Hindi, Tamil" />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1.5">LinkedIn URL</label>
          <input type="url" value={form.linkedin_url || ""} onChange={(e) => set("linkedin_url", e.target.value)}
            className={inputCls} placeholder="https://linkedin.com/in/yourprofile" />
        </div>
        <div className="flex items-center gap-3">
          <input type="checkbox" id="accepting" checked={form.is_accepting_students ?? true}
            onChange={(e) => set("is_accepting_students", e.target.checked)}
            className="w-4 h-4 rounded text-primary-600" />
          <label htmlFor="accepting" className="text-sm font-medium text-gray-700">
            Currently accepting new students
          </label>
        </div>
      </div>
    </div>
  );
}
