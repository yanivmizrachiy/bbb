import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "מתמטיקה לחטיבת הביניים",
  description:
    "אוסף שאלות מתמטיקה להדפסה — Next.js 16 + PostgreSQL. הקטלוג נטען ממסד נתונים אמיתי.",
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="he" dir="rtl">
      <body>{children}</body>
    </html>
  );
}
