"use client";
import { useState } from "react";
import { Bell, Search } from "lucide-react";
import { useAuth } from "@/contexts/AuthContext";

export default function DashboardTopbar() {
  const { user } = useAuth();
  const [searchOpen, setSearchOpen] = useState(false);

  const greet = () => {
    const h = new Date().getHours();
    if (h < 12) return "Good morning";
    if (h < 17) return "Good afternoon";
    return "Good evening";
  };

  return (
    <header className="h-16 bg-white border-b border-gray-100 flex items-center px-6 gap-4">
      <div className="flex-1">
        <p className="text-sm font-medium text-gray-900">
          {greet()}, {user?.full_name?.split(" ")[0]} 👋
        </p>
      </div>
      <button
        onClick={() => setSearchOpen(!searchOpen)}
        className="p-2 rounded-xl text-gray-500 hover:bg-gray-100"
      >
        <Search className="w-5 h-5" />
      </button>
      <button className="relative p-2 rounded-xl text-gray-500 hover:bg-gray-100">
        <Bell className="w-5 h-5" />
        <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-red-500 rounded-full" />
      </button>
      <div className="w-8 h-8 rounded-full bg-primary-100 flex items-center justify-center text-primary-700 font-bold text-sm">
        {user?.full_name?.[0] ?? "?"}
      </div>
    </header>
  );
}
