"use client";

import { useEffect, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { Booking } from "@/types";
import api from "@/lib/api";
import {
  CheckCircle2,
  Calendar,
  Clock,
  Music,
  Loader2,
  Video,
} from "lucide-react";

function formatDateTime(iso: string): { date: string; time: string } {
  const d = new Date(iso);
  return {
    date: d.toLocaleDateString("en-US", {
      weekday: "long",
      month: "long",
      day: "numeric",
      year: "numeric",
    }),
    time: d.toLocaleTimeString("en-US", {
      hour: "2-digit",
      minute: "2-digit",
      timeZoneName: "short",
    }),
  };
}

export default function ConfirmationPage() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const bookingId = searchParams.get("bookingId");

  const [booking, setBooking] = useState<Booking | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!bookingId) {
      router.replace("/");
      return;
    }

    async function fetchBooking() {
      try {
        const res = await api.get<Booking>(
          `/api/v1/bookings/my/${bookingId}`
        );
        setBooking(res.data);
      } catch {
        setError("Could not load your booking details.");
      } finally {
        setIsLoading(false);
      }
    }

    fetchBooking();
  }, [bookingId, router]);

  if (isLoading) {
    return (
      <main className="max-w-lg mx-auto px-6 py-24 flex flex-col items-center gap-4 text-gray-400">
        <Loader2 className="w-8 h-8 animate-spin" />
        <p className="text-sm">Loading your booking…</p>
      </main>
    );
  }

  if (error || !booking) {
    return (
      <main className="max-w-lg mx-auto px-6 py-24 text-center space-y-4">
        <p className="text-red-600">{error ?? "Booking not found."}</p>
        <button
          onClick={() => router.push("/")}
          className="text-sm text-violet-700 underline"
        >
          Go home
        </button>
      </main>
    );
  }

  const start = formatDateTime(booking.starts_at);
  const end = new Date(booking.ends_at).toLocaleTimeString("en-US", {
    hour: "2-digit",
    minute: "2-digit",
    timeZoneName: "short",
  });
  const durationMin = Math.round(
    (new Date(booking.ends_at).getTime() -
      new Date(booking.starts_at).getTime()) /
      60000
  );
  const price = new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
  }).format(booking.price_cents / 100);

  return (
    <main className="max-w-lg mx-auto px-6 py-16 space-y-8">
      <div className="text-center space-y-3">
        <div className="flex justify-center">
          <CheckCircle2
            className="w-14 h-14 text-green-500"
            strokeWidth={1.5}
          />
        </div>
        <h1 className="text-2xl font-bold text-gray-900">
          You&apos;re booked!
        </h1>
        <p className="text-gray-500 text-sm">
          A confirmation email has been sent to you. See you at the lesson!
        </p>
      </div>

      <div className="rounded-2xl border border-gray-200 divide-y divide-gray-100 overflow-hidden">
        <div className="flex items-center gap-3 px-5 py-4">
          <Calendar className="w-5 h-5 text-violet-600 flex-shrink-0" />
          <div>
            <p className="text-sm font-medium text-gray-900">{start.date}</p>
            <p className="text-xs text-gray-500">
              {start.time} – {end}
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3 px-5 py-4">
          <Clock className="w-5 h-5 text-violet-600 flex-shrink-0" />
          <p className="text-sm text-gray-700">{durationMin} minute lesson</p>
        </div>

        <div className="flex items-center gap-3 px-5 py-4">
          <Music className="w-5 h-5 text-violet-600 flex-shrink-0" />
          <p className="text-sm text-gray-700">
            Booking #{booking.id.slice(0, 8).toUpperCase()}
          </p>
        </div>

        <div className="flex items-center justify-between px-5 py-4">
          <span className="text-sm text-gray-500">Total paid</span>
          <span className="text-sm font-semibold text-gray-900">{price}</span>
        </div>
      </div>

      {booking.daily_room_url && (
        <a
          href={booking.daily_room_url}
          target="_blank"
          rel="noopener noreferrer"
          className="flex items-center justify-center gap-2 w-full rounded-xl bg-violet-700 px-6 py-3.5 text-white font-medium hover:bg-violet-800 transition"
        >
          <Video className="w-4 h-4" />
          Join lesson
        </a>
      )}

      <button
        onClick={() => router.push("/")}
        className="w-full rounded-xl border border-gray-200 py-3 text-sm text-gray-500 hover:bg-gray-50 transition"
      >
        Back to home
      </button>
    </main>
  );
}