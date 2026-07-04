"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { Phone, Mail, MapPin, Clock, Send, CheckCircle2 } from "lucide-react";
import { CONTACT_EMAIL, CONTACT_PHONE, API_BASE_URL } from "@/lib/constants";

export default function ContactPage() {
  const [form, setForm] = useState({ name: "", email: "", phone: "", subject: "", message: "" });
  const [submitted, setSubmitted] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      await fetch(`${API_BASE_URL}/leads/contact/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ...form, source: "contact_page" }),
      });
    } catch {
      // silent fail
    } finally {
      setLoading(false);
      setSubmitted(true);
    }
  };

  return (
    <div className="pt-24">
      {/* Header */}
      <section className="bg-gradient-hero py-20 text-center relative overflow-hidden">
        <div className="absolute inset-0 pattern-grid opacity-20" />
        <div className="container-custom relative z-10">
          <h1 className="text-4xl md:text-5xl font-black text-white mb-4">
            Get in <span className="text-transparent bg-clip-text bg-gradient-to-r from-yellow-300 to-orange-300">Touch</span>
          </h1>
          <p className="text-white/70 max-w-xl mx-auto">
            Have questions? Our team is here to help. Reach out and we&apos;ll respond within 2 hours on business days.
          </p>
        </div>
      </section>

      <section className="py-24 bg-white">
        <div className="container-custom">
          <div className="grid lg:grid-cols-3 gap-12">
            {/* Contact info */}
            <div className="lg:col-span-1">
              <h2 className="text-2xl font-black text-slate-900 mb-6">Contact Information</h2>
              <div className="space-y-5 mb-8">
                {[
                  { icon: Phone, label: "Phone", value: CONTACT_PHONE, href: `tel:${CONTACT_PHONE.replace(/\s/g, "")}` },
                  { icon: Mail, label: "Email", value: CONTACT_EMAIL, href: `mailto:${CONTACT_EMAIL}` },
                  { icon: MapPin, label: "Location", value: "India 🇮🇳 — Remote-first", href: "#" },
                  { icon: Clock, label: "Hours", value: "Mon–Sat: 9 AM – 7 PM IST", href: "#" },
                ].map((item) => {
                  const Icon = item.icon;
                  return (
                    <a key={item.label} href={item.href} className="flex items-start gap-4 group">
                      <div className="w-10 h-10 rounded-xl bg-primary-50 flex items-center justify-center flex-shrink-0 group-hover:bg-primary-100 transition-colors">
                        <Icon size={18} className="text-primary-600" />
                      </div>
                      <div>
                        <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider">{item.label}</p>
                        <p className="text-sm text-slate-700 font-medium">{item.value}</p>
                      </div>
                    </a>
                  );
                })}
              </div>

              <div className="bg-primary-50 border border-primary-100 rounded-2xl p-6">
                <h3 className="font-bold text-primary-900 mb-2">Quick Response Guarantee</h3>
                <p className="text-primary-700 text-sm leading-relaxed">
                  We respond to all inquiries within <strong>2 business hours</strong>. For urgent queries, WhatsApp us directly for an instant response.
                </p>
                <a
                  href={`https://wa.me/919876543210?text=${encodeURIComponent("Hi! I need help with career guidance.")}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="mt-4 inline-flex items-center gap-2 bg-[#25d366] text-white text-sm font-bold px-5 py-2.5 rounded-xl"
                >
                  💬 WhatsApp Us
                </a>
              </div>
            </div>

            {/* Form */}
            <div className="lg:col-span-2">
              {submitted ? (
                <motion.div
                  initial={{ scale: 0.9, opacity: 0 }}
                  animate={{ scale: 1, opacity: 1 }}
                  className="h-full flex items-center justify-center text-center py-20"
                >
                  <div>
                    <CheckCircle2 size={60} className="text-emerald-500 mx-auto mb-4" />
                    <h3 className="text-2xl font-black text-slate-900 mb-2">Message Sent!</h3>
                    <p className="text-slate-500">
                      Thank you for reaching out. We&apos;ll get back to you within 2 business hours.
                    </p>
                  </div>
                </motion.div>
              ) : (
                <form onSubmit={handleSubmit} className="space-y-5">
                  <div className="grid sm:grid-cols-2 gap-5">
                    <div>
                      <label className="block text-sm font-semibold text-slate-700 mb-1.5">Full Name *</label>
                      <input
                        name="name"
                        value={form.name}
                        onChange={handleChange}
                        required
                        placeholder="Arjun Sharma"
                        className="w-full border border-slate-200 rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary-300 focus:border-primary-400 transition-all"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-semibold text-slate-700 mb-1.5">Email Address *</label>
                      <input
                        name="email"
                        type="email"
                        value={form.email}
                        onChange={handleChange}
                        required
                        placeholder="arjun@example.com"
                        className="w-full border border-slate-200 rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary-300 focus:border-primary-400 transition-all"
                      />
                    </div>
                  </div>
                  <div className="grid sm:grid-cols-2 gap-5">
                    <div>
                      <label className="block text-sm font-semibold text-slate-700 mb-1.5">Phone Number</label>
                      <input
                        name="phone"
                        value={form.phone}
                        onChange={handleChange}
                        placeholder="+91 98765 43210"
                        className="w-full border border-slate-200 rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary-300 focus:border-primary-400 transition-all"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-semibold text-slate-700 mb-1.5">Subject *</label>
                      <select
                        name="subject"
                        value={form.subject}
                        onChange={handleChange}
                        required
                        className="w-full border border-slate-200 rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary-300 focus:border-primary-400 transition-all bg-white"
                      >
                        <option value="">Select a topic</option>
                        <option>Career Counselling Inquiry</option>
                        <option>University Admissions Help</option>
                        <option>Study Abroad Support</option>
                        <option>Pricing & Plans</option>
                        <option>Partnership Inquiry</option>
                        <option>Technical Support</option>
                        <option>Other</option>
                      </select>
                    </div>
                  </div>
                  <div>
                    <label className="block text-sm font-semibold text-slate-700 mb-1.5">Message *</label>
                    <textarea
                      name="message"
                      value={form.message}
                      onChange={handleChange}
                      required
                      rows={5}
                      placeholder="Tell us how we can help you..."
                      className="w-full border border-slate-200 rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary-300 focus:border-primary-400 transition-all resize-none"
                    />
                  </div>
                  <button
                    type="submit"
                    disabled={loading}
                    className="btn-primary flex items-center gap-2 disabled:opacity-60"
                  >
                    {loading ? "Sending..." : (
                      <>
                        Send Message <Send size={16} />
                      </>
                    )}
                  </button>
                </form>
              )}
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
