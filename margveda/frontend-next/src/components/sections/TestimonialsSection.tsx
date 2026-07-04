"use client";

import { motion } from "framer-motion";

export default function TestimonialsSection() {

  return (
    <section className="py-24 bg-slate-50">
      <div className="container-custom">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <span className="inline-block bg-emerald-50 text-emerald-700 text-sm font-semibold px-4 py-1.5 rounded-full mb-4">
            Student Stories
          </span>
          <h2 className="section-heading text-slate-900 mb-4">
            We&apos;re Just{" "}
            <span className="text-gradient">Getting Started</span>
          </h2>
          <p className="text-slate-500 max-w-xl mx-auto">
            We&apos;re building CareerBrownie with our first cohort of students. Be one of our founding users — your story could be here.
          </p>
        </motion.div>

        {/* Coming soon state */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="bg-white border border-dashed border-slate-200 rounded-3xl p-16 text-center"
        >
          <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-primary-100 to-violet-100 flex items-center justify-center mx-auto mb-5 text-3xl">
            💬
          </div>
          <h3 className="font-bold text-slate-900 text-xl mb-3">Student success stories coming soon</h3>
          <p className="text-slate-500 max-w-sm mx-auto mb-6 text-sm leading-relaxed">
            We&apos;re building CareerBrownie with our first students. If you try our platform, we&apos;d love to feature your experience here.
          </p>
          <a
            href="/book-consultation"
            className="inline-flex items-center gap-2 bg-gradient-brand text-white font-semibold px-6 py-3 rounded-xl text-sm hover:shadow-lg hover:shadow-primary-200 transition-shadow"
          >
            Be our first success story
          </a>
        </motion.div>

        {/* Trust badges */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.3 }}
          className="mt-16 flex flex-wrap justify-center gap-6"
        >
          {[
            { icon: "🇮🇳", label: "Made in India", sub: "For Indian Students" },
            { icon: "🤖", label: "AI-Powered Guidance", sub: "Personalized for You" },
            { icon: "🔒", label: "Your Data is Safe", sub: "We Never Share It" },
            { icon: "💬", label: "Free First Session", sub: "No Commitment" },
          ].map((badge) => (
            <div
              key={badge.label}
              className="flex items-center gap-3 bg-white border border-slate-100 rounded-xl px-5 py-3 shadow-sm"
            >
              <span className="text-2xl">{badge.icon}</span>
              <div>
                <p className="text-sm font-bold text-slate-900">{badge.label}</p>
                <p className="text-xs text-slate-500">{badge.sub}</p>
              </div>
            </div>
          ))}
        </motion.div>
      </div>
    </section>
  );
}
