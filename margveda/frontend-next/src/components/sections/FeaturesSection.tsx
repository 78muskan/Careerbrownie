"use client";

import { motion } from "framer-motion";
import { Brain, BarChart3, Globe2, GraduationCap, Shield, Zap } from "lucide-react";

const features = [
  {
    icon: Brain,
    title: "AI-Powered Matching",
    description: "Our proprietary AI analyzes 100+ data points to match you with the most suitable career paths based on your unique profile.",
    color: "text-violet-600 bg-violet-50",
  },
  {
    icon: BarChart3,
    title: "Real-Time Market Data",
    description: "Access live job market trends, salary benchmarks, and demand forecasts across 500+ industries and roles.",
    color: "text-blue-600 bg-blue-50",
  },
  {
    icon: GraduationCap,
    title: "University Matching",
    description: "Smart college shortlisting based on your profile, goals, and budget — spanning 500+ universities across India and abroad.",
    color: "text-emerald-600 bg-emerald-50",
  },
  {
    icon: Globe2,
    title: "Study Abroad Support",
    description: "Complete end-to-end assistance for international admissions — from country selection to visa, scholarships, and pre-departure prep.",
    color: "text-orange-600 bg-orange-50",
  },
  {
    icon: Shield,
    title: "Verified Counsellors",
    description: "All our counsellors are verified, certified, and have minimum 5 years of experience in their respective domains.",
    color: "text-red-600 bg-red-50",
  },
  {
    icon: Zap,
    title: "Instant AI Reports",
    description: "Get detailed career assessment reports, skill gap analyses, and personalized roadmaps in under 5 minutes — 24/7.",
    color: "text-yellow-600 bg-yellow-50",
  },
];

export default function FeaturesSection() {
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
          <span className="inline-block bg-primary-50 text-primary-700 text-sm font-semibold px-4 py-1.5 rounded-full mb-4">
            Why Career Brownie?
          </span>
          <h2 className="section-heading text-slate-900 mb-4">
            Built for the{" "}
            <span className="text-gradient">Next Generation</span> of Indians
          </h2>
          <p className="text-slate-500 max-w-2xl mx-auto text-lg">
            A platform that truly understands the Indian student&apos;s journey — from board exams to board rooms.
          </p>
        </motion.div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, i) => {
            const Icon = feature.icon;
            return (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: i * 0.08 }}
                className="group p-6 rounded-2xl border border-slate-100 hover:border-primary-100 hover:shadow-lg hover:shadow-primary-50 transition-all duration-300 cursor-default"
              >
                <div
                  className={`w-12 h-12 rounded-xl ${feature.color} flex items-center justify-center mb-5 group-hover:scale-110 transition-transform duration-300`}
                >
                  <Icon size={22} />
                </div>
                <h3 className="text-lg font-bold text-slate-900 mb-3">{feature.title}</h3>
                <p className="text-slate-500 text-sm leading-relaxed">{feature.description}</p>
              </motion.div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
