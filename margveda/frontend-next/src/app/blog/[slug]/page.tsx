import type { Metadata } from "next";
import Link from "next/link";
import { ArrowLeft, Clock, Tag } from "lucide-react";

export const metadata: Metadata = {
  title: "Blog Article — MargVedA",
};

export default function BlogPostPage({ params }: { params: { slug: string } }) {
  return (
    <div className="pt-24">
      <div className="container-custom py-12 max-w-3xl">
        <Link href="/blog" className="inline-flex items-center gap-2 text-primary-600 font-semibold text-sm mb-8 hover:gap-3 transition-all">
          <ArrowLeft size={16} /> Back to Blog
        </Link>

        {/* Article header */}
        <div className="mb-10">
          <div className="flex items-center gap-3 mb-4">
            <span className="bg-primary-50 text-primary-700 text-xs font-semibold px-3 py-1 rounded-full flex items-center gap-1.5">
              <Tag size={11} /> Career Insights
            </span>
            <span className="flex items-center gap-1.5 text-slate-400 text-xs">
              <Clock size={11} /> 8 min read
            </span>
          </div>
          <h1 className="text-3xl md:text-4xl font-black text-slate-900 mb-4">
            Top 20 High-Demand Careers in India for 2025
          </h1>
          <p className="text-slate-500">Published on June 8, 2026 · By Dr. Ananya Singh, Senior Career Counsellor</p>
        </div>

        {/* Article body */}
        <div className="prose prose-slate max-w-none">
          <div className="text-6xl text-center mb-8">📈</div>
          <p className="text-lg text-slate-600 leading-relaxed mb-6">
            India&apos;s job market is transforming at an unprecedented pace. With AI, climate technology, advanced healthcare, and digital finance reshaping entire industries, the careers that were once considered stable are evolving — and entirely new opportunities are emerging.
          </p>
          <p className="text-slate-600 leading-relaxed mb-6">
            This guide, compiled by MargVedA&apos;s research team and verified by industry experts, identifies the 20 highest-demand career paths for 2025 and beyond — along with the skills you need to land them.
          </p>
          <h2 className="text-2xl font-black text-slate-900 mt-8 mb-4">1. AI & Machine Learning Engineer</h2>
          <p className="text-slate-600 leading-relaxed mb-6">
            India now has over 400,000 open AI/ML roles with an average salary of ₹18–45 LPA for experienced professionals. Skills: Python, TensorFlow/PyTorch, LLM fine-tuning, MLOps.
          </p>
          <div className="bg-primary-50 border border-primary-100 rounded-2xl p-6 my-8">
            <p className="font-bold text-primary-900 mb-2">💡 MargVedA Insight</p>
            <p className="text-primary-700 text-sm">
              Ready to explore a career in AI? Take our free career assessment to see if your aptitude and interests align with tech careers.{" "}
              <a href="/book-consultation" className="underline font-semibold">Book a free session →</a>
            </p>
          </div>
        </div>

        {/* CTA */}
        <div className="mt-12 bg-gradient-hero rounded-3xl p-8 text-white text-center">
          <h3 className="text-2xl font-black mb-3">Want Personalized Career Guidance?</h3>
          <p className="text-white/70 mb-6">Speak with an expert counsellor to map out your ideal career path.</p>
          <Link href="/book-consultation" className="bg-white text-primary-700 font-bold px-8 py-3.5 rounded-xl hover:bg-yellow-50 transition-colors">
            Book Free Consultation
          </Link>
        </div>
      </div>
    </div>
  );
}
