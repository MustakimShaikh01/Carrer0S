import {
  GraduationCap,
  School,
  TrendingUp,
  AlertTriangle,
} from "lucide-react";
import { StatCard } from "@/components/dashboard/stat-card";
import { CareerTrackBreakdown } from "@/components/dashboard/career-track-breakdown";
import { InstitutionalGaps } from "@/components/dashboard/institutional-gaps";
import { RecentStudents } from "@/components/dashboard/recent-students";

// ── Demo data (will be replaced with API calls) ───────────────────────
const trackData = [
  { name: "Backend", strong: 312, needsSupport: 47, color: "#8b5cf6" },
  { name: "AI / ML", strong: 184, needsSupport: 63, color: "#6366f1" },
  { name: "Frontend", strong: 267, needsSupport: 39, color: "#a78bfa" },
  { name: "Data Eng.", strong: 153, needsSupport: 51, color: "#818cf8" },
  { name: "DevOps", strong: 98, needsSupport: 28, color: "#c4b5fd" },
  { name: "Full Stack", strong: 134, needsSupport: 22, color: "#7c3aed" },
];

const gapData = [
  { skill: "System Design", percentage: 61, severity: "critical" as const },
  { skill: "DSA (Advanced)", percentage: 54, severity: "critical" as const },
  { skill: "Cloud / DevOps", percentage: 47, severity: "high" as const },
  { skill: "Testing", percentage: 42, severity: "high" as const },
  { skill: "API Design", percentage: 31, severity: "medium" as const },
  { skill: "Databases", percentage: 24, severity: "medium" as const },
];

const recentStudents = [
  { name: "Rahul Sharma", email: "rahul@iitb.ac.in", track: "Backend", score: 82, status: "strong" as const, lastActive: "2 min ago" },
  { name: "Priya Patel", email: "priya@iitb.ac.in", track: "AI/ML", score: 68, status: "needs_support" as const, lastActive: "1 hr ago" },
  { name: "Arjun Mehta", email: "arjun@iitb.ac.in", track: "Frontend", score: 91, status: "strong" as const, lastActive: "15 min ago" },
  { name: "Sneha Gupta", email: "sneha@iitb.ac.in", track: "Data Eng.", score: 34, status: "at_risk" as const, lastActive: "3 days ago" },
  { name: "Vikram Singh", email: "vikram@iitb.ac.in", track: "Backend", score: 56, status: "needs_support" as const, lastActive: "5 hr ago" },
];

export default function DashboardPage() {
  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-white">
          Good evening, Admin
        </h1>
        <p className="mt-1 text-sm text-zinc-500">
          CSE 2027 · IIT Bombay · 1,248 students enrolled
        </p>
      </div>

      {/* Stat Cards */}
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard
          title="Total Students"
          value={1248}
          change="+128 this month"
          changeType="positive"
          icon={GraduationCap}
          gradient="bg-violet-500"
          iconColor="text-violet-400"
        />
        <StatCard
          title="Institutions"
          value={12}
          change="+2 this quarter"
          changeType="positive"
          icon={School}
          gradient="bg-indigo-500"
          iconColor="text-indigo-400"
        />
        <StatCard
          title="Avg. Evidence Score"
          value="67%"
          change="+4.2% this month"
          changeType="positive"
          icon={TrendingUp}
          gradient="bg-emerald-500"
          iconColor="text-emerald-400"
        />
        <StatCard
          title="Needs Intervention"
          value={250}
          change="20% of cohort"
          changeType="negative"
          icon={AlertTriangle}
          gradient="bg-amber-500"
          iconColor="text-amber-400"
        />
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <CareerTrackBreakdown tracks={trackData} />
        <InstitutionalGaps gaps={gapData} />
      </div>

      {/* Recent Students */}
      <RecentStudents students={recentStudents} />

      {/* Quick Actions */}
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
        <button className="group rounded-2xl border border-white/[0.06] bg-white/[0.02] p-5 text-left transition-all duration-300 hover:border-violet-500/20 hover:bg-violet-500/[0.04]">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-violet-500/10 text-violet-400 transition-colors group-hover:bg-violet-500/15">
            <GraduationCap className="h-5 w-5" />
          </div>
          <h3 className="mt-3 text-sm font-semibold text-zinc-200 group-hover:text-white">
            Create Workshop
          </h3>
          <p className="mt-1 text-xs text-zinc-500">
            Schedule a skill-building session for System Design
          </p>
        </button>
        <button className="group rounded-2xl border border-white/[0.06] bg-white/[0.02] p-5 text-left transition-all duration-300 hover:border-indigo-500/20 hover:bg-indigo-500/[0.04]">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-indigo-500/10 text-indigo-400 transition-colors group-hover:bg-indigo-500/15">
            <School className="h-5 w-5" />
          </div>
          <h3 className="mt-3 text-sm font-semibold text-zinc-200 group-hover:text-white">
            Assign Mentors
          </h3>
          <p className="mt-1 text-xs text-zinc-500">
            Pair at-risk students with mentors for 1:1 guidance
          </p>
        </button>
        <button className="group rounded-2xl border border-white/[0.06] bg-white/[0.02] p-5 text-left transition-all duration-300 hover:border-emerald-500/20 hover:bg-emerald-500/[0.04]">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-500/10 text-emerald-400 transition-colors group-hover:bg-emerald-500/15">
            <TrendingUp className="h-5 w-5" />
          </div>
          <h3 className="mt-3 text-sm font-semibold text-zinc-200 group-hover:text-white">
            View Full Report
          </h3>
          <p className="mt-1 text-xs text-zinc-500">
            Download the cohort analytics report for this batch
          </p>
        </button>
      </div>
    </div>
  );
}
