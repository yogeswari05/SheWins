import { useState, useEffect } from "react";
import { GlassCard } from "./GlassCard";
import { TypingText } from "./TypingText";
import { chatApi } from "../lib/api";
import { useTranslation } from "react-i18next";
import { useTheme } from "../context/ThemeContext";

export function FloatingAI() {
  const { i18n } = useTranslation();
  const { theme } = useTheme();
  const [isOpen, setIsOpen] = useState(false);
  const [q, setQ] = useState("");
  const [msg, setMsg] = useState<{ role: "user" | "assistant"; text: string }[]>([]);
  const [load, setLoad] = useState(false);
  const [isOnLandingPage, setIsOnLandingPage] = useState(false);

  // Check if we're on landing page
  useEffect(() => {
    setIsOnLandingPage(window.location.pathname === "/");
  }, []);

  const send = async () => {
    if (!q.trim()) return;
    setMsg((m) => [...m, { role: "user", text: q }]);
    setLoad(true);
    const question = q;
    setQ("");

    try {
      // Add context based on current page
      const contextualQuestion = isOnLandingPage 
        ? `As a helpful assistant for SheWins women's health app, please answer this question about the application or women's health diseases: ${question}`
        : question;

      const r = await chatApi.message(contextualQuestion, i18n.language);
      setMsg((m) => [
        ...m,
        { role: "assistant", text: (r.data as { reply: string }).reply || "(empty)" },
      ]);
    } catch (e: unknown) {
      setMsg((m) => [
        ...m,
        { role: "assistant", text: "Sorry, I'm having trouble connecting. Please try again." },
      ]);
    } finally {
      setLoad(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      send();
    }
  };

  return (
    <>
      {/* Floating AI Bot Button */}
      <button
        onClick={() => setIsOpen(true)}
        className={`fixed bottom-8 right-8 z-50 w-14 h-14 rounded-full shadow-lg transition-all duration-300 hover:scale-110 hover:shadow-xl flex items-center justify-center ${
          theme === 'dark'
            ? 'bg-gradient-to-br from-rose-500 to-violet-600 hover:from-rose-400 hover:to-violet-500'
            : 'bg-gradient-to-br from-rose-400 to-violet-500 hover:from-rose-300 hover:to-violet-400'
        }`}
        title="AI Assistant"
      >
        {/* Speech Bubble Icon - Centered */}
        <svg className="w-6 h-6 text-white flex-shrink-0" fill="currentColor" viewBox="0 0 24 24" style={{ margin: '0 auto' }}>
          <path d="M20 2H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h14l4 4V4c0-1.1-.9-2-2-2z"/>
        </svg>
      </button>

      {/* Chat Modal */}
      {isOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm">
          <div className="relative w-full max-w-md max-h-[80vh]">
            <GlassCard className="h-full flex flex-col">
              {/* Header */}
              <div className="flex items-center justify-between p-4 border-b border-white/10">
                <div className="flex items-center gap-3">
                  <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                    theme === 'dark'
                      ? 'bg-gradient-to-br from-blue-500 to-blue-600'
                      : 'bg-gradient-to-br from-blue-400 to-blue-500'
                  }`}>
                    <svg className="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M20 2H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h14l4 4V4c0-1.1-.9-2-2-2z"/>
                    </svg>
                  </div>
                  <div>
                    <h3 className="font-semibold text-rose-200/95">AI Assistant</h3>
                    <p className="text-xs text-zinc-500">
                      {isOnLandingPage ? "Ask about SheWins & women's health" : "Personal health guidance"}
                    </p>
                  </div>
                </div>
                <button
                  onClick={() => setIsOpen(false)}
                  className="p-2 rounded-lg hover:bg-white/10 transition-colors"
                >
                  <svg className="w-4 h-4 text-zinc-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>

              {/* Messages */}
              <div className="flex-1 overflow-y-auto p-4 space-y-3 min-h-[300px] max-h-[400px]">
                {msg.length === 0 && (
                  <div className="text-center text-zinc-500 text-sm">
                    {isOnLandingPage 
                      ? "👋 Hi! Ask me anything about SheWins or women's health diseases!"
                      : "👋 Hi! I'm here to help with your personal health questions."
                    }
                  </div>
                )}
                {msg.map((m, i) => (
                  <div
                    key={i}
                    className={`flex ${m.role === "user" ? "justify-end" : "justify-start"}`}
                  >
                    <div
                      className={`max-w-[80%] rounded-2xl px-4 py-2 ${
                        m.role === "user"
                          ? "bg-gradient-to-r from-rose-500 to-violet-600 text-white"
                          : theme === 'dark'
                            ? "bg-white/10 text-zinc-200"
                            : "bg-gray-100 text-gray-800"
                      }`}
                    >
                      {m.role === "assistant" ? (
                        <TypingText text={m.text} />
                      ) : (
                        <p className="text-sm">{m.text}</p>
                      )}
                    </div>
                  </div>
                ))}
                {load && (
                  <div className="flex justify-start">
                    <div className={`rounded-2xl px-4 py-2 ${
                      theme === 'dark'
                        ? "bg-white/10 text-zinc-200"
                        : "bg-gray-100 text-gray-800"
                    }`}>
                      <div className="flex space-x-1">
                        <div className="w-2 h-2 bg-rose-400 rounded-full animate-bounce"></div>
                        <div className="w-2 h-2 bg-rose-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                        <div className="w-2 h-2 bg-rose-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                      </div>
                    </div>
                  </div>
                )}
              </div>

              {/* Input */}
              <div className="p-4 border-t border-white/10">
                <div className="flex gap-2">
                  <input
                    type="text"
                    value={q}
                    onChange={(e) => setQ(e.target.value)}
                    onKeyPress={handleKeyPress}
                    placeholder={
                      isOnLandingPage 
                        ? "Ask about SheWins or women's health..." 
                        : "Ask about your health..."
                    }
                    className={`flex-1 rounded-full px-4 py-2 text-sm transition-colors ${
                      theme === 'dark'
                        ? 'bg-white/10 text-white placeholder:text-zinc-500 focus:bg-white/20'
                        : 'bg-gray-100 text-gray-800 placeholder:text-gray-500 focus:bg-gray-200'
                    } focus:outline-none focus:ring-2 focus:ring-rose-400/50`}
                    disabled={load}
                  />
                  <button
                    onClick={send}
                    disabled={load || !q.trim()}
                    className="p-2 rounded-full bg-gradient-to-r from-rose-500 to-violet-600 text-white transition-all hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                    </svg>
                  </button>
                </div>
              </div>
            </GlassCard>
          </div>
        </div>
      )}
    </>
  );
}
