import type { Metadata } from "next";
import { Target, Eye, Heart, Users, TrendingUp, Globe2 } from "lucide-react";

export const metadata: Metadata = {
  title: "About Us — Career Brownie",
  description:
    "Learn about Career Brownie's mission to democratize quality career guidance for every Indian student using AI and expert human counselling.",
};

const values = [
  { icon: Target, title: "Mission-Driven", desc: "Every decision we make is guided by one goal: helping every Indian student find their ideal career path." },
  { icon: Eye, title: "Transparent", desc: "No hidden fees, no misleading advice. We give honest, data-backed guidance that truly serves your best interests." },
  { icon: Heart, title: "Student-First", desc: "We measure success by our students' success — not commissions from universities or companies." },
  { icon: Globe2, title: "Inclusive", desc: "Quality career guidance shouldn't be a luxury. We're making it accessible to every Indian student regardless of location or background." },
];

const team = [
  { name: "Muskan Sahani", role: "Founder & CEO", bio: "Founder of CareerBrownie. On a mission to make world-class career guidance accessible to every Indian student, regardless of background or location.", emoji: "👩‍💼" },
];

export default function AboutPage() {
  return (
    <div className="pt-24">
      {/* Hero */}
      <section className="bg-gradient-hero py-24 relative overflow-hidden">
        <div className="absolute inset-0 pattern-grid opacity-20" />
        <div className="container-custom relative z-10 text-center">
          <span className="inline-block bg-white/10 text-white text-sm font-semibold px-4 py-1.5 rounded-full mb-5">
            Our Story
          </span>
          <h1 className="text-4xl md:text-6xl font-black text-white mb-6">
            We&apos;re on a Mission to{" "}
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-yellow-300 to-orange-300">
              Transform Career Guidance
            </span>{" "}
            in India
          </h1>
          <p className="text-white/70 max-w-2xl mx-auto text-lg leading-relaxed">
            Career Brownie was born from a simple observation: millions of talented Indian students make career decisions without proper guidance, often based on peer pressure or parental expectations. We&apos;re changing that.
          </p>
        </div>
      </section>

      {/* Mission pillars */}
      <section className="py-16 bg-white border-b border-slate-100">
        <div className="container-custom">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
            {[
              { value: "AI + Human", label: "Guidance Approach" },
              { value: "Free", label: "First Consultation" },
              { value: "Class 9–12+", label: "For All Students" },
              { value: "2026", label: "Founded in India" },
            ].map((s) => (
              <div key={s.label}>
                <p className="text-3xl font-black text-gradient mb-2">{s.value}</p>
                <p className="text-slate-500 text-sm font-medium">{s.label}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Story */}
      <section className="py-24 bg-white">
        <div className="container-custom">
          <div className="grid lg:grid-cols-2 gap-16 items-center">
            <div>
              <span className="inline-block bg-primary-50 text-primary-700 text-sm font-semibold px-4 py-1.5 rounded-full mb-4">
                The Problem We Solve
              </span>
              <h2 className="text-3xl md:text-4xl font-black text-slate-900 mb-6">
                India&apos;s Career Guidance Gap is Real
              </h2>
              <div className="space-y-4 text-slate-600 leading-relaxed">
                <p>
                  Many students across India make career decisions without access to structured guidance — relying on family advice, peer pressure, or internet searches for choices that will shape their entire lives.
                </p>
                <p>
                  The result is a significant mismatch between education and career outcomes. Talented individuals end up in roles they didn&apos;t choose intentionally, often discovering their real interests only years later — when changing course is harder.
                </p>
                <p>
                  We founded CareerBrownie in 2026 to fix this. By combining AI with expert human counselling, we&apos;re building a platform that makes quality career guidance accessible to every Indian student, regardless of location or background.
                </p>
              </div>
            </div>
            <div className="grid grid-cols-1 gap-4">
              {[
                { icon: "🎯", desc: "Personalized guidance based on your actual strengths and interests", color: "bg-primary-50 border-primary-100" },
                { icon: "🤖", desc: "AI-powered insights combined with experienced human counsellors", color: "bg-violet-50 border-violet-100" },
                { icon: "💡", desc: "Real career data — salaries, job markets, college admissions, and more", color: "bg-emerald-50 border-emerald-100" },
                { icon: "🆓", desc: "Start with a free consultation — no pressure, no commitment", color: "bg-amber-50 border-amber-100" },
              ].map((item) => (
                <div key={item.icon} className={`${item.color} border rounded-2xl px-5 py-4 flex items-start gap-4`}>
                  <span className="text-2xl mt-0.5">{item.icon}</span>
                  <p className="text-sm text-slate-700 leading-relaxed">{item.desc}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Values */}
      <section className="py-24 bg-slate-50">
        <div className="container-custom">
          <div className="text-center mb-16">
            <h2 className="section-heading text-slate-900 mb-4">
              Our Core <span className="text-gradient">Values</span>
            </h2>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {values.map((v) => {
              const Icon = v.icon;
              return (
                <div key={v.title} className="bg-white rounded-2xl p-7 border border-slate-100 text-center card-hover">
                  <div className="w-12 h-12 rounded-2xl bg-gradient-brand flex items-center justify-center mx-auto mb-4">
                    <Icon size={22} className="text-white" />
                  </div>
                  <h3 className="font-bold text-slate-900 mb-2">{v.title}</h3>
                  <p className="text-slate-500 text-sm leading-relaxed">{v.desc}</p>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Team */}
      <section className="py-24 bg-white">
        <div className="container-custom">
          <div className="text-center mb-16">
            <h2 className="section-heading text-slate-900 mb-4">
              Meet the <span className="text-gradient">Team</span>
            </h2>
            <p className="text-slate-500 max-w-xl mx-auto">
              CareerBrownie is founder-led. We&apos;re growing — advisors and team members will be listed here as we bring them on board.
            </p>
          </div>
          <div className="max-w-sm mx-auto">
            {team.map((member) => (
              <div key={member.name} className="bg-white border border-slate-100 rounded-2xl p-8 card-hover text-center">
                <div className="w-20 h-20 rounded-2xl bg-gradient-to-br from-primary-100 to-violet-100 flex items-center justify-center mx-auto mb-5 text-4xl">
                  {member.emoji}
                </div>
                <h3 className="font-bold text-slate-900 text-lg">{member.name}</h3>
                <p className="text-primary-600 text-sm font-medium mb-3">{member.role}</p>
                <p className="text-slate-500 text-sm leading-relaxed">{member.bio}</p>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
