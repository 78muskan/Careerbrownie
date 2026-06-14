"use client";
import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { Map, Plus, Loader2, CheckCircle2, BookOpen, Briefcase, Award, Users } from "lucide-react";
import api from "@/lib/api";

interface Milestone {
  title: string;
  description: string;
  type: "learning" | "project" | "career" | "certification" | "networking";
}

interface Roadmap {
  id: string;
  target_career: string;
  generated_at: string;
  plans: {
    "3_months": Milestone[];
    "6_months": Milestone[];
    "1_year": Milestone[];
    "3_years": Milestone[];
    "5_years": Milestone[];
  };
}

const PHASE_LABELS: Record<string, { label: string; color: string; bg: string }> = {
  "3_months": { label: "0–3 Months", color: "text-green-700", bg: "bg-green-50 border-green-200" },
  "6_months": { label: "3–6 Months", color: "text-blue-700", bg: "bg-blue-50 border-blue-200" },
  "1_year": { label: "6–12 Months", color: "text-violet-700", bg: "bg-violet-50 border-violet-200" },
  "3_years": { label: "1–3 Years", color: "text-orange-700", bg: "bg-orange-50 border-orange-200" },
  "5_years": { label: "3–5 Years", color: "text-rose-700", bg: "bg-rose-50 border-rose-200" },
};

const TYPE_ICON = {
  learning: <BookOpen className="w-4 h-4" />,
  project: <Briefcase className="w-4 h-4" />,
  career: <CheckCircle2 className="w-4 h-4" />,
  certification: <Award className="w-4 h-4" />,
  networking: <Users className="w-4 h-4" />,
};

const COMMON_CAREERS = [
  "Software Engineer", "Data Scientist", "Product Manager", "UI/UX Designer",
  "Marketing Manager", "Chartered Accountant", "Doctor", "Entrepreneur",
  "IAS Officer", "Content Creator",
];

export default function CareerRoadmapPage() {
  const [roadmap, setRoadmap] = useState<Roadmap | null>(null);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [targetCareer, setTargetCareer] = useState("");
  const [showForm, setShowForm] = useState(false);
  const [activePhase, setActivePhase] = useState<string>("3_months");

  useEffect(() => {
    api.get("/ai/roadmap/")
      .then((r) => setRoadmap(r.data))
      .catch(() => setShowForm(true))
      .finally(() => setLoading(false));
  }, []);

  const generate = async () => {
    if (!targetCareer.trim()) return;
    setGenerating(true);
    try {
      const { data } = await api.post("/ai/roadmap/", { target_career: targetCareer });
      setRoadmap(data);
      setShowForm(false);
    } catch {
      alert("Failed to generate roadmap. Please try again.");
    } finally {
      setGenerating(false);
    }
  };

  if (loading) return <div className="flex justify-center p-16"><Loader2 className="w-8 h-8 animate-spin text-primary-600" /></div>;

  return (
    <div className="max-w-5xl space-y-6">
      <div className="flex items-start justify-between gap-4">
        <div>
          <h1 className="text-2xl font-display font-bold text-gray-900 flex items-center gap-2">
            <Map className="w-6 h-6 text-primary-600" />
            Career Roadmap
          </h1>
          <p className="text-gray-500 mt-1">Your personalised step-by-step career action plan.</p>
        </div>
        {roadmap && (
          <button onClick={() => setShowForm(!showForm)} className="btn-secondary text-sm flex items-center gap-2">
            <Plus className="w-4 h-4" />
            New Roadmap
          </button>
        )}
      </div>

      {/* Generate form */}
      {showForm && (
        <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }}
          className="bg-white rounded-2xl p-6 shadow-sm border border-primary-100"
        >
          <h3 className="font-semibold text-gray-900 mb-4">Generate Your Career Roadmap</h3>
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-1.5">Target Career</label>
            <input type="text" value={targetCareer} onChange={(e) => setTargetCareer(e.target.value)}
              className="w-full px-4 py-3 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
              placeholder="e.g. Software Engineer, Data Scientist, IAS Officer"
            />
            <div className="flex flex-wrap gap-2 mt-2">
              {COMMON_CAREERS.map((c) => (
                <button key={c} onClick={() => setTargetCareer(c)}
                  className="text-xs bg-gray-100 hover:bg-primary-50 hover:text-primary-700 text-gray-600 px-3 py-1 rounded-full transition-colors">
                  {c}
                </button>
              ))}
            </div>
          </div>
          <button onClick={generate} disabled={!targetCareer.trim() || generating}
            className="btn-primary flex items-center gap-2 disabled:opacity-60">
            {generating && <Loader2 className="w-4 h-4 animate-spin" />}
            {generating ? "Generating…" : "Generate Roadmap"}
          </button>
        </motion.div>
      )}

      {roadmap && (
        <>
          <div className="bg-gradient-to-r from-primary-600 to-violet-600 rounded-2xl p-6 text-white">
            <p className="text-white/70 text-sm">Your roadmap for</p>
            <h2 className="text-2xl font-display font-bold mt-1">{roadmap.target_career}</h2>
            <p className="text-white/60 text-xs mt-2">
              Generated {new Date(roadmap.generated_at).toLocaleDateString("en-IN")}
            </p>
          </div>

          {/* Phase tabs */}
          <div className="flex gap-2 overflow-x-auto pb-1">
            {Object.entries(PHASE_LABELS).map(([key, meta]) => (
              <button key={key} onClick={() => setActivePhase(key)}
                className={`shrink-0 px-4 py-2 rounded-xl text-sm font-medium border transition-all ${
                  activePhase === key ? `${meta.bg} ${meta.color}` : "bg-white border-gray-200 text-gray-500 hover:border-gray-300"
                }`}
              >
                {meta.label}
              </button>
            ))}
          </div>

          {/* Milestones */}
          <div className="space-y-3">
            {(roadmap.plans[activePhase as keyof typeof roadmap.plans] || []).map((milestone, i) => (
              <motion.div key={i} initial={{ opacity: 0, x: -10 }} animate={{ opacity: 1, x: 0 }}
                transition={{ delay: i * 0.07 }}
                className="bg-white rounded-2xl p-5 shadow-sm border border-gray-100 flex gap-4"
              >
                <div className={`w-8 h-8 rounded-xl flex items-center justify-center shrink-0 ${
                  milestone.type === "career" ? "bg-green-100 text-green-700" :
                  milestone.type === "learning" ? "bg-blue-100 text-blue-700" :
                  milestone.type === "project" ? "bg-violet-100 text-violet-700" :
                  milestone.type === "certification" ? "bg-yellow-100 text-yellow-700" :
                  "bg-gray-100 text-gray-600"
                }`}>
                  {TYPE_ICON[milestone.type] ?? <CheckCircle2 className="w-4 h-4" />}
                </div>
                <div>
                  <h4 className="font-semibold text-gray-900 text-sm">{milestone.title}</h4>
                  <p className="text-sm text-gray-600 mt-1 leading-relaxed">{milestone.description}</p>
                  <span className={`inline-block mt-2 text-xs px-2 py-0.5 rounded-full font-medium ${
                    milestone.type === "career" ? "bg-green-100 text-green-700" :
                    milestone.type === "learning" ? "bg-blue-100 text-blue-700" :
                    milestone.type === "project" ? "bg-violet-100 text-violet-700" :
                    "bg-yellow-100 text-yellow-700"
                  }`}>
                    {milestone.type}
                  </span>
                </div>
              </motion.div>
            ))}
          </div>
        </>
      )}
    </div>
  );
}
