"use client";
import Link from "next/link";
import Image from "next/image";
import { usePathname } from "next/navigation";
import { useAuth } from "@/contexts/AuthContext";
import {
  LayoutDashboard, User, Target, Calendar, BookOpen,
  Sparkles, Map, Brain, Clock, BarChart2,
  Settings, LogOut, ChevronRight, FileText, Mic,
  GraduationCap, Award, Briefcase, SendHorizonal, Cpu,
  TrendingUp, Users, School, Mail,
} from "lucide-react";

const studentLinks = [
  { href: "/student/dashboard", icon: LayoutDashboard, label: "Dashboard" },
  { href: "/student/profile", icon: User, label: "My Profile" },
  { href: "/student/assessment", icon: Brain, label: "Assessments" },
  { href: "/student/ai-advisor", icon: Sparkles, label: "AI Advisor" },
  { href: "/student/ai-twin", icon: Cpu, label: "AI Career Twin" },
  { href: "/student/career-roadmap", icon: Map, label: "Career Roadmap" },
  { href: "/student/goals", icon: Target, label: "Goals" },
  { href: "/student/sessions", icon: Calendar, label: "Sessions" },
  { href: "/student/resume", icon: FileText, label: "Resume Builder" },
  { href: "/student/interview", icon: Mic, label: "Interview Coach" },
  { href: "/student/jobs", icon: Briefcase, label: "Job Matches" },
  { href: "/student/applications", icon: SendHorizonal, label: "My Applications" },
  { href: "/student/placement", icon: TrendingUp, label: "Placement Score" },
  { href: "/student/college-predictor", icon: GraduationCap, label: "College Predictor" },
  { href: "/student/scholarships", icon: Award, label: "Scholarships" },
];

const counsellorLinks = [
  { href: "/counsellor/dashboard", icon: LayoutDashboard, label: "Dashboard" },
  { href: "/counsellor/sessions", icon: Calendar, label: "My Sessions" },
  { href: "/counsellor/availability", icon: Clock, label: "Availability" },
  { href: "/counsellor/profile", icon: User, label: "My Profile" },
  { href: "/counsellor/reports", icon: BarChart2, label: "Reports" },
  { href: "/counsellor/students", icon: BookOpen, label: "Students" },
];

const schoolAdminLinks = [
  { href: "/school/dashboard", icon: School, label: "School Dashboard" },
  { href: "/school/batches", icon: BookOpen, label: "Batches" },
  { href: "/school/analytics", icon: BarChart2, label: "Student Analytics" },
  { href: "/school/reports", icon: FileText, label: "Reports" },
];

const recruiterLinks = [
  { href: "/recruiter/dashboard", icon: LayoutDashboard, label: "Dashboard" },
  { href: "/recruiter/jobs", icon: Briefcase, label: "Job Postings" },
  { href: "/recruiter/candidates", icon: Users, label: "Candidate Search" },
];

const adminLinks = [
  { href: "/admin/dashboard", icon: LayoutDashboard, label: "Dashboard" },
  { href: "/admin/leads", icon: Users, label: "Leads" },
  { href: "/admin/bookings", icon: Calendar, label: "Bookings" },
  { href: "/admin/subscribers", icon: Mail, label: "Subscribers" },
  { href: "/admin/users", icon: User, label: "Users" },
  { href: "/admin/sessions", icon: Calendar, label: "Sessions" },
];

export default function DashboardSidebar() {
  const { user, logout } = useAuth();
  const pathname = usePathname();

  const links = user?.role === "counsellor" ? counsellorLinks
    : user?.role === "admin" ? adminLinks
    : user?.role === "school_admin" ? schoolAdminLinks
    : user?.role === "recruiter" ? recruiterLinks
    : studentLinks;

  return (
    <aside className="w-64 bg-white border-r border-gray-100 flex flex-col min-h-screen shrink-0">
      <div className="p-6 border-b border-gray-100">
        <Link href="/" className="flex items-center gap-3">
          <Image src="/logo.png" alt="Career Brownie" width={36} height={36} className="rounded-xl object-contain" />
          <span className="font-display font-bold text-gray-900">Career Brownie</span>
        </Link>
      </div>

      <nav className="flex-1 p-4 space-y-1 overflow-y-auto">
        {links.map(({ href, icon: Icon, label }) => {
          const active = pathname === href;
          return (
            <Link
              key={href}
              href={href}
              className={`flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-all group ${
                active
                  ? "bg-primary-50 text-primary-700"
                  : "text-gray-600 hover:bg-gray-50 hover:text-gray-900"
              }`}
            >
              <Icon className={`w-5 h-5 shrink-0 ${active ? "text-primary-600" : "text-gray-400 group-hover:text-gray-600"}`} />
              {label}
              {active && <ChevronRight className="ml-auto w-4 h-4 text-primary-400" />}
            </Link>
          );
        })}
      </nav>

      <div className="p-4 border-t border-gray-100 space-y-1">
        <Link href="/student/settings" className="flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm text-gray-600 hover:bg-gray-50">
          <Settings className="w-5 h-5 text-gray-400" />
          Settings
        </Link>
        <button
          onClick={logout}
          className="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm text-red-600 hover:bg-red-50"
        >
          <LogOut className="w-5 h-5" />
          Sign out
        </button>
        <div className="flex items-center gap-3 px-3 py-3 mt-2 bg-gray-50 rounded-xl">
          <div className="w-8 h-8 rounded-full bg-primary-100 flex items-center justify-center text-primary-700 font-bold text-sm shrink-0">
            {user?.full_name?.[0] ?? "?"}
          </div>
          <div className="min-w-0">
            <p className="text-sm font-medium text-gray-900 truncate">{user?.full_name}</p>
            <p className="text-xs text-gray-500 truncate capitalize">{user?.role?.replace("_", " ")}</p>
          </div>
        </div>
      </div>
    </aside>
  );
}