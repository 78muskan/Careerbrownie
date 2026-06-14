import type { Metadata } from "next";
import Link from "next/link";
import { ArrowRight } from "lucide-react";

export const metadata: Metadata = {
  title: "Study Abroad Consulting — MargVedA",
  description: "Complete study abroad support for Indian students — country selection, university applications, visa guidance, scholarships, and pre-departure preparation.",
};

export default function StudyAbroadPage() {
  return (
    <div className="pt-24">
      <section className="bg-gradient-hero py-24 relative overflow-hidden">
        <div className="absolute inset-0 pattern-grid opacity-20" />
        <div className="container-custom relative z-10 max-w-2xl">
          <span className="inline-block bg-white/10 text-white text-sm font-semibold px-4 py-1.5 rounded-full mb-5">✈️ Study Abroad</span>
          <h1 className="text-4xl md:text-5xl font-black text-white mb-6">Your Global Education Journey Starts Here</h1>
          <p className="text-white/70 text-lg mb-8">From choosing the right country to landing your dream university abroad — we handle the complexity so you can focus on your future.</p>
          <Link href="/book-consultation" className="btn-primary inline-flex items-center gap-2">Book Free Session <ArrowRight size={18} /></Link>
        </div>
      </section>
      <section className="py-24 bg-white">
        <div className="container-custom">
          <div className="grid md:grid-cols-2 gap-8 mb-16">
            {[
              { flag: "🇺🇸", country: "USA", desc: "Ivy League to state universities — full-cycle support for F-1 visa and OPT." },
              { flag: "🇨🇦", country: "Canada", desc: "Study permit guidance, top university applications, and PR pathway planning." },
              { flag: "🇬🇧", country: "UK", desc: "UCAS applications, Tier 4 student visa, and scholarship hunt for Indian students." },
              { flag: "🇦🇺", country: "Australia", desc: "AQF-aligned programs, Student Visa (subclass 500), and work rights guidance." },
              { flag: "🇩🇪", country: "Germany", desc: "Free public university applications, blocked account setup, and German visa support." },
              { flag: "🇸🇬", country: "Singapore", desc: "NUS/NTU applications, SMU programs, and Singapore scholarship opportunities." },
            ].map((item) => (
              <div key={item.country} className="flex gap-5 border border-slate-100 rounded-2xl p-6 card-hover">
                <div className="text-4xl flex-shrink-0">{item.flag}</div>
                <div>
                  <h3 className="font-bold text-slate-900 text-lg mb-1">{item.country}</h3>
                  <p className="text-slate-500 text-sm">{item.desc}</p>
                </div>
              </div>
            ))}
          </div>
          <div className="text-center">
            <Link href="/book-consultation" className="btn-primary inline-flex items-center gap-2">
              Book Study Abroad Consultation <ArrowRight size={18} />
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}
