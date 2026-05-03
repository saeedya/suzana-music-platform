"use client";

import Link from "next/link";
import { Music } from "lucide-react";
import { useAuth } from "@/context/AuthContext";
import { useRouter } from "next/navigation";

export default function Navbar() {
  const { user, signout, isLoading } = useAuth();
  const router = useRouter();

  async function handleSignOut() {
    await signout();
    router.push("/");
  }

  return (
    <nav className="bg-white border-b border-gray-200 px-4 py-3">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        {/* Logo */}
        <Link href="/" className="flex items-center gap-2 shrink-0">
          <Music size={20} className="text-violet-700" />
          <span className="text-base font-bold text-violet-700 whitespace-nowrap">
            Music Platform
          </span>
        </Link>

        {/* Navigation */}
        <div className="flex items-center gap-3">
          <Link
            href="/courses"
            className="text-sm text-gray-600 hover:text-violet-700 transition-colors whitespace-nowrap"
          >
            Courses
          </Link>

          {isLoading ? null : user ? (
            <>
              <Link
                href="/dashboard"
                className="text-sm text-gray-600 hover:text-violet-700 transition-colors whitespace-nowrap"
              >
                Dashboard
              </Link>
              <button
                onClick={handleSignOut}
                className="text-sm text-red-500 hover:text-red-700 transition-colors whitespace-nowrap"
              >
                Sign out
              </button>
            </>
          ) : (
            <>
              <Link
                href="/auth/signin"
                className="text-sm text-gray-600 hover:text-violet-700 transition-colors whitespace-nowrap"
              >
                Sign in
              </Link>
              <Link
                href="/auth/signup"
                className="text-sm bg-violet-700 text-white px-3 py-1.5 rounded-lg hover:bg-violet-800 transition-colors whitespace-nowrap"
              >
                Sign up
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}