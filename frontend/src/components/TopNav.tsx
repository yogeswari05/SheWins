import { NavLink, useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { useAuth } from "../context/AuthContext";
import { useTheme } from "../context/ThemeContext";

const navItem =
  "relative flex items-center gap-2 rounded-full px-4 py-2 text-sm font-medium dark:text-rose-100/85 text-gray-700 transition-all duration-300 dark:hover:bg-white/[0.08] hover:bg-gray-100 dark:hover:text-rose-50 hover:text-gray-900";
const navActive =
  "bg-gradient-to-r from-rose-500/25 to-violet-600/20 text-white shadow-[0_0_24px_-4px_rgba(244,63,94,0.45)] ring-1 ring-rose-400/30";

export function TopNav() {
  const { t } = useTranslation();
  const nav = useNavigate();
  const { session, logout } = useAuth();
  const { theme, toggleTheme } = useTheme();

  const links: [string, string][] = [
    ["/today", t("nav.soulToday")],
    ["/track", t("nav.soulFlow")],
    ["/analytics", t("nav.soulPatterns")],
    ["/reminders", t("nav.soulNudges")],
    ["/settings", t("nav.soulMe")],
  ];

  return (
    <nav className="sticky top-0 z-50 border-b border-white/10 dark:bg-black/40 bg-white/80 backdrop-blur-xl">
      <div className="mx-auto max-w-6xl px-3 sm:px-6">
        <div className="flex items-center justify-between h-16">
          {/* Logo and Nav Items */}
          <div className="flex items-center gap-6">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 bg-gradient-to-br from-rose-500 to-violet-600 rounded-lg"></div>
              <span className="font-display text-lg font-semibold text-transparent bg-gradient-to-r dark:from-rose-100 dark:via-pink-100 dark:to-violet-200 from-rose-600 via-pink-600 to-violet-700 bg-clip-text">
                SheWins
              </span>
            </div>
            
            {/* Navigation Items */}
            <div className="hidden lg:flex items-center gap-2">
              {links.map(([to, label]) => (
                <NavLink
                  key={to}
                  to={to}
                  end={false}
                  className={({ isActive }) => (isActive ? `${navItem} ${navActive}` : navItem)}
                >
                  <span className="opacity-90">{label}</span>
                </NavLink>
              ))}
            </div>
          </div>

          {/* User Actions */}
          <div className="flex items-center gap-3">
            {/* Theme Toggle */}
            <button
              type="button"
              onClick={toggleTheme}
              className="rounded-full border border-white/15 dark:bg-white/5 bg-gray-100 p-2 dark:text-zinc-300 text-gray-700 transition hover:border-rose-400/40 dark:hover:bg-rose-500/10 hover:bg-rose-100 dark:hover:text-rose-100 hover:text-rose-600"
              title={theme === "dark" ? "Switch to light mode" : "Switch to dark mode"}
            >
              {theme === "dark" ? (
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
                </svg>
              ) : (
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
                </svg>
              )}
            </button>
            
            <div className="hidden sm:flex items-center gap-2 rounded-full border border-white/10 dark:bg-black/20 bg-gray-100 px-3 py-1.5 text-xs dark:text-zinc-300 text-gray-700 backdrop-blur-md">
              <span className="dark:text-zinc-500 text-gray-500">{t("app.signedInAs")} </span>
              <span className="dark:text-rose-200/90 text-rose-600 truncate max-w-[120px]">{session?.email}</span>
            </div>
            <button
              type="button"
              onClick={() => {
                logout();
                nav("/login", { replace: true });
              }}
              className="rounded-full border border-white/15 dark:bg-white/5 bg-gray-100 px-3 py-1.5 text-xs font-medium dark:text-zinc-300 text-gray-700 transition hover:border-rose-400/40 dark:hover:bg-rose-500/10 hover:bg-rose-100 dark:hover:text-rose-100 hover:text-rose-600"
            >
              {t("auth.signOut")}
            </button>
          </div>
        </div>

        {/* Mobile Navigation */}
        <div className="lg:hidden py-3 border-t border-white/10">
          <div className="flex flex-wrap gap-2 mb-3">
            {links.map(([to, label]) => (
              <NavLink
                key={to}
                to={to}
                end={to === "/"}
                className={({ isActive }) => (isActive ? `${navItem} ${navActive}` : navItem)}
              >
                <span className="opacity-90 text-xs">{label}</span>
              </NavLink>
            ))}
          </div>
          
          {/* Mobile Theme Toggle */}
          <div className="flex items-center justify-between border-t border-white/10 pt-3">
            <span className="text-xs dark:text-zinc-400 text-gray-500">Theme</span>
            <button
              type="button"
              onClick={toggleTheme}
              className="rounded-full border border-white/15 dark:bg-white/5 bg-gray-100 px-3 py-1.5 text-xs font-medium dark:text-zinc-300 text-gray-700 transition hover:border-rose-400/40 dark:hover:bg-rose-500/10 hover:bg-rose-100 dark:hover:text-rose-100 hover:text-rose-600 flex items-center gap-2"
            >
              {theme === "dark" ? (
                <>
                  <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
                  </svg>
                  Light
                </>
              ) : (
                <>
                  <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
                  </svg>
                  Dark
                </>
              )}
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
}
