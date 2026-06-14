"use client";
import { useEffect, useState, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import Link from "next/link";
import { CheckCircle2, XCircle, Loader2 } from "lucide-react";
import api from "@/lib/api";

function VerifyEmailContent() {
  const params = useSearchParams();
  const token = params.get("token") || "";
  const [status, setStatus] = useState<"loading" | "success" | "error">("loading");
  const [message, setMessage] = useState("");

  useEffect(() => {
    if (!token) { setStatus("error"); setMessage("Invalid verification link."); return; }
    api.get(`/auth/verify-email/?token=${token}`)
      .then(() => setStatus("success"))
      .catch((err) => {
        const msg = err?.response?.data?.error || "Verification failed. The link may have expired.";
        setMessage(msg);
        setStatus("error");
      });
  }, [token]);

  if (status === "loading") {
    return (
      <div className="text-center py-16">
        <Loader2 className="w-12 h-12 text-primary-600 animate-spin mx-auto mb-4" />
        <p className="text-gray-500">Verifying your email…</p>
      </div>
    );
  }

  if (status === "success") {
    return (
      <div className="text-center py-8">
        <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <CheckCircle2 className="w-8 h-8 text-green-600" />
        </div>
        <h2 className="text-2xl font-display font-bold text-gray-900 mb-2">Email verified!</h2>
        <p className="text-gray-500 mb-6">Your account is now active. Start your career journey.</p>
        <Link href="/login" className="btn-primary">Continue to sign in</Link>
      </div>
    );
  }

  return (
    <div className="text-center py-8">
      <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
        <XCircle className="w-8 h-8 text-red-600" />
      </div>
      <h2 className="text-2xl font-display font-bold text-gray-900 mb-2">Verification failed</h2>
      <p className="text-gray-500 mb-6">{message}</p>
      <Link href="/login" className="btn-secondary mr-3">Back to sign in</Link>
    </div>
  );
}

export default function VerifyEmailPage() {
  return (
    <Suspense>
      <VerifyEmailContent />
    </Suspense>
  );
}
