"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  BarChart3,
  GraduationCap,
  Home,
  LogOut,
  School,
  Settings,
  Users,
} from "lucide-react";
import { cn } from "@/lib/utils";

const navigation = [
  { name: "Dashboard", href: "/dashboard", icon: Home },
  { name: "Institutions", href: "/dashboard/institutions", icon: School },
  { name: "Students", href: "/dashboard/students", icon: GraduationCap },
  { name: "Analytics", href: "/dashboard/analytics", icon: BarChart3 },
  { name: "Mentors", href: "/dashboard/mentors", icon: Users },
  { name: "Settings", href: "/dashboard/settings", icon: Settings },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="fixed left-0 top-0 z-40 flex h-screen w-64 flex-col border-r border-white/[0.06] bg-[#0a0a0f]/95 backdrop-blur-xl">
      {/* Logo */}
      <div className="flex h-16 items-center gap-3 border-b border-white/[0.06] px-6">
        <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-gradient-to-br from-violet-500 to-indigo-600 text-xs font-bold text-white shadow-lg shadow-violet-500/25">
          C
        </div>
        <span className="text-lg font-semibold tracking-tight text-white">
          Career<span className="text-violet-400">OS</span>
        </span>
      </div>

      {/* Navigation */}
      <nav className="flex-1 space-y-1 px-3 py-4">
        {navigation.map((item) => {
          const isActive = pathname === item.href || pathname?.startsWith(item.href + "/");
          return (
            <Link
              key={item.name}
              href={item.href}
              className={cn(
                "group flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition-all duration-200",
                isActive
                  ? "bg-violet-500/10 text-violet-300 shadow-sm shadow-violet-500/5"
                  : "text-zinc-400 hover:bg-white/[0.04] hover:text-zinc-200"
              )}
            >
              <item.icon
                className={cn(
                  "h-4.5 w-4.5 shrink-0 transition-colors",
                  isActive
                    ? "text-violet-400"
                    : "text-zinc-500 group-hover:text-zinc-400"
                )}
              />
              {item.name}
              {isActive && (
                <div className="ml-auto h-1.5 w-1.5 rounded-full bg-violet-400 shadow-sm shadow-violet-400/50" />
              )}
            </Link>
          );
        })}
      </nav>

      {/* Bottom section */}
      <div className="border-t border-white/[0.06] p-3">
        <button className="flex w-full items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium text-zinc-500 transition-colors hover:bg-white/[0.04] hover:text-zinc-300">
          <LogOut className="h-4.5 w-4.5" />
          Sign out
        </button>
      </div>
    </aside>
  );
}
