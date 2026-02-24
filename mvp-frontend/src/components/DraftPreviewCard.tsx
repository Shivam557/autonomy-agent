type Props = {
  providerName: string;
  subject: string;
  bodyPreview: string;
  estimatedSavings: number;
};

export default function DraftPreviewCard({
  providerName,
  subject,
  bodyPreview,
  estimatedSavings,
}: Props) {
  return (
    <div className="card" role="group">
      <p style={{ fontSize: "0.9rem", color: "var(--text-secondary)" }}>
        {providerName}
      </p>

      <h3 style={{ marginTop: 6 }}>{subject}</h3>

      <p style={{ marginTop: 8 }}>{bodyPreview}</p>

      <div
        style={{
          marginTop: 16,
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        <strong>${estimatedSavings.toFixed(2)} est. savings</strong>

        <div style={{ display: "flex", gap: 8 }}>
          <button
            className="btn-primary"
            aria-label={`Approve draft for ${providerName}`}
          >
            Approve
          </button>

          <button
            style={{
              border: "1px solid var(--border)",
              background: "white",
              borderRadius: 8,
              padding: "10px 14px",
              cursor: "pointer",
            }}
          >
            Edit
          </button>
        </div>
      </div>
    </div>
  );
}