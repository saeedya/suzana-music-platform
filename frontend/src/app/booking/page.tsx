"use client";

import { useEffect, useState } from "react";
import { useAuth } from "@/context/AuthContext";
import { useRouter, useSearchParams } from "next/navigation";
import { Instrument } from "@/types";
import InstrumentStep from "@/components/booking/InstrumentStep";
import DurationStep from "@/components/booking/DurationStep";
import SlotStep from "@/components/booking/SlotStep";
import { getCourseById } from "@/lib/courses";
import { getInstruments } from "@/lib/instruments";

const STEPS = ["Instrument", "Duration", "Date & Time", "Payment"];

export default function BookingPage() {
  const { user, isLoading } = useAuth();
  const router = useRouter();
  const searchParams = useSearchParams();
  const courseId = searchParams.get("courseId");

  const [step, setStep] = useState(0);
  const [selectedInstrument, setSelectedInstrument] =
    useState<Instrument | null>(null);
  const [selectedDuration, setSelectedDuration] = useState<30 | 60 | null>(
    null
  );
  const [selectedSlot, setSelectedSlot] = useState<{
    starts_at: string;
    ends_at: string;
  } | null>(null);
  const [isResolving, setIsResolving] = useState(!!courseId);

  useEffect(() => {
    if (!courseId) return;

    async function resolveInstrumentFromCourse() {
      try {
        const course = await getCourseById(courseId!);
        if (!course) {
          setIsResolving(false);
          return;
        }

        const instruments = await getInstruments();
        const instrument = instruments.find(
          (i) => i.id === course.instrument_id
        );

        if (instrument) {
          setSelectedInstrument(instrument);
          setStep(1);
        }
      } catch {
        // Ignore errors, just don't pre-select anything
      } finally {
        setIsResolving(false);
      }
    }

    resolveInstrumentFromCourse();
  }, [courseId]);

  if (!isLoading && !user) {
    router.push("/auth/signin");
    return null;
  }

  if (isResolving) {
    return (
      <main className="max-w-2xl mx-auto px-6 py-12">
        <p className="text-center text-gray-400">Loading...</p>
      </main>
    );
  }

  function nextStep() {
    setStep((s) => s + 1);
  }

  function prevStep() {
    setStep((s) => s - 1);
  }

  return (
    <main className="max-w-2xl mx-auto px-6 py-12">
      {/* Progress bar */}
      <div className="mb-10">
        <div className="flex items-center justify-between mb-2">
          {STEPS.map((label, i) => (
            <div key={label} className="flex items-center">
              <div
                className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium transition-colors ${
                  i <= step
                    ? "bg-violet-700 text-white"
                    : "bg-gray-200 text-gray-500"
                }`}
              >
                {i + 1}
              </div>
              {i < STEPS.length - 1 && (
                <div
                  className={`h-1 w-16 mx-1 transition-colors ${
                    i < step ? "bg-violet-700" : "bg-gray-200"
                  }`}
                />
              )}
            </div>
          ))}
        </div>
        <p className="text-sm text-gray-500 mt-2">
          Step {step + 1} of {STEPS.length} — {STEPS[step]}
        </p>
      </div>

      {/* Steps */}
      {step === 0 && (
        <InstrumentStep
          selected={selectedInstrument}
          onSelect={(instrument) => {
            setSelectedInstrument(instrument);
            nextStep();
          }}
        />
      )}

      {step === 1 && (
        <DurationStep
          selected={selectedDuration}
          onSelect={(duration) => {
            setSelectedDuration(duration);
            nextStep();
          }}
          onBack={prevStep}
        />
      )}

      {step === 2 && selectedDuration && (
        <SlotStep
          duration={selectedDuration}
          onSelect={(slot) => {
            setSelectedSlot(slot);
            nextStep();
          }}
          onBack={prevStep}
        />
      )}

      {step === 3 && (
        <div className="text-center py-12">
          <p className="text-gray-500">Payment step coming soon...</p>
        </div>
      )}
    </main>
  );
}