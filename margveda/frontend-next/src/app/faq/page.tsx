import type { Metadata } from "next";
import FAQSection from "@/components/sections/FAQSection";
import NewsletterSection from "@/components/sections/NewsletterSection";

export const metadata: Metadata = {
  title: "FAQ — Career Brownie",
  description: "Find answers to frequently asked questions about Career Brownie's career guidance services, pricing, counselling sessions, and more.",
};

const extendedFaqs = [
  { q: "What subjects or streams does Career Brownie cover?", a: "We cover all streams — Science (PCM/PCB), Commerce, Arts, Humanities, and vocational courses. Our counsellors are specialized across engineering, medicine, law, business, design, and emerging fields like AI and sustainability." },
  { q: "How long does a counselling session last?", a: "Standard sessions are 60 minutes. Free introductory sessions are 30 minutes. For comprehensive guidance packages, we offer extended 90-minute deep-dive sessions." },
  { q: "Can parents attend the counselling session?", a: "Absolutely! We encourage parents to join, especially for students in Class 9-12. We have separate parent consultation packages and also offer family sessions where both student and parent perspectives are addressed." },
  { q: "Do you offer group sessions or workshops?", a: "Yes! We conduct group workshops for schools and colleges on career planning, aptitude development, and industry insights. Contact us to schedule a workshop at your institution." },
  { q: "How do you select and verify counsellors?", a: "All Career Brownie counsellors go through a rigorous 5-step vetting process: credential verification, background checks, practical skill assessment, test counselling sessions, and peer review. Only 1 in 8 applicants makes it through." },
  { q: "Is there a mobile app available?", a: "Our Progressive Web App (PWA) works seamlessly on mobile browsers. A dedicated Android and iOS app is launching in Q3 2026." },
];

export default function FAQPage() {
  return (
    <div className="pt-24">
      <section className="bg-gradient-hero py-20 text-center relative overflow-hidden">
        <div className="absolute inset-0 pattern-grid opacity-20" />
        <div className="container-custom relative z-10">
          <h1 className="text-4xl md:text-5xl font-black text-white mb-4">
            Frequently Asked <span className="text-transparent bg-clip-text bg-gradient-to-r from-yellow-300 to-orange-300">Questions</span>
          </h1>
          <p className="text-white/70 max-w-xl mx-auto">Everything you need to know about Career Brownie.</p>
        </div>
      </section>

      <FAQSection />

      {/* Extended FAQs */}
      <section className="py-16 bg-slate-50">
        <div className="container-custom max-w-3xl">
          <h2 className="text-2xl font-black text-slate-900 mb-8 text-center">More Questions</h2>
          <div className="space-y-4">
            {extendedFaqs.map((faq, i) => (
              <div key={i} className="bg-white border border-slate-100 rounded-2xl p-6">
                <h3 className="font-bold text-slate-900 mb-2">{faq.q}</h3>
                <p className="text-slate-500 text-sm leading-relaxed">{faq.a}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <NewsletterSection />
    </div>
  );
}
