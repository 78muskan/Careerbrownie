import { Building2, GraduationCap, Users, Briefcase, BarChart2, CheckCircle, ArrowRight } from "lucide-react";

const CLIENT_TYPES = [
  { icon: GraduationCap, title: "Schools", desc: "B2B career guidance for Class 8–12 students with batch analytics and parent reports", color: "bg-blue-50 text-blue-600" },
  { icon: Building2, title: "Universities", desc: "Placement readiness platform for colleges with recruiter portal integration", color: "bg-purple-50 text-purple-600" },
  { icon: Briefcase, title: "Recruiters", desc: "AI-powered candidate matching and hiring analytics across India", color: "bg-green-50 text-green-600" },
  { icon: Users, title: "Corporates", desc: "Employee career development and skill gap tracking at scale", color: "bg-orange-50 text-orange-600" },
];

const PLANS = [
  { name: "Starter", price: "₹9,999", period: "/month", users: "Up to 50 users", features: ["School/University Dashboard", "Student Analytics", "Career Reports", "Email Support"], highlighted: false },
  { name: "Growth", price: "₹24,999", period: "/month", users: "Up to 250 users", features: ["Everything in Starter", "Batch Analytics", "Parent Portal", "Recruiter Access", "Priority Support"], highlighted: true },
  { name: "Scale", price: "₹59,999", period: "/month", users: "Up to 1000 users", features: ["Everything in Growth", "AI Career Twin", "Placement Predictor", "Custom Reports", "Dedicated Manager"], highlighted: false },
];

export default function EnterprisePage() {
  return (
    <main className="min-h-screen bg-white">
      {/* Hero */}
      <section className="bg-gradient-to-br from-gray-900 via-indigo-950 to-gray-900 py-24 px-6 text-white text-center">
        <div className="max-w-3xl mx-auto">
          <div className="inline-flex items-center gap-2 bg-indigo-800/50 text-indigo-300 text-xs px-4 py-2 rounded-full mb-6">
            <Building2 className="w-3.5 h-3.5" /> Enterprise Platform
          </div>
          <h1 className="text-5xl font-bold mb-5 leading-tight">
            National Career Intelligence for <span className="text-indigo-400">Institutions</span>
          </h1>
          <p className="text-gray-300 text-lg mb-8">
            Career Brownie Enterprise powers schools, universities, and corporates with AI-driven career intelligence at scale.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <a href="/contact"
              className="bg-indigo-600 hover:bg-indigo-700 text-white px-8 py-3 rounded-xl font-medium transition flex items-center gap-2 justify-center">
              Schedule a Demo <ArrowRight className="w-4 h-4" />
            </a>
            <a href="/book-consultation"
              className="border border-gray-600 hover:border-indigo-400 text-gray-300 hover:text-white px-8 py-3 rounded-xl font-medium transition">
              Contact Sales
            </a>
          </div>
        </div>
      </section>

      {/* Client types */}
      <section className="py-20 px-6">
        <div className="max-w-5xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900">Built for Every Institution</h2>
            <p className="text-gray-500 mt-3">From individual schools to national networks</p>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {CLIENT_TYPES.map(client => (
              <div key={client.title} className="bg-white border border-gray-100 rounded-2xl p-6 hover:shadow-md transition-shadow">
                <div className={`w-12 h-12 rounded-xl ${client.color} flex items-center justify-center mb-4`}>
                  <client.icon className="w-6 h-6" />
                </div>
                <h3 className="font-semibold text-gray-900 mb-2">{client.title}</h3>
                <p className="text-sm text-gray-500 leading-relaxed">{client.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Stats */}
      <section className="bg-indigo-600 py-16 px-6 text-white">
        <div className="max-w-4xl mx-auto grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
          {[
            { value: "500+", label: "Schools Onboarded" },
            { value: "50,000+", label: "Students Guided" },
            { value: "200+", label: "Recruiting Partners" },
            { value: "94%", label: "Placement Rate" },
          ].map(stat => (
            <div key={stat.label}>
              <div className="text-4xl font-bold mb-1">{stat.value}</div>
              <div className="text-indigo-200 text-sm">{stat.label}</div>
            </div>
          ))}
        </div>
      </section>

      {/* Pricing */}
      <section className="py-20 px-6">
        <div className="max-w-5xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900">Simple, Transparent Pricing</h2>
            <p className="text-gray-500 mt-3">Annual contracts available with up to 30% discount</p>
          </div>
          <div className="grid md:grid-cols-3 gap-6">
            {PLANS.map(plan => (
              <div key={plan.name}
                className={`rounded-2xl p-8 ${plan.highlighted ? "bg-indigo-600 text-white shadow-2xl shadow-indigo-200 scale-105" : "bg-white border border-gray-100"}`}>
                <div className={`text-sm font-medium mb-1 ${plan.highlighted ? "text-indigo-200" : "text-gray-500"}`}>{plan.users}</div>
                <h3 className={`text-xl font-bold mb-2 ${plan.highlighted ? "text-white" : "text-gray-900"}`}>{plan.name}</h3>
                <div className={`mb-6 ${plan.highlighted ? "text-white" : "text-gray-900"}`}>
                  <span className="text-4xl font-bold">{plan.price}</span>
                  <span className={`text-sm ${plan.highlighted ? "text-indigo-200" : "text-gray-400"}`}>{plan.period}</span>
                </div>
                <ul className="space-y-3 mb-8">
                  {plan.features.map(f => (
                    <li key={f} className={`flex items-center gap-2 text-sm ${plan.highlighted ? "text-indigo-100" : "text-gray-600"}`}>
                      <CheckCircle className={`w-4 h-4 flex-shrink-0 ${plan.highlighted ? "text-indigo-300" : "text-green-500"}`} />
                      {f}
                    </li>
                  ))}
                </ul>
                <a href="/contact"
                  className={`block text-center py-3 rounded-xl font-medium text-sm transition ${plan.highlighted ? "bg-white text-indigo-600 hover:bg-indigo-50" : "border border-gray-200 text-gray-700 hover:bg-gray-50"}`}>
                  Get Started
                </a>
              </div>
            ))}
          </div>
          <p className="text-center text-sm text-gray-400 mt-8">
            Government institutions and NGOs eligible for 50% discount. <a href="/contact" className="text-indigo-600 hover:underline">Contact us</a>
          </p>
        </div>
      </section>

      {/* CTA */}
      <section className="bg-gray-900 py-16 px-6 text-center text-white">
        <h2 className="text-3xl font-bold mb-4">Ready to transform career outcomes at scale?</h2>
        <p className="text-gray-400 mb-8">Join 500+ institutions already using Career Brownie Enterprise</p>
        <a href="/contact"
          className="inline-flex items-center gap-2 bg-indigo-600 hover:bg-indigo-700 text-white px-8 py-3 rounded-xl font-medium transition">
          Schedule a Demo <ArrowRight className="w-4 h-4" />
        </a>
        <div className="mt-6 text-sm text-gray-500">
          <BarChart2 className="w-4 h-4 inline mr-1" />
          Average ROI for enterprise clients: 4.2× in Year 1
        </div>
      </section>
    </main>
  );
}
