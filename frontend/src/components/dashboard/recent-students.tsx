"use client";

interface RecentStudentProps {
  students: {
    name: string;
    email: string;
    track: string;
    score: number;
    status: "strong" | "needs_support" | "at_risk";
    lastActive: string;
  }[];
}

export function RecentStudents({ students }: RecentStudentProps) {
  return (
    <div className="rounded-2xl border border-white/[0.06] bg-white/[0.02] p-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-sm font-semibold text-zinc-300">
            Recent Students
          </h3>
          <p className="mt-1 text-xs text-zinc-600">
            Latest activity across batches
          </p>
        </div>
        <button className="rounded-lg border border-white/[0.06] bg-white/[0.03] px-3 py-1.5 text-xs font-medium text-zinc-400 transition-colors hover:bg-white/[0.06] hover:text-zinc-200">
          View all
        </button>
      </div>

      <div className="mt-5">
        <table className="w-full">
          <thead>
            <tr className="border-b border-white/[0.04] text-left text-[11px] font-medium uppercase tracking-wider text-zinc-600">
              <th className="pb-3">Student</th>
              <th className="pb-3">Track</th>
              <th className="pb-3">Evidence</th>
              <th className="pb-3">Status</th>
              <th className="pb-3 text-right">Last Active</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-white/[0.04]">
            {students.map((student) => (
              <tr
                key={student.email}
                className="group transition-colors hover:bg-white/[0.02]"
              >
                <td className="py-3">
                  <div className="flex items-center gap-3">
                    <div className="flex h-8 w-8 items-center justify-center rounded-full bg-gradient-to-br from-violet-500/20 to-indigo-500/20 text-xs font-semibold text-violet-300">
                      {student.name
                        .split(" ")
                        .map((n) => n[0])
                        .join("")}
                    </div>
                    <div>
                      <p className="text-sm font-medium text-zinc-200 group-hover:text-white">
                        {student.name}
                      </p>
                      <p className="text-xs text-zinc-600">{student.email}</p>
                    </div>
                  </div>
                </td>
                <td className="py-3">
                  <span className="rounded-md bg-white/[0.04] px-2 py-1 text-xs font-medium text-zinc-400">
                    {student.track}
                  </span>
                </td>
                <td className="py-3">
                  <div className="flex items-center gap-2">
                    <div className="h-1.5 w-16 overflow-hidden rounded-full bg-white/[0.04]">
                      <div
                        className="h-full rounded-full bg-gradient-to-r from-violet-500 to-indigo-400"
                        style={{ width: `${student.score}%` }}
                      />
                    </div>
                    <span className="text-xs font-semibold text-zinc-300">
                      {student.score}%
                    </span>
                  </div>
                </td>
                <td className="py-3">
                  <span
                    className={`inline-flex items-center gap-1 rounded-full px-2 py-0.5 text-[11px] font-semibold ${
                      student.status === "strong"
                        ? "bg-emerald-500/10 text-emerald-400"
                        : student.status === "needs_support"
                          ? "bg-amber-500/10 text-amber-400"
                          : "bg-rose-500/10 text-rose-400"
                    }`}
                  >
                    <span
                      className={`h-1.5 w-1.5 rounded-full ${
                        student.status === "strong"
                          ? "bg-emerald-400"
                          : student.status === "needs_support"
                            ? "bg-amber-400"
                            : "bg-rose-400"
                      }`}
                    />
                    {student.status === "strong"
                      ? "Strong"
                      : student.status === "needs_support"
                        ? "Needs Support"
                        : "At Risk"}
                  </span>
                </td>
                <td className="py-3 text-right text-xs text-zinc-500">
                  {student.lastActive}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
