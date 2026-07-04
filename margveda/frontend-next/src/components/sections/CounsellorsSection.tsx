"use client";

import { motion } from "framer-motion";
import Link from "next/link";
import { ArrowRight } from "lucide-react";

const SPECIALIZATIONS = [
  { icon: "🧭", label: "Career Counselling", desc: "Discover the right path based on your strengths and interests." },
  { icon: "🎓", label: "University Admissions", desc: "Shortlisting, SOP writing, and application strategy." },
  { icon: "✈️", label: "Study Abroad", desc: "USA, UK, Canada — end-to-end admissions and visa guidance." },
  { icon: "💼", label: "Career Transitions", desc: "Skill gap analysis and roadmaps for professionals changing tracks." },
  { icon: "📊", label: "MBA & Business", desc: "CAT, GMAT, IIM applications and B-school strategy." },
  { icon: "🤖", label: "AI & Tech Careers", desc: "Navigating careers in software, data science, and emerging tech." },
];

export default function CounsellorsSection() {
  return (
    <section className="py-24 bg-white">
      <div className="container-custom">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <span className="inline-block bg-violet-50 text-violet-700 text-sm font-semibold px-4 py-1.5 rounded-full mb-4">
            Expert Guidance
          </span>
          <h2 className="section-heading text-slate-900 mb-4">
            Personalized Career{" "}
            <span className="text-gradient">Counselling</span>
          </h2>
          <p className="text-slate-500 max-w-xl mx-auto">
            We pair AI insights with experienced human counsellors across every major career domain — so you get guidance that&apos;s both data-driven and deeply personal.
          </p>
        </motion.div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
          {SPECIALIZATIONS.map((s, i) => (
            <motion.div
              key={s.label}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: i * 0.08 }}
              className="bg-slate-50 border border-slate-100 rounded-2xl p-6 card-hover"
            >
              <span className="text-3xl mb-4 block">{s.icon}</span>
              <h3 className="font-bold text-slate-900 mb-2">{s.label}</h3>
              <p className="text-slate-500 text-sm leading-relaxed">{s.desc}</p>
            </motion.div>
          ))}
        </div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.3 }}
          className="text-center"
        >
          <Link href="/book-consultation" className="btn-primary inline-flex items-center gap-2">
            Book a Free Consultation
            <ArrowRight size={18} />
          </Link>
        </motion.div>
      </div>
    </section>
  );
}
