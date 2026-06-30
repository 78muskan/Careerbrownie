"use client";

import { useState } from "react";
import { Sparkles, X } from "lucide-react";
import dynamic from "next/dynamic";

const ChatWidget = dynamic(() => import("./ChatWidget"), { ssr: false });

export default function FloatingChatButton() {
  const [open, setOpen] = useState(false);

  return (
    <>
      <ChatWidget open={open} onClose={() => setOpen(false)} />

      {/* FAB — hidden when chat is open on mobile */}
      {!open && (
        <button
          onClick={() => setOpen(true)}
          aria-label="Open AI Career Chat"
          className="fixed bottom-6 right-6 z-40 flex items-center gap-2 bg-gradient-to-r from-violet-600 to-purple-700 text-white shadow-lg shadow-violet-500/30 hover:shadow-violet-500/50 hover:scale-105 transition-all px-4 py-3 rounded-2xl font-semibold text-sm"
        >
          <Sparkles className="w-4 h-4" />
          <span className="hidden sm:inline">Ask AI Counsellor</span>
          <span className="sm:hidden">AI Chat</span>
        </button>
      )}
    </>
  );
}
