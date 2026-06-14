"use client";
import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { Briefcase, MapPin, Search, Filter, ExternalLink, Clock } from "lucide-react";

interface Job {
  id: string;
  title: string;
  company_name: string;
  company_industry: string;
  location: string;
  job_type: string;
  salary_min: number | null;
  salary_max: number | null;
  domain: string;
  created_at: string;
}

interface Internship {
  id: string;
  title: string;
  company_name: string;
  location: string;
  duration_months: number;
  stipend_monthly: number | null;
  is_remote: boolean;
}

export default function PublicJobsPage() {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [internships, setInternships] = useState<Internship[]>([]);
  const [search, setSearch] = useState("");
  const [domain, setDomain] = useState("");
  const [tab, setTab] = useState<"jobs" | "internships">("jobs");
  const [loading, setLoading] = useState(true);

  const fetchJobs = async () => {
    setLoading(true);
    const params = new URLSearchParams({ q: search, domain });
    const res = await fetch(`/api/v1/jobs/jobs/?${params}`);
    const data = await res.json();
    setJobs(data.jobs || []);
    setInternships(data.internships || []);
    setLoading(false);
  };

  useEffect(() => { fetchJobs(); }, []);

  return (
    <main className="min-h-screen bg-gray-50">
      {/* Hero */}
      <section className="bg-gradient-to-br from-indigo-600 to-purple-700 py-16 px-6 text-white">
        <div className="max-w-3xl mx-auto text-center">
          <motion.h1 initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }}
            className="text-4xl font-bold mb-3">Find Your Dream Career</motion.h1>
          <p className="text-indigo-200 mb-8">Jobs and internships matched to India&apos;s top students</p>
          <div className="flex gap-3 bg-white rounded-2xl p-2 shadow-lg">
            <div className="flex-1 flex items-center gap-2 px-3">
              <Search className="w-5 h-5 text-gray-400" />
              <input value={search} onChange={e => setSearch(e.target.value)}
                placeholder="Job title, company, or skill..."
                className="flex-1 text-gray-800 outline-none text-sm py-2" />
            </div>
            <select value={domain} onChange={e => setDomain(e.target.value)}
              className="text-gray-600 text-sm outline-none px-3 border-l border-gray-200 bg-transparent">
              <option value="">All Domains</option>
              <option value="technology">Technology</option>
              <option value="data_science">Data Science</option>
              <option value="finance">Finance</option>
              <option value="marketing">Marketing</option>
              <option value="design">Design</option>
            </select>
            <button onClick={fetchJobs}
              className="bg-indigo-600 text-white text-sm font-medium px-6 py-2 rounded-xl hover:bg-indigo-700 transition">
              Search
            </button>
          </div>
        </div>
      </section>

      <div className="max-w-5xl mx-auto px-6 py-10">
        {/* Tabs */}
        <div className="flex gap-3 mb-6">
          {(["jobs", "internships"] as const).map(t => (
            <button key={t} onClick={() => setTab(t)}
              className={`px-5 py-2 rounded-xl text-sm font-medium transition-colors capitalize ${tab === t ? "bg-indigo-600 text-white" : "bg-white text-gray-600 border border-gray-200 hover:bg-gray-50"}`}>
              {t} ({t === "jobs" ? jobs.length : internships.length})
            </button>
          ))}
        </div>

        {loading && (
          <div className="text-center py-10 text-gray-400">Loading opportunities...</div>
        )}

        {!loading && tab === "jobs" && (
          <div className="space-y-4">
            {jobs.length === 0 && (
              <div className="text-center py-12 bg-white rounded-2xl border border-gray-100">
                <Briefcase className="w-12 h-12 text-gray-300 mx-auto mb-3" />
                <p className="text-gray-400">No jobs posted yet</p>
              </div>
            )}
            {jobs.map((job, i) => (
              <motion.div key={job.id} initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.06 }}
                className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-1">
                      <h2 className="font-semibold text-gray-900 text-lg">{job.title}</h2>
                      <span className="text-xs bg-indigo-100 text-indigo-700 px-2 py-0.5 rounded-full capitalize">
                        {job.job_type.replace("_", " ")}
                      </span>
                    </div>
                    <div className="text-gray-500 text-sm">{job.company_name} · <span className="capitalize">{job.company_industry}</span></div>
                    <div className="flex flex-wrap gap-3 mt-2 text-xs text-gray-400">
                      <span className="flex items-center gap-1"><MapPin className="w-3.5 h-3.5" />{job.location}</span>
                      <span className="flex items-center gap-1"><Clock className="w-3.5 h-3.5" />{new Date(job.created_at).toLocaleDateString("en-IN")}</span>
                      {(job.salary_min || job.salary_max) && (
                        <span className="text-green-600 font-medium">
                          ₹{((job.salary_min || 0) / 100000).toFixed(1)}L – ₹{((job.salary_max || 0) / 100000).toFixed(1)}L
                        </span>
                      )}
                    </div>
                  </div>
                  <a href="/login"
                    className="flex-shrink-0 flex items-center gap-1.5 bg-indigo-600 text-white text-sm px-4 py-2 rounded-xl hover:bg-indigo-700 transition">
                    Apply <ExternalLink className="w-3.5 h-3.5" />
                  </a>
                </div>
              </motion.div>
            ))}
          </div>
        )}

        {!loading && tab === "internships" && (
          <div className="space-y-4">
            {internships.length === 0 && (
              <div className="text-center py-12 bg-white rounded-2xl border border-gray-100">
                <Filter className="w-12 h-12 text-gray-300 mx-auto mb-3" />
                <p className="text-gray-400">No internships posted yet</p>
              </div>
            )}
            {internships.map((intern, i) => (
              <motion.div key={intern.id} initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.06 }}
                className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-1">
                      <h2 className="font-semibold text-gray-900 text-lg">{intern.title}</h2>
                      {intern.is_remote && (
                        <span className="text-xs bg-green-100 text-green-700 px-2 py-0.5 rounded-full">Remote</span>
                      )}
                    </div>
                    <div className="text-gray-500 text-sm">{intern.company_name}</div>
                    <div className="flex gap-3 mt-2 text-xs text-gray-400">
                      <span><MapPin className="w-3.5 h-3.5 inline mr-0.5" />{intern.location}</span>
                      <span>{intern.duration_months} months</span>
                      {intern.stipend_monthly && (
                        <span className="text-green-600 font-medium">₹{intern.stipend_monthly.toLocaleString()}/month</span>
                      )}
                    </div>
                  </div>
                  <a href="/login"
                    className="flex-shrink-0 bg-purple-600 text-white text-sm px-4 py-2 rounded-xl hover:bg-purple-700 transition">
                    Apply
                  </a>
                </div>
              </motion.div>
            ))}
          </div>
        )}
      </div>
    </main>
  );
}
