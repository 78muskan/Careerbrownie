"use client";

import { motion } from "framer-motion";

const partners = [
  { name: "IIT Bombay", logo: "🏛️" },
  { name: "IIM Ahmedabad", logo: "📚" },
  { name: "BITS Pilani", logo: "🔬" },
  { name: "Delhi University", logo: "🎓" },
  { name: "VIT Vellore", logo: "🏫" },
  { name: "Manipal University", logo: "📖" },
  { name: "SRM Institute", logo: "⚗️" },
  { name: "Amity University", logo: "🌐" },
  { name: "Symbiosis", logo: "📝" },
  { name: "Christ University", logo: "✨" },
  { name: "FLAME University", logo: "🎯" },
  { name: "Ashoka University", logo: "💡" },
];

const intlPartners = [
  { name: "University of Toronto", country: "🇨🇦" },
  { name: "University of Melbourne", country: "🇦🇺" },
  { name: "NUS Singapore", country: "🇸🇬" },
  { name: "Imperial College London", country: "🇬🇧" },
  { name: "TU Munich", country: "🇩🇪" },
  { name: "University of Edinburgh", country: "🇬🇧" },
];

export default function UniversityPartnersSection() {
  return (
    <section className="py-20 bg-white overflow-hidden">
      <div className="container-custom">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-12"
        >
          <span className="inline-block bg-emerald-50 text-emerald-700 text-sm font-semibold px-4 py-1.5 rounded-full mb-4">
            University Partners
          </span>
          <h2 className="section-heading text-slate-900 mb-3">
            Guidance for <span className="text-gradient">Universities Across India</span>
          </h2>
          <p className="text-slate-500">Helping students explore and apply to institutions across India and abroad</p>
        </motion.div>

        {/* Indian Universities ticker */}
        <div className="mb-10">
          <p className="text-xs font-semibold text-slate-400 uppercase tracking-widest text-center mb-5">India&apos;s Top Universities</p>
          <div className="relative overflow-hidden">
            <div className="flex gap-4 animate-[scroll_30s_linear_infinite]" style={{ width: "max-content" }}>
              {[...partners, ...partners].map((p, i) => (
                <div
                  key={i}
                  className="flex-shrink-0 bg-slate-50 border border-slate-100 rounded-xl px-6 py-3.5 flex items-center gap-3 hover:border-primary-200 transition-colors"
                >
                  <span className="text-2xl">{p.logo}</span>
                  <span className="text-sm font-semibold text-slate-700 whitespace-nowrap">{p.name}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* International partners */}
        <div>
          <p className="text-xs font-semibold text-slate-400 uppercase tracking-widest text-center mb-5">Global University Partners</p>
          <div className="flex flex-wrap justify-center gap-3">
            {intlPartners.map((p) => (
              <div
                key={p.name}
                className="flex items-center gap-2 bg-slate-50 border border-slate-100 rounded-full px-5 py-2.5 text-sm font-medium text-slate-700 hover:border-primary-200 hover:text-primary-700 transition-colors cursor-default"
              >
                <span>{p.country}</span>
                {p.name}
              </div>
            ))}
            <div className="flex items-center gap-2 bg-primary-50 border border-primary-100 rounded-full px-5 py-2.5 text-sm font-medium text-primary-700">
              +494 more universities
            </div>
          </div>
        </div>
      </div>

      <style jsx>{`
        @keyframes scroll {
          0% { transform: translateX(0); }
          100% { transform: translateX(-50%); }
        }
      `}</style>
    </section>
  );
}
