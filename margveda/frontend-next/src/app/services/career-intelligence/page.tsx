import type { Metadata } from "next";
import Link from "next/link";
import { ArrowRight } from "lucide-react";

export const metadata: Metadata = {
  title: "Career Intelligence — Career Brownie",
  description: "Real-time career intelligence: job market trends, salary benchmarks, skill demand forecasts, and industry insights for Indian professionals.",
};

export default function CareerIntelligencePage() {
  return (
    <div className="pt-24">
      <section className="bg-gradient-hero py-24 relative overflow-hidden">
        <div className="absolute inset-0 pattern-grid opacity-20" />
        <div className="container-custom relative z-10 max-w-2xl">
          <span className="inline-block bg-white/10 text-white text-sm font-semibold px-4 py-1.5 rounded-full mb-5">📊 Career Intelligence</span>
          <h1 className="text-4xl md:text-5xl font-black text-white mb-6">Data-Driven Career Decisions, Not Guesswork</h1>
          <p className="text-white/70 text-lg mb-8">Real-time job market data, salary benchmarks, emerging role forecasts, and personalized skill gap reports — all in one platform.</p>
          <Link href="/book-consultation" className="btn-primary inline-flex items-center gap-2">Get Your Career Report <ArrowRight size={18} /></Link>
        </div>
      </section>
      <section className="py-24 bg-white">
        <div className="container-custom">
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-16">
            {[
              { emoji: "📈", title: "Job Market Trends", desc: "Real-time demand data across 500+ roles and 50+ industries in India." },
              { emoji: "💰", title: "Salary Benchmarks", desc: "Up-to-date salary ranges by role, experience, company size, and location." },
              { emoji: "🔍", title: "Skill Gap Analysis", desc: "Compare your current skills against what top companies need — know exactly what to learn." },
              { emoji: "🔮", title: "Future-Proof Index", desc: "Which careers are growing, stable, or at risk of automation? We tell you." },
            ].map((item) => (
              <div key={item.title} className="border border-slate-100 rounded-2xl p-6 card-hover text-center">
                <div className="text-4xl mb-3">{item.emoji}</div>
                <h3 className="font-bold text-slate-900 mb-2">{item.title}</h3>
                <p className="text-slate-500 text-sm">{item.desc}</p>
              </div>
            ))}
          </div>
          <div className="text-center">
            <Link href="/book-consultation" className="btn-primary inline-flex items-center gap-2">
              Get Your Personalized Report <ArrowRight size={18} />
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}
