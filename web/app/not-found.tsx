import Link from "next/link";

export default function NotFound() {
  return (
    <div
      style={{
        maxWidth: 560,
        margin: "0 auto",
        padding: "80px 20px",
        textAlign: "center",
      }}
    >
      <div
        style={{
          fontSize: 56,
          fontWeight: 800,
          lineHeight: 1,
          background: "linear-gradient(135deg,#4f46e5,#7c3aed 55%,#0d9488)",
          WebkitBackgroundClip: "text",
          backgroundClip: "text",
          color: "transparent",
        }}
      >
        404
      </div>
      <h1 style={{ fontSize: 22, fontWeight: 800, color: "#1f2a44", margin: "10px 0 6px" }}>
        הדף לא נמצא
      </h1>
      <p style={{ color: "#6b7280", marginBottom: 22 }}>
        ייתכן שהנושא שחיפשת אינו קיים או שהקישור שגוי.
      </p>
      <Link
        href="/"
        style={{
          display: "inline-block",
          color: "#fff",
          background: "#4f46e5",
          padding: "12px 24px",
          borderRadius: 13,
          fontWeight: 700,
          textDecoration: "none",
        }}
      >
        חזרה לכל הנושאים
      </Link>
    </div>
  );
}
