import Link from "next/link";
import { Mail, Phone, MapPin, Globe, ExternalLink } from "lucide-react";
import { CONTACT_EMAIL, CONTACT_PHONE, SOCIAL_LINKS } from "@/lib/constants";

const footerLinks = {
  Services: [
    { label: "Career Counselling", href: "/services/career-counselling" },
    { label: "University Admissions", href: "/services/university-admissions" },
    { label: "Study Abroad", href: "/services/study-abroad" },
    { label: "Career Intelligence", href: "/services/career-intelligence" },
    { label: "AI Career Guidance", href: "/services/ai-career-guidance" },
  ],
  Company: [
    { label: "About Us", href: "/about" },
    { label: "Blog", href: "/blog" },
    { label: "Careers", href: "/careers" },
    { label: "Press", href: "/press" },
    { label: "Partner with Us", href: "/partners" },
  ],
  Support: [
    { label: "Contact Us", href: "/contact" },
    { label: "Book Consultation", href: "/book-consultation" },
    { label: "FAQ", href: "/faq" },
    { label: "Privacy Policy", href: "/privacy-policy" },
    { label: "Terms & Conditions", href: "/terms-conditions" },
    { label: "Refund Policy", href: "/refund-policy" },
  ],
};

const socialIcons = [
  { label: "IN", href: SOCIAL_LINKS.instagram, title: "Instagram" },
  { label: "Li", href: SOCIAL_LINKS.linkedin, title: "LinkedIn" },
  { label: "Tw", href: SOCIAL_LINKS.twitter, title: "Twitter/X" },
  { label: "Yt", href: SOCIAL_LINKS.youtube, title: "YouTube" },
  { label: "Fb", href: SOCIAL_LINKS.facebook, title: "Facebook" },
];

export default function Footer() {
  return (
    <footer className="bg-slate-950 text-slate-300">
      {/* CTA Banner */}
      <div className="bg-gradient-brand py-14">
        <div className="container-custom text-center">
          <h2 className="text-3xl md:text-4xl font-black text-white mb-4">
            Ready to Find Your Perfect Career Path?
          </h2>
          <p className="text-white/80 mb-8 max-w-xl mx-auto">
            Join 50,000+ students who found their direction with MargVedA. Start with a free consultation today.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              href="/book-consultation"
              className="bg-white text-primary-700 font-bold px-8 py-3.5 rounded-lg hover:bg-slate-100 transition-colors"
            >
              Book Free Session
            </Link>
            <Link
              href="/contact"
              className="border-2 border-white/50 text-white font-semibold px-8 py-3.5 rounded-lg hover:bg-white/10 transition-colors"
            >
              Talk to an Expert
            </Link>
          </div>
        </div>
      </div>

      {/* Main footer */}
      <div className="container-custom py-16">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-10">
          {/* Brand column */}
          <div className="lg:col-span-2">
            <Link href="/" className="flex items-center gap-2.5 mb-5">
              <div className="w-10 h-10 rounded-xl bg-gradient-brand flex items-center justify-center">
                <span className="text-white font-black text-lg">M</span>
              </div>
              <span className="font-black text-2xl text-white">
                Marg<span className="text-primary-400">VedA</span>
              </span>
            </Link>
            <p className="text-sm leading-relaxed mb-6 text-slate-400 max-w-xs">
              India&apos;s leading AI-powered career intelligence platform helping students
              and professionals discover, plan, and achieve their ideal career paths.
            </p>

            {/* Contact info */}
            <div className="space-y-3 mb-6">
              <a
                href={`tel:${CONTACT_PHONE.replace(/\s/g, "")}`}
                className="flex items-center gap-3 text-sm hover:text-white transition-colors"
              >
                <div className="w-8 h-8 rounded-lg bg-slate-800 flex items-center justify-center flex-shrink-0">
                  <Phone size={14} className="text-primary-400" />
                </div>
                {CONTACT_PHONE}
              </a>
              <a
                href={`mailto:${CONTACT_EMAIL}`}
                className="flex items-center gap-3 text-sm hover:text-white transition-colors"
              >
                <div className="w-8 h-8 rounded-lg bg-slate-800 flex items-center justify-center flex-shrink-0">
                  <Mail size={14} className="text-primary-400" />
                </div>
                {CONTACT_EMAIL}
              </a>
              <div className="flex items-start gap-3 text-sm">
                <div className="w-8 h-8 rounded-lg bg-slate-800 flex items-center justify-center flex-shrink-0 mt-0.5">
                  <MapPin size={14} className="text-primary-400" />
                </div>
                <span>MargVedA HQ, Koramangala, Bengaluru, Karnataka 560034</span>
              </div>
            </div>

            {/* Social icons */}
            <div className="flex items-center gap-3">
              {socialIcons.map(({ label, href, title }) => (
                <a
                  key={title}
                  href={href}
                  target="_blank"
                  rel="noopener noreferrer"
                  aria-label={title}
                  title={title}
                  className="w-9 h-9 rounded-lg bg-slate-800 flex items-center justify-center hover:bg-primary-600 transition-colors text-xs font-bold"
                >
                  {label}
                </a>
              ))}
            </div>
          </div>

          {/* Links columns */}
          {Object.entries(footerLinks).map(([section, links]) => (
            <div key={section}>
              <h4 className="text-white font-bold text-sm uppercase tracking-widest mb-5">
                {section}
              </h4>
              <ul className="space-y-3">
                {links.map((link) => (
                  <li key={link.href}>
                    <Link
                      href={link.href}
                      className="text-sm text-slate-400 hover:text-white transition-colors"
                    >
                      {link.label}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </div>

      {/* Bottom bar */}
      <div className="border-t border-slate-800">
        <div className="container-custom py-6 flex flex-col md:flex-row items-center justify-between gap-4 text-sm text-slate-500">
          <p>© {new Date().getFullYear()} MargVedA. All rights reserved.</p>
          <div className="flex items-center gap-1">
            <span>Made with</span>
            <span className="text-red-400 mx-1">❤️</span>
            <span>in India 🇮🇳</span>
          </div>
          <div className="flex items-center gap-4">
            <Link href="/privacy-policy" className="hover:text-white transition-colors">
              Privacy
            </Link>
            <Link href="/terms-conditions" className="hover:text-white transition-colors">
              Terms
            </Link>
            <Link href="/refund-policy" className="hover:text-white transition-colors">
              Refund
            </Link>
          </div>
        </div>
      </div>
    </footer>
  );
}
