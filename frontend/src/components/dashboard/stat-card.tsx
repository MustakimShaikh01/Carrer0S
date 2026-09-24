import { cn } from "@/lib/utils";
import type { LucideIcon } from "lucide-react";

interface StatCardProps {
  title: string;
  value: string | number;
  change?: string;
  changeType?: "positive" | "negative" | "neutral";
  icon: LucideIcon;
  gradient: string;
  iconColor: string;
}

export function StatCard({
  title,
  value,
  change,
  changeType = "neutral",
  icon: Icon,
  gradient,
  iconColor,
}: StatCardProps) {
  return (
    <div className="group relative overflow-hidden rounded-2xl border border-white/[0.06] bg-white/[0.02] p-6 transition-all duration-300 hover:border-white/[0.1] hover:bg-white/[0.04]">
      {/* Background gradient glow */}
      <div
        className={cn(
          "absolute -right-8 -top-8 h-24 w-24 rounded-full opacity-20 blur-2xl transition-opacity duration-500 group-hover:opacity-30",
          gradient
        )}
      />

      <div className="relative flex items-start justify-between">
        <div>
          <p className="text-sm font-medium text-zinc-500">{title}</p>
          <p className="mt-2 text-3xl font-bold tracking-tight text-white">
            {typeof value === "number" ? value.toLocaleString() : value}
          </p>
          {change && (
            <p
              className={cn(
                "mt-2 flex items-center gap-1 text-xs font-medium",
                changeType === "positive" && "text-emerald-400",
                changeType === "negative" && "text-rose-400",
                changeType === "neutral" && "text-zinc-500"
              )}
            >
              {changeType === "positive" && "↑"}
              {changeType === "negative" && "↓"}
              {change}
            </p>
          )}
        </div>
        <div
          className={cn(
            "flex h-10 w-10 items-center justify-center rounded-xl border border-white/[0.06]",
            "bg-white/[0.03] transition-colors group-hover:bg-white/[0.06]"
          )}
        >
          <Icon className={cn("h-5 w-5", iconColor)} />
        </div>
      </div>
    </div>
  );
}
