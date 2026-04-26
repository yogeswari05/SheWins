import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { GlassCard } from "../components/GlassCard";
import { useTheme } from "../context/ThemeContext";
import { BubbleCursor } from "../components/BubbleCursor";
import { AmbientBackground } from "../components/AmbientBackground";

export default function Features() {
  const { theme, toggleTheme } = useTheme();
  const navigate = useNavigate();

  const features = [
    {
      title: "Track Your Cycle",
      description: "Monitor your menstrual cycle, symptoms, and patterns with intuitive tracking tools designed for your privacy and comfort.",
      icon: "📊"
    },
    {
      title: "AI Health Assistant", 
      description: "Get personalized guidance and answers to your health questions from our intelligent AI assistant, available 24/7.",
      icon: "🤖"
    },
    {
      title: "Smart Analytics",
      description: "Understand your body better with detailed insights, trend analysis, and visualizations of your health patterns.",
      icon: "📈"
    },
    {
      title: "Gentle Reminders",
      description: "Never miss important dates with customizable notifications and reminders that respect your privacy.",
      icon: "🔔"
    },
    {
      title: "Privacy First",
      description: "Your health data is yours alone. We use advanced encryption and never share your personal information.",
      icon: "🔒"
    },
    {
      title: "Multi-language Support",
      description: "Available in English, Hindi, and Telugu to serve diverse communities with culturally sensitive care.",
      icon: "🌍"
    }
  ];

  return (
    <>
      <BubbleCursor />
      <AmbientBackground />
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
              
              <div className="flex items-center gap-4">
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
            </div>
          </div>
        </nav>

        {/* Back to Home Button */}
        <div className="relative mx-auto max-w-6xl px-3 sm:px-6 py-4">
          <div className="flex justify-start">
            <button 
              onClick={() => navigate("/")}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-colors ${
                theme === 'dark'
                  ? 'bg-white/10 border border-white/20 text-white hover:bg-white/20'
                  : 'bg-gray-100 border border-gray-300 text-gray-700 hover:bg-gray-200'
              }`}
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
              </svg>
              Back to Home
            </button>
          </div>
        </div>

        {/* Features Section */}
        <section className="py-20 lg:py-32">
          <div className="mx-auto max-w-6xl px-3 sm:px-6">
            <div className="text-center space-y-6 mb-16">
              <h1 className={`font-display text-4xl sm:text-5xl lg:text-6xl font-semibold tracking-tight transition-colors duration-300 ${
                theme === 'dark'
                  ? 'text-transparent bg-gradient-to-r from-rose-100 via-pink-100 to-violet-200 bg-clip-text'
                  : 'text-transparent bg-gradient-to-r from-rose-600 via-pink-600 to-violet-600 bg-clip-text'
              }`}>
                Everything You Need
              </h1>
              <p className={`text-lg sm:text-xl leading-relaxed max-w-3xl mx-auto transition-colors duration-300 ${
                theme === 'dark' ? 'text-zinc-300' : 'text-gray-700'
              }`}>
                Comprehensive tools designed specifically for your menstrual health and wellness journey. 
                SheWins provides the features you need to take control of your health with confidence.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {features.map((feature, index) => (
                <GlassCard 
                  key={index} 
                  className={`p-8 text-center space-y-6 hover:scale-105 transition-transform duration-300 ${
                    theme === 'dark'
                      ? 'bg-black/40 border-white/10'
                      : 'bg-white/80 border-gray-200'
                  }`}
                >
                  <div className="text-5xl mb-4">{feature.icon}</div>
                  <h3 className={`text-xl font-semibold transition-colors duration-300 ${
                    theme === 'dark' ? 'text-white' : 'text-gray-900'
                  }`}>{feature.title}</h3>
                  <p className={`text-sm leading-relaxed transition-colors duration-300 ${
                    theme === 'dark' ? 'text-zinc-300' : 'text-gray-700'
                  }`}>{feature.description}</p>
                </GlassCard>
              ))}
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
                Join thousands of women who trust SheWins for their menstrual health and wellness journey.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <button 
                  onClick={() => navigate("/signup")}
                  className="rounded-full bg-gradient-to-r from-rose-500 to-violet-600 px-8 py-4 text-base font-semibold text-white shadow-lg hover:shadow-xl transition-all hover:scale-105 hover-bubble ripple-effect relative z-10"
                >
                  Get Started
                </button>
                <button 
                  onClick={() => navigate("/")}
                  className={`rounded-full px-8 py-4 text-base font-medium transition-all hover:scale-105 hover-bubble ripple-effect relative z-10 ${
                    theme === 'dark'
                      ? 'border border-white/20 bg-white/5 text-white backdrop-blur-sm hover:bg-white/10'
                      : 'border border-gray-300 bg-gray-50 text-gray-700 hover:bg-gray-100'
                  }`}
                >
                  Back to Home
                </button>
              </div>
            </GlassCard>
          </div>
        </section>
      </div>
    </>
  );
}
