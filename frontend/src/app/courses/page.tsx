export const dynamic = "force-dynamic";
import { Course } from "@/types";
import Link from "next/link";

async function getCourses(): Promise<Course[]> {
  const res = await fetch(
    `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/v1/courses/`,
    { cache: "no-store" }
  );
  if (!res.ok) return [];
  return res.json();
}

function levelLabel(level: string) {
  const labels: Record<string, string> = {
    beginner: "Beginner",
    intermediate: "Intermediate",
    advanced: "Advanced",
    all: "All levels",
  };
  return labels[level] || level;
}

export default async function CoursesPage() {
  const courses = await getCourses();

  return (
    <main className="max-w-5xl mx-auto px-6 py-12">
      <h1 className="text-3xl font-bold text-gray-900 mb-2">Courses</h1>
      <p className="text-gray-500 mb-10">
        Choose a course and start learning today
      </p>

      {courses.length === 0 ? (
        <div className="text-center py-20 text-gray-400">
          No courses available yet.
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {courses.map((course) => (
            <Link
              key={course.id}
              href={`/courses/${course.slug}`}
              className="bg-white border border-gray-200 rounded-xl p-6 hover:border-violet-300 hover:shadow-md transition-all"
            >
              <div className="flex items-center justify-between mb-3">
                <span className="text-xs bg-violet-100 text-violet-700 px-2 py-1 rounded-full font-medium">
                  {levelLabel(course.level)}
                </span>
                <span className="text-sm font-semibold text-gray-900">
                  ${(course.price_cents / 100).toFixed(2)}
                </span>
              </div>
              <h2 className="text-lg font-semibold text-gray-900 mb-2">
                {course.title}
              </h2>
              {course.description && (
                <p className="text-sm text-gray-500 line-clamp-2">
                  {course.description}
                </p>
              )}
              {course.lesson_count && (
                <p className="text-xs text-gray-400 mt-3">
                  {course.lesson_count} lessons
                </p>
              )}
            </Link>
          ))}
        </div>
      )}
    </main>
  );
}