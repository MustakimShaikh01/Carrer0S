"use client";

interface SkillGapProps {
  gaps: {
    skill: string;
    percentage: number;
    severity: "critical" | "high" | "medium";
  }[];
}

export function InstitutionalGaps({ gaps }: SkillGapProps) {
  return (
    <div className="rounded-2xl border border-white/[0.06] bg-white/[0.02] p-6">
      <h3 className="text-sm font-semibold text-zinc-300">
        Top Institutional Gaps
      </h3>
      <p className="mt-1 text-xs text-zinc-600">
        % of students missing this skill
      </p>

      <div className="mt-6 space-y-3">
        {gaps.map((gap) => (
          <div key={gap.skill} className="group">
            <div className="mb-1.5 flex items-center justify-between">
              <span className="text-sm font-medium text-zinc-300">
                {gap.skill}
              </span>
              <div className="flex items-center gap-2">
                <span
                  className={`rounded-md px-1.5 py-0.5 text-[10px] font-semibold uppercase ${
                    gap.severity === "critical"
                      ? "bg-rose-500/10 text-rose-400"
                      : gap.severity === "high"
                        ? "bg-amber-500/10 text-amber-400"
                        : "bg-zinc-500/10 text-zinc-400"
                  }`}
                >
                  {gap.severity}
                </span>
                <span className="min-w-[3ch] text-right text-sm font-semibold text-zinc-200">
                  {gap.percentage}%
                </span>
              </div>
            </div>
            <div className="h-1.5 overflow-hidden rounded-full bg-white/[0.04]">
              <div
                className={`h-full rounded-full transition-all duration-700 group-hover:opacity-80 ${
                  gap.severity === "critical"
                    ? "bg-gradient-to-r from-rose-500 to-rose-400"
                    : gap.severity === "high"
                      ? "bg-gradient-to-r from-amber-500 to-amber-400"
                      : "bg-gradient-to-r from-zinc-500 to-zinc-400"
                }`}
                style={{ width: `${gap.percentage}%` }}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
