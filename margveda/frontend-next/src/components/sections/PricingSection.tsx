"use client";

import { motion } from "framer-motion";
import Link from "next/link";
import { Check, Star } from "lucide-react";
import { cn } from "@/lib/utils";

const plans = [
  {
    name: "Explorer",
    price: "Free",
    period: "Forever",
    description: "Perfect to get started with career discovery",
    features: [
      "Basic Career Assessment",
      "3 AI Career Recommendations",
      "1 Free 30-min Consultation",
      "Access to Blog & Resources",
      "Email Support",
    ],
    cta: "Get Started Free",
    href: "/book-consultation",
    popular: false,
    color: "border-slate-200",
  },
  {
    name: "Pathfinder",
    price: "₹2,499",
    period: "/ month",
    description: "Best for serious students planning their future",
    features: [
      "Full Career Assessment Report",
      "Unlimited AI Recommendations",
      "3 Expert Counselling Sessions",
      "University Shortlisting (10+)",
      "Skill Gap Analysis",
      "Career Roadmap",
      "WhatsApp Support",
      "Priority Booking",
    ],
    cta: "Start Pathfinder",
    href: "/book-consultation",
    popular: true,
    color: "border-primary-500",
  },
  {
    name: "Achiever",
    price: "₹5,999",
    period: "/ month",
    description: "Complete guidance for premium outcomes",
    features: [
      "Everything in Pathfinder",
      "Unlimited Expert Sessions",
      "Study Abroad Consulting",
      "SOP & Application Review",
      "Interview Preparation",
      "Scholarship Guidance",
      "Dedicated Counsellor",
      "24/7 Priority Support",
    ],
    cta: "Go Achiever",
    href: "/book-consultation",
    popular: false,
    color: "border-violet-200",
  },
];

export default function PricingSection() {
  return (
    <section className="py-24 bg-slate-50">
      <div className="container-custom">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <span className="inline-block bg-primary-50 text-primary-700 text-sm font-semibold px-4 py-1.5 rounded-full mb-4">
            Pricing
          </span>
          <h2 className="section-heading text-slate-900 mb-4">
            Simple, Transparent{" "}
            <span className="text-gradient">Pricing</span>
          </h2>
          <p className="text-slate-500 max-w-xl mx-auto">
            No hidden fees. No surprise charges. Cancel anytime. Start free, upgrade when you&apos;re ready.
          </p>
        </motion.div>

        <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
          {plans.map((plan, i) => (
            <motion.div
              key={plan.name}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: i * 0.1 }}
              className={cn(
                "relative bg-white rounded-2xl border-2 p-8",
                plan.popular ? "border-primary-500 shadow-xl shadow-primary-100" : plan.color,
                "card-hover"
              )}
            >
              {plan.popular && (
                <div className="absolute -top-4 left-1/2 -translate-x-1/2">
                  <div className="bg-gradient-brand text-white text-xs font-bold px-5 py-1.5 rounded-full flex items-center gap-1.5 shadow-lg">
                    <Star size={12} className="fill-white" />
                    Most Popular
                  </div>
                </div>
              )}

              <div className="mb-6">
                <h3 className="text-xl font-bold text-slate-900 mb-1">{plan.name}</h3>
                <p className="text-slate-500 text-sm">{plan.description}</p>
              </div>

              <div className="mb-8">
                <span className="text-4xl font-black text-slate-900">{plan.price}</span>
                <span className="text-slate-400 text-sm ml-1">{plan.period}</span>
              </div>

              <ul className="space-y-3 mb-8">
                {plan.features.map((feature) => (
                  <li key={feature} className="flex items-center gap-3 text-sm text-slate-600">
                    <div className={cn(
                      "w-5 h-5 rounded-full flex items-center justify-center flex-shrink-0",
                      plan.popular ? "bg-primary-500" : "bg-slate-100"
                    )}>
                      <Check size={11} className={plan.popular ? "text-white" : "text-slate-600"} />
                    </div>
                    {feature}
                  </li>
                ))}
              </ul>

              <Link
                href={plan.href}
                className={cn(
                  "block w-full text-center font-bold text-sm py-3.5 rounded-xl transition-all",
                  plan.popular
                    ? "bg-gradient-brand text-white hover:shadow-lg hover:shadow-primary-200"
                    : "border-2 border-slate-200 text-slate-700 hover:border-primary-400 hover:text-primary-600"
                )}
              >
                {plan.cta}
              </Link>
            </motion.div>
          ))}
        </div>

        <motion.p
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          className="text-center text-slate-400 text-sm mt-8"
        >
          All plans include 7-day free trial. No credit card required to start.
        </motion.p>
      </div>
    </section>
  );
}
