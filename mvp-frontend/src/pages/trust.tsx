import TrustPanel from "@/components/TrustPanel";

export default function Trust() {
  return (
    <main className="container" style={{ padding: "80px 0" }}>
      <h1>Trust & Privacy</h1>

      <div style={{ marginTop: 32, maxWidth: 700 }}>
        <TrustPanel
          bullets={[
            "This MVP does not send emails automatically.",
            "All drafts are reviewed and edited by you before sending.",
            "No payment or account access is required in this demo.",
          ]}
        />
      </div>
    </main>
  );
}