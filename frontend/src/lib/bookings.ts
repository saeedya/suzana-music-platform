import api from "./api";
import { Booking } from "@/types";

export async function getMyBookings(): Promise<Booking[]> {
  const response = await api.get<Booking[]>("/api/v1/bookings/my");
  return response.data;
}

export interface CreateBookingPayload {
  instrument_id: string;
  starts_at: string;
  ends_at: string;
  price_cents: number;
  notes?: string;
}

export async function createBooking(
  payload: CreateBookingPayload
): Promise<Booking> {
  const response = await api.post<Booking>("/api/v1/bookings/", payload);
  return response.data;
}

export interface PaymentIntentResponse {
  client_secret: string;
  payment_intent_id: string;
}

export async function createPaymentIntent(
  bookingId: string
): Promise<PaymentIntentResponse> {
  const response = await api.post<PaymentIntentResponse>(
    "/api/v1/payments/create-intent",
    { booking_id: bookingId }
  );
  return response.data;
}