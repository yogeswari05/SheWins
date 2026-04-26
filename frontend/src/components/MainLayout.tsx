import { useEffect } from "react";
import { Outlet } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { userApi } from "../lib/api";
import { TopNav } from "./TopNav";
import { FloatingAI } from "./FloatingAI";

export function MainLayout() {
  const { i18n } = useTranslation();

  useEffect(() => {
    const loc = i18n.language.split("-")[0] || "en";
    void userApi.init(loc).catch(() => {});
  }, [i18n.language]);

  return (
    <div className="relative min-h-screen">
      <TopNav />
      <main className="mx-auto max-w-6xl px-3 pb-8 pt-8 sm:px-6 min-h-[calc(100vh-4rem)]">
        <Outlet />
      </main>
      <footer className="mt-auto border-t border-white/10 dark:bg-black/40 bg-white/80 backdrop-blur-xl py-8">
        <div className="mx-auto max-w-6xl px-3 sm:px-6 text-center text-[11px] leading-relaxed dark:text-zinc-600 text-gray-600">
          <div className="flex items-center justify-center gap-2 mb-4">
            <div className="w-6 h-6 bg-gradient-to-br from-rose-500 to-violet-600 rounded-lg"></div>
            <span className="font-display text-lg font-semibold text-transparent bg-gradient-to-r dark:from-rose-100 dark:via-pink-100 dark:to-violet-200 from-rose-600 via-pink-600 to-violet-700 bg-clip-text">
              SheWins
            </span>
          </div>
        </div>
      </footer>
      <FloatingAI />
    </div>
  );
}
