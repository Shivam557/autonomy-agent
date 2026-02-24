import Link from "next/link";
import React from "react";

type Props = {
  headline: string;
  subheadline: string;
  primaryCtaLabel: string;
  secondaryCtaLabel: string;
  bullets?: string[];
};

export default function Hero({
  headline,
  subheadline,
  primaryCtaLabel,
  secondaryCtaLabel,
  bullets = [],
}: Props) {
  return (
    <section
      aria-labelledby="hero-title"
      style={{ padding: "64px 0", background: "transparent" }}
    >
      <div className="container" style={{ display: "grid", gap: 20 }}>
        <div style={{ maxWidth: 760 }}>
          <h1 id="hero-title" style={{ marginBottom: 12 }}>
            {headline}
          </h1>

          <p style={{ marginTop: 8, maxWidth: 640 }}>{subheadline}</p>

          <div style={{ marginTop: 24, display: "flex", gap: 12 }}>
            <Link
              href="/login"
              className="btn-primary"
              role="button"
              aria-label={primaryCtaLabel}
            >
              {primaryCtaLabel}
            </Link>

            <Link href="/how-it-works" aria-label={secondaryCtaLabel}>
              <button
                style={{
                  border: "1px solid var(--border)",
                  borderRadius: 8,
                  padding: "10px 14px",
                  background: "white",
                  cursor: "pointer",
                }}
              >
                {secondaryCtaLabel}
              </button>
            </Link>
          </div>
        </div>

        {bullets.length > 0 && (
          <ul
            aria-label="How it works bullets"
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
              gap: 12,
              marginTop: 18,
              listStyle: "none",
              padding: 0,
            }}
          >
            {bullets.map((b, i) => (
              <li key={i} className="card" style={{ display: "block" }}>
                <strong style={{ display: "block", marginBottom: 6 }}>
                  {i + 1}.
                </strong>
                <p style={{ margin: 0 }}>{b}</p>
              </li>
            ))}
          </ul>
        )}
      </div>
    </section>
  );
}


