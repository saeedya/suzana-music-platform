import api from "./api";
import { Course } from "@/types";

export async function getCourseById(courseId: string): Promise<Course | null> {
  try {
    const response = await api.get<Course>(`/api/v1/courses/id/${courseId}`);
    return response.data;
  } catch {
    return null;
  }
}