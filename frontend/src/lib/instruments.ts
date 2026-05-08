import api from "./api";
import { Instrument } from "@/types";

export async function getInstruments(): Promise<Instrument[]> {
  const response = await api.get<Instrument[]>("/api/v1/instruments/");
  return response.data;
}