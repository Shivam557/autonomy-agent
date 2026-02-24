import Hero from "@/components/Hero";
import type { NextPage } from "next";

const headline = "Draft cancellation, refund, and fee-waiver emails — fast";
const subheadline =
  "Pre-drafted, editable messages to request cancellations or refunds from providers.";
const primaryCta = "Get started";
const secondaryCta = "How it works";
const bullets = [
  "Choose a use case and review a draft.",
  "Edit the message locally and preview the result.",
  "Download or copy the final email to send to the provider.",
];

const Home: NextPage = () => {
  return (
    <main>
      <Hero
        headline={headline}
        subheadline={subheadline}
        primaryCtaLabel={primaryCta}
        secondaryCtaLabel={secondaryCta}
        bullets={bullets}
      />

      <section className="container" style={{ padding: "28px 0 80px" }}>
        {/* Placeholder for below-the-fold content: use-cases, trust, etc. */}
        <div style={{ display: "grid", gap: 16 }}>
          <h2>Use cases</h2>
          <p>
            Examples include subscription cancellations, accidental purchases,
            and billing errors—each with a ready-to-edit draft.
          </p>
        </div>
      </section>
    </main>
  );
};

export default Home;