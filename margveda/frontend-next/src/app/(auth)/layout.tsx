import type { ReactNode } from "react";

export default function AuthLayout({ children }: { children: ReactNode }) {
  return (
    <div className="min-h-screen flex">
      {/* Left panel — branding */}
      <div className="hidden lg:flex lg:w-1/2 bg-gradient-hero flex-col justify-between p-12 relative overflow-hidden">
        <div className="absolute inset-0 pattern-dots opacity-10" />
        <div className="relative z-10">
          <div className="flex items-center gap-3 mb-16">
            <div className="w-10 h-10 rounded-xl bg-white/20 backdrop-blur flex items-center justify-center">
              <span className="text-white font-bold text-xl">M</span>
            </div>
            <span className="text-white font-display font-bold text-xl">MargVedA</span>
          </div>
          <h2 className="text-4xl font-display font-bold text-white leading-tight mb-6">
            Your career journey starts with the right guidance.
          </h2>
          <p className="text-white/70 text-lg leading-relaxed">
            Join 10,000+ students who found their dream career with India&apos;s most advanced AI career platform.
          </p>
        </div>
        <div className="relative z-10 grid grid-cols-3 gap-4">
          {[
            { value: "10K+", label: "Students guided" },
            { value: "95%", label: "Satisfaction rate" },
            { value: "500+", label: "Careers unlocked" },
          ].map((s) => (
            <div key={s.label} className="bg-white/10 backdrop-blur rounded-2xl p-4 text-center">
              <div className="text-2xl font-bold text-white">{s.value}</div>
              <div className="text-white/60 text-xs mt-1">{s.label}</div>
            </div>
          ))}
        </div>
      </div>
      {/* Right panel — form */}
      <div className="flex-1 flex items-center justify-center p-6 lg:p-12 bg-white">
        <div className="w-full max-w-md">{children}</div>
      </div>
    </div>
  );
}
