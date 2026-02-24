type Props = {
  title: string;
  description: string;
  exampleSavings: number;
};

export default function UseCaseCard({ title, description, exampleSavings }: Props) {
  return (
    <div className="card">
      <h3 style={{ fontSize: "1.1rem", marginBottom: 8 }}>{title}</h3>
      <p style={{ marginBottom: 12 }}>{description}</p>
      <strong>${exampleSavings.toFixed(2)} possible savings</strong>
    </div>
  );
}