export interface Instrument {
  id: string;
  name: string;
  slug: string;
}

export interface Course {
  id: string;
  instrument_id: string;
  title: string;
  slug: string;
  description: string | null;
  price_cents: number;
  level: string;
  lesson_count: number | null;
  is_published: boolean;
  created_at: string;
}

export interface Booking {
  id: string;
  student_id: string;
  instrument_id: string;
  starts_at: string;
  ends_at: string;
  status: string;
  price_cents: number;
  notes: string | null;
  stripe_payment_intent_id: string | null;
  daily_room_url: string | null;
  created_at: string;
}

export interface User {
  id: string;
  email: string;
  full_name: string;
  is_admin: boolean;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}