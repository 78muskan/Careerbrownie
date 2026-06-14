export interface User {
  id: string;
  email: string;
  full_name: string;
  phone?: string;
  role: "student" | "counsellor" | "admin" | "school_admin" | "recruiter" | "parent" | "enterprise";
  avatar?: string;
  is_verified: boolean;
  auth_provider: string;
}

export interface AuthTokens {
  access: string;
  refresh: string;
}

export interface AuthResponse extends AuthTokens {
  user: User;
}

export interface LoginPayload {
  email: string;
  password: string;
}

export interface RegisterPayload {
  email: string;
  full_name: string;
  password: string;
  phone?: string;
  role?: "student" | "counsellor";
}
