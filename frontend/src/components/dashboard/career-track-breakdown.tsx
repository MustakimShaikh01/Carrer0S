"use client";

interface CareerTrackBarProps {
  tracks: {
    name: string;
    strong: number;
    needsSupport: number;
    color: string;
  }[];
}

export function CareerTrackBreakdown({ tracks }: CareerTrackBarProps) {
  const maxTotal = Math.max(...tracks.map((t) => t.strong + t.needsSupport));

  return (
    <div className="rounded-2xl border border-white/[0.06] bg-white/[0.02] p-6">
      <h3 className="text-sm font-semibold text-zinc-300">
        Career Track Breakdown
      </h3>
      <p className="mt-1 text-xs text-zinc-600">
        Strong vs. needs support by track
      </p>

      <div className="mt-6 space-y-4">
        {tracks.map((track) => {
          const total = track.strong + track.needsSupport;
          const strongPct = (track.strong / maxTotal) * 100;
          const needsPct = (track.needsSupport / maxTotal) * 100;

          return (
            <div key={track.name} className="group">
              <div className="mb-2 flex items-center justify-between text-xs">
                <span className="font-medium text-zinc-300">{track.name}</span>
                <span className="text-zinc-500">
                  <span className="text-zinc-300">{track.strong}</span>
                  {" / "}
                  <span className="text-amber-400">{track.needsSupport}</span>
                  <span className="ml-1 text-zinc-600">({total})</span>
                </span>
              </div>
              <div className="flex h-2 gap-0.5 overflow-hidden rounded-full bg-white/[0.03]">
                <div
                  className="rounded-l-full transition-all duration-500 group-hover:opacity-90"
                  style={{
                    width: `${strongPct}%`,
                    backgroundColor: track.color,
                  }}
                />
                <div
                  className="rounded-r-full bg-amber-500/40 transition-all duration-500 group-hover:bg-amber-500/50"
                  style={{ width: `${needsPct}%` }}
                />
              </div>
            </div>
          );
        })}
      </div>

      <div className="mt-6 flex items-center gap-4 text-[11px] text-zinc-500">
        <div className="flex items-center gap-1.5">
          <div className="h-2 w-2 rounded-full bg-violet-500" />
          Strong evidence
        </div>
        <div className="flex items-center gap-1.5">
          <div className="h-2 w-2 rounded-full bg-amber-500/50" />
          Needs support
        </div>
      </div>
    </div>
  );
}
