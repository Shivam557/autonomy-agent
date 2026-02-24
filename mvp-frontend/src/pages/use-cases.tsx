import UseCaseCard from "@/components/UseCaseCard";
import data from "@/data/mock.json";

export default function UseCases() {
  return (
    <main className="container" style={{ padding: "80px 0" }}>
      <h1>Use cases</h1>

      <div
        style={{
          marginTop: 32,
          display: "grid",
          gap: 24,
          gridTemplateColumns: "repeat(auto-fit, minmax(260px, 1fr))",
        }}
      >
        {data.useCases.map((uc, i) => (
          <UseCaseCard key={i} {...uc} />
        ))}
      </div>
    </main>
  );
}