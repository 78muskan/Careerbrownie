import type { Metadata } from "next";
import HeroSection from "@/components/sections/HeroSection";
import FeaturesSection from "@/components/sections/FeaturesSection";
import ServicesSection from "@/components/sections/ServicesSection";
import HowItWorksSection from "@/components/sections/HowItWorksSection";
import TestimonialsSection from "@/components/sections/TestimonialsSection";
import CounsellorsSection from "@/components/sections/CounsellorsSection";
import UniversityPartnersSection from "@/components/sections/UniversityPartnersSection";
import PricingSection from "@/components/sections/PricingSection";
import FAQSection from "@/components/sections/FAQSection";
import NewsletterSection from "@/components/sections/NewsletterSection";

export const metadata: Metadata = {
  title: "MargVedA — India's AI-Powered Career Intelligence Platform",
  description:
    "Discover your ideal career path with MargVedA. AI-powered career guidance, expert counselling, university admissions support, and study abroad assistance for Indian students.",
};

export default function HomePage() {
  return (
    <>
      <HeroSection />
      <FeaturesSection />
      <ServicesSection />
      <HowItWorksSection />
      <TestimonialsSection />
      <CounsellorsSection />
      <UniversityPartnersSection />
      <PricingSection />
      <FAQSection />
      <NewsletterSection />
    </>
  );
}
