"use client";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { motion } from "framer-motion";
import { MapPin, Globe, Users, TrendingUp, BookOpen, Award, ArrowLeft } from "lucide-react";
import Link from "next/link";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export default function UniversityDetailPage() {
  const { slug } = useParams<{ slug: string }>();
  const [uni, setUni] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (slug) {
      fetch(`${API_BASE}/universities/${slug}/`)
        .then(r => r.json()).then(setUni).finally(() => setLoading(false));
    }
  }, [slug]);

  if (loading) return <div className="flex items-center justify-center h-64"><div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600" /></div>;
  if (!uni || uni.error) return <div className="p-8 text-center text-gray-500">University not found.</div>;

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero */}
      <div className="bg-gradient-to-br from-slate-800 to-indigo-900 text-white py-12 px-6">
        <div className="max-w-4xl mx-auto">
          <Link href="/universities" className="flex items-center gap-1 text-indigo-300 hover:text-white mb-6 text-sm">
            <ArrowLeft className="w-4 h-4" /> Back to Universities
          </Link>
          <div className="flex items-start justify-between">
            <div>
              <h1 className="text-3xl font-bold mb-2">{uni.name}</h1>
              {(uni.location || uni.country) && (
                <p className="flex items-center gap-1 text-indigo-200 mb-3">
                  <MapPin className="w-4 h-4" /> {uni.location || uni.country}
                </p>
              )}
              <div className="flex flex-wrap gap-2">
                {uni.nirf_rank && <span className="bg-white/20 px-3 py-1 rounded-full text-sm">NIRF Rank #{uni.nirf_rank}</span>}
                {uni.qs_rank && <span className="bg-white/20 px-3 py-1 rounded-full text-sm">QS #{uni.qs_rank}</span>}
                {uni.naac_grade && <span className="bg-green-400/30 px-3 py-1 rounded-full text-sm">NAAC {uni.naac_grade}</span>}
                {uni.established && <span className="bg-white/10 px-3 py-1 rounded-full text-sm">Est. {uni.established}</span>}
              </div>
            </div>
            {uni.website && (
              <a href={uni.website} target="_blank" rel="noopener noreferrer"
                className="flex items-center gap-1 text-sm bg-white/20 hover:bg-white/30 px-4 py-2 rounded-xl transition">
                <Globe className="w-4 h-4" /> Website
              </a>
            )}
          </div>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-6 py-8">
        {/* Stats */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-8">
          {[
            { label: "Avg Package", value: uni.placements?.avg_package_lpa ? `₹${uni.placements.avg_package_lpa}L/yr` : (uni.tuition_per_year_usd ? `$${uni.tuition_per_year_usd.toLocaleString()}/yr` : "—"), icon: <TrendingUp className="w-5 h-5" />, color: "text-green-600 bg-green-50" },
            { label: "Placement Rate", value: uni.placements?.placement_pct ? `${uni.placements.placement_pct}%` : "—", icon: <Users className="w-5 h-5" />, color: "text-blue-600 bg-blue-50" },
            { label: "Fees/Year", value: uni.fees_per_year_inr ? `₹${(uni.fees_per_year_inr / 1000).toFixed(0)}K` : "—", icon: <Award className="w-5 h-5" />, color: "text-purple-600 bg-purple-50" },
            { label: "Top Package", value: uni.placements?.highest_package_lpa ? `₹${uni.placements.highest_package_lpa}L` : "—", icon: <BookOpen className="w-5 h-5" />, color: "text-orange-600 bg-orange-50" },
          ].map((s, i) => (
            <motion.div key={i} initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.1 }}
              className="bg-white rounded-2xl border border-gray-200 p-4 flex items-center gap-3">
              <div className={`w-10 h-10 rounded-xl flex items-center justify-center ${s.color}`}>{s.icon}</div>
              <div>
                <p className="font-bold text-gray-900">{s.value}</p>
                <p className="text-xs text-gray-500">{s.label}</p>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Description */}
        <div className="bg-white rounded-2xl border border-gray-200 p-6 mb-6">
          <h2 className="font-semibold text-gray-800 mb-3">About</h2>
          <p className="text-gray-600 leading-relaxed">{uni.description}</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
          {/* Notable for */}
          {uni.notable_for?.length > 0 && (
            <div className="bg-white rounded-2xl border border-gray-200 p-6">
              <h2 className="font-semibold text-gray-800 mb-3">Notable Programs</h2>
              <div className="flex flex-wrap gap-2">
                {uni.notable_for.map((f: string) => (
                  <span key={f} className="bg-indigo-50 text-indigo-700 px-3 py-1 rounded-full text-sm">{f}</span>
                ))}
              </div>
            </div>
          )}

          {/* Entrance exams */}
          {uni.entrance_exams?.length > 0 && (
            <div className="bg-white rounded-2xl border border-gray-200 p-6">
              <h2 className="font-semibold text-gray-800 mb-3">Entrance Exams</h2>
              <div className="flex flex-wrap gap-2">
                {uni.entrance_exams.map((e: string) => (
                  <span key={e} className="bg-orange-50 text-orange-700 border border-orange-100 px-3 py-1 rounded-full text-sm font-medium">{e}</span>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Suggested programs */}
        {uni.suggested_programs?.length > 0 && (
          <div className="bg-white rounded-2xl border border-gray-200 p-6">
            <h2 className="font-semibold text-gray-800 mb-4">Suggested Programs</h2>
            <div className="space-y-3">
              {uni.suggested_programs.map((p: any) => (
                <div key={p.slug} className="flex items-center justify-between p-3 bg-gray-50 rounded-xl">
                  <div>
                    <p className="font-medium text-gray-800 text-sm">{p.name}</p>
                    <p className="text-xs text-gray-500 capitalize">{p.level} • {p.duration_years} years • Avg ₹{p.avg_package_lpa}LPA</p>
                  </div>
                  <div className="flex flex-wrap gap-1">
                    {p.entrance_exams?.slice(0, 2).map((e: string) => (
                      <span key={e} className="text-xs bg-indigo-100 text-indigo-700 px-2 py-0.5 rounded-full">{e}</span>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* CTA */}
        <div className="mt-6 flex gap-4">
          <Link href="/student/college-predictor"
            className="flex-1 text-center bg-indigo-600 text-white py-3 rounded-xl hover:bg-indigo-700 transition font-medium">
            Check Your Admission Chances
          </Link>
          <Link href="/student/scholarships"
            className="flex-1 text-center border border-indigo-200 text-indigo-700 py-3 rounded-xl hover:bg-indigo-50 transition font-medium">
            Find Scholarships
          </Link>
        </div>
      </div>
    </div>
  );
}
