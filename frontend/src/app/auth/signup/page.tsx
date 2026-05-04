"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import { Music, Eye, EyeOff } from "lucide-react";

function validatePassword(password: string): string | null {
  if (password.length < 8) return "At least 8 characters required";
  if (!/[A-Z]/.test(password)) return "At least one uppercase letter required";
  if (!/[0-9]/.test(password)) return "At least one number required";
  if (!/[!@#$%^&*]/.test(password)) return "At least one special character (!@#$%^&*) required";
  return null;
}

export default function SignUpPage() {
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const { signup } = useAuth();
  const router = useRouter();

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");

    const passwordError = validatePassword(password);
    if (passwordError) {
      setError(passwordError);
      return;
    }

    setIsLoading(true);
    try {
      await signup({ full_name: fullName, email, password });
      router.push("/dashboard");
    } catch {
      setError("Something went wrong. Please try again.");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="flex min-h-[calc(100vh-64px)]">
      <div className="hidden lg:flex flex-1 flex-col items-center justify-center bg-violet-700 p-12">
        <Music size={56} className="text-white opacity-80 mb-6" />
        <h2 className="text-3xl font-bold text-white mb-3">Start learning</h2>
        <p className="text-white opacity-70 text-center max-w-xs">
          Join students from around the world learning music online
        </p>
      </div>

      <div className="flex flex-1 items-center justify-center p-8">
        <div className="w-full max-w-md">
          <h1 className="text-2xl font-bold text-gray-900 mb-1">
            Create account
          </h1>
          <p className="text-gray-500 text-sm mb-8">
            Start your musical journey today
          </p>

          {error && (
            <div className="bg-red-50 text-red-600 text-sm px-4 py-3 rounded-lg mb-6">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-5">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Full name
              </label>
              <input
                type="text"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                required
                placeholder="John Doe"
                className="w-full border border-gray-300 rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-violet-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Email
              </label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                placeholder="you@example.com"
                className="w-full border border-gray-300 rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-violet-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Password
              </label>
              <div className="relative">
                <input
                  type={showPassword ? "text" : "password"}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  placeholder="••••••••"
                  className="w-full border border-gray-300 rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-violet-500 pr-10"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
                >
                  {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                </button>
              </div>
              <p className="text-xs text-gray-400 mt-1">
                Min 8 chars, uppercase, number, special character (!@#$%^&*)
              </p>
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="w-full bg-violet-700 text-white py-2.5 rounded-lg text-sm font-medium hover:bg-violet-800 transition-colors disabled:opacity-50"
            >
              {isLoading ? "Creating account..." : "Create account"}
            </button>
          </form>

          <p className="mt-6 text-center text-sm text-gray-500">
            Already have an account?{" "}
            <Link href="/auth/signin" className="text-violet-700 hover:underline font-medium">
              Sign in
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}