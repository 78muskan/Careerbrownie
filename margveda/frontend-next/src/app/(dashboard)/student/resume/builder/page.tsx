"use client";
import { useEffect, useState, Suspense } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import { Plus, Trash2, Save, ChevronDown, ChevronUp } from "lucide-react";
import api from "@/lib/api";

const SECTION_TEMPLATES: Record<string, object> = {
  experience: { company: "", role: "", start_date: "", end_date: "", description: "" },
  education: { institution: "", degree: "", field: "", start_year: "", end_year: "", grade: "" },
  skills: { category: "Technical", skills: "" },
  projects: { name: "", description: "", tech_stack: "", link: "" },
  certifications: { name: "", issuer: "", date: "", link: "" },
  achievements: { title: "", description: "", year: "" },
};

function BuilderContent() {
  const params = useSearchParams();
  const router = useRouter();
  const resumeId = params.get("id");

  const [resume, setResume] = useState<any>(null);
  const [saving, setSaving] = useState(false);
  const [activeSection, setActiveSection] = useState<string | null>(null);

  useEffect(() => {
    if (resumeId) api.get(`/resume/${resumeId}/`).then(r => setResume(r.data));
  }, [resumeId]);

  async function savePersonalInfo(field: string, value: string) {
    const updated = { ...resume.personal_info, [field]: value };
    setResume((p: any) => ({ ...p, personal_info: updated }));
    await api.patch(`/resume/${resumeId}/`, { personal_info: updated });
  }

  async function addSection(sectionType: string) {
    const res = await api.post(`/resume/${resumeId}/sections/`, {
      section_type: sectionType,
      title: sectionType.charAt(0).toUpperCase() + sectionType.slice(1),
      content: [{ ...SECTION_TEMPLATES[sectionType] }],
      order: resume.sections.length,
    });
    setResume((p: any) => ({ ...p, sections: [...p.sections, res.data] }));
    setActiveSection(res.data.id);
  }

  async function deleteSection(sectionId: string) {
    await api.delete(`/resume/${resumeId}/sections/${sectionId}/`);
    setResume((p: any) => ({ ...p, sections: p.sections.filter((s: any) => s.id !== sectionId) }));
  }

  async function updateSectionContent(sectionId: string, content: object[]) {
    setSaving(true);
    await api.patch(`/resume/${resumeId}/sections/${sectionId}/`, { content });
    setResume((p: any) => ({
      ...p, sections: p.sections.map((s: any) => s.id === sectionId ? { ...s, content } : s),
    }));
    setSaving(false);
  }

  async function saveSummary(summary: string) {
    await api.patch(`/resume/${resumeId}/`, { summary });
    setResume((p: any) => ({ ...p, summary }));
  }

  if (!resume) return <div className="flex items-center justify-center h-64"><div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600" /></div>;

  const PI_FIELDS = [
    { key: "name", label: "Full Name" },
    { key: "email", label: "Email" },
    { key: "phone", label: "Phone" },
    { key: "city", label: "City" },
    { key: "linkedin", label: "LinkedIn URL" },
    { key: "github", label: "GitHub URL" },
    { key: "title", label: "Professional Title" },
  ];

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">{resume.title}</h1>
          <p className="text-sm text-gray-500">Build your ATS-optimised resume</p>
        </div>
        <div className="flex gap-3">
          {saving && <span className="text-sm text-indigo-600 flex items-center gap-1"><Save className="w-4 h-4 animate-pulse" /> Saving…</span>}
          <button onClick={() => router.push(`/student/resume/ats?id=${resumeId}`)}
            className="bg-green-600 text-white px-4 py-2 rounded-xl hover:bg-green-700 text-sm">
            Get ATS Score →
          </button>
        </div>
      </div>

      {/* Personal Info */}
      <section className="bg-white rounded-2xl border border-gray-200 p-6 mb-4">
        <h2 className="font-semibold text-gray-800 mb-4">Personal Information</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {PI_FIELDS.map(f => (
            <div key={f.key}>
              <label className="text-xs text-gray-500 mb-1 block">{f.label}</label>
              <input defaultValue={resume.personal_info?.[f.key] || ""} onBlur={e => savePersonalInfo(f.key, e.target.value)}
                className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-300" />
            </div>
          ))}
        </div>
      </section>

      {/* Summary */}
      <section className="bg-white rounded-2xl border border-gray-200 p-6 mb-4">
        <h2 className="font-semibold text-gray-800 mb-4">Professional Summary</h2>
        <textarea defaultValue={resume.summary} onBlur={e => saveSummary(e.target.value)} rows={4}
          placeholder="Write a 2-3 sentence summary highlighting your top skills and career goals…"
          className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-300 resize-none" />
      </section>

      {/* Dynamic Sections */}
      {resume.sections.map((section: any) => (
        <motion.section key={section.id} layout
          className="bg-white rounded-2xl border border-gray-200 mb-4 overflow-hidden">
          <div className="flex items-center justify-between px-6 py-4 cursor-pointer"
            onClick={() => setActiveSection(activeSection === section.id ? null : section.id)}>
            <h2 className="font-semibold text-gray-800 capitalize">{section.title}</h2>
            <div className="flex items-center gap-2">
              <button onClick={e => { e.stopPropagation(); deleteSection(section.id); }}
                className="text-red-400 hover:text-red-600 p-1">
                <Trash2 className="w-4 h-4" />
              </button>
              {activeSection === section.id ? <ChevronUp className="w-4 h-4 text-gray-400" /> : <ChevronDown className="w-4 h-4 text-gray-400" />}
            </div>
          </div>

          <AnimatePresence>
            {activeSection === section.id && (
              <motion.div initial={{ height: 0 }} animate={{ height: "auto" }} exit={{ height: 0 }}
                className="overflow-hidden">
                <div className="px-6 pb-6">
                  {(Array.isArray(section.content) ? section.content : []).map((item: any, idx: number) => (
                    <div key={idx} className="mb-4 p-4 bg-gray-50 rounded-xl">
                      {Object.keys(item).map(field => (
                        <div key={field} className="mb-3">
                          <label className="text-xs text-gray-500 capitalize block mb-1">{field.replace("_", " ")}</label>
                          {field === "description" ? (
                            <textarea defaultValue={item[field]} rows={3} onBlur={e => {
                              const updated = [...section.content];
                              updated[idx] = { ...updated[idx], [field]: e.target.value };
                              updateSectionContent(section.id, updated);
                            }} className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-200 resize-none" />
                          ) : (
                            <input defaultValue={item[field]} onBlur={e => {
                              const updated = [...section.content];
                              updated[idx] = { ...updated[idx], [field]: e.target.value };
                              updateSectionContent(section.id, updated);
                            }} className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-200" />
                          )}
                        </div>
                      ))}
                    </div>
                  ))}
                  <button onClick={() => updateSectionContent(section.id, [
                    ...(Array.isArray(section.content) ? section.content : []),
                    { ...SECTION_TEMPLATES[section.section_type] || {} },
                  ])} className="flex items-center gap-1 text-sm text-indigo-600 hover:text-indigo-800">
                    <Plus className="w-4 h-4" /> Add Entry
                  </button>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </motion.section>
      ))}

      {/* Add Section */}
      <div className="bg-gray-50 rounded-2xl border-2 border-dashed border-gray-200 p-6">
        <p className="text-sm text-gray-600 mb-3 font-medium">Add Section</p>
        <div className="flex flex-wrap gap-2">
          {Object.keys(SECTION_TEMPLATES).map(type => (
            <button key={type} onClick={() => addSection(type)}
              className="flex items-center gap-1 text-sm border border-indigo-200 text-indigo-700 px-3 py-1.5 rounded-lg hover:bg-indigo-50 transition">
              <Plus className="w-3 h-3" /> {type.charAt(0).toUpperCase() + type.slice(1)}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}

export default function ResumeBuilderPage() {
  return (
    <Suspense fallback={<div className="flex items-center justify-center h-64"><div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600" /></div>}>
      <BuilderContent />
    </Suspense>
  );
}
