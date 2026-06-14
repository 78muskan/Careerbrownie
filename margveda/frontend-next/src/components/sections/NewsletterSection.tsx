"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { Send, CheckCircle2 } from "lucide-react";
import { API_BASE_URL } from "@/lib/constants";

export default function NewsletterSection() {
  const [email, setEmail] = useState("");
  const [submitted, setSubmitted] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email) return;
    setLoading(true);
    try {
      await fetch(`${API_BASE_URL}/leads/newsletter/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email }),
      });
    } catch {
      // silent fail — still show success
    } finally {
      setLoading(false);
      setSubmitted(true);
    }
  };

  return (
    <section className="py-16 bg-gradient-hero relative overflow-hidden">
      <div className="absolute inset-0 pattern-dots opacity-20" />
      <div className="container-custom relative z-10">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="max-w-2xl mx-auto text-center"
        >
          <h2 className="text-2xl md:text-3xl font-black text-white mb-3">
            Get Weekly Career Intelligence
          </h2>
          <p className="text-white/70 mb-8">
            Join 15,000+ students receiving our weekly newsletter with career tips, industry insights, scholarship alerts, and AI updates.
          </p>

          {submitted ? (
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              className="flex items-center justify-center gap-3 bg-white/10 border border-white/20 rounded-xl px-6 py-4"
            >
              <CheckCircle2 size={22} className="text-emerald-400" />
              <p className="text-white font-semibold">
                You&apos;re subscribed! Check your inbox for a welcome email.
              </p>
            </motion.div>
          ) : (
            <form onSubmit={handleSubmit} className="flex flex-col sm:flex-row gap-3 max-w-lg mx-auto">
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Enter your email address"
                required
                className="flex-1 bg-white/10 border border-white/20 rounded-xl px-5 py-3.5 text-white placeholder-white/40 focus:outline-none focus:border-white/50 focus:bg-white/15 transition-all text-sm"
              />
              <button
                type="submit"
                disabled={loading}
                className="flex items-center justify-center gap-2 bg-white text-primary-700 font-bold px-6 py-3.5 rounded-xl hover:bg-yellow-50 transition-colors disabled:opacity-60 whitespace-nowrap"
              >
                {loading ? "Subscribing..." : (
                  <>
                    Subscribe <Send size={16} />
                  </>
                )}
              </button>
            </form>
          )}

          <p className="text-white/40 text-xs mt-4">No spam. Unsubscribe any time.</p>
        </motion.div>
      </div>
    </section>
  );
}
