import React from "react";

type Props = {
  emailPlaceholder?: string;
  passwordPlaceholder?: string;
  primaryButtonLabel?: string;
  socialButtonLabel?: string;
  trustLines?: string[];
};

export default function LoginCard({
  emailPlaceholder = "you@domain.com",
  passwordPlaceholder = "Password",
  primaryButtonLabel = "Continue",
  socialButtonLabel = "Continue with Google",
  trustLines = [],
}: Props) {
  return (
    <div className="card" style={{ maxWidth: 420, margin: "0 auto" }}>
      <form
        aria-labelledby="login-title"
        onSubmit={(e) => e.preventDefault()}
        noValidate
      >
        <h1 id="login-title" style={{ marginBottom: 8 }}>
          Sign in
        </h1>

        <label htmlFor="email" style={{ display: "block", marginTop: 12 }}>
          Email
        </label>
        <input
          id="email"
          name="email"
          type="email"
          placeholder={emailPlaceholder}
          style={{
            width: "100%",
            padding: 10,
            marginTop: 6,
            border: "1px solid var(--border)",
            borderRadius: 8,
          }}
        />

        <label htmlFor="password" style={{ display: "block", marginTop: 12 }}>
          Password
        </label>
        <input
          id="password"
          name="password"
          type="password"
          placeholder={passwordPlaceholder}
          style={{
            width: "100%",
            padding: 10,
            marginTop: 6,
            border: "1px solid var(--border)",
            borderRadius: 8,
          }}
        />

        <button
          type="submit"
          className="btn-primary"
          style={{ width: "100%", marginTop: 16 }}
        >
          {primaryButtonLabel}
        </button>

        <div
          aria-hidden="true"
          style={{
            textAlign: "center",
            marginTop: 12,
            color: "var(--text-secondary)",
            fontSize: "0.9rem",
          }}
        >
          OR
        </div>

        <button
          type="button"
          aria-label="Continue with Google"
          style={{
            width: "100%",
            marginTop: 12,
            padding: "10px 12px",
            borderRadius: 8,
            border: "1px solid var(--border)",
            background: "white",
            cursor: "pointer",
          }}
        >
          {socialButtonLabel}
        </button>

        <div
          id="login-trust"
          style={{
            marginTop: 14,
            color: "var(--text-secondary)",
            fontSize: "0.9rem",
            lineHeight: 1.4,
          }}
        >
          {trustLines.map((t, i) => (
            <p key={i} style={{ margin: "6px 0" }}>
              {t}
            </p>
          ))}
        </div>
      </form>
    </div>
  );
}