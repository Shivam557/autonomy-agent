import DraftPreviewCard from "@/components/DraftPreviewCard";
import data from "@/data/mock.json";

export default function Dashboard() {
  const drafts = data.drafts;

  return (
    <main className="container" style={{ padding: "80px 0" }}>
      <h1>Dashboard</h1>

      {/* Summary cards */}
      <div
        style={{
          marginTop: 32,
          display: "grid",
          gap: 24,
          gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
        }}
      >
        <div className="card">
          <strong>Money you might recover</strong>
          <h2 style={{ marginTop: 8 }}>
            $
            {drafts
              .reduce((sum, d) => sum + d.estimatedSavings, 0)
              .toFixed(2)}
          </h2>
        </div>

        <div className="card">
          <strong>Drafts ready</strong>
          <h2 style={{ marginTop: 8 }}>{drafts.length}</h2>
        </div>

        <div className="card">
          <strong>Actions pending approval</strong>
          <h2 style={{ marginTop: 8 }}>0</h2>
        </div>
      </div>

      {/* Draft list */}
      <section style={{ marginTop: 48 }}>
        <h2>Drafts</h2>

        <div style={{ marginTop: 24, display: "grid", gap: 24 }}>
          {drafts.map((d, i) => (
            <DraftPreviewCard key={i} {...d} />
          ))}
        </div>
      </section>
    </main>
  );
}