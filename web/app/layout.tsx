import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  metadataBase: new URL("https://bbb-ten-plum.vercel.app"),
  title: "מתמטיקה לחטיבת הביניים — אוסף שאלות להדפסה",
  description:
    "אוסף דפי עבודה ושאלות במתמטיקה לחטיבת הביניים — אלגברה, גאומטריה ואי-ודאות — מוכנים להדפסה ב-A4, עם גרפיקה וקטורית וכתיב מתמטי מקצועי.",
  keywords: [
    "מתמטיקה",
    "חטיבת הביניים",
    "דפי עבודה",
    "אלגברה",
    "גאומטריה",
    "הסתברות",
    "אי-ודאות",
    "כיתה ז",
    "כיתה ח",
  ],
  openGraph: {
    type: "website",
    locale: "he_IL",
    siteName: "מתמטיקה לחטיבת הביניים",
    title: "מתמטיקה לחטיבת הביניים — אוסף שאלות להדפסה",
    description:
      "דפי עבודה ושאלות במתמטיקה לחטיבת הביניים — אלגברה, גאומטריה ואי-ודאות — מוכנים להדפסה ב-A4.",
  },
  robots: { index: true, follow: true },
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
