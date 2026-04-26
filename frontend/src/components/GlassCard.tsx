import type { ReactNode } from "react";

export function GlassCard({
  children,
  className = "",
  glow = false,
}: {
  children: ReactNode;
  className?: string;
  glow?: boolean;
}) {
  return (
    <div
      className={[
        "relative rounded-3xl border border-white/[0.12] bg-white/[0.06] p-6 shadow-2xl backdrop-blur-2xl",
        glow ? "eh-card-glow" : "",
        className,
      ]
        .filter(Boolean)
        .join(" ")}
    >
      <div className="pointer-events-none absolute inset-0 rounded-3xl bg-gradient-to-br from-white/[0.08] via-transparent to-rose-500/[0.04]" />
      <div className="relative z-[1]">{children}</div>
    </div>
  );
}
