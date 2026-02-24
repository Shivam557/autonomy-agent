import LoginCard from "@/components/LoginCard";
import type { NextPage } from "next";

const Login: NextPage = () => {
  return (
    <main
      className="container"
      style={{
        padding: "80px 0",
        minHeight: "60vh",
        display: "grid",
        placeItems: "center",
      }}
    >
      <LoginCard
        emailPlaceholder="you@domain.com"
        passwordPlaceholder="Password"
        primaryButtonLabel="Continue"
        socialButtonLabel="Continue with Google"
        trustLines={[
          "We never store your password — this is a UI-only demo.",
          "By continuing you agree to our privacy overview.",
        ]}
      />
    </main>
  );
};

export default Login;