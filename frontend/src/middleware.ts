import { clerkMiddleware, createRouteMatcher } from "@clerk/nextjs/server";
import { NextResponse } from "next/server";

const isPublicRoute = createRouteMatcher([
  "/sign-in(.*)",
  "/sign-up(.*)",
  "/api/auth(.*)",
]);

const isApiRoute = createRouteMatcher(["/api/(.*)"]);

export default clerkMiddleware(async (auth, request) => {
  // Protect all routes except public ones
  if (!isPublicRoute(request) && !isApiRoute(request)) {
    await auth.protect();
  }
});

export const config = {
  matcher: ["/((?!_next|static|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)"],
};
