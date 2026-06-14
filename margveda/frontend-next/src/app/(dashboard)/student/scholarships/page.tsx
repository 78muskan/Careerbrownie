"use client";
import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { Award, Filter, ExternalLink, Star, Calendar, CheckCircle, Bookmark } from "lucide-react";
import api from "@/lib/api";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

interface Scholarship {
  slug: string;
  name: string;
  provider: string;
  country: string;
  value_description: string;
  eligibility: string[];
  fields: string[];
  deadline_month?: number;
  merit_based: boolean;
  need_based: boolean;
  renewable: boolean;
  url?: string;
  match_score?: number;
}

const MONTHS = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

export default function ScholarshipsPage() {
  const [scholarships, setScholarships] = useState<Scholarship[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<"all" | "merit" | "need">("all");
  const [countryFilter, setCountryFilter] = useState("");
  const [saved, setSaved] = useState<string[]>([]);

  useEffect(() => {
    loadScholarships();
  }, []);

  async function loadScholarships() {
    // Try matched scholarships first (needs auth)
    try {
      const res = await api.get("/universities/scholarships/match/");
      setScholarships(res.data.results);
    } catch {
      // Fall back to public list
      const res = await fetch(`${API_BASE}/universities/scholarships/`);
      const data = await res.json();
      setScholarships(data.results || []);
    }
    setLoading(false);
  }

  async function saveScholarship(slug: string) {
    try {
      await api.post("/universities/scholarships/my-applications/", { scholarship_slug: slug });
      setSaved(prev => [...prev, slug]);
    } catch {
      setSaved(prev => [...prev, slug]);
    }
  }

  const filtered = scholarships.filter(s => {
    if (filter === "merit" && !s.merit_based) return false;
    if (filter === "need" && !s.need_based) return false;
    if (countryFilter && !s.country.toLowerCase().includes(countryFilter.toLowerCase())) return false;
    return true;
  }).sort((a, b) => (b.match_score || 0) - (a.match_score || 0));

  if (loading) return <div className="flex items-center justify-center h-64"><div className="animate-spin rounded-full h-8 w-8 border-b-2 border-yellow-500" /></div>;

  return (
    <div className="p-6 max-w-5xl mx-auto">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
          <Award className="w-6 h-6 text-yellow-600" /> Scholarships
        </h1>
        <p className="text-gray-500 mt-1">Discover merit and need-based scholarships for India and study abroad.</p>
      </div>

      {/* Filters */}
      <div className="flex items-center gap-3 mb-6 flex-wrap">
        <Filter className="w-4 h-4 text-gray-400" />
        {(["all", "merit", "need"] as const).map(f => (
          <button key={f} onClick={() => setFilter(f)}
            className={`text-sm px-4 py-1.5 rounded-full transition ${filter === f ? "bg-indigo-600 text-white" : "bg-gray-100 text-gray-600 hover:bg-gray-200"}`}>
            {f.charAt(0).toUpperCase() + f.slice(1)} {f === "merit" ? "Based" : f === "need" ? "Based" : ""}
          </button>
        ))}
        <input placeholder="Filter by country…" value={countryFilter} onChange={e => setCountryFilter(e.target.value)}
          className="border border-gray-200 rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-200" />
        <span className="text-sm text-gray-400">{filtered.length} scholarships</span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
        {filtered.map((s, i) => (
          <motion.div key={s.slug} initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.07 }}
            className="bg-white rounded-2xl border border-gray-200 p-5 hover:shadow-md transition relative">

            {s.match_score && s.match_score >= 60 && (
              <div className="absolute top-4 right-4">
                <span className="flex items-center gap-1 text-xs bg-yellow-100 text-yellow-700 px-2 py-0.5 rounded-full">
                  <Star className="w-3 h-3" /> {s.match_score}% match
                </span>
              </div>
            )}

            <div className="mb-3 pr-20">
              <h3 className="font-bold text-gray-900 mb-0.5">{s.name}</h3>
              <p className="text-sm text-gray-500">{s.provider} • {s.country}</p>
            </div>

            <div className="bg-green-50 rounded-xl px-3 py-2 mb-3">
              <p className="text-sm text-green-800 font-medium">{s.value_description}</p>
            </div>

            <div className="flex flex-wrap gap-1.5 mb-3">
              {s.merit_based && <span className="text-xs bg-blue-100 text-blue-700 px-2 py-0.5 rounded-full flex items-center gap-1"><CheckCircle className="w-3 h-3" /> Merit</span>}
              {s.need_based && <span className="text-xs bg-purple-100 text-purple-700 px-2 py-0.5 rounded-full flex items-center gap-1"><CheckCircle className="w-3 h-3" /> Need</span>}
              {s.renewable && <span className="text-xs bg-gray-100 text-gray-600 px-2 py-0.5 rounded-full">Renewable</span>}
              {s.deadline_month && (
                <span className="text-xs bg-red-50 text-red-700 px-2 py-0.5 rounded-full flex items-center gap-1">
                  <Calendar className="w-3 h-3" /> Deadline: {MONTHS[s.deadline_month]}
                </span>
              )}
            </div>

            <div className="mb-3">
              <p className="text-xs text-gray-500 mb-1.5">Key Eligibility</p>
              <ul className="space-y-0.5">
                {s.eligibility.slice(0, 3).map((e, j) => (
                  <li key={j} className="text-xs text-gray-600 flex items-start gap-1">
                    <span className="mt-0.5 shrink-0">•</span> {e}
                  </li>
                ))}
              </ul>
            </div>

            <div className="flex items-center gap-2 pt-3 border-t border-gray-100">
              <button onClick={() => saveScholarship(s.slug)}
                className={`flex items-center gap-1 text-xs px-3 py-1.5 rounded-lg transition ${saved.includes(s.slug) ? "bg-yellow-100 text-yellow-700" : "border border-gray-200 text-gray-600 hover:border-yellow-300"}`}>
                <Bookmark className="w-3 h-3" /> {saved.includes(s.slug) ? "Saved" : "Save"}
              </button>
              {s.url && (
                <a href={s.url} target="_blank" rel="noopener noreferrer"
                  className="flex items-center gap-1 text-xs bg-indigo-50 text-indigo-700 px-3 py-1.5 rounded-lg hover:bg-indigo-100 transition">
                  <ExternalLink className="w-3 h-3" /> Apply
                </a>
              )}
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
