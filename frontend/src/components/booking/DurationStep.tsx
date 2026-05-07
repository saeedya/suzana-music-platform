"use client";

import { Clock } from "lucide-react";

export default function DurationStep({
  selected,
  onSelect,
  onBack,
}: {
  selected: 30 | 60 | null;
  onSelect: (duration: 30 | 60) => void;
  onBack: () => void;
}) {
  const options = [
    {
      duration: 30 as const,
      label: "30 minutes",
      desc: "Quick focused lesson — great for beginners",
    },
    {
      duration: 60 as const,
      label: "60 minutes",
      desc: "Full lesson — recommended for all levels",
    },
  ];

  return (
    <div>
      <h2 className="text-2xl font-bold text-gray-900 mb-2">
        Session duration
      </h2>
      <p className="text-gray-500 mb-8">How long would you like your lesson?</p>

      <div className="space-y-4 mb-8">
        {options.map(({ duration, label, desc }) => (
          <button
            key={duration}
            onClick={() => onSelect(duration)}
            className={`w-full p-6 rounded-xl border-2 text-left transition-all hover:border-violet-300 hover:shadow-md ${
              selected === duration
                ? "border-violet-700 bg-violet-50"
                : "border-gray-200 bg-white"
            }`}
          >
            <div className="flex items-center gap-4">
              <div className="bg-violet-100 p-3 rounded-lg">
                <Clock size={24} className="text-violet-700" />
              </div>
              <div>
                <h3 className="font-semibold text-gray-900">{label}</h3>
                <p className="text-sm text-gray-500">{desc}</p>
              </div>
            </div>
          </button>
        ))}
      </div>

      <button
        onClick={onBack}
        className="text-sm text-gray-500 hover:text-gray-700 transition-colors"
      >
        ← Back
      </button>
    </div>
  );
}