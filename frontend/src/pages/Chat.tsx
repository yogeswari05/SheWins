import { useState } from "react";
import { useTranslation } from "react-i18next";
import { GlassCard } from "../components/GlassCard";
import { TypingText } from "../components/TypingText";
import { LoadingState } from "../components/LoadingSkeleton";
import { chatApi } from "../lib/api";
import { useTheme } from "../context/ThemeContext";
import { BubbleCursor } from "../components/BubbleCursor";
import { AmbientBackground } from "../components/AmbientBackground";

export default function Chat() {
  const { t, i18n } = useTranslation();
  const { theme, toggleTheme } = useTheme();
  const [q, setQ] = useState("");
  const [msg, setMsg] = useState<{ role: "user" | "assistant"; text: string }[]>([]);
  const [load, setLoad] = useState(false);

  const send = async () => {
    if (!q.trim()) return;
    setMsg((m) => [...m, { role: "user", text: q }]);
    setLoad(true);
    const question = q;
    setQ("");
    try {
      const r = await chatApi.message(question, i18n.language);
      setMsg((m) => [
        ...m,
        { role: "assistant", text: (r.data as { reply: string }).reply || "(empty)" },
      ]);
    } catch (e: unknown) {
      setMsg((m) => [
        ...m,
        {
          role: "assistant",
          text:
            (e as Error).message ||
            "Could not reach the AI — add ANTHROPIC_API_KEY or OPENAI_API_KEY on the server.",
        },
      ]);
    } finally {
      setLoad(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div>
        <h2 className="font-display text-2xl text-rose-50">{t("nav.soulGuide")}</h2>
        <p className="mt-2 max-w-xl text-sm leading-relaxed text-zinc-400">{t("chat.hint")}</p>
      </div>
      <GlassCard className="min-h-[400px]">
        <div className="max-h-96 space-y-4 overflow-y-auto pr-2 scrollbar-thin scrollbar-thumb-violet-600/20 scrollbar-track-transparent">
          {msg.map((m, i) => (
            <div
              key={i}
              className={`flex ${
                m.role === "user" ? "justify-end" : "justify-start"
              } animate-fadeIn`}
            >
              <div className={`max-w-[80%] ${
                m.role === "user"
                  ? "rounded-2xl rounded-br-md bg-gradient-to-br from-rose-500/90 to-pink-600/90 px-4 py-3 text-sm leading-relaxed text-white shadow-lg shadow-rose-900/30"
                  : "rounded-2xl rounded-bl-md border border-violet-400/20 bg-violet-950/40 px-4 py-3 text-sm leading-relaxed text-violet-100/95 backdrop-blur-sm"
                }`}
              >
                {m.role === "assistant" ? (
                  <TypingText 
                    text={m.text} 
                    speed={15}
                    className="whitespace-pre-wrap"
                  />
                ) : (
                  <div className="whitespace-pre-wrap">{m.text}</div>
                )}
              </div>
            </div>
          ))}
          {load && (
            <div className="flex justify-start">
              <div className="rounded-2xl rounded-bl-md border border-violet-400/20 bg-violet-950/40 px-4 py-3 text-sm text-violet-100/95">
                <div className="flex items-center gap-2">
                  <div className="flex gap-1">
                    <div className="w-2 h-2 bg-violet-400 rounded-full animate-bounce" style={{animationDelay: '0ms'}}></div>
                    <div className="w-2 h-2 bg-violet-400 rounded-full animate-bounce" style={{animationDelay: '150ms'}}></div>
                    <div className="w-2 h-2 bg-violet-400 rounded-full animate-bounce" style={{animationDelay: '300ms'}}></div>
                  </div>
                  <span className="text-xs text-violet-300/70">AI is thinking...</span>
                </div>
              </div>
            </div>
          )}
        </div>
      </GlassCard>
      <div className="flex gap-3">
        <div className="flex-1 relative">
          <input
            className="w-full rounded-2xl border border-white/10 bg-black/40 px-4 py-3 pr-12 text-sm text-zinc-100 outline-none transition focus:border-violet-400/35 focus:ring-2 focus:ring-violet-400/15 placeholder-zinc-500"
            value={q}
            onChange={(e) => setQ(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && !e.shiftKey && (e.preventDefault(), void send())}
            placeholder={t("chat.placeholder")}
            disabled={load}
          />
          {q && (
            <button
              type="button"
              onClick={() => setQ("")}
              className="absolute right-3 top-1/2 -translate-y-1/2 text-zinc-400 hover:text-zinc-200 transition-colors"
            >
              ✕
            </button>
          )}
        </div>
        <button
          type="button"
          onClick={() => void send()}
          disabled={load || !q.trim()}
          className="shrink-0 rounded-2xl bg-gradient-to-r from-violet-600 to-fuchsia-600 px-6 py-3 text-sm font-semibold text-white shadow-[0_0_24px_-8px_rgba(167,139,250,0.5)] transition hover:brightness-110 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
        >
          {load ? (
            <>
              <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
              Sending...
            </>
          ) : (
            <>
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
              </svg>
              {t("chat.send")}
            </>
          )}
        </button>
      </div>
    </div>
  );
}
