"use client";

import { motion } from "framer-motion";
import { HOW_IT_WORKS } from "@/lib/constants";

export default function HowItWorksSection() {
  return (
    <section className="py-24 bg-white overflow-hidden">
      <div className="container-custom">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <span className="inline-block bg-violet-50 text-violet-700 text-sm font-semibold px-4 py-1.5 rounded-full mb-4">
            How It Works
          </span>
          <h2 className="section-heading text-slate-900 mb-4">
            Your Career Journey in{" "}
            <span className="text-gradient">4 Simple Steps</span>
          </h2>
          <p className="text-slate-500 max-w-xl mx-auto text-lg">
            From self-discovery to career success — our proven process guides you every step of the way.
          </p>
        </motion.div>

        {/* Steps */}
        <div className="relative">
          {/* Connector line (desktop) */}
          <div className="hidden lg:block absolute top-16 left-1/2 -translate-x-1/2 w-3/4 h-0.5 bg-gradient-to-r from-primary-100 via-primary-400 to-violet-100" />

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {HOW_IT_WORKS.map((step, idx) => (
              <motion.div
                key={step.step}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: idx * 0.1 }}
                className="relative text-center group"
              >
                {/* Step number circle */}
                <div className="relative inline-block mb-6">
                  <div className="w-16 h-16 rounded-2xl bg-gradient-brand flex items-center justify-center mx-auto shadow-lg group-hover:shadow-primary-200 transition-shadow text-2xl">
                    {step.icon}
                  </div>
                  <div className="absolute -top-2 -right-2 w-7 h-7 rounded-full bg-white border-2 border-primary-500 flex items-center justify-center text-xs font-black text-primary-600">
                    {idx + 1}
                  </div>
                </div>

                <h3 className="text-lg font-bold text-slate-900 mb-3">{step.title}</h3>
                <p className="text-slate-500 text-sm leading-relaxed">{step.description}</p>
              </motion.div>
            ))}
          </div>
        </div>

        {/* Feature highlight box */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.4 }}
          className="mt-16 bg-gradient-hero rounded-3xl p-10 md:p-14 text-white relative overflow-hidden"
        >
          <div className="absolute inset-0 pattern-dots opacity-20" />
          <div className="relative z-10 grid md:grid-cols-2 gap-10 items-center">
            <div>
              <h3 className="text-3xl font-black mb-4">
                Free Career Assessment — Worth ₹2,999
              </h3>
              <p className="text-white/70 mb-6 leading-relaxed">
                Take our comprehensive 20-minute career assessment and get a detailed report on your strengths, ideal career paths, skill gaps, and personalized action plan — completely free.
              </p>
              <a href="/book-consultation" className="inline-flex items-center gap-2 bg-white text-primary-700 font-bold px-7 py-3.5 rounded-xl hover:bg-yellow-50 transition-colors shadow-xl">
                Take Free Assessment →
              </a>
            </div>
            <div className="grid grid-cols-2 gap-4">
              {[
                { value: "20 min", label: "Assessment Time" },
                { value: "50+", label: "Career Options Analyzed" },
                { value: "100%", label: "Personalized Report" },
                { value: "Free", label: "No Credit Card Needed" },
              ].map((item) => (
                <div key={item.label} className="bg-white/10 rounded-2xl p-5 border border-white/20 text-center">
                  <p className="text-2xl font-black text-yellow-300">{item.value}</p>
                  <p className="text-white/70 text-sm mt-1">{item.label}</p>
                </div>
              ))}
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
