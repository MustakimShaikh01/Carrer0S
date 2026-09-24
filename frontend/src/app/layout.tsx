import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({
  variable: "--font-geist-sans",
  subsets: ["latin"],
  display: "swap",
});

export const metadata: Metadata = {
  title: "CareerOS — Technical Career Intelligence Platform",
  description:
    "Measures demonstrated skills, identifies gaps, recommends actions, and provides institutional analytics for technical career readiness.",
  keywords: [
    "career intelligence",
    "edtech",
    "skill assessment",
    "career readiness",
    "technical hiring",
  ],
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html
      lang="en"
      className={`${inter.variable} h-full antialiased dark`}
    >
      <body className="min-h-full flex flex-col bg-[#07070b] text-zinc-200">
        {children}
      </body>
    </html>
  );
}
