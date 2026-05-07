import api from "./api";

export interface Slot {
  starts_at: string;
  ends_at: string;
  local_time: string;
}

export async function getAvailableSlots(
  date: string,
  sessionDuration: number
): Promise<Slot[]> {
  const response = await api.get<Slot[]>("/api/v1/availability/slots", {
    params: {
      target_date: date,
      session_duration: sessionDuration,
    },
  });
  return response.data;
}