"use client";
import { useState } from "react";
import { motion } from "framer-motion";
import { Search, User, Star, Filter } from "lucide-react";
import api from "@/lib/api";

interface Candidate {
  student_id: string;
  name: string;
  profile_score: number;
  top_careers: string[];
  skills: string[];
  career_domain: string;
}

export default function CandidateSearchPage() {
  const [skills, setSkills] = useState("");
  const [domain, setDomain] = useState("");
  const [minScore, setMinScore] = useState(0);
  const [candidates, setCandidates] = useState<Candidate[]>([]);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);

  const search = async () => {
    setLoading(true);
    setSearched(true);
    const res = await api.get("/jobs/recruiter/candidates/", {
      params: { skills, domain, min_score: minScore },
    });
    setCandidates(res.data.candidates);
    setLoading(false);
  };

  return (
    <div className="p-6 space-y-6">
      <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }}>
        <h1 className="text-2xl font-bold text-gray-900">Candidate Search</h1>
        <p className="text-gray-500 mt-1">Find students matching your job requirements</p>
      </motion.div>

      {/* Filters */}
      <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}
        className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
        <div className="flex items-center gap-2 mb-4">
          <Filter className="w-5 h-5 text-indigo-600" />
          <h2 className="font-medium text-gray-800">Search Filters</h2>
        </div>
        <div className="grid md:grid-cols-4 gap-4">
          <div className="md:col-span-2">
            <label className="block text-sm text-gray-600 mb-1">Skills (comma-separated)</label>
            <input value={skills} onChange={e => setSkills(e.target.value)}
              placeholder="e.g. python, react, machine learning"
              className="w-full border border-gray-200 rounded-xl px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400" />
          </div>
          <div>
            <label className="block text-sm text-gray-600 mb-1">Domain</label>
            <select value={domain} onChange={e => setDomain(e.target.value)}
              className="w-full border border-gray-200 rounded-xl px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400">
              <option value="">All Domains</option>
              <option value="technology">Technology</option>
              <option value="data_science">Data Science</option>
              <option value="finance">Finance</option>
              <option value="marketing">Marketing</option>
              <option value="design">Design</option>
            </select>
          </div>
          <div>
            <label className="block text-sm text-gray-600 mb-1">Min Profile Score: {minScore}%</label>
            <input type="range" min={0} max={100} step={10} value={minScore}
              onChange={e => setMinScore(Number(e.target.value))}
              className="w-full accent-indigo-600 mt-2" />
          </div>
        </div>
        <button onClick={search}
          className="mt-4 flex items-center gap-2 bg-indigo-600 text-white px-6 py-2.5 rounded-xl hover:bg-indigo-700 transition text-sm font-medium">
          <Search className="w-4 h-4" /> Search Candidates
        </button>
      </motion.div>

      {/* Results */}
      {loading && <div className="text-center py-8 text-gray-400">Searching candidates...</div>}

      {!loading && searched && (
        <div>
          <p className="text-sm text-gray-500 mb-3">{candidates.length} candidates found</p>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
            {candidates.map((c, i) => (
              <motion.div key={c.student_id} initial={{ opacity: 0, scale: 0.97 }} animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: i * 0.05 }}
                className="bg-white rounded-2xl p-5 shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
                <div className="flex items-start gap-3 mb-4">
                  <div className="w-10 h-10 bg-indigo-100 rounded-full flex items-center justify-center flex-shrink-0">
                    <User className="w-5 h-5 text-indigo-600" />
                  </div>
                  <div>
                    <div className="font-semibold text-gray-900">{c.name}</div>
                    <div className="text-xs text-gray-400 capitalize">{(c.career_domain || "").replace(/_/g, " ")}</div>
                  </div>
                  <div className="ml-auto text-right">
                    <div className="flex items-center gap-1 text-orange-500">
                      <Star className="w-3.5 h-3.5 fill-orange-400" />
                      <span className="text-sm font-medium">{c.profile_score}%</span>
                    </div>
                    <div className="text-xs text-gray-400">Profile</div>
                  </div>
                </div>
                {c.top_careers.length > 0 && (
                  <div className="mb-3">
                    <div className="text-xs text-gray-400 mb-1">Career Goals</div>
                    <div className="flex flex-wrap gap-1">
                      {c.top_careers.slice(0, 2).map(career => (
                        <span key={career} className="text-xs bg-purple-100 text-purple-700 px-2 py-0.5 rounded-full capitalize">
                          {career.replace(/_/g, " ")}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
                <div>
                  <div className="text-xs text-gray-400 mb-1">Skills</div>
                  <div className="flex flex-wrap gap-1">
                    {c.skills.slice(0, 5).map(skill => (
                      <span key={skill} className="text-xs bg-gray-100 text-gray-600 px-2 py-0.5 rounded-full">{skill}</span>
                    ))}
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
          {candidates.length === 0 && (
            <div className="text-center py-10 bg-white rounded-2xl border border-gray-100">
              <Search className="w-10 h-10 text-gray-300 mx-auto mb-3" />
              <p className="text-gray-400">No candidates match your criteria</p>
              <p className="text-sm text-gray-300 mt-1">Try reducing the minimum score or broadening skills</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
