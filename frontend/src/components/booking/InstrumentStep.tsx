"use client";

import { useEffect, useState } from "react";
import { Instrument } from "@/types";
import api from "@/lib/api";

const INSTRUMENT_ICONS: Record<string, string> = {
  cello: "🎻",
  piano: "🎹",
  guitar: "🎸",
  "music-theory": "🎵",
};

export default function InstrumentStep({
  selected,
  onSelect,
}: {
  selected: Instrument | null;
  onSelect: (instrument: Instrument) => void;
}) {
  const [instruments, setInstruments] = useState<Instrument[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .get<Instrument[]>("/api/v1/instruments/")
      .then((res) => setInstruments(res.data))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <p className="text-gray-400 text-center py-12">Loading...</p>;
  }

  return (
    <div>
      <h2 className="text-2xl font-bold text-gray-900 mb-2">
        Choose an instrument
      </h2>
      <p className="text-gray-500 mb-8">
        What would you like to learn?
      </p>

      <div className="grid grid-cols-2 gap-4">
        {instruments.map((instrument) => (
          <button
            key={instrument.id}
            onClick={() => onSelect(instrument)}
            className={`p-6 rounded-xl border-2 text-left transition-all hover:border-violet-300 hover:shadow-md ${
              selected?.id === instrument.id
                ? "border-violet-700 bg-violet-50"
                : "border-gray-200 bg-white"
            }`}
          >
            <div className="text-3xl mb-3">
              {INSTRUMENT_ICONS[instrument.slug] || "🎵"}
            </div>
            <h3 className="font-semibold text-gray-900">{instrument.name}</h3>
          </button>
        ))}
      </div>
    </div>
  );
}