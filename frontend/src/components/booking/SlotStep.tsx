"use client";

import { useState } from "react";
import { getAvailableSlots, Slot } from "@/lib/availability";
import { Calendar, Clock } from "lucide-react";

function formatDate(dateStr: string): string {
  return new Date(dateStr).toLocaleDateString("en-US", {
    weekday: "long",
    month: "long",
    day: "numeric",
  });
}

function formatLocalTime(slot: Slot): string {
  return new Date(slot.starts_at).toLocaleTimeString("en-US", {
    hour: "2-digit",
    minute: "2-digit",
    timeZoneName: "short",
  });
}

export default function SlotStep({
  duration,
  onSelect,
  onBack,
}: {
  duration: 30 | 60;
  onSelect: (slot: { starts_at: string; ends_at: string }) => void;
  onBack: () => void;
}) {
  const [selectedDate, setSelectedDate] = useState<string>("");
  const [slots, setSlots] = useState<Slot[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleDateChange(date: string) {
    setSelectedDate(date);
    setSlots([]);
    setError("");
    setLoading(true);
    try {
      const result = await getAvailableSlots(date, duration);
      setSlots(result);
      if (result.length === 0) {
        setError("No available slots for this date. Please try another day.");
      }
    } catch {
      setError("Failed to load slots. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  // Minimum date: tomorrow
  const tomorrow = new Date();
  tomorrow.setDate(tomorrow.getDate() + 1);
  const minDate = tomorrow.toISOString().split("T")[0];

  return (
    <div>
      <h2 className="text-2xl font-bold text-gray-900 mb-2">
        Pick a date & time
      </h2>
      <p className="text-gray-500 mb-8">
        Times shown in your local timezone
      </p>

      {/* Date picker */}
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          <Calendar size={16} className="inline mr-2 text-violet-700" />
          Select a date
        </label>
        <input
          type="date"
          min={minDate}
          value={selectedDate}
          onChange={(e) => handleDateChange(e.target.value)}
          className="w-full border border-gray-300 rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-violet-500"
        />
      </div>

      {/* Slots */}
      {loading && (
        <p className="text-gray-400 text-center py-8">Loading slots...</p>
      )}

      {error && (
        <div className="bg-red-50 text-red-600 text-sm px-4 py-3 rounded-lg mb-4">
          {error}
        </div>
      )}

      {slots.length > 0 && (
        <div>
          <p className="text-sm font-medium text-gray-700 mb-3">
            <Clock size={16} className="inline mr-2 text-violet-700" />
            Available slots for {formatDate(selectedDate)}
          </p>
          <div className="grid grid-cols-3 gap-3 mb-8">
            {slots.map((slot) => (
              <button
                key={slot.starts_at}
                onClick={() => onSelect(slot)}
                className="p-3 rounded-lg border-2 border-gray-200 bg-white text-sm font-medium text-gray-700 hover:border-violet-300 hover:bg-violet-50 transition-all"
              >
                {formatLocalTime(slot)}
              </button>
            ))}
          </div>
        </div>
      )}

      <button
        onClick={onBack}
        className="text-sm text-gray-500 hover:text-gray-700 transition-colors"
      >
        ← Back
      </button>
    </div>
  );
}