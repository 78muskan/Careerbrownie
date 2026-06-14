"use client";
import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { Briefcase, MapPin, Clock, TrendingUp, ExternalLink } from "lucide-react";
import api from "@/lib/api";

interface JobMatch {
  id: string;
  title: string;
  company_name: string;
  company_industry: string;
  location: string;
  job_type: string;
  salary_min: number | null;
  salary_max: number | null;
  match_score: number;
  skills_required: string[];
}

interface InternshipMatch {
  id: string;
  title: string;
  company_name: string;
  location: string;
  duration_months: number;
  stipend_monthly: number | null;
  match_score: number;
}

interface MatchData {
  job_matches: JobMatch[];
  internship_matches: InternshipMatch[];
}

function MatchBadge({ score }: { score: number }) {
  const color = score >= 70 ? "bg-green-100 text-green-700" : score >= 40 ? "bg-yellow-100 text-yellow-700" : "bg-gray-100 text-gray-500";
  return <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${color}`}>{score}% match</span>;
}

export default function StudentJobsPage() {
  const [data, setData] = useState<MatchData | null>(null);
  const [loading, setLoading] = useState(true);
  const [tab, setTab] = useState<"jobs" | "internships">("jobs");

  useEffect(() => {
    api.get("/jobs/my-matches/").then(r => { setData(r.data); setLoading(false); });
  }, []);

  if (loading) return <div className="flex items-center justify-center h-64"><div className="animate-spin w-8 h-8 border-4 border-indigo-600 border-t-transparent rounded-full" /></div>;
  if (!data) return null;

  return (
    <div className="p-6 space-y-6">
      <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }}>
        <h1 className="text-2xl font-bold text-gray-900">Job Matches</h1>
        <p className="text-gray-500 mt-1">Roles matched to your skills and career goals</p>
      </motion.div>

      {/* Tabs */}
      <div className="flex gap-2">
        {(["jobs", "internships"] as const).map(t => (
          <button key={t} onClick={() => setTab(t)}
            className={`px-4 py-2 rounded-xl text-sm font-medium transition-colors capitalize ${tab === t ? "bg-indigo-600 text-white" : "bg-white text-gray-600 border border-gray-200 hover:bg-gray-50"}`}>
            {t} ({t === "jobs" ? data.job_matches.length : data.internship_matches.length})
          </button>
        ))}
        <a href="/jobs" className="ml-auto text-sm text-indigo-600 hover:underline flex items-center gap-1">
          Browse all jobs <ExternalLink className="w-3.5 h-3.5" />
        </a>
      </div>

      {tab === "jobs" && (
        <div className="space-y-4">
          {data.job_matches.length === 0 && (
            <div className="text-center py-10 bg-white rounded-2xl border border-gray-100">
              <Briefcase className="w-10 h-10 text-gray-300 mx-auto mb-3" />
              <p className="text-gray-400">No job matches yet</p>
              <p className="text-sm text-gray-300 mt-1">Complete your profile to unlock personalised matches</p>
            </div>
          )}
          {data.job_matches.map((job, i) => (
            <motion.div key={job.id} initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.07 }}
              className="bg-white rounded-2xl p-5 shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
              <div className="flex items-start justify-between gap-3">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1">
                    <h3 className="font-semibold text-gray-900">{job.title}</h3>
                    <MatchBadge score={job.match_score} />
                  </div>
                  <div className="text-sm text-gray-500">{job.company_name} · <span className="capitalize">{job.company_industry}</span></div>
                  <div className="flex flex-wrap gap-3 mt-2 text-xs text-gray-400">
                    <span className="flex items-center gap-1"><MapPin className="w-3.5 h-3.5" />{job.location}</span>
                    <span className="flex items-center gap-1"><Clock className="w-3.5 h-3.5" />{job.job_type.replace("_", " ")}</span>
                    {(job.salary_min || job.salary_max) && (
                      <span className="text-green-600 font-medium">
                        ₹{((job.salary_min || 0) / 100000).toFixed(1)}L – ₹{((job.salary_max || 0) / 100000).toFixed(1)}L
                      </span>
                    )}
                  </div>
                  {job.skills_required.length > 0 && (
                    <div className="flex flex-wrap gap-1 mt-2">
                      {job.skills_required.slice(0, 5).map(s => (
                        <span key={s} className="text-xs bg-indigo-50 text-indigo-600 px-2 py-0.5 rounded-full">{s}</span>
                      ))}
                    </div>
                  )}
                </div>
                <button
                  onClick={() => api.post("/jobs/applications/", { job: job.id }).then(() => alert("Applied!"))}
                  className="flex-shrink-0 bg-indigo-600 text-white text-sm px-4 py-2 rounded-xl hover:bg-indigo-700 transition">
                  Apply
                </button>
              </div>
            </motion.div>
          ))}
        </div>
      )}

      {tab === "internships" && (
        <div className="space-y-4">
          {data.internship_matches.length === 0 && (
            <div className="text-center py-10 bg-white rounded-2xl border border-gray-100">
              <TrendingUp className="w-10 h-10 text-gray-300 mx-auto mb-3" />
              <p className="text-gray-400">No internship matches yet</p>
            </div>
          )}
          {data.internship_matches.map((intern, i) => (
            <motion.div key={intern.id} initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.07 }}
              className="bg-white rounded-2xl p-5 shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1">
                    <h3 className="font-semibold text-gray-900">{intern.title}</h3>
                    <MatchBadge score={intern.match_score} />
                  </div>
                  <div className="text-sm text-gray-500">{intern.company_name}</div>
                  <div className="flex gap-3 mt-2 text-xs text-gray-400">
                    <span><MapPin className="w-3.5 h-3.5 inline mr-0.5" />{intern.location}</span>
                    <span>{intern.duration_months} months</span>
                    {intern.stipend_monthly && (
                      <span className="text-green-600 font-medium">₹{intern.stipend_monthly.toLocaleString()}/mo</span>
                    )}
                  </div>
                </div>
                <button
                  onClick={() => api.post("/jobs/applications/", { internship: intern.id }).then(() => alert("Applied!"))}
                  className="flex-shrink-0 bg-purple-600 text-white text-sm px-4 py-2 rounded-xl hover:bg-purple-700 transition">
                  Apply
                </button>
              </div>
            </motion.div>
          ))}
        </div>
      )}
    </div>
  );
}
