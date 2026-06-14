"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { CheckCircle2, Calendar, Clock, User, Phone, Mail, BookOpen } from "lucide-react";
import { API_BASE_URL } from "@/lib/constants";

const services = [
  "Career Counselling",
  "University Admissions",
  "Study Abroad",
  "Career Intelligence Report",
  "AI Career Guidance",
  "Skill Gap Analysis",
];

const timeSlots = [
  "9:00 AM", "10:00 AM", "11:00 AM",
  "12:00 PM", "2:00 PM", "3:00 PM",
  "4:00 PM", "5:00 PM", "6:00 PM",
];

export default function BookConsultationPage() {
  const [step, setStep] = useState(1);
  const [form, setForm] = useState({
    name: "", email: "", phone: "", grade: "",
    service: "", preferred_date: "", preferred_time: "", message: "",
  });
  const [submitted, setSubmitted] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      await fetch(`${API_BASE_URL}/leads/consultation/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ...form, source: "book_consultation" }),
      });
    } catch {
      // silent
    } finally {
      setLoading(false);
      setSubmitted(true);
    }
  };

  if (submitted) {
    return (
      <div className="pt-24 min-h-screen bg-slate-50 flex items-center justify-center">
        <motion.div
          initial={{ scale: 0.8, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          className="bg-white rounded-3xl p-12 text-center max-w-md shadow-xl"
        >
          <div className="w-20 h-20 rounded-full bg-emerald-100 flex items-center justify-center mx-auto mb-5">
            <CheckCircle2 size={40} className="text-emerald-500" />
          </div>
          <h2 className="text-2xl font-black text-slate-900 mb-3">Consultation Booked!</h2>
          <p className="text-slate-500 mb-6 leading-relaxed">
            Your free consultation has been scheduled. Our team will confirm your booking via email and WhatsApp within 2 hours.
          </p>
          <div className="bg-primary-50 border border-primary-100 rounded-xl p-4 text-sm text-primary-700 mb-6">
            <strong>What&apos;s next?</strong> You&apos;ll receive a confirmation email with a calendar invite and the video call link.
          </div>
          <a href="/" className="btn-primary">
            Back to Home
          </a>
        </motion.div>
      </div>
    );
  }

  return (
    <div className="pt-24 bg-slate-50 min-h-screen">
      {/* Header */}
      <section className="bg-gradient-hero py-16 text-center relative overflow-hidden">
        <div className="absolute inset-0 pattern-grid opacity-20" />
        <div className="container-custom relative z-10">
          <div className="inline-flex items-center gap-2 bg-emerald-400/20 text-emerald-300 border border-emerald-400/30 rounded-full px-4 py-1.5 mb-4 text-sm font-semibold">
            ✨ 100% Free — No Credit Card Required
          </div>
          <h1 className="text-4xl md:text-5xl font-black text-white mb-4">
            Book Your Free <span className="text-transparent bg-clip-text bg-gradient-to-r from-yellow-300 to-orange-300">Career Consultation</span>
          </h1>
          <p className="text-white/70 max-w-lg mx-auto">
            30 minutes with an expert counsellor. No sales pitch. Just honest, actionable career advice tailored to you.
          </p>
        </div>
      </section>

      <section className="py-16">
        <div className="container-custom">
          <div className="grid lg:grid-cols-3 gap-10">
            {/* Benefits sidebar */}
            <div className="lg:col-span-1">
              <div className="bg-white rounded-2xl p-7 border border-slate-100 sticky top-28">
                <h3 className="font-black text-slate-900 text-lg mb-5">What You Get in Your Free Session</h3>
                <ul className="space-y-4">
                  {[
                    { icon: "🎯", text: "Personalized career path analysis" },
                    { icon: "📊", text: "AI-generated profile report" },
                    { icon: "🏫", text: "Top 5 university recommendations" },
                    { icon: "📋", text: "Actionable 30-day roadmap" },
                    { icon: "💬", text: "Q&A with an expert counsellor" },
                  ].map((item) => (
                    <li key={item.text} className="flex items-start gap-3">
                      <span className="text-xl">{item.icon}</span>
                      <span className="text-sm text-slate-600">{item.text}</span>
                    </li>
                  ))}
                </ul>
                <div className="mt-6 pt-5 border-t border-slate-100 text-center">
                  <p className="text-2xl font-black text-slate-900 mb-1">
                    <span className="line-through text-slate-300 text-lg mr-2">₹2,999</span>
                    <span className="text-gradient">FREE</span>
                  </p>
                  <p className="text-slate-400 text-xs">Limited slots available daily</p>
                </div>
              </div>
            </div>

            {/* Form */}
            <div className="lg:col-span-2">
              <form onSubmit={handleSubmit} className="bg-white rounded-2xl border border-slate-100 p-8 space-y-6">
                <h2 className="text-xl font-black text-slate-900">Fill in Your Details</h2>

                <div className="grid sm:grid-cols-2 gap-5">
                  <div>
                    <label className="block text-sm font-semibold text-slate-700 mb-1.5">Full Name *</label>
                    <div className="relative">
                      <User size={16} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
                      <input
                        name="name" value={form.name} onChange={handleChange}
                        required placeholder="Your full name"
                        className="w-full pl-10 border border-slate-200 rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary-300"
                      />
                    </div>
                  </div>
                  <div>
                    <label className="block text-sm font-semibold text-slate-700 mb-1.5">Email Address *</label>
                    <div className="relative">
                      <Mail size={16} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
                      <input
                        name="email" type="email" value={form.email} onChange={handleChange}
                        required placeholder="your@email.com"
                        className="w-full pl-10 border border-slate-200 rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary-300"
                      />
                    </div>
                  </div>
                  <div>
                    <label className="block text-sm font-semibold text-slate-700 mb-1.5">Phone Number *</label>
                    <div className="relative">
                      <Phone size={16} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
                      <input
                        name="phone" value={form.phone} onChange={handleChange}
                        required placeholder="+91 98765 43210"
                        className="w-full pl-10 border border-slate-200 rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary-300"
                      />
                    </div>
                  </div>
                  <div>
                    <label className="block text-sm font-semibold text-slate-700 mb-1.5">Current Grade/Status *</label>
                    <select
                      name="grade" value={form.grade} onChange={handleChange} required
                      className="w-full border border-slate-200 rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary-300 bg-white"
                    >
                      <option value="">Select your status</option>
                      <option>Class 9–10</option>
                      <option>Class 11–12</option>
                      <option>1st/2nd Year College</option>
                      <option>3rd/4th Year College</option>
                      <option>Recent Graduate</option>
                      <option>Working Professional (1–3 years)</option>
                      <option>Working Professional (3+ years)</option>
                      <option>Parent (for child)</option>
                    </select>
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-semibold text-slate-700 mb-2">What do you need help with? *</label>
                  <div className="grid sm:grid-cols-3 gap-3">
                    {services.map((s) => (
                      <label
                        key={s}
                        className={`flex items-center gap-2.5 border rounded-xl p-3 cursor-pointer transition-all text-sm ${
                          form.service === s
                            ? "border-primary-400 bg-primary-50 text-primary-700"
                            : "border-slate-200 hover:border-slate-300 text-slate-600"
                        }`}
                      >
                        <input
                          type="radio" name="service" value={s}
                          checked={form.service === s}
                          onChange={handleChange}
                          className="sr-only"
                        />
                        <span className={`w-4 h-4 rounded-full border-2 flex-shrink-0 ${
                          form.service === s ? "border-primary-500 bg-primary-500" : "border-slate-300"
                        }`} />
                        {s}
                      </label>
                    ))}
                  </div>
                </div>

                <div className="grid sm:grid-cols-2 gap-5">
                  <div>
                    <label className="block text-sm font-semibold text-slate-700 mb-1.5">Preferred Date *</label>
                    <div className="relative">
                      <Calendar size={16} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
                      <input
                        name="preferred_date" type="date" value={form.preferred_date} onChange={handleChange}
                        required min={new Date().toISOString().split("T")[0]}
                        className="w-full pl-10 border border-slate-200 rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary-300"
                      />
                    </div>
                  </div>
                  <div>
                    <label className="block text-sm font-semibold text-slate-700 mb-1.5">Preferred Time *</label>
                    <div className="relative">
                      <Clock size={16} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
                      <select
                        name="preferred_time" value={form.preferred_time} onChange={handleChange} required
                        className="w-full pl-10 border border-slate-200 rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary-300 bg-white"
                      >
                        <option value="">Select time slot</option>
                        {timeSlots.map((t) => (
                          <option key={t}>{t} IST</option>
                        ))}
                      </select>
                    </div>
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-semibold text-slate-700 mb-1.5">
                    Brief about your situation (optional)
                  </label>
                  <div className="relative">
                    <BookOpen size={16} className="absolute left-3.5 top-3.5 text-slate-400" />
                    <textarea
                      name="message" value={form.message} onChange={handleChange}
                      rows={3} placeholder="Tell us a bit about your current situation and what you're hoping to achieve..."
                      className="w-full pl-10 border border-slate-200 rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary-300 resize-none"
                    />
                  </div>
                </div>

                <button
                  type="submit"
                  disabled={loading}
                  className="w-full btn-primary text-base py-4 flex items-center justify-center gap-2 disabled:opacity-60"
                >
                  {loading ? "Booking..." : "Book My Free Consultation →"}
                </button>

                <p className="text-xs text-center text-slate-400">
                  By submitting, you agree to our{" "}
                  <a href="/privacy-policy" className="text-primary-600 underline">Privacy Policy</a>.
                  We never share your data.
                </p>
              </form>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
