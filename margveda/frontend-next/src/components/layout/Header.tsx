"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import Image from "next/image";
import { usePathname } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import { Menu, X, ChevronDown, Phone, Sparkles } from "lucide-react";
import { NAV_LINKS, CONTACT_PHONE } from "@/lib/constants";
import { cn } from "@/lib/utils";

export default function Header() {
  const [scrolled, setScrolled] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);
  const [openDropdown, setOpenDropdown] = useState<string | null>(null);
  const pathname = usePathname();

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 20);
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  useEffect(() => {
    setMobileOpen(false);
    setOpenDropdown(null);
  }, [pathname]);

  useEffect(() => {
    document.body.style.overflow = mobileOpen ? "hidden" : "";
    return () => { document.body.style.overflow = ""; };
  }, [mobileOpen]);

  const isActive = (href: string) =>
    href === "/" ? pathname === "/" : pathname.startsWith(href);

  return (
    <>
      <motion.header
        initial={{ y: -100 }}
        animate={{ y: 0 }}
        transition={{ duration: 0.5, ease: "easeOut" }}
        className={cn(
          "fixed top-0 left-0 right-0 z-50 transition-all duration-300",
          scrolled
            ? "bg-white/95 backdrop-blur-md shadow-sm border-b border-slate-100"
            : "bg-transparent"
        )}
      >
        {/* Top bar */}
        <div className="hidden md:block bg-gradient-brand text-white text-sm py-2">
          <div className="container-custom flex items-center justify-between">
            <p className="flex items-center gap-2">
              <Sparkles size={14} />
              India&apos;s AI-Powered Career Guidance Platform — Personalized for Every Student
            </p>
            <a
              href={`tel:${CONTACT_PHONE.replace(/\s/g, "")}`}
              className="flex items-center gap-1.5 hover:text-yellow-300 transition-colors"
            >
              <Phone size={14} />
              {CONTACT_PHONE}
            </a>
          </div>
        </div>

        {/* Main nav */}
        <nav className="container-custom flex items-center justify-between h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-2.5 flex-shrink-0">
            <Image src="/logo.svg" alt="Career Brownie" width={36} height={36} className="rounded-xl object-contain" unoptimized />
            <span
              className={cn(
                "font-black text-xl tracking-tight transition-colors",
                scrolled ? "text-slate-900" : "text-white"
              )}
            >
              Career<span className="text-gradient"> Brownie</span>
            </span>
          </Link>

          {/* Desktop nav links */}
          <div className="hidden lg:flex items-center gap-1">
            {NAV_LINKS.map((link) => (
              <div
                key={link.href}
                className="relative"
                onMouseEnter={() => link.children && setOpenDropdown(link.label)}
                onMouseLeave={() => setOpenDropdown(null)}
              >
                <Link
                  href={link.href}
                  className={cn(
                    "flex items-center gap-1 px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200",
                    isActive(link.href)
                      ? "text-primary-600 bg-primary-50"
                      : scrolled
                      ? "text-slate-700 hover:text-primary-600 hover:bg-primary-50"
                      : "text-white/90 hover:text-white hover:bg-white/10"
                  )}
                >
                  {link.label}
                  {link.children && (
                    <ChevronDown
                      size={14}
                      className={cn(
                        "transition-transform duration-200",
                        openDropdown === link.label ? "rotate-180" : ""
                      )}
                    />
                  )}
                </Link>

                {/* Dropdown */}
                {link.children && (
                  <AnimatePresence>
                    {openDropdown === link.label && (
                      <motion.div
                        initial={{ opacity: 0, y: 8, scale: 0.95 }}
                        animate={{ opacity: 1, y: 0, scale: 1 }}
                        exit={{ opacity: 0, y: 8, scale: 0.95 }}
                        transition={{ duration: 0.15 }}
                        className="absolute top-full left-0 mt-1 w-60 bg-white rounded-xl shadow-xl border border-slate-100 py-2 overflow-hidden"
                      >
                        {link.children.map((child) => (
                          <Link
                            key={child.href}
                            href={child.href}
                            className="block px-4 py-2.5 text-sm text-slate-700 hover:bg-primary-50 hover:text-primary-600 transition-colors"
                          >
                            {child.label}
                          </Link>
                        ))}
                      </motion.div>
                    )}
                  </AnimatePresence>
                )}
              </div>
            ))}
          </div>

          {/* CTA buttons */}
          <div className="hidden lg:flex items-center gap-3">
            <Link
              href="/contact"
              className={cn(
                "text-sm font-medium px-4 py-2 rounded-lg transition-all",
                scrolled
                  ? "text-slate-700 hover:text-primary-600"
                  : "text-white/90 hover:text-white"
              )}
            >
              Talk to Expert
            </Link>
            <Link
              href="/book-consultation"
              className="btn-primary text-sm"
            >
              Book Free Session
            </Link>
          </div>

          {/* Mobile menu button */}
          <button
            onClick={() => setMobileOpen(!mobileOpen)}
            className={cn(
              "lg:hidden p-2 rounded-lg transition-colors",
              scrolled ? "text-slate-700" : "text-white"
            )}
            aria-label="Toggle menu"
          >
            {mobileOpen ? <X size={22} /> : <Menu size={22} />}
          </button>
        </nav>
      </motion.header>

      {/* Mobile menu */}
      <AnimatePresence>
        {mobileOpen && (
          <>
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setMobileOpen(false)}
              className="fixed inset-0 bg-black/50 z-40 lg:hidden"
            />
            <motion.div
              initial={{ x: "100%" }}
              animate={{ x: 0 }}
              exit={{ x: "100%" }}
              transition={{ type: "tween", duration: 0.3 }}
              className="fixed right-0 top-0 bottom-0 w-80 bg-white z-50 lg:hidden shadow-2xl overflow-y-auto"
            >
              <div className="flex items-center justify-between p-5 border-b border-slate-100">
                <Link href="/" className="flex items-center gap-2">
                  <Image src="/logo.svg" alt="Career Brownie" width={32} height={32} className="rounded-lg object-contain" unoptimized />
                  <span className="font-black text-lg text-slate-900">
                    Career<span className="text-gradient"> Brownie</span>
                  </span>
                </Link>
                <button
                  onClick={() => setMobileOpen(false)}
                  className="p-1.5 rounded-lg hover:bg-slate-100 text-slate-600"
                >
                  <X size={20} />
                </button>
              </div>

              <div className="p-4 space-y-1">
                {NAV_LINKS.map((link) => (
                  <div key={link.href}>
                    <Link
                      href={link.href}
                      className={cn(
                        "flex items-center justify-between w-full px-4 py-3 rounded-xl text-sm font-medium transition-colors",
                        isActive(link.href)
                          ? "bg-primary-50 text-primary-600"
                          : "text-slate-700 hover:bg-slate-50"
                      )}
                      onClick={() =>
                        link.children
                          ? setOpenDropdown(
                              openDropdown === link.label ? null : link.label
                            )
                          : setMobileOpen(false)
                      }
                    >
                      {link.label}
                      {link.children && (
                        <ChevronDown
                          size={16}
                          className={cn(
                            "transition-transform",
                            openDropdown === link.label ? "rotate-180" : ""
                          )}
                        />
                      )}
                    </Link>

                    {link.children && openDropdown === link.label && (
                      <div className="ml-4 mt-1 space-y-1">
                        {link.children.map((child) => (
                          <Link
                            key={child.href}
                            href={child.href}
                            className="block px-4 py-2.5 text-sm text-slate-600 hover:text-primary-600 hover:bg-primary-50 rounded-lg transition-colors"
                            onClick={() => setMobileOpen(false)}
                          >
                            {child.label}
                          </Link>
                        ))}
                      </div>
                    )}
                  </div>
                ))}
              </div>

              <div className="p-4 border-t border-slate-100 space-y-3">
                <Link
                  href="/contact"
                  className="block w-full btn-secondary text-sm text-center"
                  onClick={() => setMobileOpen(false)}
                >
                  Talk to Expert
                </Link>
                <Link
                  href="/book-consultation"
                  className="block w-full btn-primary text-sm text-center"
                  onClick={() => setMobileOpen(false)}
                >
                  Book Free Session
                </Link>
              </div>
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </>
  );
}
