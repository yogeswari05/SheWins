import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { GlassCard } from "../components/GlassCard";
import { useTheme } from "../context/ThemeContext";
import { BubbleCursor } from "../components/BubbleCursor";
import { AmbientBackground } from "../components/AmbientBackground";

export default function FAQs() {
  const { theme, toggleTheme } = useTheme();
  const navigate = useNavigate();

  const faqs = [
    {
      question: "What is SheWins and how does it work?",
      answer: "SheWins is your personal menstrual health companion that helps you track your cycle, get AI-powered guidance, and understand your body better. Our app uses advanced algorithms to provide personalized insights while maintaining complete privacy."
    },
    {
      question: "Is my health data secure and private?",
      answer: "Absolutely! We use end-to-end encryption and never share your personal health information. Your data is stored securely and you have complete control over what information you share with our AI assistant."
    },
    {
      question: "How accurate are the cycle predictions?",
      answer: "Our predictions become more accurate as you log more data. The AI analyzes your personal patterns, symptoms, and cycle history to provide increasingly precise predictions about your next period and fertile windows."
    },
    {
      question: "Can SheWins help detect health issues early?",
      answer: "While SheWins is not a medical diagnostic tool, it can help identify patterns and irregularities that might warrant medical attention. We always recommend consulting healthcare professionals for any health concerns."
    },
    {
      question: "Is the app suitable for all ages?",
      answer: "SheWins is designed for women of all ages who want to understand their menstrual health better. Whether you're just starting your period journey or have been tracking for years, our app adapts to your needs."
    },
    {
      question: "How does the AI assistant work?",
      answer: "Our AI assistant is trained on women's health information and provides personalized guidance based on your symptoms and patterns. It's available 24/7 to answer questions about menstrual health, wellness, and related concerns."
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

        {/* FAQ Section */}
        <section className="py-20 lg:py-32">
          <div className="mx-auto max-w-4xl px-3 sm:px-6">
            <div className="text-center space-y-6 mb-16">
              <h1 className={`font-display text-4xl sm:text-5xl lg:text-6xl font-semibold tracking-tight transition-colors duration-300 ${
                theme === 'dark'
                  ? 'text-transparent bg-gradient-to-r from-rose-100 via-pink-100 to-violet-200 bg-clip-text'
                  : 'text-transparent bg-gradient-to-r from-rose-600 via-pink-600 to-violet-600 bg-clip-text'
              }`}>
                Frequently Asked Questions
              </h1>
              <p className={`text-lg sm:text-xl leading-relaxed transition-colors duration-300 ${
                theme === 'dark' ? 'text-zinc-300' : 'text-gray-700'
              }`}>
                Everything you need to know about SheWins and how we help you take control of your health journey.
              </p>
            </div>

            <div className="space-y-6">
              {faqs.map((faq, index) => (
                <GlassCard 
                  key={index} 
                  className={`p-8 space-y-4 transition-colors duration-300 ${
                    theme === 'dark'
                      ? 'bg-black/40 border-white/10'
                      : 'bg-white/80 border-gray-200'
                  }`}
                >
                  <h3 className={`text-xl font-semibold transition-colors duration-300 ${
                    theme === 'dark' ? 'text-white' : 'text-gray-900'
                  }`}>{faq.question}</h3>
                  <p className={`text-base leading-relaxed transition-colors duration-300 ${
                    theme === 'dark' ? 'text-zinc-300' : 'text-gray-700'
                  }`}>{faq.answer}</p>
                </GlassCard>
              ))}
            </div>
          </div>
        </section>
      </div>
    </>
  );
}
