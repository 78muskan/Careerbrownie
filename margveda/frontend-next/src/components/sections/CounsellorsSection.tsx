"use client";

import { motion } from "framer-motion";
import Link from "next/link";
import { Star, Clock, Users, ArrowRight } from "lucide-react";
import { COUNSELLORS } from "@/lib/constants";

export default function CounsellorsSection() {
  return (
    <section className="py-24 bg-white">
      <div className="container-custom">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <span className="inline-block bg-violet-50 text-violet-700 text-sm font-semibold px-4 py-1.5 rounded-full mb-4">
            Expert Team
          </span>
          <h2 className="section-heading text-slate-900 mb-4">
            Meet Our{" "}
            <span className="text-gradient">Expert Counsellors</span>
          </h2>
          <p className="text-slate-500 max-w-xl mx-auto">
            Certified career counsellors with decades of combined experience in every domain — from engineering to MBA, from arts to tech.
          </p>
        </motion.div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {COUNSELLORS.map((counsellor, i) => (
            <motion.div
              key={counsellor.id}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: i * 0.1 }}
              className="group bg-white border border-slate-100 rounded-2xl overflow-hidden card-hover"
            >
              {/* Card header */}
              <div className="relative h-36 bg-gradient-to-br from-primary-500 to-violet-600 flex items-end p-5">
                <div className="absolute top-4 right-4 bg-white/20 rounded-full px-3 py-1 text-white text-xs font-semibold backdrop-blur-sm">
                  {counsellor.specialization}
                </div>
                {/* Avatar */}
                <div className="w-16 h-16 rounded-2xl border-4 border-white bg-gradient-to-br from-primary-200 to-violet-300 flex items-center justify-center text-2xl font-black text-white shadow-lg">
                  {counsellor.name.charAt(0)}
                </div>
              </div>

              <div className="p-5">
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <h3 className="font-bold text-slate-900 text-lg">{counsellor.name}</h3>
                    <p className="text-slate-500 text-sm">{counsellor.title}</p>
                  </div>
                  <div className="flex items-center gap-1 bg-amber-50 rounded-lg px-2.5 py-1">
                    <Star size={14} className="fill-amber-400 text-amber-400" />
                    <span className="text-sm font-bold text-amber-600">{counsellor.rating}</span>
                  </div>
                </div>

                <div className="flex items-center gap-4 mb-4 text-sm text-slate-500">
                  <div className="flex items-center gap-1.5">
                    <Clock size={13} />
                    {counsellor.experience}
                  </div>
                  <div className="flex items-center gap-1.5">
                    <Users size={13} />
                    {counsellor.sessions} Sessions
                  </div>
                </div>

                <div className="flex flex-wrap gap-2 mb-5">
                  {counsellor.tags.map((tag) => (
                    <span
                      key={tag}
                      className="text-xs bg-primary-50 text-primary-700 rounded-full px-3 py-1 font-medium"
                    >
                      {tag}
                    </span>
                  ))}
                </div>

                <Link
                  href="/book-consultation"
                  className="flex items-center justify-center gap-2 w-full bg-gradient-brand text-white font-semibold text-sm py-3 rounded-xl hover:shadow-lg hover:shadow-primary-200 transition-shadow"
                >
                  Book Session
                  <ArrowRight size={16} />
                </Link>
              </div>
            </motion.div>
          ))}
        </div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.3 }}
          className="text-center mt-10"
        >
          <Link href="/about#counsellors" className="btn-secondary inline-flex items-center gap-2">
            View All 200+ Counsellors
            <ArrowRight size={18} />
          </Link>
        </motion.div>
      </div>
    </section>
  );
}
