"use client";

import { Bell, Search } from "lucide-react";

export function TopBar() {
  return (
    <header className="sticky top-0 z-30 flex h-16 items-center justify-between border-b border-white/[0.06] bg-[#0a0a0f]/80 px-8 backdrop-blur-xl">
      {/* Search */}
      <div className="relative flex-1 max-w-md">
        <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-zinc-500" />
        <input
          type="text"
          placeholder="Search students, institutions..."
          className="w-full rounded-xl border border-white/[0.06] bg-white/[0.03] py-2 pl-10 pr-4 text-sm text-zinc-200 placeholder-zinc-600 outline-none transition-colors focus:border-violet-500/30 focus:bg-white/[0.05] focus:ring-1 focus:ring-violet-500/20"
        />
      </div>

      {/* Right side */}
      <div className="flex items-center gap-4">
        {/* Notifications */}
        <button className="relative rounded-xl border border-white/[0.06] bg-white/[0.03] p-2 text-zinc-400 transition-colors hover:bg-white/[0.06] hover:text-zinc-200">
          <Bell className="h-4 w-4" />
          <span className="absolute -right-0.5 -top-0.5 flex h-4 w-4 items-center justify-center rounded-full bg-violet-500 text-[10px] font-bold text-white shadow-lg shadow-violet-500/30">
            3
          </span>
        </button>

        {/* User avatar */}
        <div className="flex items-center gap-3">
          <div className="h-8 w-8 rounded-full bg-gradient-to-br from-violet-500 to-indigo-600 shadow-lg shadow-violet-500/20" />
          <div className="hidden sm:block">
            <p className="text-sm font-medium text-zinc-200">Admin User</p>
            <p className="text-xs text-zinc-500">super_admin</p>
          </div>
        </div>
      </div>
    </header>
  );
}
