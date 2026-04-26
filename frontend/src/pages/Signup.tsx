import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { useAuth } from "../context/AuthContext";
import { GlassCard } from "../components/GlassCard";

export default function Signup() {
  const { t } = useTranslation();
  const { signup, session } = useAuth();
  const nav = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");
  const [err, setErr] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    if (session?.access_token) nav("/today", { replace: true });
  }, [session, nav]);

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErr(null);
    if (password.length < 8) {
      setErr(t("auth.passwordHint"));
      return;
    }
    setBusy(true);
    try {
      await signup(email.trim(), password, name.trim());
      nav("/today", { replace: true });
    } catch (e: unknown) {
      const status = (e as { response?: { status?: number } })?.response?.status;
      if (status === 409) setErr(t("auth.emailTaken"));
      else setErr(t("auth.signupFailed"));
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="relative mx-auto flex min-h-screen max-w-lg flex-col justify-center px-4 py-16">
      <GlassCard glow className="mx-auto w-full max-w-md">
        <p className="text-center text-[10px] font-semibold uppercase tracking-[0.4em] text-violet-300/80">
          {t("auth.beginSoft")}
        </p>
        <h2 className="mt-2 text-center font-display text-2xl text-rose-50 sm:text-3xl">
          {t("auth.signupTitle")}
        </h2>
        <p className="mx-auto mt-2 max-w-sm text-center text-sm leading-relaxed text-zinc-400">
          {t("auth.signupBlurb")}
        </p>
        <form onSubmit={submit} className="mt-8 space-y-4">
          {err && (
            <p className="rounded-xl border border-amber-500/30 bg-amber-950/40 px-3 py-2 text-center text-sm text-amber-100">
              {err}
            </p>
          )}
          <label className="block text-xs font-medium uppercase tracking-wider text-zinc-500">
            {t("auth.callYou")}
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="mt-1.5 w-full rounded-xl border border-white/10 bg-black/40 px-4 py-3 text-sm text-zinc-100 outline-none transition focus:border-violet-400/40 focus:ring-2 focus:ring-violet-400/20"
              placeholder={t("auth.namePlaceholder")}
            />
          </label>
          <label className="block text-xs font-medium uppercase tracking-wider text-zinc-500">
            {t("auth.email")}
            <input
              type="email"
              autoComplete="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="mt-1.5 w-full rounded-xl border border-white/10 bg-black/40 px-4 py-3 text-sm text-zinc-100 outline-none transition focus:border-rose-400/40 focus:ring-2 focus:ring-rose-400/20"
            />
          </label>
          <label className="block text-xs font-medium uppercase tracking-wider text-zinc-500">
            {t("auth.password")}
            <input
              type="password"
              autoComplete="new-password"
              required
              minLength={8}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="mt-1.5 w-full rounded-xl border border-white/10 bg-black/40 px-4 py-3 text-sm text-zinc-100 outline-none transition focus:border-rose-400/40 focus:ring-2 focus:ring-rose-400/20"
            />
          </label>
          <button
            type="submit"
            disabled={busy}
            className="w-full rounded-xl bg-gradient-to-r from-violet-600 via-fuchsia-600 to-rose-500 py-3.5 text-sm font-semibold text-white shadow-[0_0_32px_-6px_rgba(167,139,250,0.5)] transition hover:brightness-110 disabled:opacity-50"
          >
            {busy ? t("auth.pleaseWait") : t("auth.beginJourney")}
          </button>
        </form>
        <p className="mt-6 text-center text-sm text-zinc-500">
          {t("auth.haveAccount")}{" "}
          <Link to="/login" className="font-medium text-violet-300 underline-offset-4 hover:text-violet-200 hover:underline">
            {t("auth.signIn")}
          </Link>
        </p>
      </GlassCard>
    </div>
  );
}
