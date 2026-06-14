"use client";

import { motion } from "framer-motion";
import Link from "next/link";
import { ArrowRight, Play, Star, Users, Award, TrendingUp } from "lucide-react";
import { STATS } from "@/lib/constants";

const floatingCards = [
  { icon: "🎯", label: "AI Career Match", value: "98% Accuracy", color: "bg-violet-50 border-violet-100" },
  { icon: "📈", label: "Avg Salary Boost", value: "+45% in 1 Year", color: "bg-emerald-50 border-emerald-100" },
  { icon: "🏆", label: "Top Placements", value: "Google, IIM & More", color: "bg-amber-50 border-amber-100" },
];

export default function HeroSection() {
  return (
    <section className="relative min-h-screen flex items-center overflow-hidden bg-gradient-hero pt-28 pb-20">
      {/* Background patterns */}
      <div className="absolute inset-0 pattern-grid opacity-30" />
      <div className="absolute inset-0">
        {/* Glow blobs */}
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-primary-600/20 rounded-full blur-3xl animate-pulse-slow" />
        <div className="absolute bottom-1/4 right-1/4 w-80 h-80 bg-violet-600/20 rounded-full blur-3xl animate-pulse-slow" style={{ animationDelay: "1.5s" }} />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-64 h-64 bg-pink-500/10 rounded-full blur-3xl animate-pulse-slow" style={{ animationDelay: "0.75s" }} />
      </div>

      <div className="container-custom relative z-10 w-full">
        <div className="grid lg:grid-cols-2 gap-16 items-center">
          {/* Left content */}
          <div>
            {/* Badge */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
              className="inline-flex items-center gap-2 bg-white/10 border border-white/20 rounded-full px-4 py-1.5 mb-6"
            >
              <span className="w-2 h-2 bg-emerald-400 rounded-full animate-pulse" />
              <span className="text-white/90 text-sm font-medium">
                India&apos;s #1 AI Career Platform — Trusted by 50,000+ Students
              </span>
            </motion.div>

            {/* Headline */}
            <motion.h1
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.1 }}
              className="text-5xl md:text-6xl xl:text-7xl font-black text-white mb-6 leading-[1.1]"
            >
              Discover Your{" "}
              <span className="relative">
                <span className="text-transparent bg-clip-text bg-gradient-to-r from-yellow-300 via-orange-300 to-pink-300">
                  Ideal Career
                </span>
                <motion.svg
                  viewBox="0 0 300 20"
                  className="absolute -bottom-2 left-0 w-full"
                  initial={{ pathLength: 0 }}
                  animate={{ pathLength: 1 }}
                  transition={{ duration: 0.8, delay: 0.8 }}
                >
                  <motion.path
                    d="M10 15 Q75 5 150 12 Q225 19 290 8"
                    stroke="url(#underlineGradient)"
                    strokeWidth="3"
                    fill="none"
                    strokeLinecap="round"
                  />
                  <defs>
                    <linearGradient id="underlineGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                      <stop offset="0%" stopColor="#fbbf24" />
                      <stop offset="100%" stopColor="#f472b6" />
                    </linearGradient>
                  </defs>
                </motion.svg>
              </span>{" "}
              with AI
            </motion.h1>

            {/* Subtext */}
            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="text-lg text-white/70 mb-8 max-w-lg leading-relaxed"
            >
              MargVedA combines cutting-edge AI with expert human counselling to help students from Class 9 to professionals chart their perfect career path. Get personalized guidance, real-time insights, and university admissions support — all in one place.
            </motion.p>

            {/* CTA buttons */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.3 }}
              className="flex flex-col sm:flex-row gap-4 mb-10"
            >
              <Link
                href="/book-consultation"
                className="inline-flex items-center justify-center gap-2 bg-white text-primary-700 font-bold px-8 py-4 rounded-xl hover:bg-yellow-50 transition-all shadow-xl hover:shadow-2xl hover:-translate-y-0.5"
              >
                Book Free Consultation
                <ArrowRight size={18} />
              </Link>
              <Link
                href="/services/ai-career-guidance"
                className="inline-flex items-center justify-center gap-2.5 border-2 border-white/30 text-white font-semibold px-8 py-4 rounded-xl hover:bg-white/10 transition-all"
              >
                <div className="w-8 h-8 rounded-full bg-white/20 flex items-center justify-center">
                  <Play size={14} className="fill-white text-white ml-0.5" />
                </div>
                See How It Works
              </Link>
            </motion.div>

            {/* Trust indicators */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.6, delay: 0.5 }}
              className="flex items-center gap-4"
            >
              <div className="flex -space-x-2">
                {[1, 2, 3, 4, 5].map((i) => (
                  <div
                    key={i}
                    className="w-9 h-9 rounded-full border-2 border-primary-800 bg-gradient-to-br from-primary-400 to-violet-500 flex items-center justify-center text-white text-xs font-bold"
                  >
                    {["P", "A", "R", "S", "M"][i - 1]}
                  </div>
                ))}
              </div>
              <div>
                <div className="flex items-center gap-1 mb-0.5">
                  {[1, 2, 3, 4, 5].map((i) => (
                    <Star key={i} size={12} className="fill-yellow-400 text-yellow-400" />
                  ))}
                  <span className="text-yellow-400 text-sm font-bold ml-1">4.9/5</span>
                </div>
                <p className="text-white/60 text-xs">Trusted by 50,000+ students across India</p>
              </div>
            </motion.div>
          </div>

          {/* Right visual */}
          <motion.div
            initial={{ opacity: 0, x: 40 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.7, delay: 0.3 }}
            className="hidden lg:block relative"
          >
            {/* Central card */}
            <div className="relative mx-auto max-w-sm">
              <div className="bg-white/10 backdrop-blur-xl border border-white/20 rounded-3xl p-8 text-white">
                {/* Career path visual */}
                <div className="text-center mb-6">
                  <div className="w-20 h-20 rounded-2xl bg-gradient-to-br from-primary-500 to-violet-500 mx-auto mb-4 flex items-center justify-center shadow-xl">
                    <span className="text-4xl">🧭</span>
                  </div>
                  <h3 className="font-bold text-xl mb-1">Your Career Path</h3>
                  <p className="text-white/60 text-sm">AI-Powered Analysis Complete</p>
                </div>

                {/* Progress bars */}
                {[
                  { label: "Data Science", match: 96, color: "bg-emerald-400" },
                  { label: "Product Management", match: 88, color: "bg-blue-400" },
                  { label: "UX Design", match: 74, color: "bg-purple-400" },
                ].map((item) => (
                  <div key={item.label} className="mb-4">
                    <div className="flex justify-between items-center mb-1.5">
                      <span className="text-sm font-medium">{item.label}</span>
                      <span className="text-sm font-bold">{item.match}%</span>
                    </div>
                    <div className="h-2 bg-white/10 rounded-full overflow-hidden">
                      <motion.div
                        className={`h-full ${item.color} rounded-full`}
                        initial={{ width: 0 }}
                        animate={{ width: `${item.match}%` }}
                        transition={{ duration: 1.2, delay: 1 }}
                      />
                    </div>
                  </div>
                ))}

                <Link
                  href="/book-consultation"
                  className="block mt-6 bg-white text-primary-700 font-bold text-sm py-3 rounded-xl text-center hover:bg-primary-50 transition-colors"
                >
                  View Full Report →
                </Link>
              </div>

              {/* Floating cards */}
              {floatingCards.map((card, i) => (
                <motion.div
                  key={card.label}
                  animate={{ y: [0, i % 2 === 0 ? -10 : 10, 0] }}
                  transition={{
                    duration: 3 + i,
                    repeat: Infinity,
                    ease: "easeInOut",
                  }}
                  className={`absolute ${
                    i === 0 ? "-left-12 top-8" : i === 1 ? "-right-14 top-1/2 -translate-y-1/2" : "-left-10 bottom-10"
                  } bg-white rounded-2xl shadow-2xl border ${card.color} px-4 py-3 min-w-[160px]`}
                >
                  <div className="flex items-center gap-2.5">
                    <span className="text-2xl">{card.icon}</span>
                    <div>
                      <p className="text-xs text-slate-500 font-medium">{card.label}</p>
                      <p className="text-sm font-bold text-slate-800">{card.value}</p>
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>
          </motion.div>
        </div>

        {/* Stats row */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.6 }}
          className="grid grid-cols-2 md:grid-cols-4 gap-6 mt-16 pt-12 border-t border-white/10"
        >
          {STATS.map((stat, i) => (
            <div key={i} className="text-center">
              <p className="text-3xl md:text-4xl font-black text-white mb-1">{stat.value}</p>
              <p className="text-white/60 text-sm">{stat.label}</p>
            </div>
          ))}
        </motion.div>
      </div>

      {/* Bottom wave */}
      <div className="absolute bottom-0 left-0 right-0">
        <svg viewBox="0 0 1440 80" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M0 80L60 70C120 60 240 40 360 35C480 30 600 40 720 50C840 60 960 70 1080 65C1200 60 1320 40 1380 30L1440 20V80H0Z" fill="white" />
        </svg>
      </div>
    </section>
  );
}
