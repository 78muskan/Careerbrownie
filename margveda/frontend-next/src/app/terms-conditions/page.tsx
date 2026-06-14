import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Terms & Conditions — MargVedA",
};

export default function TermsPage() {
  return (
    <div className="pt-24 bg-white">
      <section className="bg-gradient-hero py-16 text-center relative overflow-hidden">
        <div className="absolute inset-0 pattern-grid opacity-20" />
        <div className="container-custom relative z-10">
          <h1 className="text-4xl font-black text-white mb-3">Terms &amp; Conditions</h1>
          <p className="text-white/60 text-sm">Last updated: June 12, 2026</p>
        </div>
      </section>
      <div className="container-custom py-16 max-w-4xl">
        <div className="space-y-8">
          {[
            { title: "1. Acceptance of Terms", content: "By accessing or using MargVedA's platform, you agree to be bound by these Terms and Conditions. If you do not agree, please do not use our services." },
            { title: "2. Services Description", content: "MargVedA provides career guidance, counselling sessions, AI-powered career assessments, university admissions support, and related educational advisory services. Our services are advisory in nature and do not guarantee specific career or admission outcomes." },
            { title: "3. User Eligibility", content: "Users must be at least 13 years of age to create an account. Users under 18 should have parental consent. Schools and institutions using MargVedA for students take responsibility for ensuring appropriate use." },
            { title: "4. Account Responsibilities", content: "You are responsible for maintaining the confidentiality of your login credentials, all activities that occur under your account, and providing accurate information. MargVedA reserves the right to suspend accounts that violate these terms." },
            { title: "5. Payment Terms", content: "Paid plans are billed monthly or annually in advance. All prices are in Indian Rupees (INR). Payments are processed securely through Razorpay. You are responsible for any applicable taxes." },
            { title: "6. Intellectual Property", content: "All content on MargVedA — including AI models, career data, articles, assessments, and design — is the intellectual property of MargVedA Technologies Pvt. Ltd. You may not reproduce, distribute, or create derivative works without written permission." },
            { title: "7. Limitation of Liability", content: "MargVedA provides guidance based on available data and counsellor expertise but cannot guarantee specific outcomes. Our liability is limited to the amount paid for services in the preceding 3 months. We are not liable for indirect, consequential, or punitive damages." },
            { title: "8. Governing Law", content: "These terms are governed by the laws of India. Disputes shall be subject to the exclusive jurisdiction of courts in Bengaluru, Karnataka." },
          ].map((section) => (
            <div key={section.title}>
              <h2 className="text-xl font-black text-slate-900 mb-3">{section.title}</h2>
              <p className="text-slate-600 leading-relaxed">{section.content}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
