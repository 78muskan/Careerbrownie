import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

const PROTECTED_PREFIXES = ["/student", "/counsellor", "/admin"];
const AUTH_ROUTES = ["/login", "/register", "/forgot-password"];

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  // Tokens live in localStorage (client-side), so we use a cookie set by the client
  // as a lightweight signal. The real auth check happens in the API layer.
  const isLoggedIn = request.cookies.has("mv_auth");

  const isProtected = PROTECTED_PREFIXES.some((p) => pathname.startsWith(p));
  const isAuthPage = AUTH_ROUTES.some((r) => pathname.startsWith(r));

  if (isProtected && !isLoggedIn) {
    const url = request.nextUrl.clone();
    url.pathname = "/login";
    url.searchParams.set("next", pathname);
    return NextResponse.redirect(url);
  }

  if (isAuthPage && isLoggedIn) {
    return NextResponse.redirect(new URL("/student/dashboard", request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/student/:path*", "/counsellor/:path*", "/admin/:path*", "/login", "/register", "/forgot-password"],
};
