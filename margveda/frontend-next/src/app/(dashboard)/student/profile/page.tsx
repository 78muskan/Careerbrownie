"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import { User, MapPin, BookOpen, Target, Edit2, Loader2 } from "lucide-react";
import api from "@/lib/api";

interface Profile {
  current_education: string;
  stream: string;
  institution_name: string;
  graduation_year: number | null;
  percentage_cgpa: number | null;
  city: string;
  state: string;
  career_interests: string[];
  preferred_industries: string[];
  target_roles: string[];
  technical_skills: string[];
  soft_skills: string[];
  certifications: string[];
  languages: string[];
  short_term_goal: string;
  long_term_goal: string;
  preferred_work_style: string;
  profile_score: number;
  study_abroad_interest: boolean;
}

function Tag({ label }: { label: string }) {
  return <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary-50 text-primary-700">{label}</span>;
}

export default function StudentProfilePage() {
  const [profile, setProfile] = useState<Profile | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get("/student/profile/")
      .then((r) => setProfile(r.data))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="flex justify-center p-16"><Loader2 className="w-8 h-8 animate-spin text-primary-600" /></div>;

  return (
    <div className="max-w-3xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-display font-bold text-gray-900">My Profile</h1>
          {profile && (
            <div className="flex items-center gap-2 mt-1">
              <div className="w-32 h-1.5 bg-gray-200 rounded-full overflow-hidden">
                <div className="h-full bg-primary-500 rounded-full" style={{ width: `${profile.profile_score}%` }} />
              </div>
              <span className="text-xs text-gray-500">{profile?.profile_score}% complete</span>
            </div>
          )}
        </div>
        <Link href="/student/profile/build" className="btn-primary flex items-center gap-2 text-sm">
          <Edit2 className="w-4 h-4" />
          Edit profile
        </Link>
      </div>

      {!profile ? (
        <div className="text-center bg-white rounded-2xl p-12 border border-gray-100">
          <User className="w-12 h-12 text-gray-300 mx-auto mb-4" />
          <p className="text-gray-500 mb-4">You haven&apos;t set up your profile yet.</p>
          <Link href="/student/profile/build" className="btn-primary">Build profile</Link>
        </div>
      ) : (
        <>
          {/* Academic */}
          <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
            <h3 className="font-semibold text-gray-900 flex items-center gap-2 mb-4"><BookOpen className="w-5 h-5 text-primary-600" />Academic Information</h3>
            <dl className="grid grid-cols-2 gap-x-8 gap-y-3 text-sm">
              {[
                ["Education", profile.current_education?.replace("_", " ")],
                ["Stream", profile.stream],
                ["Institution", profile.institution_name],
                ["Grad. Year", profile.graduation_year],
                ["Score", profile.percentage_cgpa],
              ].map(([k, v]) => v ? (
                <div key={String(k)}>
                  <dt className="text-gray-400 text-xs uppercase tracking-wide">{k}</dt>
                  <dd className="text-gray-800 font-medium mt-0.5">{String(v)}</dd>
                </div>
              ) : null)}
              {(profile.city || profile.state) && (
                <div className="col-span-2">
                  <dt className="text-gray-400 text-xs uppercase tracking-wide">Location</dt>
                  <dd className="text-gray-800 font-medium mt-0.5 flex items-center gap-1">
                    <MapPin className="w-3.5 h-3.5 text-gray-400" />
                    {[profile.city, profile.state].filter(Boolean).join(", ")}
                  </dd>
                </div>
              )}
            </dl>
          </div>

          {/* Career interests */}
          {(profile.career_interests?.length > 0 || profile.target_roles?.length > 0) && (
            <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
              <h3 className="font-semibold text-gray-900 flex items-center gap-2 mb-4"><Target className="w-5 h-5 text-violet-600" />Career Interests</h3>
              {profile.career_interests?.length > 0 && (
                <div className="mb-3">
                  <p className="text-xs text-gray-400 uppercase tracking-wide mb-2">Interests</p>
                  <div className="flex flex-wrap gap-2">{profile.career_interests.map((t) => <Tag key={t} label={t} />)}</div>
                </div>
              )}
              {profile.target_roles?.length > 0 && (
                <div>
                  <p className="text-xs text-gray-400 uppercase tracking-wide mb-2">Target Roles</p>
                  <div className="flex flex-wrap gap-2">{profile.target_roles.map((t) => <Tag key={t} label={t} />)}</div>
                </div>
              )}
            </div>
          )}

          {/* Skills */}
          {(profile.technical_skills?.length > 0 || profile.soft_skills?.length > 0) && (
            <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
              <h3 className="font-semibold text-gray-900 mb-4">Skills</h3>
              {profile.technical_skills?.length > 0 && (
                <div className="mb-3">
                  <p className="text-xs text-gray-400 uppercase tracking-wide mb-2">Technical</p>
                  <div className="flex flex-wrap gap-2">{profile.technical_skills.map((t) => <Tag key={t} label={t} />)}</div>
                </div>
              )}
              {profile.soft_skills?.length > 0 && (
                <div>
                  <p className="text-xs text-gray-400 uppercase tracking-wide mb-2">Soft skills</p>
                  <div className="flex flex-wrap gap-2">{profile.soft_skills.map((t) => <span key={t} className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs bg-green-50 text-green-700">{t}</span>)}</div>
                </div>
              )}
            </div>
          )}
        </>
      )}
    </div>
  );
}
