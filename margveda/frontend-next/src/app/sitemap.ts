import type { MetadataRoute } from "next";

const BASE_URL = process.env.NEXT_PUBLIC_SITE_URL || "https://margveda.com";

export default function sitemap(): MetadataRoute.Sitemap {
  const routes = [
    { url: "/", priority: 1.0, changeFrequency: "daily" as const },
    { url: "/about", priority: 0.8, changeFrequency: "monthly" as const },
    { url: "/services", priority: 0.9, changeFrequency: "weekly" as const },
    { url: "/services/career-counselling", priority: 0.9, changeFrequency: "weekly" as const },
    { url: "/services/university-admissions", priority: 0.9, changeFrequency: "weekly" as const },
    { url: "/services/study-abroad", priority: 0.9, changeFrequency: "weekly" as const },
    { url: "/services/career-intelligence", priority: 0.8, changeFrequency: "weekly" as const },
    { url: "/services/ai-career-guidance", priority: 0.8, changeFrequency: "weekly" as const },
    { url: "/book-consultation", priority: 0.95, changeFrequency: "weekly" as const },
    { url: "/contact", priority: 0.7, changeFrequency: "monthly" as const },
    { url: "/blog", priority: 0.8, changeFrequency: "daily" as const },
    { url: "/faq", priority: 0.6, changeFrequency: "monthly" as const },
    { url: "/privacy-policy", priority: 0.3, changeFrequency: "yearly" as const },
    { url: "/terms-conditions", priority: 0.3, changeFrequency: "yearly" as const },
    { url: "/refund-policy", priority: 0.3, changeFrequency: "yearly" as const },
  ];

  return routes.map((r) => ({
    url: `${BASE_URL}${r.url}`,
    lastModified: new Date(),
    changeFrequency: r.changeFrequency,
    priority: r.priority,
  }));
}
