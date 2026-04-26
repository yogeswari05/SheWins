import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { GlassCard } from "../components/GlassCard";
import { useTheme } from "../context/ThemeContext";
import { BubbleCursor } from "../components/BubbleCursor";
import { FloatingAI } from "../components/FloatingAI";
import logoImage from "../assets/images/logo.png";

export default function Landing() {
  const navigate = useNavigate();
  const { theme, toggleTheme } = useTheme();
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <>
      <BubbleCursor />
      <div className={`min-h-screen transition-colors duration-300 ${
        theme === 'dark' 
          ? 'bg-gradient-to-br from-[#050308] via-[#0a0b1e] to-[#1a0d26]' 
          : 'bg-gradient-to-br from-rose-50 via-pink-50 to-purple-50'
      }`}>
      {/* Navigation */}
      <nav className={`sticky top-0 z-50 backdrop-blur-xl border transition-colors duration-300 ${
        theme === 'dark'
          ? 'bg-black/40 border-white/10'
          : 'bg-white/80 border-gray-200'
      }`}>
        <div className="mx-auto max-w-6xl px-3 sm:px-6">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 bg-gradient-to-br from-rose-500 to-violet-600 rounded-lg"></div>
              <span className={`font-display text-xl font-semibold transition-colors duration-300 ${
                theme === 'dark'
                  ? 'text-transparent bg-gradient-to-r from-rose-100 via-pink-100 to-violet-200 bg-clip-text'
                  : 'text-transparent bg-gradient-to-r from-rose-600 via-pink-600 to-violet-600 bg-clip-text'
              }`}>
                SheWins
              </span>
            </div>
            
            {/* Desktop Navigation */}
            <div className="hidden md:flex items-center gap-4">
              <button 
                onClick={() => navigate("/features")}
                className={`transition-colors hover-bubble ripple-effect relative z-10 ${
                  theme === 'dark'
                    ? 'text-zinc-300 hover:text-white'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                Features
              </button>
              <button 
                onClick={() => navigate("/faqs")}
                className={`transition-colors hover-bubble ripple-effect relative z-10 ${
                  theme === 'dark'
                    ? 'text-zinc-300 hover:text-white'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                FAQs
              </button>
              <button 
                onClick={() => navigate("/about-diseases")}
                className={`transition-colors hover-bubble ripple-effect relative z-10 ${
                  theme === 'dark'
                    ? 'text-zinc-300 hover:text-white'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                About Diseases
              </button>
              <button 
                onClick={toggleTheme}
                className={`p-2 rounded-lg transition-colors ${
                  theme === 'dark'
                    ? 'text-zinc-300 hover:text-white hover:bg-white/10'
                    : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                }`}
                title="Toggle theme"
              >
                {theme === 'dark' ? (
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
                  </svg>
                ) : (
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
                  </svg>
                )}
              </button>
              <button 
                onClick={() => navigate("/login")}
                className={`transition-colors hover-bubble ripple-effect relative z-10 ${
                  theme === 'dark'
                    ? 'text-zinc-300 hover:text-white'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                Sign In
              </button>
              <button 
                onClick={() => navigate("/signup")}
                className="rounded-full bg-gradient-to-r from-rose-500 to-violet-600 px-4 py-2 text-sm font-medium text-white shadow-lg hover:shadow-xl transition-all hover-bubble ripple-effect relative z-10"
              >
                Get Started
              </button>
            </div>

            {/* Mobile Menu Button */}
            <button 
              className={`md:hidden transition-colors ${
                theme === 'dark'
                  ? 'text-zinc-300 hover:text-white'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
              onClick={() => setIsMenuOpen(!isMenuOpen)}
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
          </div>

            {/* Mobile Menu */}
          {isMenuOpen && (
            <div className={`md:hidden py-4 border-t transition-colors ${
              theme === 'dark'
                ? 'border-white/10'
                : 'border-gray-200'
            }`}>
              <div className="flex flex-col gap-4">
                <button 
                  onClick={() => { navigate("/features"); setIsMenuOpen(false); }}
                  className={`flex items-center gap-2 p-2 rounded-lg transition-colors text-left ${
                    theme === 'dark'
                      ? 'text-zinc-300 hover:text-white hover:bg-white/10'
                      : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                  }`}
                >
                  <span>Features</span>
                </button>
                <button 
                  onClick={() => { navigate("/faqs"); setIsMenuOpen(false); }}
                  className={`flex items-center gap-2 p-2 rounded-lg transition-colors text-left ${
                    theme === 'dark'
                      ? 'text-zinc-300 hover:text-white hover:bg-white/10'
                      : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                  }`}
                >
                  <span>FAQs</span>
                </button>
                <button 
                  onClick={() => { navigate("/about-diseases"); setIsMenuOpen(false); }}
                  className={`flex items-center gap-2 p-2 rounded-lg transition-colors text-left ${
                    theme === 'dark'
                      ? 'text-zinc-300 hover:text-white hover:bg-white/10'
                      : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                  }`}
                >
                  <span>About Diseases</span>
                </button>
                <button 
                  onClick={toggleTheme}
                  className={`flex items-center gap-2 p-2 rounded-lg transition-colors text-left ${
                    theme === 'dark'
                      ? 'text-zinc-300 hover:text-white hover:bg-white/10'
                      : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                  }`}
                >
                  {theme === 'dark' ? (
                    <>
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
                      </svg>
                      <span>Light Mode</span>
                    </>
                  ) : (
                    <>
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
                      </svg>
                      <span>Dark Mode</span>
                    </>
                  )}
                </button>
                <button 
                  onClick={() => { navigate("/login"); setIsMenuOpen(false); }}
                  className={`transition-colors text-left ${
                    theme === 'dark'
                      ? 'text-zinc-300 hover:text-white'
                      : 'text-gray-600 hover:text-gray-900'
                  }`}
                >
                  Sign In
                </button>
                <button 
                  onClick={() => { navigate("/signup"); setIsMenuOpen(false); }}
                  className="rounded-full bg-gradient-to-r from-rose-500 to-violet-600 px-4 py-2 text-sm font-medium text-white shadow-lg hover:shadow-xl transition-all"
                >
                  Get Started
                </button>
              </div>
            </div>
          )}
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative overflow-hidden min-h-[calc(100vh-64px)]">
        <div className={`absolute inset-0 transition-colors duration-300 ${
          theme === 'dark'
            ? 'bg-gradient-to-br from-rose-500/10 via-transparent to-violet-600/10'
            : 'bg-gradient-to-br from-rose-200/20 via-transparent to-violet-200/20'
        }`}></div>
        <div className="relative mx-auto max-w-7xl px-3 sm:px-6 h-full flex items-start justify-center pt-16 py-20 lg:py-32">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            {/* Left Side - Content */}
            <div className="space-y-8 lg:pl-8">
              <div className="space-y-6">
                <h1 className={`font-display text-4xl sm:text-5xl lg:text-6xl font-semibold tracking-tight transition-colors duration-300 ${
                  theme === 'dark'
                    ? 'text-transparent bg-gradient-to-r from-rose-100 via-pink-100 to-violet-200 bg-clip-text'
                    : 'text-transparent bg-gradient-to-r from-rose-600 via-pink-600 to-violet-600 bg-clip-text'
                }`}>
                  Your Personal
                  <br />
                  Health Companion
                </h1>
                <p className={`text-lg sm:text-xl leading-relaxed transition-colors duration-300 ${
                  theme === 'dark'
                    ? 'text-zinc-300'
                    : 'text-gray-700'
                }`}>
                  SheWins is your trusted menstrual health and wellness companion. Track your cycle, get AI-powered guidance, and understand your body better with privacy-first design.
                </p>
              </div>
              
              <div className="space-y-4">
                <button 
                  onClick={() => navigate("/signup")}
                  className="rounded-full bg-gradient-to-r from-rose-500 to-violet-600 px-8 py-4 text-base font-semibold text-white shadow-lg hover:shadow-xl transition-all hover:scale-105 hover-bubble ripple-effect relative z-10"
                >
                  Get Started
                </button>
                <button 
                  onClick={() => navigate("/features")}
                  className={`rounded-full px-8 py-4 text-base font-medium transition-all hover:scale-105 hover-bubble ripple-effect relative z-10 ${
                    theme === 'dark'
                      ? 'border border-white/20 bg-white/5 text-white backdrop-blur-sm hover:bg-white/10'
                      : 'border border-gray-300 bg-gray-50 text-gray-700 hover:bg-gray-100'
                  }`}
                >
                  Explore Features
                </button>
              </div>
            </div>
            
            {/* Right Side - Logo with Moving Visuals */}
            <div className="flex justify-center lg:justify-end relative">
              <div className="relative">
                {/* Moving visual elements */}
                <div className="absolute -top-8 -left-8 w-4 h-4 bg-gradient-to-r from-rose-400 to-pink-400 rounded-full animate-pulse opacity-60"></div>
                <div className="absolute -top-4 -right-6 w-3 h-3 bg-gradient-to-r from-violet-400 to-purple-400 rounded-full animate-bounce opacity-40"></div>
                <div className="absolute -bottom-6 -left-10 w-2 h-2 bg-gradient-to-r from-pink-400 to-rose-400 rounded-full animate-spin opacity-30"></div>
                <div className="absolute -bottom-4 -right-8 w-3 h-3 bg-gradient-to-r from-purple-400 to-indigo-400 rounded-full animate-ping opacity-50"></div>
                
                <div className={`w-80 h-80 sm:w-96 sm:h-96 lg:w-full lg:h-full max-w-md lg:max-w-lg transition-colors duration-300 ${
                  theme === 'dark'
                    ? 'bg-white/10 border-white/20'
                    : 'bg-white/80 border-gray-300'
                } backdrop-blur-sm flex items-center justify-center p-8 rounded-3xl relative`}>
                  <img 
                      src={logoImage} 
                      alt="SheWins - Empowering women's health"
                      className="w-full h-full object-cover rounded-2xl"
                    />
                </div>
                <div className="absolute -bottom-4 -right-4 w-20 h-20 bg-gradient-to-r from-rose-500 to-violet-600 rounded-full opacity-20 blur-xl"></div>
                <div className="absolute -top-4 -left-4 w-16 h-16 bg-gradient-to-r from-violet-500 to-pink-600 rounded-full opacity-20 blur-xl"></div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 lg:py-32">
        <div className="mx-auto max-w-4xl px-3 sm:px-6 text-center">
          <GlassCard className={`p-12 space-y-8 transition-colors duration-300 ${
            theme === 'dark'
              ? 'bg-black/40 border-white/10'
              : 'bg-white/80 border-gray-200'
          }`}>
            <h2 className={`font-display text-3xl font-semibold transition-colors duration-300 ${
              theme === 'dark'
                ? 'text-transparent bg-gradient-to-r from-rose-100 via-pink-100 to-violet-200 bg-clip-text'
                : 'text-transparent bg-gradient-to-r from-rose-600 via-pink-600 to-violet-600 bg-clip-text'
            }`}>
              Ready to Start Your Health Journey?
            </h2>
            <p className={`text-lg transition-colors duration-300 ${
              theme === 'dark' ? 'text-zinc-300' : 'text-gray-700'
            }`}>
              Join thousands of women who trust Elite Her for their menstrual health and wellness journey.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button 
                onClick={() => navigate("/signup")}
                className="rounded-full bg-gradient-to-r from-rose-500 to-violet-600 px-8 py-4 text-base font-semibold text-white shadow-lg hover:shadow-xl transition-all hover:scale-105 hover-bubble ripple-effect relative z-10"
              >
                Get Started
              </button>
              <button 
                onClick={() => navigate("/login")}
                className={`rounded-full px-8 py-4 text-base font-medium transition-all hover:scale-105 hover-bubble ripple-effect relative z-10 ${
                  theme === 'dark'
                    ? 'border border-white/20 bg-white/5 text-white backdrop-blur-sm hover:bg-white/10'
                    : 'border border-gray-300 bg-gray-50 text-gray-700 hover:bg-gray-100'
                }`}
              >
                I Already Have an Account
              </button>
            </div>
          </GlassCard>
        </div>
      </section>

      {/* Footer */}
      <footer className={`border-t backdrop-blur-xl py-12 transition-colors duration-300 ${
        theme === 'dark'
          ? 'border-white/10 bg-black/40'
          : 'border-gray-200 bg-white/80'
      }`}>
        <div className="mx-auto max-w-6xl px-3 sm:px-6 text-center">
          <div className="flex items-center justify-center gap-2 mb-4">
            <div className="w-6 h-6 bg-gradient-to-br from-rose-500 to-violet-600 rounded-lg"></div>
            <span className={`font-display text-lg font-semibold transition-colors duration-300 ${
              theme === 'dark'
                ? 'text-transparent bg-gradient-to-r from-rose-100 via-pink-100 to-violet-200 bg-clip-text'
                : 'text-transparent bg-gradient-to-r from-rose-600 via-pink-600 to-violet-600 bg-clip-text'
            }`}>
              SheWins
            </span>
          </div>
          <p className={`text-sm transition-colors duration-300 ${
            theme === 'dark' ? 'text-zinc-400' : 'text-gray-600'
          }`}>
            Your privacy-first menstrual health companion from SheWins. Always here for you.
          </p>
        </div>
      </footer>
      </div>
      <FloatingAI />
    </>
  );
}
