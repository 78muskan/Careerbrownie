import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Privacy Policy — Career Brownie",
  description: "Career Brownie's privacy policy explaining how we collect, use, and protect your personal data.",
};

export default function PrivacyPolicyPage() {
  return (
    <div className="pt-24 bg-white">
      <section className="bg-gradient-hero py-16 text-center relative overflow-hidden">
        <div className="absolute inset-0 pattern-grid opacity-20" />
        <div className="container-custom relative z-10">
          <h1 className="text-4xl font-black text-white mb-3">Privacy Policy</h1>
          <p className="text-white/60 text-sm">Last updated: June 12, 2026</p>
        </div>
      </section>
      <div className="container-custom py-16 max-w-4xl">
        <div className="prose prose-slate max-w-none space-y-8">
          {[
            {
              title: "1. Information We Collect",
              content: "We collect information you provide directly, such as your name, email address, phone number, educational background, and career interests when you register, book consultations, or use our platform. We also collect usage data, device information, and cookies to improve your experience.",
            },
            {
              title: "2. How We Use Your Information",
              content: "We use your information to: provide personalized career guidance and recommendations; connect you with suitable counsellors; send confirmation and update emails; improve our AI models and services; send relevant newsletters (with your consent); and comply with legal obligations.",
            },
            {
              title: "3. Data Sharing",
              content: "We do NOT sell your personal data to third parties. We may share anonymized, aggregated data for research purposes. We share necessary data with counsellors assigned to your sessions, payment processors for billing, and cloud service providers who process data on our behalf under strict data protection agreements.",
            },
            {
              title: "4. Data Security",
              content: "We implement industry-standard security measures including AES-256 encryption for data at rest, TLS 1.3 for data in transit, regular security audits, access controls and audit logs, and secure development practices. While no system is 100% secure, we continuously improve our security posture.",
            },
            {
              title: "5. Your Rights",
              content: "Under applicable Indian data protection laws, you have the right to: access your personal data; correct inaccurate data; request deletion of your data; withdraw consent for marketing; and file a complaint with regulators. To exercise these rights, email us at privacy@careerbrownie.com.",
            },
            {
              title: "6. Cookies",
              content: "We use essential cookies for site functionality, analytics cookies (Google Analytics) to understand usage patterns, and preference cookies to remember your settings. You can control cookies through your browser settings.",
            },
            {
              title: "7. Contact",
              content: "For privacy-related queries, contact us at careerbrownie@gmail.com. We are a remote-first company based in India.",
            },
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
