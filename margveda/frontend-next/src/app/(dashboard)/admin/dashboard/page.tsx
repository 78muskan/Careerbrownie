"use client";
import Link from "next/link";
import { Users, Calendar, Database, ExternalLink } from "lucide-react";

export default function AdminDashboardPage() {
  return (
    <div className="max-w-5xl space-y-6">
      <h1 className="text-2xl font-display font-bold text-gray-900">Admin Dashboard</h1>
      <p className="text-gray-500">Platform overview and management.</p>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        {[
          { label: "Manage Users", desc: "View and manage all users", icon: <Users className="w-6 h-6 text-primary-600" />, href: "http://localhost:8000/admin/users/user/", external: true },
          { label: "Manage Sessions", desc: "View all counselling sessions", icon: <Calendar className="w-6 h-6 text-violet-600" />, href: "http://localhost:8000/admin/sessions_app/session/", external: true },
          { label: "Django Admin", desc: "Full admin panel", icon: <Database className="w-6 h-6 text-gray-600" />, href: "http://localhost:8000/admin/", external: true },
        ].map((item) => (
          <a
            key={item.label}
            href={item.href}
            target={item.external ? "_blank" : undefined}
            rel="noopener noreferrer"
            className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 hover:border-primary-300 hover:shadow-md transition-all group"
          >
            <div className="mb-4">{item.icon}</div>
            <p className="font-semibold text-gray-900 flex items-center gap-1.5">
              {item.label}
              {item.external && <ExternalLink className="w-3.5 h-3.5 text-gray-400 group-hover:text-gray-600" />}
            </p>
            <p className="text-sm text-gray-500 mt-1">{item.desc}</p>
          </a>
        ))}
      </div>

      <div className="bg-blue-50 border border-blue-100 rounded-2xl p-6">
        <p className="text-blue-800 font-medium">Full admin management is available at the Django admin panel.</p>
        <a href="http://localhost:8000/admin/" target="_blank" rel="noopener noreferrer" className="mt-2 inline-block text-blue-600 text-sm hover:underline">
          Open Django Admin → admin@margveda.com / Admin@1234
        </a>
      </div>
    </div>
  );
}
