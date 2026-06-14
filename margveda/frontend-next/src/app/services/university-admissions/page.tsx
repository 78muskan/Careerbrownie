import type { Metadata } from "next";
import Link from "next/link";
import { ArrowRight } from "lucide-react";

export const metadata: Metadata = {
  title: "University Admissions Consulting — MargVedA",
  description: "Expert guidance for IIT, NIT, IIM, and top university admissions. SOP writing, application review, interview prep, and more.",
};

export default function UniversityAdmissionsPage() {
  return (
    <div className="pt-24">
      <section className="bg-gradient-hero py-24 relative overflow-hidden">
        <div className="absolute inset-0 pattern-grid opacity-20" />
        <div className="container-custom relative z-10 max-w-2xl">
          <span className="inline-block bg-white/10 text-white text-sm font-semibold px-4 py-1.5 rounded-full mb-5">🎓 University Admissions</span>
          <h1 className="text-4xl md:text-5xl font-black text-white mb-6">Get Into Your Dream College with Expert Support</h1>
          <p className="text-white/70 text-lg mb-8">From shortlisting the right colleges to crafting standout applications — our admissions experts guide you every step of the way.</p>
          <Link href="/book-consultation" className="btn-primary inline-flex items-center gap-2">Book Free Session <ArrowRight size={18} /></Link>
        </div>
      </section>
      <section className="py-24 bg-white">
        <div className="container-custom">
          <div className="grid md:grid-cols-3 gap-6 mb-16">
            {[
              { emoji: "🏛️", title: "IIT/NIT Guidance", desc: "JEE strategy, mock tests, counselling session planning, and seat prediction tools." },
              { emoji: "💼", title: "MBA Admissions", desc: "CAT prep strategy, IIM shortlisting, PI-WAT preparation, and profile building." },
              { emoji: "⚕️", title: "Medical Admissions", desc: "NEET guidance, AIIMS/JIPMER strategy, and medical college counselling." },
              { emoji: "⚖️", title: "Law Schools", desc: "CLAT prep, NLU shortlisting, and personal statement review." },
              { emoji: "🎨", title: "Design & Arts", desc: "NID/NIFT entrance prep, portfolio review, and art school applications." },
              { emoji: "💻", title: "Tech Programs", desc: "B.Tech/M.Tech applications, GATE guidance, and research program admissions." },
            ].map((item) => (
              <div key={item.title} className="border border-slate-100 rounded-2xl p-6 card-hover bg-white">
                <div className="text-3xl mb-3">{item.emoji}</div>
                <h3 className="font-bold text-slate-900 mb-2">{item.title}</h3>
                <p className="text-slate-500 text-sm">{item.desc}</p>
              </div>
            ))}
          </div>
          <div className="text-center">
            <Link href="/book-consultation" className="btn-primary inline-flex items-center gap-2">
              Book Admissions Consultation <ArrowRight size={18} />
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}
