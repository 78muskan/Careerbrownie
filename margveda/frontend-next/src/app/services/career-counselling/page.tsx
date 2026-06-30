import type { Metadata } from "next";
import Link from "next/link";
import { ArrowRight, CheckCircle2 } from "lucide-react";

export const metadata: Metadata = {
  title: "Career Counselling — Career Brownie",
  description: "Expert 1-on-1 career counselling for students and professionals. Psychometric assessments, career roadmaps, and personalized guidance from certified counsellors.",
};

export default function CareerCounsellingPage() {
  return (
    <div className="pt-24">
      <section className="bg-gradient-hero py-24 relative overflow-hidden">
        <div className="absolute inset-0 pattern-grid opacity-20" />
        <div className="container-custom relative z-10">
          <div className="max-w-2xl">
            <span className="inline-block bg-white/10 text-white text-sm font-semibold px-4 py-1.5 rounded-full mb-5">🧭 Career Counselling</span>
            <h1 className="text-4xl md:text-6xl font-black text-white mb-6">
              Find Your Perfect Career Path with Expert Guidance
            </h1>
            <p className="text-white/70 text-lg mb-8">
              One-on-one sessions with certified counsellors who understand India&apos;s job market and your unique potential. Stop guessing — start planning.
            </p>
            <Link href="/book-consultation" className="btn-primary inline-flex items-center gap-2">
              Book Free Session <ArrowRight size={18} />
            </Link>
          </div>
        </div>
      </section>

      <section className="py-24 bg-white">
        <div className="container-custom">
          <div className="grid lg:grid-cols-2 gap-16 items-center mb-20">
            <div>
              <h2 className="text-3xl font-black text-slate-900 mb-6">What Our Career Counselling Covers</h2>
              <div className="space-y-4">
                {[
                  "In-depth psychometric and aptitude assessment",
                  "Identifying your core strengths and interests",
                  "Mapping career options to your profile",
                  "Creating a personalized 12-month career roadmap",
                  "Guidance on courses, certifications, and skills to build",
                  "Interview preparation and resume review",
                  "Ongoing support and progress check-ins",
                ].map((item) => (
                  <div key={item} className="flex items-center gap-3">
                    <CheckCircle2 size={18} className="text-emerald-500 flex-shrink-0" />
                    <span className="text-slate-600">{item}</span>
                  </div>
                ))}
              </div>
            </div>
            <div className="bg-slate-50 rounded-3xl p-8 space-y-4">
              <h3 className="font-black text-slate-900 text-xl mb-5">Who Is This For?</h3>
              {[
                { emoji: "📚", label: "Class 9-12 Students", desc: "Stream selection, entrance exam guidance, career planning" },
                { emoji: "🎓", label: "College Students", desc: "Internship strategy, campus placement prep, higher studies" },
                { emoji: "💼", label: "Working Professionals", desc: "Career transitions, promotions, role changes" },
                { emoji: "👨‍👩‍👧", label: "Parents", desc: "Understanding career options for their children" },
              ].map((item) => (
                <div key={item.label} className="flex items-start gap-4 bg-white rounded-xl p-4 border border-slate-100">
                  <span className="text-2xl">{item.emoji}</span>
                  <div>
                    <p className="font-bold text-slate-900 text-sm">{item.label}</p>
                    <p className="text-slate-500 text-xs">{item.desc}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="text-center bg-gradient-hero rounded-3xl py-14 px-8 relative overflow-hidden">
            <div className="absolute inset-0 pattern-dots opacity-20" />
            <div className="relative z-10">
              <h2 className="text-3xl font-black text-white mb-4">Start with a Free 30-Min Session</h2>
              <p className="text-white/70 mb-8 max-w-md mx-auto">No commitment, no credit card. Just honest, expert career advice.</p>
              <Link href="/book-consultation" className="inline-flex items-center gap-2 bg-white text-primary-700 font-bold px-8 py-4 rounded-xl hover:bg-yellow-50 transition-colors">
                Book Free Consultation <ArrowRight size={18} />
              </Link>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
