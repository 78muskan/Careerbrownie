"use client";

import Link from "next/link";
import { ArrowRight, Zap, Brain, Target, BookOpen, TrendingUp, Award } from "lucide-react";
import { useState } from "react";
import dynamic from "next/dynamic";

const ChatWidget = dynamic(() => import("@/components/chat/ChatWidget"), { ssr: false });

const FEATURES = [
  { icon: Brain, text: "Analyze your academic background and generate career recommendations" },
  { icon: Zap, text: "Answer any career question instantly — no waiting, no scheduling" },
  { icon: Target, text: "Generate detailed skill gap reports and learning roadmaps" },
  { icon: TrendingUp, text: "Compare career options based on your priorities (salary, growth, lifestyle)" },
  { icon: BookOpen, text: "Help you prepare for job interviews with mock Q&A sessions" },
  { icon: Award, text: "Track your progress and update recommendations as you grow" },
];

export default function AiCareerGuidancePage() {
  const [chatOpen, setChatOpen] = useState(false);

  return (
    <div className="pt-24">
      {/* Hero */}
      <section className="bg-gradient-hero py-24 relative overflow-hidden">
        <div className="absolute inset-0 pattern-grid opacity-20" />
        <div className="absolute top-1/3 right-1/4 w-96 h-96 bg-violet-500/20 rounded-full blur-3xl" />
        <div className="container-custom relative z-10 max-w-2xl">
          <span className="inline-block bg-white/10 text-white text-sm font-semibold px-4 py-1.5 rounded-full mb-5">
            🤖 AI Career Guidance
          </span>
          <h1 className="text-4xl md:text-5xl font-black text-white mb-6">
            India&apos;s Most Advanced AI Career Counsellor
          </h1>
          <p className="text-white/70 text-lg mb-8">
            Available 24/7. Never judges. Endlessly patient. Ask anything about careers,
            colleges, exams, or salaries — and get an honest, personalized answer.
          </p>
          <div className="flex gap-4 flex-wrap">
            <button
              onClick={() => setChatOpen(true)}
              className="btn-primary inline-flex items-center gap-2"
            >
              Try AI Counsellor Now <ArrowRight size={18} />
            </button>
            <Link
              href="/book-consultation"
              className="border-2 border-white/30 text-white font-semibold px-6 py-3 rounded-xl hover:bg-white/10 transition-colors"
            >
              Book Human Expert
            </Link>
          </div>
        </div>
      </section>

      {/* Features + Live Demo */}
      <section className="py-24 bg-white">
        <div className="container-custom">
          <div className="grid lg:grid-cols-2 gap-16 items-center mb-16">
            {/* Feature list */}
            <div>
              <h2 className="text-3xl font-black text-slate-900 mb-6">What the AI Can Do</h2>
              <div className="space-y-4">
                {FEATURES.map(({ icon: Icon, text }, i) => (
                  <div key={i} className="flex items-start gap-3">
                    <div className="w-8 h-8 rounded-xl bg-violet-100 flex items-center justify-center flex-shrink-0 mt-0.5">
                      <Icon className="w-4 h-4 text-violet-600" />
                    </div>
                    <span className="text-slate-600 text-sm leading-relaxed">{text}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Demo chat preview card */}
            <div className="bg-slate-900 rounded-3xl p-8 text-white relative">
              <div className="space-y-4">
                <div className="flex gap-3">
                  <div className="w-8 h-8 rounded-full bg-primary-500 flex items-center justify-center text-sm font-bold flex-shrink-0">
                    U
                  </div>
                  <div className="bg-slate-800 rounded-2xl rounded-tl-none px-4 py-3 text-sm text-slate-300">
                    I&apos;m in Class 12 PCM and confused between engineering and data science. What
                    should I choose?
                  </div>
                </div>
                <div className="flex gap-3 flex-row-reverse">
                  <div className="w-8 h-8 rounded-full bg-gradient-to-br from-violet-500 to-purple-600 flex items-center justify-center text-sm font-bold flex-shrink-0">
                    AI
                  </div>
                  <div className="bg-violet-900/50 border border-violet-700/30 rounded-2xl rounded-tr-none px-4 py-3 text-sm text-slate-200 max-w-xs">
                    Great question! Both are excellent paths in 2025. Do you prefer building systems
                    (engineering) or extracting insights from data? Your answer will tell us a lot
                    about which direction fits your personality better...
                  </div>
                </div>
              </div>
              <div className="mt-6 pt-4 border-t border-slate-700">
                <p className="text-slate-400 text-xs text-center mb-4">
                  Powered by local AI · Available 24/7 · 100% Private
                </p>
                <button
                  onClick={() => setChatOpen(true)}
                  className="w-full bg-violet-600 hover:bg-violet-700 text-white font-semibold py-3 rounded-xl transition-colors flex items-center justify-center gap-2 text-sm"
                >
                  Start Your Conversation <ArrowRight size={16} />
                </button>
              </div>
            </div>
          </div>

          {/* Bottom CTA */}
          <div className="text-center bg-gradient-to-br from-violet-50 to-purple-50 rounded-3xl p-12 border border-violet-100">
            <h3 className="text-2xl font-black text-slate-900 mb-3">
              Ready to find your perfect career path?
            </h3>
            <p className="text-slate-600 mb-6 max-w-md mx-auto">
              Chat with our AI for free. No sign-up needed.
            </p>
            <button
              onClick={() => setChatOpen(true)}
              className="btn-primary inline-flex items-center gap-2"
            >
              Start AI Career Chat <ArrowRight size={18} />
            </button>
          </div>
        </div>
      </section>

      <ChatWidget open={chatOpen} onClose={() => setChatOpen(false)} />
    </div>
  );
}
