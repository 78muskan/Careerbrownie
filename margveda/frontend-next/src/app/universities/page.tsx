"use client";
import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { Search, MapPin, Star, ExternalLink, Filter } from "lucide-react";
import Link from "next/link";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

interface University {
  slug: string;
  name: string;
  type?: string;
  location?: string;
  country?: string;
  nirf_rank?: number;
  qs_rank?: number;
  naac_grade?: string;
  fees_per_year_inr?: number;
  tuition_per_year_usd?: number;
  description: string;
  notable_for: string[];
  entrance_exams?: string[];
  placements?: { avg_package_lpa?: number; placement_pct?: number };
}

const TYPES = ["", "engineering", "medical", "management", "general", "arts_science"];
const COUNTRIES = ["India", "USA", "UK", "Singapore", "Germany", "Canada"];

export default function UniversitiesPage() {
  const [universities, setUniversities] = useState<University[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [typeFilter, setTypeFilter] = useState("");
  const [countryFilter, setCountryFilter] = useState("");

  useEffect(() => {
    fetchUniversities();
  }, [typeFilter, countryFilter]);

  async function fetchUniversities() {
    setLoading(true);
    const params = new URLSearchParams();
    if (typeFilter) params.set("type", typeFilter);
    if (countryFilter) params.set("country", countryFilter);
    if (search) params.set("q", search);
    const res = await fetch(`${API_BASE}/universities/?${params}`);
    const data = await res.json();
    setUniversities(data.results || []);
    setLoading(false);
  }

  const filtered = search
    ? universities.filter(u => u.name.toLowerCase().includes(search.toLowerCase()) ||
        u.notable_for?.some(f => f.toLowerCase().includes(search.toLowerCase())))
    : universities;

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero */}
      <div className="bg-gradient-to-br from-indigo-900 to-purple-900 text-white py-16 px-6">
        <div className="max-w-5xl mx-auto">
          <h1 className="text-4xl font-bold mb-3">University Explorer</h1>
          <p className="text-indigo-200 text-lg mb-8">Discover Indian and global universities. Compare fees, rankings, placements, and entrance requirements.</p>
          <div className="flex gap-3 max-w-2xl">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input value={search} onChange={e => setSearch(e.target.value)} onKeyDown={e => e.key === "Enter" && fetchUniversities()}
                placeholder="Search universities or programs (e.g. IIT, CS, MBA)…"
                className="w-full pl-10 pr-4 py-3 rounded-xl text-gray-900 focus:outline-none focus:ring-2 focus:ring-indigo-300" />
            </div>
            <button onClick={fetchUniversities} className="bg-indigo-500 hover:bg-indigo-400 px-6 rounded-xl font-medium transition">Search</button>
          </div>
        </div>
      </div>

      <div className="max-w-5xl mx-auto px-6 py-8">
        {/* Filters */}
        <div className="flex items-center gap-3 mb-6 flex-wrap">
          <Filter className="w-4 h-4 text-gray-500" />
          <select value={typeFilter} onChange={e => setTypeFilter(e.target.value)}
            className="border border-gray-200 rounded-lg px-3 py-1.5 text-sm bg-white focus:outline-none focus:ring-2 focus:ring-indigo-200">
            <option value="">All Types</option>
            {TYPES.filter(Boolean).map(t => <option key={t} value={t}>{t.replace("_", " ").replace(/\b\w/g, l => l.toUpperCase())}</option>)}
          </select>
          <select value={countryFilter} onChange={e => setCountryFilter(e.target.value)}
            className="border border-gray-200 rounded-lg px-3 py-1.5 text-sm bg-white focus:outline-none focus:ring-2 focus:ring-indigo-200">
            <option value="">All Countries</option>
            {COUNTRIES.map(c => <option key={c} value={c}>{c}</option>)}
          </select>
          <span className="text-sm text-gray-500">{filtered.length} universities</span>
        </div>

        {/* Quick links */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-8">
          {[
            { label: "College Predictor", href: "/student/college-predictor", emoji: "🎯" },
            { label: "Scholarships", href: "/student/scholarships", emoji: "🏆" },
            { label: "Study Abroad", href: "/universities?country=USA", emoji: "✈️" },
            { label: "Top IITs", href: "/universities?type=engineering", emoji: "🏛️" },
          ].map(l => (
            <Link key={l.label} href={l.href}
              className="flex items-center gap-2 bg-white rounded-xl border border-gray-200 px-4 py-3 text-sm font-medium text-gray-700 hover:shadow-md hover:border-indigo-200 transition">
              <span>{l.emoji}</span> {l.label}
            </Link>
          ))}
        </div>

        {loading ? (
          <div className="flex items-center justify-center py-20"><div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600" /></div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
            {filtered.map((uni, i) => (
              <motion.div key={uni.slug} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.05 }}
                className="bg-white rounded-2xl border border-gray-200 p-5 hover:shadow-md transition">
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <h3 className="font-bold text-gray-900">{uni.name}</h3>
                    {uni.location && (
                      <p className="flex items-center gap-1 text-sm text-gray-500 mt-0.5">
                        <MapPin className="w-3 h-3" /> {uni.location || uni.country}
                      </p>
                    )}
                  </div>
                  <div className="text-right shrink-0">
                    {uni.nirf_rank && <p className="text-xs text-indigo-600 font-bold">NIRF #{uni.nirf_rank}</p>}
                    {uni.qs_rank && <p className="text-xs text-indigo-600 font-bold">QS #{uni.qs_rank}</p>}
                    {uni.naac_grade && <span className="text-xs bg-green-100 text-green-700 px-2 py-0.5 rounded-full">{uni.naac_grade}</span>}
                  </div>
                </div>

                <p className="text-sm text-gray-600 mb-3 line-clamp-2">{uni.description}</p>

                <div className="flex flex-wrap gap-1.5 mb-3">
                  {uni.notable_for?.slice(0, 4).map(f => (
                    <span key={f} className="text-xs bg-indigo-50 text-indigo-700 px-2 py-0.5 rounded-full">{f}</span>
                  ))}
                </div>

                <div className="flex items-center justify-between pt-3 border-t border-gray-100">
                  <div className="text-xs text-gray-500">
                    {uni.fees_per_year_inr && <span>₹{(uni.fees_per_year_inr / 100000).toFixed(1)}L/yr</span>}
                    {uni.tuition_per_year_usd && <span>${uni.tuition_per_year_usd.toLocaleString()}/yr</span>}
                    {uni.placements?.avg_package_lpa && <span className="ml-2">· Avg ₹{uni.placements.avg_package_lpa}LPA</span>}
                  </div>
                  <Link href={`/universities/${uni.slug}`} className="text-sm text-indigo-600 hover:text-indigo-800 font-medium flex items-center gap-1">
                    View <ExternalLink className="w-3 h-3" />
                  </Link>
                </div>
              </motion.div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
