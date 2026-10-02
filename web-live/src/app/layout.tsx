import type { Metadata } from "next";

import "./globals.css";

export const metadata: Metadata = {
  title: "Job Tracker",
  description:
    "İş başvurularını takip et, CV'nle ilanları eşleştir, eksik yetkinliklerini gör.",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="tr" className="h-full antialiased">
      <body className="min-h-full flex flex-col">{children}</body>
    </html>
  );
}
