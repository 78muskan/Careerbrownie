"use client";
import { createContext, useContext, useEffect, useState, useCallback, ReactNode } from "react";
import { useRouter } from "next/navigation";
import api from "@/lib/api";
import type { User, LoginPayload, RegisterPayload, AuthResponse } from "@/types/auth";

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (payload: LoginPayload) => Promise<void>;
  register: (payload: RegisterPayload) => Promise<void>;
  logout: () => Promise<void>;
  refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  const refreshUser = useCallback(async () => {
    try {
      const { data } = await api.get("/auth/me/");
      setUser(data);
    } catch {
      setUser(null);
    }
  }, []);

  useEffect(() => {
    const access = localStorage.getItem("access_token");
    if (access) {
      refreshUser().finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, [refreshUser]);

  const setAuthCookie = (set: boolean) => {
    if (set) {
      document.cookie = "mv_auth=1; path=/; max-age=604800; SameSite=Lax";
    } else {
      document.cookie = "mv_auth=; path=/; max-age=0";
    }
  };

  const login = async (payload: LoginPayload) => {
    const { data }: { data: AuthResponse } = await api.post("/auth/login/", payload);
    localStorage.setItem("access_token", data.access);
    localStorage.setItem("refresh_token", data.refresh);
    setAuthCookie(true);
    setUser(data.user);
    if (data.user.role === "student") router.push("/student/dashboard");
    else if (data.user.role === "counsellor") router.push("/counsellor/dashboard");
    else router.push("/admin/dashboard");
  };

  const register = async (payload: RegisterPayload) => {
    const { data }: { data: AuthResponse } = await api.post("/auth/register/", payload);
    localStorage.setItem("access_token", data.access);
    localStorage.setItem("refresh_token", data.refresh);
    setAuthCookie(true);
    setUser(data.user);
    router.push("/student/dashboard");
  };

  const logout = async () => {
    const refresh = localStorage.getItem("refresh_token");
    try {
      if (refresh) await api.post("/auth/logout/", { refresh });
    } catch {
      // best-effort
    } finally {
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      setAuthCookie(false);
      setUser(null);
      router.push("/login");
    }
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout, refreshUser }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
