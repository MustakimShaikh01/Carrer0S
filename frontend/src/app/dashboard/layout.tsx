import { Sidebar } from "@/components/layout/sidebar";
import { TopBar } from "@/components/layout/topbar";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen bg-[#07070b]">
      <Sidebar />
      <div className="ml-64">
        <TopBar />
        <main className="p-8">{children}</main>
      </div>
    </div>
  );
}
