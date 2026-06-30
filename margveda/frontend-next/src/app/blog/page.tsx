import type { Metadata } from "next";
import Link from "next/link";
import { ArrowRight, Clock, Tag } from "lucide-react";

export const metadata: Metadata = {
  title: "Career Guidance Blog — Career Brownie",
  description:
    "Expert articles, career tips, exam strategies, and industry insights to help Indian students and professionals navigate their career journeys.",
};

const blogPosts = [
  {
    slug: "top-careers-india-2025",
    title: "Top 20 High-Demand Careers in India for 2025",
    excerpt: "AI, climate tech, healthcare, and finance are reshaping India's job market. Here's what skills you need to be future-ready.",
    category: "Career Insights",
    readTime: "8 min",
    date: "June 8, 2026",
    featured: true,
    emoji: "📈",
  },
  {
    slug: "iit-admission-guide-2025",
    title: "Complete IIT JEE Preparation Guide: Strategy That Works",
    excerpt: "A week-by-week study plan from IIT alumni and top coaches that helped 500+ students crack JEE Advanced.",
    category: "Exam Strategy",
    readTime: "12 min",
    date: "June 5, 2026",
    featured: false,
    emoji: "🏛️",
  },
  {
    slug: "mba-or-startup",
    title: "MBA vs. Startup: What Should You Choose in 2025?",
    excerpt: "The age-old dilemma, settled. We analyzed 1,000+ career trajectories to bring you the honest answer.",
    category: "Career Decisions",
    readTime: "6 min",
    date: "June 1, 2026",
    featured: false,
    emoji: "🎯",
  },
  {
    slug: "study-abroad-scholarships-india",
    title: "15 Scholarships Indian Students Can Apply to Right Now",
    excerpt: "From Chevening to Commonwealth and DAAD — a curated list of fully-funded scholarships open for Indian students.",
    category: "Study Abroad",
    readTime: "10 min",
    date: "May 28, 2026",
    featured: false,
    emoji: "✈️",
  },
  {
    slug: "ai-jobs-india",
    title: "How to Land an AI/ML Job in India (Even Without a CS Degree)",
    excerpt: "Paths into India's booming AI industry — from certification to projects to networking. Real success stories included.",
    category: "Tech Careers",
    readTime: "9 min",
    date: "May 22, 2026",
    featured: false,
    emoji: "🤖",
  },
  {
    slug: "career-change-30s",
    title: "Is It Too Late to Change Careers in Your 30s? (No, Here's Why)",
    excerpt: "37% of India's career changers are between 28–35. The data, the strategies, and inspiring stories to get you started.",
    category: "Career Transitions",
    readTime: "7 min",
    date: "May 18, 2026",
    featured: false,
    emoji: "🔄",
  },
];

const categories = ["All", "Career Insights", "Exam Strategy", "Study Abroad", "Tech Careers", "Career Decisions", "Career Transitions"];

export default function BlogPage() {
  return (
    <div className="pt-24">
      <section className="bg-gradient-hero py-20 text-center relative overflow-hidden">
        <div className="absolute inset-0 pattern-grid opacity-20" />
        <div className="container-custom relative z-10">
          <h1 className="text-4xl md:text-5xl font-black text-white mb-4">
            Career <span className="text-transparent bg-clip-text bg-gradient-to-r from-yellow-300 to-orange-300">Intelligence</span> Blog
          </h1>
          <p className="text-white/70 max-w-xl mx-auto">
            Expert insights, exam strategies, and career guidance written by India&apos;s top counsellors and industry experts.
          </p>
        </div>
      </section>

      <section className="py-16 bg-white">
        <div className="container-custom">
          {/* Category filter */}
          <div className="flex gap-2 flex-wrap mb-12">
            {categories.map((cat) => (
              <button
                key={cat}
                className={`px-4 py-2 rounded-full text-sm font-medium transition-all ${
                  cat === "All"
                    ? "bg-primary-600 text-white"
                    : "bg-slate-100 text-slate-600 hover:bg-primary-50 hover:text-primary-600"
                }`}
              >
                {cat}
              </button>
            ))}
          </div>

          {/* Featured post */}
          <div className="mb-10">
            {blogPosts.filter((p) => p.featured).map((post) => (
              <Link key={post.slug} href={`/blog/${post.slug}`}
                className="group grid md:grid-cols-2 gap-8 bg-gradient-hero rounded-3xl p-8 md:p-10 text-white overflow-hidden relative"
              >
                <div className="absolute inset-0 pattern-grid opacity-10" />
                <div className="relative z-10">
                  <span className="inline-block bg-white/20 text-white text-xs font-semibold px-3 py-1 rounded-full mb-4">
                    Featured
                  </span>
                  <h2 className="text-2xl md:text-3xl font-black mb-3 group-hover:text-yellow-200 transition-colors">
                    {post.title}
                  </h2>
                  <p className="text-white/70 mb-5">{post.excerpt}</p>
                  <div className="flex items-center gap-4 text-sm text-white/60">
                    <span className="flex items-center gap-1.5"><Clock size={13} />{post.readTime} read</span>
                    <span>{post.date}</span>
                  </div>
                </div>
                <div className="relative z-10 flex items-center justify-center">
                  <div className="w-40 h-40 rounded-3xl bg-white/10 border border-white/20 flex items-center justify-center text-7xl">
                    {post.emoji}
                  </div>
                </div>
              </Link>
            ))}
          </div>

          {/* Grid */}
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {blogPosts.filter((p) => !p.featured).map((post) => (
              <Link
                key={post.slug}
                href={`/blog/${post.slug}`}
                className="group bg-white border border-slate-100 rounded-2xl overflow-hidden card-hover"
              >
                <div className="h-40 bg-gradient-to-br from-primary-50 to-violet-50 flex items-center justify-center text-6xl">
                  {post.emoji}
                </div>
                <div className="p-6">
                  <div className="flex items-center gap-2 mb-3">
                    <Tag size={12} className="text-primary-500" />
                    <span className="text-xs font-semibold text-primary-600">{post.category}</span>
                    <span className="text-slate-200">·</span>
                    <Clock size={12} className="text-slate-400" />
                    <span className="text-xs text-slate-400">{post.readTime}</span>
                  </div>
                  <h3 className="font-bold text-slate-900 mb-2 group-hover:text-primary-600 transition-colors line-clamp-2">
                    {post.title}
                  </h3>
                  <p className="text-slate-500 text-sm line-clamp-2 mb-4">{post.excerpt}</p>
                  <div className="flex items-center justify-between text-xs text-slate-400">
                    <span>{post.date}</span>
                    <span className="flex items-center gap-1 text-primary-600 font-semibold group-hover:gap-2 transition-all">
                      Read <ArrowRight size={12} />
                    </span>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
