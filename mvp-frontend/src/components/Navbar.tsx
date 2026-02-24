import Link from "next/link";

export default function Navbar() {
  return (
    <header
      style={{
        borderBottom: "1px solid var(--border)",
        position: "sticky",
        top: 0,
        background: "white",
        zIndex: 10,
      }}
    >
      <div
        className="container"
        style={{
          height: 64,
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
        }}
      >
        <Link href="/" style={{ fontWeight: 600 }}>
          MVP
        </Link>

        <nav
          aria-label="Main navigation"
          style={{ display: "flex", gap: 24, alignItems: "center" }}
        >
          <Link href="/how-it-works">How it works</Link>
          <Link href="/use-cases">Use cases</Link>
          <Link href="/trust">Trust</Link>

          <Link
            href="/login"
            className="btn-primary"
            aria-label="Get started"
          >
            Get started
          </Link>
        </nav>
      </div>
    </header>
  );
}