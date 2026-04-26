import { useNavigate } from "react-router-dom";
import { GlassCard } from "../components/GlassCard";
import { useTheme } from "../context/ThemeContext";
import { BubbleCursor } from "../components/BubbleCursor";
import { AmbientBackground } from "../components/AmbientBackground";

export default function AboutDiseases() {
  const { theme, toggleTheme } = useTheme();
  const navigate = useNavigate();

  const diseases = [
    {
      name: "PCOS (Polycystic Ovary Syndrome)",
      description: "A hormonal disorder causing enlarged ovaries with small cysts. Common symptoms include irregular periods, excess hair growth, acne, and weight gain. Early detection through cycle tracking can help manage symptoms effectively.",
      prevalence: "Affects 6-12% of women of reproductive age",
      symptoms: ["Irregular periods", "Excess hair growth", "Acne", "Weight gain", "Infertility"]
    },
    {
      name: "Endometriosis",
      description: "Tissue similar to uterine lining grows outside the uterus. Can cause severe pain, heavy bleeding, and fertility issues. Tracking pain patterns helps in diagnosis and treatment planning.",
      prevalence: "Affects 1 in 10 women during reproductive years",
      symptoms: ["Pelvic pain", "Heavy periods", "Pain during intercourse", "Infertility", "Fatigue"]
    },
    {
      name: "Fibroids",
      description: "Noncancerous growths in the uterus that can cause heavy bleeding, pain, and pressure. Regular symptom tracking helps monitor growth patterns and treatment effectiveness.",
      prevalence: "Up to 70% of women develop fibroids by age 50",
      symptoms: ["Heavy bleeding", "Pelvic pressure", "Frequent urination", "Back pain", "Pain during periods"]
    },
    {
      name: "Thyroid Disorders",
      description: "Thyroid imbalances can significantly impact menstrual cycles, causing irregular periods, heavy bleeding, or absent cycles. AI analysis of cycle patterns can help identify thyroid-related issues early.",
      prevalence: "1 in 8 women experience thyroid problems",
      symptoms: ["Irregular cycles", "Mood changes", "Weight changes", "Fatigue", "Temperature sensitivity"]
    },
    {
      name: "Premature Ovarian Failure",
      description: "Loss of normal ovarian function before age 40. Can cause irregular periods, hot flashes, and fertility challenges. Early pattern recognition through tracking is crucial for diagnosis.",
      prevalence: "Affects 1% of women under 40",
      symptoms: ["Irregular periods", "Hot flashes", "Night sweats", "Vaginal dryness", "Mood swings"]
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

        {/* Disease Information Section */}
        <section className="py-20 lg:py-32">
          <div className="mx-auto max-w-6xl px-3 sm:px-6">
            <div className="text-center space-y-6 mb-16">
              <h1 className={`font-display text-4xl sm:text-5xl lg:text-6xl font-semibold tracking-tight transition-colors duration-300 ${
                theme === 'dark'
                  ? 'text-transparent bg-gradient-to-r from-rose-100 via-pink-100 to-violet-200 bg-clip-text'
                  : 'text-transparent bg-gradient-to-r from-rose-600 via-pink-600 to-violet-600 bg-clip-text'
              }`}>
                Understanding Women's Health
              </h1>
              <p className={`text-lg sm:text-xl leading-relaxed max-w-3xl mx-auto transition-colors duration-300 ${
                theme === 'dark' ? 'text-zinc-300' : 'text-gray-700'
              }`}>
                Knowledge is power. Learn about common health conditions that affect women's reproductive wellness, 
                and how SheWins can help you identify patterns early for better health management.
              </p>
            </div>

            <div className="space-y-8">
              {diseases.map((disease, index) => (
                <GlassCard 
                  key={index} 
                  className={`p-8 space-y-6 transition-colors duration-300 ${
                    theme === 'dark'
                      ? 'bg-black/40 border-white/10'
                      : 'bg-white/80 border-gray-200'
                  }`}
                >
                  <div className="flex items-start gap-4">
                    <div className={`w-16 h-16 rounded-full flex items-center justify-center flex-shrink-0 ${
                      index % 2 === 0 ? 'bg-gradient-to-br from-rose-500 to-violet-600' : 'bg-gradient-to-br from-pink-500 to-rose-600'
                    }`}>
                      <span className="text-white text-2xl font-bold">{index + 1}</span>
                    </div>
                    <div className="flex-1 space-y-4">
                      <h3 className={`text-2xl font-bold transition-colors duration-300 ${
                        theme === 'dark' ? 'text-white' : 'text-gray-900'
                      }`}>{disease.name}</h3>
                      <p className={`text-base leading-relaxed transition-colors duration-300 ${
                        theme === 'dark' ? 'text-zinc-300' : 'text-gray-700'
                      }`}>{disease.description}</p>
                      <div className="space-y-2">
                        <p className={`text-sm font-medium transition-colors duration-300 ${
                          theme === 'dark' ? 'text-zinc-400' : 'text-gray-600'
                        }`}>Prevalence: <span className={`${
                          theme === 'dark' ? 'text-rose-400' : 'text-rose-600'
                        }`}>{disease.prevalence}</span></p>
                        <div>
                          <p className={`text-sm font-medium transition-colors duration-300 ${
                            theme === 'dark' ? 'text-zinc-400' : 'text-gray-600'
                          }`}>Common Symptoms:</p>
                          <div className="flex flex-wrap gap-2 mt-2">
                            {disease.symptoms.map((symptom, symptomIndex) => (
                              <span key={symptomIndex} className={`px-3 py-1 rounded-full text-xs transition-colors duration-300 ${
                                theme === 'dark'
                                  ? 'bg-white/10 text-zinc-300 border border-white/20'
                                  : 'bg-gray-100 text-gray-700 border border-gray-300'
                              }`}>{symptom}</span>
                            ))}
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </GlassCard>
              ))}
            </div>
          </div>
        </section>
      </div>
    </>
  );
}
