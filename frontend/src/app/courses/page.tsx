export const dynamic = "force-dynamic";

import { Course, Instrument } from "@/types";
import CourseList from "@/components/course/CourseList";

async function getCourses(): Promise<Course[]> {
  const res = await fetch(
    `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/v1/courses/`,
    { cache: "no-store" }
  );
  if (!res.ok) return [];
  return res.json();
}

async function getInstruments(): Promise<Instrument[]> {
  const res = await fetch(
    `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/v1/instruments/`,
    { cache: "no-store" }
  );
  if (!res.ok) return [];
  return res.json();
}

export default async function CoursesPage() {
  const [courses, instruments] = await Promise.all([
    getCourses(),
    getInstruments(),
  ]);

  return (
    <main className="max-w-5xl mx-auto px-6 py-12">
      <h1 className="text-3xl font-bold text-gray-900 mb-2">Courses</h1>
      <p className="text-gray-500 mb-10">
        Choose a course and start learning today
      </p>
      <CourseList courses={courses} instruments={instruments} />
    </main>
  );
}