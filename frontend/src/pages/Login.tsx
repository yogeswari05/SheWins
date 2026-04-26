import { useEffect, useState } from "react";
import { Link, useNavigate, useLocation } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { useAuth } from "../context/AuthContext";
import { GlassCard } from "../components/GlassCard";

export default function Login() {
  const { t } = useTranslation();
  const { login, session } = useAuth();
  const nav = useNavigate();
  const loc = useLocation() as { state?: { from?: string } };
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [err, setErr] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    if (session?.access_token) {
      nav(loc.state?.from || "/today", { replace: true });
    }
  }, [session, nav, loc.state]);

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErr(null);
    setBusy(true);
    try {
      await login(email.trim(), password);
      nav(loc.state?.from || "/today", { replace: true });
    } catch {
      setErr(t("auth.badCredentials"));
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="relative mx-auto flex min-h-screen max-w-lg flex-col justify-center px-4 py-16">
      <GlassCard glow className="mx-auto w-full max-w-md">
        <p className="text-center text-[10px] font-semibold uppercase tracking-[0.4em] text-rose-300/80">
          {t("auth.welcomeBack")}
        </p>
        <h2 className="mt-2 text-center font-display text-2xl text-rose-50 sm:text-3xl">
          {t("auth.loginTitle")}
        </h2>
        <p className="mx-auto mt-2 max-w-sm text-center text-sm leading-relaxed text-zinc-400">
          {t("auth.loginBlurb")}
        </p>
        <form onSubmit={submit} className="mt-8 space-y-4">
          {err && (
            <p className="rounded-xl border border-rose-500/30 bg-rose-950/50 px-3 py-2 text-center text-sm text-rose-200">
              {err}
            </p>
          )}
          <label className="block text-xs font-medium uppercase tracking-wider text-zinc-500">
            {t("auth.email")}
            <input
              type="email"
              autoComplete="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="mt-1.5 w-full rounded-xl border border-white/10 bg-black/40 px-4 py-3 text-sm text-zinc-100 outline-none ring-rose-400/0 transition focus:border-rose-400/40 focus:ring-2 focus:ring-rose-400/20"
            />
          </label>
          <label className="block text-xs font-medium uppercase tracking-wider text-zinc-500">
            {t("auth.password")}
            <input
              type="password"
              autoComplete="current-password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="mt-1.5 w-full rounded-xl border border-white/10 bg-black/40 px-4 py-3 text-sm text-zinc-100 outline-none transition focus:border-rose-400/40 focus:ring-2 focus:ring-rose-400/20"
            />
          </label>
          <button
            type="submit"
            disabled={busy}
            className="w-full rounded-xl bg-gradient-to-r from-rose-500 via-pink-500 to-violet-600 py-3.5 text-sm font-semibold text-white shadow-[0_0_32px_-6px_rgba(236,72,153,0.55)] transition hover:brightness-110 disabled:opacity-50"
          >
            {busy ? t("auth.pleaseWait") : t("auth.signIn")}
          </button>
        </form>
        <p className="mt-6 text-center text-sm text-zinc-500">
          {t("auth.noAccount")}{" "}
          <Link to="/signup" className="font-medium text-rose-300 underline-offset-4 hover:text-rose-200 hover:underline">
            {t("auth.createSpace")}
          </Link>
        </p>
      </GlassCard>
    </div>
  );
}
