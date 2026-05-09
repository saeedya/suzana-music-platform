"use client";

import { useEffect, useState } from "react";
import {
  Elements,
  PaymentElement,
  useElements,
  useStripe,
} from "@stripe/react-stripe-js";
import { loadStripe } from "@stripe/stripe-js";
import { Instrument } from "@/types";
import { createBooking, createPaymentIntent } from "@/lib/bookings";
import { Loader2, Lock } from "lucide-react";

const stripePromise = loadStripe(
  process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY!
);

const PRICE_CENTS: Record<30 | 60, number> = {
  30: 3500,
  60: 6500,
};

function formatPrice(cents: number): string {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
  }).format(cents / 100);
}

function formatSlot(starts_at: string, ends_at: string): string {
  const start = new Date(starts_at);
  const end = new Date(ends_at);
  const date = start.toLocaleDateString("en-US", {
    weekday: "long",
    month: "long",
    day: "numeric",
  });
  const startTime = start.toLocaleTimeString("en-US", {
    hour: "2-digit",
    minute: "2-digit",
  });
  const endTime = end.toLocaleTimeString("en-US", {
    hour: "2-digit",
    minute: "2-digit",
    timeZoneName: "short",
  });
  return `${date} · ${startTime}–${endTime}`;
}

interface CheckoutFormProps {
  bookingId: string;
  priceCents: number;
  onSuccess: (bookingId: string) => void;
}

function CheckoutForm({ bookingId, priceCents, onSuccess }: CheckoutFormProps) {
  const stripe = useStripe();
  const elements = useElements();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!stripe || !elements) return;

    setIsSubmitting(true);
    setErrorMessage(null);

    const { error } = await stripe.confirmPayment({
      elements,
      redirect: "if_required",
    });

    if (error) {
      setErrorMessage(error.message ?? "Payment failed. Please try again.");
      setIsSubmitting(false);
      return;
    }

    onSuccess(bookingId);
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <PaymentElement />

      {errorMessage && (
        <div className="rounded-lg bg-red-50 border border-red-200 px-4 py-3 text-sm text-red-700">
          {errorMessage}
        </div>
      )}

      <button
        type="submit"
        disabled={!stripe || isSubmitting}
        className="w-full flex items-center justify-center gap-2 rounded-xl bg-violet-700 px-6 py-3.5 text-white font-medium transition hover:bg-violet-800 disabled:opacity-60 disabled:cursor-not-allowed"
      >
        {isSubmitting ? (
          <>
            <Loader2 className="w-4 h-4 animate-spin" />
            Processing…
          </>
        ) : (
          <>
            <Lock className="w-4 h-4" />
            Pay {formatPrice(priceCents)}
          </>
        )}
      </button>

      <p className="text-center text-xs text-gray-400 flex items-center justify-center gap-1">
        <Lock className="w-3 h-3" />
        Secured by Stripe · 256-bit SSL encryption
      </p>
    </form>
  );
}

interface PaymentStepProps {
  instrument: Instrument;
  duration: 30 | 60;
  slot: { starts_at: string; ends_at: string };
  onSuccess: (bookingId: string) => void;
  onBack: () => void;
}

export default function PaymentStep({
  instrument,
  duration,
  slot,
  onSuccess,
  onBack,
}: PaymentStepProps) {
  const [clientSecret, setClientSecret] = useState<string | null>(null);
  const [bookingId, setBookingId] = useState<string | null>(null);
  const [isInitializing, setIsInitializing] = useState(true);
  const [initError, setInitError] = useState<string | null>(null);

  const priceCents = PRICE_CENTS[duration];

  useEffect(() => {
    async function init() {
      try {
        const booking = await createBooking({
          instrument_id: instrument.id,
          starts_at: slot.starts_at,
          ends_at: slot.ends_at,
          price_cents: priceCents,
        });

        const intent = await createPaymentIntent(booking.id);
        setBookingId(booking.id);
        setClientSecret(intent.client_secret);
      } catch {
        setInitError(
          "Could not initialise payment. Please go back and try again."
        );
      } finally {
        setIsInitializing(false);
      }
    }
    init();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div className="space-y-6">
      {/* Booking summary */}
      <div className="rounded-xl border border-gray-200 bg-gray-50 p-5 space-y-3">
        <h2 className="text-sm font-semibold uppercase tracking-wide text-gray-500">
          Booking summary
        </h2>
        <div className="flex items-start justify-between gap-4">
          <div className="space-y-1">
            <p className="font-semibold text-gray-900 capitalize">
              {instrument.name} lesson · {duration} min
            </p>
            <p className="text-sm text-gray-500">
              {formatSlot(slot.starts_at, slot.ends_at)}
            </p>
          </div>
          <span className="text-lg font-bold text-violet-700 whitespace-nowrap">
            {formatPrice(priceCents)}
          </span>
        </div>
      </div>

      {/* Payment form */}
      {isInitializing && (
        <div className="flex flex-col items-center justify-center py-16 gap-3 text-gray-400">
          <Loader2 className="w-6 h-6 animate-spin" />
          <p className="text-sm">Setting up payment…</p>
        </div>
      )}

      {initError && (
        <div className="rounded-lg bg-red-50 border border-red-200 px-4 py-4 text-sm text-red-700">
          {initError}
        </div>
      )}

      {clientSecret && bookingId && (
        <Elements
          stripe={stripePromise}
          options={{
            clientSecret,
            appearance: {
              theme: "stripe",
              variables: {
                colorPrimary: "#6d28d9",
                borderRadius: "10px",
                fontFamily: "inherit",
              },
            },
          }}
        >
          <CheckoutForm bookingId={bookingId} priceCents={priceCents} onSuccess={onSuccess} />
        </Elements>
      )}

      {!isInitializing && (
        <button
          type="button"
          onClick={onBack}
          disabled={!!clientSecret}
          className="w-full rounded-xl border border-gray-200 py-3 text-sm text-gray-500 transition hover:bg-gray-50 disabled:opacity-40 disabled:cursor-not-allowed"
        >
          ← Back
        </button>
      )}
    </div>
  );
}