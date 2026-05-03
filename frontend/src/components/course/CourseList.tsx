"use client";

import { useState } from "react";
import Link from "next/link";
import { Course, Instrument } from "@/types";

function levelLabel(level: string) {
  const labels: Record<string, string> = {
    beginner: "Beginner",
    intermediate: "Intermediate",
    advanced: "Advanced",
    all: "All levels",
  };
  return labels[level] || level;
}

export default function CourseList({
  courses,
  instruments,
}: {
  courses: Course[];
  instruments: Instrument[];
}) {
  const [selected, setSelected] = useState<string | null>(null);

  const filtered = selected
    ? courses.filter((c) => c.instrument_id === selected)
    : courses;

  return (
    <div>
      {/* Filter tabs */}
      <div className="flex gap-2 flex-wrap mb-8">
        <button
          onClick={() => setSelected(null)}
          className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
            selected === null
              ? "bg-violet-700 text-white"
              : "bg-gray-100 text-gray-600 hover:bg-gray-200"
          }`}
        >
          All
        </button>
        {instruments.map((instrument) => (
          <button
            key={instrument.id}
            onClick={() => setSelected(instrument.id)}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              selected === instrument.id
                ? "bg-violet-700 text-white"
                : "bg-gray-100 text-gray-600 hover:bg-gray-200"
            }`}
          >
            {instrument.name}
          </button>
        ))}
      </div>

      {/* Course grid */}
      {filtered.length === 0 ? (
        <div className="text-center py-20 text-gray-400">
          No courses available yet.
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filtered.map((course) => (
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
    </div>
  );
}