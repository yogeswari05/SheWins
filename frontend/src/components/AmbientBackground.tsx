import { useEffect, useRef } from "react";

/**
 * Soft floating orbs + cursor-reactive light (Cursor-style atmosphere).
 */
export function AmbientBackground() {
  const rootRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const el = rootRef.current;
    if (!el) return;
    const onMove = (e: PointerEvent) => {
      const x = (e.clientX / window.innerWidth) * 100;
      const y = (e.clientY / window.innerHeight) * 100;
      el.style.setProperty("--mx", `${x}%`);
      el.style.setProperty("--my", `${y}%`);
    };
    window.addEventListener("pointermove", onMove, { passive: true });
    return () => window.removeEventListener("pointermove", onMove);
  }, []);

  return (
    <div
      ref={rootRef}
      className="pointer-events-none fixed inset-0 -z-10 overflow-hidden"
      aria-hidden
    >
      <div
        className="absolute inset-0 opacity-90"
        style={{
          background:
            "radial-gradient(ellipse 80% 50% at 50% -20%, rgba(190, 24, 93, 0.25), transparent), radial-gradient(ellipse 60% 40% at 100% 50%, rgba(139, 92, 246, 0.18), transparent), radial-gradient(ellipse 50% 50% at 0% 80%, rgba(244, 63, 94, 0.15), transparent), #07040a",
        }}
      />
      <div
        className="absolute inset-0 transition-opacity duration-500"
        style={{
          background:
            "radial-gradient(520px circle at var(--mx, 50%) var(--my, 45%), rgba(251, 207, 232, 0.14), transparent 55%)",
        }}
      />
      <div className="absolute -left-20 top-1/4 h-[420px] w-[420px] rounded-full bg-fuchsia-600/25 blur-[100px] eh-float-slow" />
      <div className="absolute right-0 top-1/3 h-[380px] w-[380px] rounded-full bg-rose-500/20 blur-[90px] eh-float" />
      <div className="absolute bottom-0 left-1/3 h-[360px] w-[360px] rounded-full bg-violet-600/20 blur-[100px] eh-float-delay" />
      <div className="absolute bottom-1/4 right-1/4 h-[200px] w-[200px] rounded-full bg-pink-300/15 blur-[60px] eh-float-slow" />
      <div className="absolute inset-0 bg-[url('data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A//www.w3.org/2000/svg%22%20viewBox%3D%220%200%2032%2032%22%20width%3D%2232%22%20height%3D%2232%22%20fill%3D%22none%22%20stroke%3D%22rgba%28255%2C255%2C255%2C0.03%29%22%3E%3Cpath%20d%3D%22M0%20.5H31.5V32%22/%3E%3C/svg%3E')] opacity-40" />
    </div>
  );
}
