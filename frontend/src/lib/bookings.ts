import api from "./api";
import { Booking } from "@/types";

export async function getMyBookings(): Promise<Booking[]> {
  const response = await api.get<Booking[]>("/api/v1/bookings/my");
  return response.data;
}