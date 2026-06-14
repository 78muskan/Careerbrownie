import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Refund Policy — MargVedA",
};

export default function RefundPolicyPage() {
  return (
    <div className="pt-24 bg-white">
      <section className="bg-gradient-hero py-16 text-center relative overflow-hidden">
        <div className="absolute inset-0 pattern-grid opacity-20" />
        <div className="container-custom relative z-10">
          <h1 className="text-4xl font-black text-white mb-3">Refund Policy</h1>
          <p className="text-white/60 text-sm">Last updated: June 12, 2026</p>
        </div>
      </section>
      <div className="container-custom py-16 max-w-4xl">
        {/* Quick summary */}
        <div className="grid sm:grid-cols-3 gap-5 mb-12">
          {[
            { icon: "✅", title: "7-Day Money Back", desc: "Full refund within 7 days if unused" },
            { icon: "🔄", title: "Session Rescheduling", desc: "Free rescheduling up to 24hrs before" },
            { icon: "💬", title: "Easy Process", desc: "Email us — resolved in 3 business days" },
          ].map((item) => (
            <div key={item.title} className="bg-emerald-50 border border-emerald-100 rounded-2xl p-5 text-center">
              <div className="text-3xl mb-2">{item.icon}</div>
              <h3 className="font-bold text-slate-900 mb-1">{item.title}</h3>
              <p className="text-slate-500 text-sm">{item.desc}</p>
            </div>
          ))}
        </div>

        <div className="space-y-8">
          {[
            { title: "1. Subscription Plans", content: "All subscription plans come with a 7-day free trial. If you cancel within 7 days of your first paid charge and have not used more than 1 counselling session, you are eligible for a full refund. After 7 days, refunds are not provided for the current billing period. You may cancel at any time to prevent future charges." },
            { title: "2. Individual Counselling Sessions", content: "Sessions cancelled more than 24 hours before the scheduled time receive a full credit to your account (valid for 60 days). Sessions cancelled within 24 hours are non-refundable but may be rescheduled once. No-shows without prior notice are non-refundable." },
            { title: "3. Study Abroad Packages", content: "Study abroad consulting packages are refundable within 7 days of purchase if no services have been delivered. Once document review, university shortlisting, or SOP work has begun, a partial refund may be issued based on work completed, at MargVedA's discretion." },
            { title: "4. How to Request a Refund", content: "Email refunds@margveda.com with your order ID and reason. We process all refund requests within 3 business days. Approved refunds are credited back to the original payment method within 5–7 business days." },
            { title: "5. Exceptions", content: "Refunds are not available for: AI Career Reports once downloaded, Group workshop tickets, and One-time event fees. We reserve the right to modify this policy at any time with 30 days' notice." },
          ].map((section) => (
            <div key={section.title}>
              <h2 className="text-xl font-black text-slate-900 mb-3">{section.title}</h2>
              <p className="text-slate-600 leading-relaxed">{section.content}</p>
            </div>
          ))}
        </div>

        <div className="mt-10 bg-primary-50 border border-primary-100 rounded-2xl p-6">
          <p className="font-bold text-primary-900 mb-1">Need help with a refund?</p>
          <p className="text-primary-700 text-sm mb-3">Our support team will resolve your concern within 3 business days.</p>
          <Link href="/contact" className="btn-primary text-sm inline-block">
            Contact Support
          </Link>
        </div>
      </div>
    </div>
  );
}
