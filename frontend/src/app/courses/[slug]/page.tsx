import { Course } from "@/types";
import { notFound } from "next/navigation";
import { BookOpen, Clock, BarChart } from "lucide-react";
import BookingButton from "@/components/course/BookingButton";

async function getCourse(slug: string): Promise<Course | null> {
  const res = await fetch(
    `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/v1/courses/${slug}`,
    { cache: "no-store" }
  );
  if (!res.ok) return null;
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

export default async function CourseDetailPage({
  params,
}: {
  params: { slug: string };
}) {
  const course = await getCourse(params.slug);
  if (!course) notFound();

  return (
    <main className="max-w-4xl mx-auto px-6 py-12">
      {/* Header */}
      <div className="mb-8">
        <span className="text-xs bg-violet-100 text-violet-700 px-3 py-1 rounded-full font-medium">
          {levelLabel(course.level)}
        </span>
        <h1 className="text-4xl font-bold text-gray-900 mt-4 mb-3">
          {course.title}
        </h1>
        {course.description && (
          <p className="text-lg text-gray-600">{course.description}</p>
        )}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        {/* Course info */}
        <div className="md:col-span-2 space-y-6">
          <div className="bg-white border border-gray-200 rounded-xl p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">
              Course details
            </h2>
            <div className="space-y-3">
              <div className="flex items-center gap-3 text-gray-600">
                <BarChart size={18} className="text-violet-700" />
                <span className="text-sm">Level: {levelLabel(course.level)}</span>
              </div>
              {course.lesson_count && (
                <div className="flex items-center gap-3 text-gray-600">
                  <BookOpen size={18} className="text-violet-700" />
                  <span className="text-sm">{course.lesson_count} lessons</span>
                </div>
              )}
              <div className="flex items-center gap-3 text-gray-600">
                <Clock size={18} className="text-violet-700" />
                <span className="text-sm">Self-paced learning</span>
              </div>
            </div>
          </div>
        </div>

        {/* Booking card */}
        <div className="bg-white border border-gray-200 rounded-xl p-6 h-fit">
          <div className="text-3xl font-bold text-gray-900 mb-1">
            ${(course.price_cents / 100).toFixed(2)}
          </div>
          <p className="text-sm text-gray-500 mb-6">One-time payment</p>
          <BookingButton courseId={course.id} />
        </div>
      </div>
    </main>
  );
}