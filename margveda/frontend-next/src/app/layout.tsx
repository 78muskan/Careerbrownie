import type { Metadata } from "next";
import { Inter, Plus_Jakarta_Sans } from "next/font/google";
import "./globals.css";
import Header from "@/components/layout/Header";
import Footer from "@/components/layout/Footer";
import WhatsAppButton from "@/components/layout/WhatsAppButton";
import FloatingChatButton from "@/components/chat/FloatingChatButton";
import { AuthProvider } from "@/contexts/AuthContext";
import { SITE_NAME, SITE_DESCRIPTION } from "@/lib/constants";

const inter = Inter({
  variable: "--font-sans",
  subsets: ["latin"],
  display: "swap",
});

const plusJakarta = Plus_Jakarta_Sans({
  variable: "--font-display",
  subsets: ["latin"],
  display: "swap",
});

export const metadata: Metadata = {
  title: {
    default: `${SITE_NAME} — India's AI-Powered Career Intelligence Platform`,
    template: `%s | ${SITE_NAME}`,
  },
  description: SITE_DESCRIPTION,
  keywords: [
    "career counselling India",
    "AI career guidance",
    "university admissions consultant",
    "study abroad India",
    "career assessment online",
    "best career counsellor India",
    "IIT NIT admissions guidance",
    "MBA admissions consultant India",
  ],
  authors: [{ name: "Career Brownie" }],
  creator: "Career Brownie",
  openGraph: {
    type: "website",
    locale: "en_IN",
    url: "https://careerbrownie.com",
    siteName: SITE_NAME,
    title: `${SITE_NAME} — India's AI-Powered Career Intelligence Platform`,
    description: SITE_DESCRIPTION,
    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Career Brownie Career Intelligence Platform",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    site: "@careerbrownie",
    creator: "@careerbrownie",
    title: `${SITE_NAME} — India's AI-Powered Career Intelligence Platform`,
    description: SITE_DESCRIPTION,
    images: ["/og-image.png"],
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      "max-video-preview": -1,
      "max-image-preview": "large",
      "max-snippet": -1,
    },
  },
  icons: {
    icon: "/favicon.ico",
    shortcut: "/favicon-16x16.png",
    apple: "/apple-touch-icon.png",
  },
  manifest: "/site.webmanifest",
  alternates: {
    canonical: "https://careerbrownie.com",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={`${inter.variable} ${plusJakarta.variable}`}>
      <body className="min-h-screen flex flex-col antialiased">
        <AuthProvider>
          <Header />
          <main className="flex-1">{children}</main>
          <Footer />
          <WhatsAppButton />
          <FloatingChatButton />
        </AuthProvider>
      </body>
    </html>
  );
}
