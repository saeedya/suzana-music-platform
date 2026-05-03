import Link from "next/link";
import { Music, Video, Calendar } from "lucide-react";

export default function HomePage() {
  return (
    <main>
      {/* Hero section */}
      <section className="bg-violet-700 py-24 px-6 text-center">
        <Music size={48} className="mx-auto mb-6 text-white opacity-80" />
        <h1 className="text-5xl font-bold text-white mb-4">
          Learn Music Online
        </h1>
        <p className="text-xl text-white opacity-80 mb-10 max-w-xl mx-auto">
          Private lessons in Cello, Piano, Guitar and Music Theory with a
          professional instructor with 30+ years of experience.
        </p>
        <div className="flex gap-4 justify-center">
          <Link
            href="/courses"
            className="bg-amber-400 text-amber-900 px-8 py-3 rounded-lg font-medium hover:bg-amber-300 transition-colors"
          >
            Browse Courses
          </Link>
          <Link
            href="/auth/signup"
            className="bg-white text-violet-700 px-8 py-3 rounded-lg font-medium hover:bg-gray-100 transition-colors"
          >
            Get Started
          </Link>
        </div>
      </section>

      {/* Features section */}
      <section className="py-20 px-6 max-w-5xl mx-auto">
        <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
          Everything you need to learn music
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {[
            {
              icon: <Music size={32} className="text-violet-700" />,
              title: "Expert Instructor",
              desc: "30+ years of professional experience in Cello, Piano, Guitar and Music Theory",
            },
            {
              icon: <Video size={32} className="text-violet-700" />,
              title: "Live Video Lessons",
              desc: "High quality video lessons from the comfort of your home",
            },
            {
              icon: <Calendar size={32} className="text-violet-700" />,
              title: "Flexible Scheduling",
              desc: "Book lessons at times that work for you, anywhere in the world",
            },
          ].map((feature) => (
            <div
              key={feature.title}
              className="bg-white p-6 rounded-xl border border-gray-200"
            >
              <div className="mb-4">{feature.icon}</div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                {feature.title}
              </h3>
              <p className="text-sm text-gray-600">{feature.desc}</p>
            </div>
          ))}
        </div>
      </section>
    </main>
  );
}