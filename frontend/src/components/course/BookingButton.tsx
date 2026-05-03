"use client";

import { useAuth } from "@/context/AuthContext";
import { useRouter } from "next/navigation";

export default function BookingButton({ courseId }: { courseId: string }) {
  const { user } = useAuth();
  const router = useRouter();

  function handleClick() {
    if (!user) {
      router.push("/auth/signin");
      return;
    }
    router.push(`/booking?courseId=${courseId}`);
  }

  return (
    <button
      onClick={handleClick}
      className="w-full bg-violet-700 text-white py-3 rounded-lg font-medium hover:bg-violet-800 transition-colors"
    >
      {user ? "Book this course" : "Sign in to book"}
    </button>
  );
}