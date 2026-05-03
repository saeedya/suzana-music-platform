import api from "./api";
import { AuthResponse } from "@/types";

export interface SignInData {
  email: string;
  password: string;
}

export interface SignUpData {
  email: string;
  password: string;
  full_name: string;
}

export async function signIn(data: SignInData): Promise<AuthResponse> {
  const response = await api.post<AuthResponse>("/api/v1/auth/signin", data);
  return response.data;
}

export async function signUp(data: SignUpData): Promise<AuthResponse> {
  const response = await api.post<AuthResponse>("/api/v1/auth/signup", data);
  return response.data;
}

export async function signOut(token: string): Promise<void> {
  await api.post("/api/v1/auth/signout", { jwt: token });
}