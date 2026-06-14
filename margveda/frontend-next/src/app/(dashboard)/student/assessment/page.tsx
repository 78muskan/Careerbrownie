"use client";
import Link from "next/link";
import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { Brain, Zap, Target, CheckCircle2, ArrowRight, Clock } from "lucide-react";
import api from "@/lib/api";

const ASSESSMENTS = [
  {
    key: "interest",
    title: "Interest Assessment",
    subtitle: "Discover your RIASEC career type",
    description: "Find out which career domains align with your natural interests and preferences.",
    icon: <Brain className="w-8 h-8 text-violet-600" />,
    bg: "bg-violet-50",
    border: "border-violet-200",
    duration: "8 min",
    questions: 12,
  },
  {
    key: "personality",
    title: "Personality Assessment",
    subtitle: "Understand your work style",
    description: "Uncover your Big 5 personality traits and how they shape your ideal career.",
    icon: <Zap className="w-8 h-8 text-yellow-600" />,
    bg: "bg-yellow-50",
    border: "border-yellow-200",
    duration: "6 min",
    questions: 8,
  },
  {
    key: "aptitude",
    title: "Aptitude Assessment",
    subtitle: "Test your cognitive strengths",
    description: "Measure your numerical, verbal, and logical reasoning abilities.",
    icon: <Target className="w-8 h-8 text-blue-600" />,
    bg: "bg-blue-50",
    border: "border-blue-200",
    duration: "10 min",
    questions: 6,
  },
  {
    key: "readiness",
    title: "Career Readiness",
    subtitle: "How ready are you for your career?",
    description: "Assess your self-awareness, market knowledge, skills, and planning maturity.",
    icon: <CheckCircle2 className="w-8 h-8 text-green-600" />,
    bg: "bg-green-50",
    border: "border-green-200",
    duration: "5 min",
    questions: 8,
  },
];

export default function AssessmentLandingPage() {
  const [completed, setCompleted] = useState<string[]>([]);

  useEffect(() => {
    api.get("/ai/assessment/results/")
      .then((r) => setCompleted((r.data as Array<{assessment_type: string}>).map((x) => x.assessment_type)))
      .catch(() => {});
  }, []);

  const allDone = completed.length >= 4;

  return (
    <div className="max-w-4xl space-y-6">
      <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }}>
        <h1 className="text-2xl font-display font-bold text-gray-900">Career Assessment Engine</h1>
        <p className="text-gray-500 mt-1">
          Complete all 4 assessments to unlock your personalised AI career roadmap and insights.
        </p>
      </motion.div>

      {/* Progress bar */}
      <div className="bg-white rounded-2xl p-5 shadow-sm border border-gray-100">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm font-medium text-gray-700">Assessment Progress</span>
          <span className="text-sm font-bold text-primary-600">{completed.length}/4 Complete</span>
        </div>
        <div className="w-full bg-gray-100 rounded-full h-2">
          <div className="bg-gradient-to-r from-primary-500 to-violet-500 h-2 rounded-full transition-all"
            style={{ width: `${(completed.length / 4) * 100}%` }} />
        </div>
        {allDone && (
          <p className="text-sm text-green-600 mt-2 font-medium">
            All assessments complete! Your AI career insights are ready.
          </p>
        )}
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {ASSESSMENTS.map((a, i) => {
          const done = completed.includes(a.key);
          return (
            <motion.div key={a.key} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.1 }}
              className={`bg-white rounded-2xl p-6 shadow-sm border transition-all hover:shadow-md ${done ? "border-green-200" : a.border}`}
            >
              <div className={`w-14 h-14 ${a.bg} rounded-2xl flex items-center justify-center mb-4`}>
                {done ? <CheckCircle2 className="w-8 h-8 text-green-600" /> : a.icon}
              </div>
              <h3 className="font-semibold text-gray-900">{a.title}</h3>
              <p className="text-xs text-gray-500 mt-0.5">{a.subtitle}</p>
              <p className="text-sm text-gray-600 mt-2 leading-relaxed">{a.description}</p>
              <div className="flex items-center gap-3 mt-3 text-xs text-gray-400">
                <span className="flex items-center gap-1"><Clock className="w-3.5 h-3.5" />{a.duration}</span>
                <span>{a.questions} questions</span>
              </div>
              <div className="mt-4">
                {done ? (
                  <div className="flex gap-2">
                    <span className="inline-flex items-center gap-1 text-xs font-medium text-green-700 bg-green-50 px-3 py-1.5 rounded-lg">
                      <CheckCircle2 className="w-3.5 h-3.5" /> Completed
                    </span>
                    <Link href={`/student/assessment/${a.key}/result`}
                      className="text-xs text-primary-600 hover:underline flex items-center gap-1 px-3 py-1.5">
                      View result <ArrowRight className="w-3 h-3" />
                    </Link>
                  </div>
                ) : (
                  <Link href={`/student/assessment/${a.key}`}
                    className="inline-flex items-center gap-2 btn-primary text-sm">
                    Start <ArrowRight className="w-4 h-4" />
                  </Link>
                )}
              </div>
            </motion.div>
          );
        })}
      </div>

      {completed.length > 0 && (
        <div className="flex gap-3">
          <Link href="/student/ai-advisor" className="btn-primary flex items-center gap-2">
            <Brain className="w-4 h-4" />
            View AI Career Insights
          </Link>
          <Link href="/student/career-roadmap" className="btn-secondary flex items-center gap-2">
            <Target className="w-4 h-4" />
            Generate Roadmap
          </Link>
        </div>
      )}
    </div>
  );
}
