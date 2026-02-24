
import { ReactNode } from "react";
import Navbar from "@/components/Navbar";

type Props = {
  children: ReactNode;
};

export default function Layout({ children }: Props) {
  return (
    <>
      <Navbar />
      <main style={{ paddingTop: 64 }}>{children}</main>
      <footer
        style={{
          borderTop: "1px solid var(--border)",
          marginTop: 96,
          padding: "24px 0",
        }}
      >
        <div className="container">
          <small style={{ color: "var(--text-secondary)" }}>
            © 2026 MVP
          </small>
        </div>
      </footer>
    </>
  );
}