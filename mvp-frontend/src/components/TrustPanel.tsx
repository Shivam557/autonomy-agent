type Props = {
  bullets: string[];
};

export default function TrustPanel({ bullets }: Props) {
  return (
    <div
      className="card"
      style={{
        display: "grid",
        gap: 16,
      }}
    >
      {bullets.map((b, i) => (
        <p key={i} style={{ margin: 0 }}>
          {b}
        </p>
      ))}
    </div>
  );
}