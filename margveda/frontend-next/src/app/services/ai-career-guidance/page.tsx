import type { Metadata } from "next";
import Link from "next/link";
import { ArrowRight } from "lucide-react";

export const metadata: Metadata = {
  title: "AI Career Guidance — MargVedA",
  description: "India's most advanced AI career counsellor. Get instant, personalized career advice 24/7. Powered by Claude AI and OpenAI.",
};

export default function AiCareerGuidancePage() {
  return (
    <div className="pt-24">
      <section className="bg-gradient-hero py-24 relative overflow-hidden">
        <div className="absolute inset-0 pattern-grid opacity-20" />
        <div className="absolute top-1/3 right-1/4 w-96 h-96 bg-violet-500/20 rounded-full blur-3xl" />
        <div className="container-custom relative z-10 max-w-2xl">
          <span className="inline-block bg-white/10 text-white text-sm font-semibold px-4 py-1.5 rounded-full mb-5">🤖 AI Career Guidance</span>
          <h1 className="text-4xl md:text-5xl font-black text-white mb-6">India&apos;s Most Advanced AI Career Counsellor</h1>
          <p className="text-white/70 text-lg mb-8">Available 24/7. Never judges. Endlessly patient. Powered by Claude AI — our AI counsellor has helped 50,000+ students find their career path.</p>
          <div className="flex gap-4 flex-wrap">
            <Link href="/book-consultation" className="btn-primary inline-flex items-center gap-2">Try AI Counsellor <ArrowRight size={18} /></Link>
            <Link href="/book-consultation" className="border-2 border-white/30 text-white font-semibold px-6 py-3 rounded-xl hover:bg-white/10 transition-colors">Book Human Expert</Link>
          </div>
        </div>
      </section>
      <section className="py-24 bg-white">
        <div className="container-custom">
          <div className="grid lg:grid-cols-2 gap-16 items-center mb-16">
            <div>
              <h2 className="text-3xl font-black text-slate-900 mb-6">What the AI Can Do</h2>
              <div className="space-y-4">
                {[
                  "Analyze your academic background and generate career recommendations",
                  "Answer any career question instantly — no waiting, no scheduling",
                  "Generate detailed skill gap reports and learning roadmaps",
                  "Compare career options based on your priorities (salary, growth, lifestyle)",
                  "Help you prepare for job interviews with mock Q&A sessions",
                  "Track your progress and update recommendations as you grow",
                ].map((item, i) => (
                  <div key={i} className="flex items-start gap-3">
                    <div className="w-6 h-6 rounded-full bg-primary-100 text-primary-600 flex items-center justify-center text-xs font-bold flex-shrink-0 mt-0.5">{i + 1}</div>
                    <span className="text-slate-600 text-sm">{item}</span>
                  </div>
                ))}
              </div>
            </div>
            <div className="bg-slate-900 rounded-3xl p-8 text-white">
              <div className="space-y-4">
                <div className="flex gap-3">
                  <div className="w-8 h-8 rounded-full bg-primary-500 flex items-center justify-center text-sm font-bold flex-shrink-0">U</div>
                  <div className="bg-slate-800 rounded-2xl rounded-tl-none px-4 py-3 text-sm text-slate-300">
                    I&apos;m in Class 12 PCM and confused between engineering and data science. What should I choose?
                  </div>
                </div>
                <div className="flex gap-3 flex-row-reverse">
                  <div className="w-8 h-8 rounded-full bg-gradient-brand flex items-center justify-center text-sm font-bold flex-shrink-0">AI</div>
                  <div className="bg-primary-900/50 border border-primary-700/30 rounded-2xl rounded-tr-none px-4 py-3 text-sm text-slate-200 max-w-xs">
                    Great question! Both are excellent paths in 2025. Let me ask you: do you prefer building systems (engineering) or extracting insights from data (data science)? Your answer will tell us a lot about which direction fits your personality better...
                  </div>
                </div>
              </div>
              <div className="mt-6 pt-4 border-t border-slate-700">
                <p className="text-slate-400 text-xs text-center">Powered by Claude AI · Available 24/7 · 100% Private</p>
              </div>
            </div>
          </div>
          <div className="text-center">
            <Link href="/book-consultation" className="btn-primary inline-flex items-center gap-2">
              Start AI Career Chat <ArrowRight size={18} />
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}
