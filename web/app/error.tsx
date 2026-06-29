"use client";

// Branded error boundary — shows a clean Hebrew screen instead of the raw
// "server error" page (e.g. while the database is still being connected).
export default function Error({ reset }: { error: Error & { digest?: string }; reset: () => void }) {
  return (
    <div style={{ maxWidth: 560, margin: "0 auto", padding: "80px 20px", textAlign: "center" }}>
      <div
        style={{
          fontSize: 50,
          fontWeight: 800,
          lineHeight: 1,
          background: "linear-gradient(135deg,#4f46e5,#7c3aed 55%,#0d9488)",
          WebkitBackgroundClip: "text",
          backgroundClip: "text",
          color: "transparent",
        }}
      >
        רגע אחד…
      </div>
      <h1 style={{ fontSize: 22, fontWeight: 800, color: "#1f2a44", margin: "10px 0 6px" }}>
        משהו השתבש זמנית
      </h1>
      <p style={{ color: "#6b7280", marginBottom: 22 }}>
        ייתכן שהאתר עדיין מסיים להתחבר. נסו לטעון מחדש בעוד רגע.
      </p>
      <button
        onClick={() => reset()}
        style={{
          color: "#fff",
          background: "#4f46e5",
          padding: "12px 24px",
          borderRadius: 13,
          fontWeight: 700,
          border: "none",
          cursor: "pointer",
          fontSize: 15,
          fontFamily: "inherit",
        }}
      >
        נסו שוב
      </button>
    </div>
  );
}
