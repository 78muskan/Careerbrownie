"use client";
import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { Target, BookOpen, TrendingUp, ArrowRight } from "lucide-react";
import Link from "next/link";
import api from "@/lib/api";

interface CareerMatch {
  career_key: string;
  career_name: string;
  match_pct: number;
  missing_skills: string[];
  skills_required: string[];
  avg_salary_lpa?: string;
  growth_rate?: string;
}

interface SkillGapData {
  career_matches: CareerMatch[];
  skill_gaps: { skill: string; priority: string }[];
  student_skills: string[];
  learning_resources: { title: string; type: string; duration: string; free: boolean; url?: string }[];
}

const PRIORITY_COLOR: Record<string, string> = {
  high: "bg-red-100 text-red-700 border-red-200",
  medium: "bg-yellow-100 text-yellow-700 border-yellow-200",
  low: "bg-green-100 text-green-700 border-green-200",
};

export default function SkillGapPage() {
  const [data, setData] = useState<SkillGapData | null>(null);
  const [loading, setLoading] = useState(true);
  const [selectedCareer, setSelectedCareer] = useState<string | null>(null);
  const [careerGaps, setCareerGaps] = useState<string[]>([]);

  useEffect(() => {
    api.get("/ai/advisor/").then(r => {
      setData({
        career_matches: r.data.career_matches || [],
        skill_gaps: r.data.skill_gaps || [],
        student_skills: r.data.student_skills || [],
        learning_resources: r.data.learning_resources || [],
      });
    }).finally(() => setLoading(false));
  }, []);

  async function analyseCareer(careerKey: string) {
    setSelectedCareer(careerKey);
    const res = await api.get(`/ai/careers/${careerKey}/`);
    setCareerGaps(res.data.skill_gaps || []);
  }

  if (loading) return <div className="flex items-center justify-center h-64"><div className="animate-spin rounded-full h-8 w-8 border-b-2 border-orange-500" /></div>;

  return (
    <div className="p-6 max-w-5xl mx-auto">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
          <Target className="w-6 h-6 text-orange-600" /> Skill Gap Analyser
        </h1>
        <p className="text-gray-500 mt-1">Identify the exact skills you need to land your target role.</p>
      </div>

      {data && (
        <>
          {/* Your skills */}
          {data.student_skills.length > 0 && (
            <div className="bg-white rounded-2xl border border-gray-200 p-6 mb-6">
              <h2 className="font-semibold text-gray-800 mb-3">Your Current Skills</h2>
              <div className="flex flex-wrap gap-2">
                {data.student_skills.map(s => (
                  <span key={s} className="text-sm bg-indigo-50 text-indigo-700 border border-indigo-100 px-3 py-1 rounded-full">{s}</span>
                ))}
              </div>
              {data.student_skills.length === 0 && (
                <p className="text-sm text-gray-400">Complete your profile to see skill analysis. <Link href="/student/profile/build" className="text-indigo-600 underline">Build Profile →</Link></p>
              )}
            </div>
          )}

          {/* Career selector */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            {data.career_matches.slice(0, 6).map((career, i) => (
              <motion.div key={career.career_key} initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.08 }}
                onClick={() => analyseCareer(career.career_key)}
                className={`cursor-pointer rounded-2xl border p-4 transition ${selectedCareer === career.career_key ? "border-orange-400 bg-orange-50" : "border-gray-200 bg-white hover:shadow-md"}`}>
                <div className="flex items-center justify-between mb-2">
                  <h3 className="font-semibold text-gray-900 text-sm">{career.career_name}</h3>
                  <span className={`text-xs font-bold px-2 py-0.5 rounded-full ${career.match_pct >= 70 ? "bg-green-100 text-green-700" : career.match_pct >= 50 ? "bg-yellow-100 text-yellow-700" : "bg-red-100 text-red-700"}`}>
                    {career.match_pct}%
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-1.5 mb-2">
                  <div className="bg-orange-500 h-1.5 rounded-full" style={{ width: `${career.match_pct}%` }} />
                </div>
                <p className="text-xs text-gray-500">{career.missing_skills.length} skills to develop</p>
              </motion.div>
            ))}
          </div>

          {/* Detailed gap for selected career */}
          {selectedCareer && careerGaps.length > 0 && (
            <motion.div initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }}
              className="bg-white rounded-2xl border border-gray-200 p-6 mb-6">
              <h2 className="font-semibold text-gray-800 mb-4">
                Skills to Develop for {data.career_matches.find(c => c.career_key === selectedCareer)?.career_name}
              </h2>
              <div className="flex flex-wrap gap-2">
                {careerGaps.map((skill, i) => (
                  <motion.span key={skill} initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: i * 0.05 }}
                    className="text-sm bg-red-50 text-red-700 border border-red-100 px-3 py-1 rounded-full flex items-center gap-1">
                    <span className="w-1.5 h-1.5 rounded-full bg-red-400" /> {skill}
                  </motion.span>
                ))}
              </div>
            </motion.div>
          )}

          {/* Overall skill gaps */}
          {data.skill_gaps.length > 0 && (
            <div className="bg-white rounded-2xl border border-gray-200 p-6 mb-6">
              <h2 className="font-semibold text-gray-800 mb-4">Priority Skills to Learn</h2>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                {data.skill_gaps.map((gap: any) => (
                  <div key={gap.skill || gap} className={`flex items-center justify-between px-4 py-2.5 rounded-xl border ${PRIORITY_COLOR[gap.priority || "medium"]}`}>
                    <span className="text-sm font-medium">{gap.skill || gap}</span>
                    {gap.priority && <span className="text-xs capitalize">{gap.priority}</span>}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Learning resources */}
          {data.learning_resources.length > 0 && (
            <div className="bg-white rounded-2xl border border-gray-200 p-6">
              <h2 className="font-semibold text-gray-800 mb-4 flex items-center gap-2">
                <BookOpen className="w-5 h-5 text-indigo-600" /> Recommended Learning Resources
              </h2>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                {data.learning_resources.slice(0, 8).map((r: any, i: number) => (
                  <motion.div key={i} initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: i * 0.08 }}
                    className="flex items-start gap-3 p-4 bg-gray-50 rounded-xl">
                    <TrendingUp className="w-4 h-4 text-indigo-500 mt-0.5 shrink-0" />
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-gray-800">{r.title}</p>
                      <div className="flex items-center gap-2 mt-1">
                        <span className="text-xs text-gray-400 capitalize">{r.type}</span>
                        <span className="text-xs text-gray-400">•</span>
                        <span className="text-xs text-gray-400">{r.duration}</span>
                        {r.free && <span className="text-xs bg-green-100 text-green-700 px-1.5 py-0.5 rounded-full">Free</span>}
                      </div>
                    </div>
                    {r.url && (
                      <a href={r.url} target="_blank" rel="noopener noreferrer"
                        className="text-indigo-600 hover:text-indigo-800">
                        <ArrowRight className="w-4 h-4" />
                      </a>
                    )}
                  </motion.div>
                ))}
              </div>
            </div>
          )}

          {!data.career_matches.length && (
            <div className="text-center py-20 bg-gray-50 rounded-2xl border-2 border-dashed border-gray-200">
              <Target className="w-12 h-12 text-gray-400 mx-auto mb-4" />
              <p className="text-lg font-semibold text-gray-700">Complete your profile & assessments first</p>
              <p className="text-gray-500 mb-6">We need your skills and interests to generate a personalised gap analysis.</p>
              <Link href="/student/assessment" className="bg-indigo-600 text-white px-6 py-3 rounded-xl hover:bg-indigo-700">
                Take Assessment
              </Link>
            </div>
          )}
        </>
      )}
    </div>
  );
}
