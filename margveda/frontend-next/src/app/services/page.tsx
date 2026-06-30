import type { Metadata } from "next";
import Link from "next/link";
import { ArrowRight } from "lucide-react";
import { SERVICES_LIST } from "@/lib/constants";

export const metadata: Metadata = {
  title: "Our Services — Career Brownie",
  description:
    "Explore Career Brownie's comprehensive career guidance services — from career counselling and university admissions to study abroad and AI career guidance.",
};

export default function ServicesPage() {
  return (
    <div className="pt-24">
      {/* Header */}
      <section className="bg-gradient-hero py-20 text-center relative overflow-hidden">
        <div className="absolute inset-0 pattern-grid opacity-20" />
        <div className="container-custom relative z-10">
          <h1 className="text-4xl md:text-5xl font-black text-white mb-4">
            Our <span className="text-transparent bg-clip-text bg-gradient-to-r from-yellow-300 to-orange-300">Services</span>
          </h1>
          <p className="text-white/70 max-w-xl mx-auto text-lg">
            Comprehensive career support from discovery to destination — everything you need in one platform.
          </p>
        </div>
      </section>

      {/* Services grid */}
      <section className="py-24 bg-white">
        <div className="container-custom">
          <div className="grid md:grid-cols-2 gap-8">
            {SERVICES_LIST.map((service) => (
              <div key={service.id} className="group border border-slate-100 rounded-3xl p-8 card-hover bg-white">
                <div className={`w-16 h-16 rounded-2xl bg-gradient-to-br ${service.color} flex items-center justify-center mb-6 text-3xl shadow-lg group-hover:scale-110 transition-transform`}>
                  {service.icon}
                </div>
                <h2 className="text-2xl font-black text-slate-900 mb-3">{service.title}</h2>
                <p className="text-slate-500 mb-6 leading-relaxed">{service.description}</p>
                <ul className="grid grid-cols-2 gap-2 mb-7">
                  {service.features.map((f) => (
                    <li key={f} className="flex items-center gap-2 text-sm text-slate-600">
                      <span className="w-4 h-4 rounded-full bg-primary-100 text-primary-600 flex items-center justify-center text-xs font-bold">✓</span>
                      {f}
                    </li>
                  ))}
                </ul>
                <Link href={service.href} className="inline-flex items-center gap-2 text-primary-600 font-bold group-hover:gap-3 transition-all">
                  Explore Service <ArrowRight size={16} />
                </Link>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
