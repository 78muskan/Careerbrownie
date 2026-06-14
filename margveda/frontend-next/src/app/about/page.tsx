import type { Metadata } from "next";
import { Target, Eye, Heart, Users, TrendingUp, Globe2 } from "lucide-react";

export const metadata: Metadata = {
  title: "About Us — MargVedA",
  description:
    "Learn about MargVedA's mission to democratize quality career guidance for every Indian student using AI and expert human counselling.",
};

const values = [
  { icon: Target, title: "Mission-Driven", desc: "Every decision we make is guided by one goal: helping every Indian student find their ideal career path." },
  { icon: Eye, title: "Transparent", desc: "No hidden fees, no misleading advice. We give honest, data-backed guidance that truly serves your best interests." },
  { icon: Heart, title: "Student-First", desc: "We measure success by our students' success — not commissions from universities or companies." },
  { icon: Globe2, title: "Inclusive", desc: "Quality career guidance shouldn't be a luxury. We're making it accessible to every Indian student regardless of location or background." },
];

const team = [
  { name: "Aryan Kapoor", role: "Founder & CEO", bio: "IIT Bombay alum. Former McKinsey consultant. Obsessed with democratizing career intelligence.", emoji: "👨‍💼" },
  { name: "Dr. Meera Pillai", role: "Head of Counselling", bio: "PhD in Educational Psychology. 18 years guiding students across India. Certified career coach.", emoji: "👩‍🏫" },
  { name: "Rohan Gupta", role: "CTO & AI Lead", bio: "IIT Delhi + Stanford MS. Built AI systems at Google. Leading MargVedA's career intelligence engine.", emoji: "👨‍💻" },
  { name: "Priya Sharma", role: "Head of University Relations", bio: "Former admissions officer at top institutions. Deep relationships with 500+ universities globally.", emoji: "👩‍🎓" },
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
            MargVedA was born from a simple observation: millions of talented Indian students make career decisions without proper guidance, often based on peer pressure or parental expectations. We&apos;re changing that.
          </p>
        </div>
      </section>

      {/* Stats */}
      <section className="py-16 bg-white border-b border-slate-100">
        <div className="container-custom">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
            {[
              { value: "50,000+", label: "Students Guided" },
              { value: "200+", label: "Expert Counsellors" },
              { value: "500+", label: "University Partners" },
              { value: "4.9★", label: "Average Rating" },
            ].map((s) => (
              <div key={s.label}>
                <p className="text-4xl font-black text-gradient mb-2">{s.value}</p>
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
                  Over <strong>93% of Indian students</strong> lack access to professional career guidance. Most rely on family advice, peer pressure, or random internet searches to make decisions that will shape their entire lives.
                </p>
                <p>
                  The result? <strong>40% of engineering graduates</strong> end up in roles unrelated to their degree. <strong>67% of professionals</strong> regret their career choices by age 30. Countless talented individuals are stuck in wrong careers because no one showed them a better path.
                </p>
                <p>
                  We founded MargVedA in 2022 to fix this. By combining cutting-edge AI with expert human counselling, we&apos;ve created a platform that makes world-class career guidance affordable and accessible to every Indian.
                </p>
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              {[
                { stat: "93%", desc: "Students lack proper career guidance", color: "bg-red-50 border-red-100" },
                { stat: "40%", desc: "Engineering grads in wrong jobs", color: "bg-orange-50 border-orange-100" },
                { stat: "₹2L+", desc: "Avg. salary increase after guidance", color: "bg-emerald-50 border-emerald-100" },
                { stat: "95%", desc: "Students satisfied with MargVedA", color: "bg-primary-50 border-primary-100" },
              ].map((item) => (
                <div key={item.stat} className={`${item.color} border rounded-2xl p-6 text-center`}>
                  <p className="text-3xl font-black text-slate-900 mb-2">{item.stat}</p>
                  <p className="text-sm text-slate-600">{item.desc}</p>
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
              A team of educators, technologists, and career professionals united by a shared mission.
            </p>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {team.map((member) => (
              <div key={member.name} className="bg-white border border-slate-100 rounded-2xl p-6 card-hover text-center">
                <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-primary-100 to-violet-100 flex items-center justify-center mx-auto mb-4 text-3xl">
                  {member.emoji}
                </div>
                <h3 className="font-bold text-slate-900">{member.name}</h3>
                <p className="text-primary-600 text-sm font-medium mb-3">{member.role}</p>
                <p className="text-slate-500 text-xs leading-relaxed">{member.bio}</p>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
