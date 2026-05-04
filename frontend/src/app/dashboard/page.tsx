"use client";

import { useEffect, useState } from "react";
import { useAuth } from "@/context/AuthContext";
import { useRouter } from "next/navigation";
import { getMyBookings } from "@/lib/bookings";
import { Booking } from "@/types";
import { Calendar, Video, Clock } from "lucide-react";

function statusColor(status: string) {
  const colors: Record<string, string> = {
    pending: "bg-yellow-100 text-yellow-700",
    confirmed: "bg-green-100 text-green-700",
    cancelled: "bg-red-100 text-red-700",
    completed: "bg-gray-100 text-gray-600",
  };
  return colors[status] || "bg-gray-100 text-gray-600";
}

function formatDate(dateStr: string) {
  return new Date(dateStr).toLocaleDateString("en-US", {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

export default function DashboardPage() {
  const { user, isLoading } = useAuth();
  const router = useRouter();
  const [bookings, setBookings] = useState<Booking[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!isLoading && !user) {
      router.push("/auth/signin");
      return;
    }
    if (user) {
      getMyBookings()
        .then(setBookings)
        .catch(console.error)
        .finally(() => setLoading(false));
    }
  }, [user, isLoading, router]);

  if (isLoading || loading) {
    return (
      <div className="flex items-center justify-center min-h-[calc(100vh-64px)]">
        <p className="text-gray-400">Loading...</p>
      </div>
    );
  }

  const upcoming = bookings.filter(
    (b) => b.status === "confirmed" && new Date(b.starts_at) > new Date()
  );
  const past = bookings.filter(
    (b) => b.status === "completed" || new Date(b.starts_at) < new Date()
  );

  return (
    <main className="max-w-4xl mx-auto px-6 py-12">
      <h1 className="text-3xl font-bold text-gray-900 mb-1">
        Welcome, {user?.full_name}!
      </h1>
      <p className="text-gray-500 mb-10">Manage your lessons and bookings</p>

      {/* Upcoming lessons */}
      <section className="mb-10">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">
          Upcoming lessons
        </h2>
        {upcoming.length === 0 ? (
          <div className="bg-white border border-gray-200 rounded-xl p-8 text-center text-gray-400">
            No upcoming lessons
          </div>
        ) : (
          <div className="space-y-4">
            {upcoming.map((booking) => (
              <div
                key={booking.id}
                className="bg-white border border-gray-200 rounded-xl p-6"
              >
                <div className="flex items-center justify-between mb-3">
                  <span
                    className={`text-xs px-2 py-1 rounded-full font-medium ${statusColor(booking.status)}`}
                  >
                    {booking.status}
                  </span>
                  <span className="text-lg font-semibold text-gray-900">
                    ${(booking.price_cents / 100).toFixed(2)}
                  </span>
                </div>
                <div className="space-y-2">
                  <div className="flex items-center gap-2 text-sm text-gray-600">
                    <Calendar size={16} className="text-violet-700" />
                    <span>{formatDate(booking.starts_at)}</span>
                  </div>
                  <div className="flex items-center gap-2 text-sm text-gray-600">
                    <Clock size={16} className="text-violet-700" />
                    <span>Until {formatDate(booking.ends_at)}</span>
                  </div>
                </div>
                {booking.daily_room_url && (
                  <a
                    href={booking.daily_room_url as string}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="mt-4 flex items-center gap-2 bg-violet-700 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-violet-800 transition-colors w-fit"
                  >
                    <Video size={16} />
                    Join lesson
                  </a>
                )}
              </div>
            ))}
          </div>
        )}
      </section>

      {/* Past lessons */}
      {past.length > 0 && (
        <section>
          <h2 className="text-xl font-semibold text-gray-900 mb-4">
            Past lessons
          </h2>
          <div className="space-y-4">
            {past.map((booking) => (
              <div
                key={booking.id}
                className="bg-white border border-gray-200 rounded-xl p-6 opacity-60"
              >
                <div className="flex items-center justify-between mb-3">
                  <span
                    className={`text-xs px-2 py-1 rounded-full font-medium ${statusColor(booking.status)}`}
                  >
                    {booking.status}
                  </span>
                  <span className="text-lg font-semibold text-gray-900">
                    ${(booking.price_cents / 100).toFixed(2)}
                  </span>
                </div>
                <div className="flex items-center gap-2 text-sm text-gray-600">
                  <Calendar size={16} />
                  <span>{formatDate(booking.starts_at)}</span>
                </div>
              </div>
            ))}
          </div>
        </section>
      )}
    </main>
  );
}