"use client";
import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { FileText, Plus, Trash2, Star, ExternalLink, BarChart2 } from "lucide-react";
import Link from "next/link";
import api from "@/lib/api";

interface Resume {
  id: string;
  title: string;
  template: string;
  is_primary: boolean;
  updated_at: string;
  sections: { section_type: string }[];
}

export default function ResumePage() {
  const [resumes, setResumes] = useState<Resume[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get("/resume/").then(r => setResumes(r.data)).finally(() => setLoading(false));
  }, []);

  async function createResume() {
    const res = await api.post("/resume/", { title: "New Resume", template: "modern_clean" });
    setResumes(prev => [res.data, ...prev]);
  }

  async function deleteResume(id: string) {
    await api.delete(`/resume/${id}/`);
    setResumes(prev => prev.filter(r => r.id !== id));
  }

  async function setPrimary(id: string) {
    await api.patch(`/resume/${id}/`, { is_primary: true });
    setResumes(prev => prev.map(r => ({ ...r, is_primary: r.id === id })));
  }

  if (loading) return <div className="flex items-center justify-center h-64"><div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600" /></div>;

  return (
    <div className="p-6 max-w-5xl mx-auto">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Resume Builder</h1>
          <p className="text-gray-500 mt-1">Create ATS-optimised resumes. Get your score before applying.</p>
        </div>
        <button onClick={createResume} className="flex items-center gap-2 bg-indigo-600 text-white px-4 py-2 rounded-xl hover:bg-indigo-700 transition">
          <Plus className="w-4 h-4" /> New Resume
        </button>
      </div>

      {resumes.length === 0 ? (
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}
          className="text-center py-20 bg-gray-50 rounded-2xl border-2 border-dashed border-gray-200">
          <FileText className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <p className="text-lg font-semibold text-gray-700">No resumes yet</p>
          <p className="text-gray-500 mb-6">Create your first resume and get an ATS score</p>
          <button onClick={createResume} className="bg-indigo-600 text-white px-6 py-3 rounded-xl hover:bg-indigo-700">
            Create Resume
          </button>
        </motion.div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {resumes.map((resume, i) => (
            <motion.div key={resume.id} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.08 }}
              className="bg-white rounded-2xl border border-gray-200 p-5 hover:shadow-md transition">
              <div className="flex items-start justify-between mb-3">
                <div className="flex items-center gap-2">
                  <div className="w-10 h-10 bg-indigo-100 rounded-xl flex items-center justify-center">
                    <FileText className="w-5 h-5 text-indigo-600" />
                  </div>
                  <div>
                    <p className="font-semibold text-gray-900 text-sm">{resume.title}</p>
                    <p className="text-xs text-gray-400 capitalize">{resume.template.replace("_", " ")}</p>
                  </div>
                </div>
                {resume.is_primary && (
                  <span className="text-xs bg-yellow-100 text-yellow-700 px-2 py-0.5 rounded-full flex items-center gap-1">
                    <Star className="w-3 h-3" /> Primary
                  </span>
                )}
              </div>

              <p className="text-xs text-gray-400 mb-4">
                {resume.sections.length} section{resume.sections.length !== 1 ? "s" : ""} •
                Updated {new Date(resume.updated_at).toLocaleDateString("en-IN")}
              </p>

              <div className="flex gap-2">
                <Link href={`/student/resume/builder?id=${resume.id}`}
                  className="flex-1 text-center text-xs bg-indigo-50 text-indigo-700 py-2 rounded-lg hover:bg-indigo-100 transition">
                  Edit
                </Link>
                <Link href={`/student/resume/ats?id=${resume.id}`}
                  className="flex-1 flex items-center justify-center gap-1 text-xs bg-green-50 text-green-700 py-2 rounded-lg hover:bg-green-100 transition">
                  <BarChart2 className="w-3 h-3" /> ATS Score
                </Link>
                {!resume.is_primary && (
                  <button onClick={() => setPrimary(resume.id)}
                    className="text-xs bg-yellow-50 text-yellow-700 px-2 py-2 rounded-lg hover:bg-yellow-100 transition" title="Set as primary">
                    <Star className="w-3 h-3" />
                  </button>
                )}
                <button onClick={() => deleteResume(resume.id)}
                  className="text-xs bg-red-50 text-red-600 px-2 py-2 rounded-lg hover:bg-red-100 transition">
                  <Trash2 className="w-3 h-3" />
                </button>
              </div>
            </motion.div>
          ))}
        </div>
      )}

      {/* Quick links */}
      <div className="mt-10 grid grid-cols-1 md:grid-cols-2 gap-4">
        <Link href="/student/interview" className="p-5 bg-purple-50 rounded-2xl border border-purple-100 hover:shadow-md transition group">
          <h3 className="font-semibold text-purple-800 mb-1">Interview Coach</h3>
          <p className="text-sm text-purple-600">Practice HR, behavioural & technical interviews with instant feedback.</p>
        </Link>
        <Link href="/student/skill-gap" className="p-5 bg-orange-50 rounded-2xl border border-orange-100 hover:shadow-md transition group">
          <h3 className="font-semibold text-orange-800 mb-1">Skill Gap Analyser</h3>
          <p className="text-sm text-orange-600">Find the gap between your current skills and your target career.</p>
        </Link>
      </div>
    </div>
  );
}
