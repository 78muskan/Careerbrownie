"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { ChevronDown } from "lucide-react";
import { FAQS } from "@/lib/constants";
import { cn } from "@/lib/utils";

export default function FAQSection() {
  const [openIdx, setOpenIdx] = useState<number | null>(0);

  return (
    <section className="py-24 bg-white">
      <div className="container-custom">
        <div className="grid lg:grid-cols-2 gap-16 items-start">
          {/* Left */}
          <motion.div
            initial={{ opacity: 0, x: -30 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            <span className="inline-block bg-primary-50 text-primary-700 text-sm font-semibold px-4 py-1.5 rounded-full mb-4">
              FAQ
            </span>
            <h2 className="section-heading text-slate-900 mb-6">
              Frequently Asked{" "}
              <span className="text-gradient">Questions</span>
            </h2>
            <p className="text-slate-500 mb-8 leading-relaxed">
              Got questions about career guidance, our platform, or how we can help you? We&apos;ve got you covered. Don&apos;t find your answer here? Chat with us on WhatsApp.
            </p>
            <div className="bg-primary-50 rounded-2xl p-6 border border-primary-100">
              <p className="text-sm font-semibold text-primary-800 mb-1">Still have questions?</p>
              <p className="text-sm text-primary-600 mb-4">Our team is available Mon-Sat, 9 AM – 7 PM IST</p>
              <a
                href="/contact"
                className="inline-flex items-center gap-2 bg-gradient-brand text-white text-sm font-semibold px-5 py-2.5 rounded-lg"
              >
                Contact Us
              </a>
            </div>
          </motion.div>

          {/* Right - accordion */}
          <motion.div
            initial={{ opacity: 0, x: 30 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="space-y-3"
          >
            {FAQS.map((faq, i) => (
              <div
                key={i}
                className={cn(
                  "border rounded-xl overflow-hidden transition-colors",
                  openIdx === i ? "border-primary-200 bg-primary-50" : "border-slate-100 bg-white hover:border-slate-200"
                )}
              >
                <button
                  onClick={() => setOpenIdx(openIdx === i ? null : i)}
                  className="w-full flex items-center justify-between gap-4 p-5 text-left"
                >
                  <span className={cn(
                    "text-sm font-semibold leading-snug",
                    openIdx === i ? "text-primary-700" : "text-slate-900"
                  )}>
                    {faq.q}
                  </span>
                  <ChevronDown
                    size={18}
                    className={cn(
                      "flex-shrink-0 transition-transform duration-300",
                      openIdx === i ? "rotate-180 text-primary-600" : "text-slate-400"
                    )}
                  />
                </button>

                <AnimatePresence initial={false}>
                  {openIdx === i && (
                    <motion.div
                      initial={{ height: 0 }}
                      animate={{ height: "auto" }}
                      exit={{ height: 0 }}
                      transition={{ duration: 0.25 }}
                      className="overflow-hidden"
                    >
                      <p className="px-5 pb-5 text-sm text-slate-600 leading-relaxed">
                        {faq.a}
                      </p>
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
            ))}
          </motion.div>
        </div>
      </div>
    </section>
  );
}
