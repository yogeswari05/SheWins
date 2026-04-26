import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { GlassCard } from "../components/GlassCard";
import { LoadingState, CardSkeleton } from "../components/LoadingSkeleton";
import { cyclesApi, type CycleIn } from "../lib/api";
import { useTheme } from "../context/ThemeContext";
import { BubbleCursor } from "../components/BubbleCursor";
import { AmbientBackground } from "../components/AmbientBackground";

// Mood emojis for better UX
const MOOD_OPTIONS = [
  { emoji: "😊", label: "happy", value: "happy" },
  { emoji: "😔", label: "sad", value: "sad" },
  { emoji: "😰", label: "anxious", value: "anxious" },
  { emoji: "😤", label: "irritable", value: "irritable" },
  { emoji: "😴", label: "tired", value: "tired" },
  { emoji: "🤗", label: "calm", value: "calm" },
  { emoji: "💪", label: "energetic", value: "energetic" },
  { emoji: "🥰", label: "loved", value: "loved" },
  { emoji: "😕", label: "confused", value: "confused" },
  { emoji: "🤒", label: "unwell", value: "unwell" },
];

// Common symptoms for quick selection
const COMMON_SYMPTOMS = [
  "cramps", "bloating", "headache", "acne", "fatigue", "breast_tenderness",
  "back_pain", "nausea", "food_cravings", "mood_swings", "spotting", "insomnia"
];

type Row = CycleIn & { id: string; alerts?: any };

interface Alert {
  type: 'warning' | 'info' | 'error' | 'health_alert';
  message: string;
  importance?: 'low' | 'medium' | 'high';
}

export default function Track() {
  const { t } = useTranslation();
  const { theme, toggleTheme } = useTheme();
  const [rows, setRows] = useState<Row[]>([]);
  const [trackingScenario, setTrackingScenario] = useState<'not-period' | 'on-period' | 'post-period'>('not-period');
  const [form, setForm] = useState<CycleIn>({
    start_date: new Date().toISOString().slice(0, 10),
    end_date: "",
    flow: "medium",
    symptoms: [],
    mood: "",
    sleep_hours: 7,
    stress: 5,
    exercise: "moderate",
    notes: "",
  });
  const [sympStr, setSympStr] = useState("");
  const [selectedSymptoms, setSelectedSymptoms] = useState<string[]>([]);
  const [customSymptom, setCustomSymptom] = useState("");
  const [symptomSuggestions, setSymptomSuggestions] = useState<string[]>([]);
  const [showSymptomSuggestions, setShowSymptomSuggestions] = useState(false);
  const [selectedMood, setSelectedMood] = useState("");
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [showSuccessMessage, setShowSuccessMessage] = useState(false);
  const [successMessage, setSuccessMessage] = useState("");
  const [isLoading, setIsLoading] = useState(true);

  const load = async () => {
    setIsLoading(true);
    try {
      const response = await cyclesApi.list();
      setRows((response.data as Row[]) || []);
    } catch (error) {
      console.error('Error loading cycles:', error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    void load();
  }, []);

  // Load symptom suggestions when typing
  const handleSymptomInputChange = async (value: string) => {
    setSympStr(value);
    if (value.length > 1) {
      try {
        const response = await fetch(`/api/cycles/symptoms/suggestions?q=${encodeURIComponent(value)}&limit=5`);
        const data = await response.json();
        setSymptomSuggestions(data.suggestions);
        setShowSymptomSuggestions(true);
      } catch (error) {
        console.error('Error fetching symptom suggestions:', error);
      }
    } else {
      setShowSymptomSuggestions(false);
    }
  };

  // Add symptom from suggestions
  const addSymptomFromSuggestion = (symptom: string) => {
    if (!selectedSymptoms.includes(symptom)) {
      setSelectedSymptoms([...selectedSymptoms, symptom]);
    }
    setSympStr("");
    setShowSymptomSuggestions(false);
  };

  // Add custom symptom
  const addCustomSymptom = () => {
    if (customSymptom.trim() && !selectedSymptoms.includes(customSymptom.trim())) {
      setSelectedSymptoms([...selectedSymptoms, customSymptom.trim()]);
      setCustomSymptom("");
    }
  };

  // Toggle common symptom
  const toggleCommonSymptom = (symptom: string) => {
    if (selectedSymptoms.includes(symptom)) {
      setSelectedSymptoms(selectedSymptoms.filter(s => s !== symptom));
    } else {
      setSelectedSymptoms([...selectedSymptoms, symptom]);
    }
  };

  // Remove selected symptom
  const removeSelectedSymptom = (symptom: string) => {
    setSelectedSymptoms(selectedSymptoms.filter(s => s !== symptom));
  };

  // Handle mood selection
  const handleMoodSelect = (moodValue: string) => {
    setSelectedMood(moodValue);
    setForm({ ...form, mood: moodValue });
  };

  // Generate engaging success messages
  const generateSuccessMessage = () => {
    const messages = [
      "🌸 Great job! Your cycle has been logged successfully.",
      "💪 You're taking control of your health - amazing!",
      "✨ Cycle logged! Keep up the great self-care.",
      "🎯 Health tracking complete! You're doing great.",
      "🌟 Awesome! Your health data is now saved.",
      "💖 Perfect! Consistent tracking leads to better insights.",
      "🦋 Beautiful! You're nurturing your wellbeing.",
      "🌺 Wonderful! Your health journey matters."
    ];
    return messages[Math.floor(Math.random() * messages.length)];
  };

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // Combine all symptoms
    const allSymptoms = [...new Set([...selectedSymptoms, ...sympStr.split(/[,;]/).map(s => s.trim().toLowerCase()).filter(Boolean)])];
    
    try {
      const response = await cyclesApi.create({ 
        ...form, 
        symptoms: allSymptoms, 
        end_date: form.end_date || undefined 
      });
      
      // Handle alerts from backend
      if (response.data.alerts) {
        const alertMessages: Alert[] = [];
        
        // Process warnings
        response.data.alerts.warnings.forEach((warning: string) => {
          alertMessages.push({
            type: 'warning',
            message: warning.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
            importance: 'medium'
          });
        });
        
        // Process suggestions
        response.data.alerts.suggestions.forEach((suggestion: any) => {
          alertMessages.push({
            type: suggestion.type === 'error' ? 'error' : suggestion.type === 'health_alert' ? 'health_alert' : 'info',
            message: suggestion.message,
            importance: suggestion.health_importance === 'high' ? 'high' : 'low'
          });
        });
        
        setAlerts(alertMessages);
      }
      
      // Show success message
      setSuccessMessage(generateSuccessMessage());
      setShowSuccessMessage(true);
      setTimeout(() => setShowSuccessMessage(false), 5000);
      
      // Reset form
      setSympStr("");
      setSelectedSymptoms([]);
      setCustomSymptom("");
      setSelectedMood("");
      setForm({
        start_date: new Date().toISOString().slice(0, 10),
        end_date: "",
        flow: "medium",
        symptoms: [],
        mood: "",
        sleep_hours: 7,
        stress: 5,
        exercise: "moderate",
        notes: "",
      });
      
      await load();
    } catch (error) {
      console.error('Error saving cycle:', error);
    }
  };

  const input =
    "mt-1.5 w-full rounded-xl border border-white/10 bg-black/35 px-4 py-2.5 text-sm text-zinc-100 outline-none transition focus:border-rose-400/35 focus:ring-2 focus:ring-rose-400/15";

  return (
    <>
      <BubbleCursor />
      <AmbientBackground />
      <div className="max-w-4xl mx-auto px-4 space-y-8 text-center">
        {/* Welcome Header */}
        <div className="text-center mb-8">
          <h1 className="font-display text-3xl font-bold text-transparent bg-gradient-to-r from-rose-200 via-pink-200 to-violet-200 bg-clip-text mb-4">
            Tell me about your day
          </h1>
          <p className="text-lg text-zinc-300 max-w-2xl mx-auto">
            I'm here to listen and care about you. Share how you're feeling today, and I'll help you understand your patterns.
          </p>
        </div>

      {/* Success Message */}
        {showSuccessMessage && (
          <div className="rounded-2xl bg-gradient-to-r from-green-500/20 to-emerald-500/20 border border-green-400/30 p-4">
            <p className="text-green-300 text-center font-medium">{successMessage}</p>
          </div>
        )}

        {/* Alerts */}
        {alerts.length > 0 && (
          <div className="space-y-2">
            {alerts.map((alert, index) => (
              <div
                key={index}
                className={`rounded-xl border p-4 ${
                  alert.type === 'error' ? 'bg-red-500/10 border-red-400/30 text-red-300' :
                  alert.type === 'warning' ? 'bg-yellow-500/10 border-yellow-400/30 text-yellow-300' :
                  alert.type === 'health_alert' ? 'bg-orange-500/10 border-orange-400/30 text-orange-300' :
                  'bg-blue-500/10 border-blue-400/30 text-blue-300'
                }`}
              >
                <p className="text-sm">{alert.message}</p>
              </div>
            ))}
          </div>
        )}

        {/* Scenario Selection */}
        <GlassCard glow className="text-center">
          <h2 className="font-display text-xl text-transparent bg-gradient-to-r from-rose-200 via-pink-200 to-violet-200 bg-clip-text mb-4">
            What would you like to share with me today?
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <button
              type="button"
              onClick={() => setTrackingScenario('not-period')}
              className={`p-4 rounded-2xl border transition-all ${
                trackingScenario === 'not-period'
                  ? 'border-rose-400 bg-rose-400/20 text-rose-300'
                  : 'border-white/10 bg-black/35 text-zinc-400 hover:border-rose-400/35'
              }`}
            >
              <div className="text-2xl mb-2">🌸</div>
              <h3 className="font-medium mb-1">I'm not on my period</h3>
              <p className="text-xs opacity-80">Share how I'm feeling today</p>
            </button>
            
            <button
              type="button"
              onClick={() => setTrackingScenario('on-period')}
              className={`p-4 rounded-2xl border transition-all ${
                trackingScenario === 'on-period'
                  ? 'border-rose-400 bg-rose-400/20 text-rose-300'
                  : 'border-white/10 bg-black/35 text-zinc-400 hover:border-rose-400/35'
              }`}
            >
              <div className="text-2xl mb-2">🩸</div>
              <h3 className="font-medium mb-1">I'm on my period</h3>
              <p className="text-xs opacity-80">Tell me about today's flow</p>
            </button>
            
            <button
              type="button"
              onClick={() => setTrackingScenario('post-period')}
              className={`p-4 rounded-2xl border transition-all ${
                trackingScenario === 'post-period'
                  ? 'border-rose-400 bg-rose-400/20 text-rose-300'
                  : 'border-white/10 bg-black/35 text-zinc-400 hover:border-rose-400/35'
              }`}
            >
              <div className="text-2xl mb-2">📅</div>
              <h3 className="font-medium mb-1">My period just ended</h3>
              <p className="text-xs opacity-80">Share how it went overall</p>
            </button>
          </div>
        </GlassCard>

        {/* Dynamic Form Based on Scenario */}
        <GlassCard glow className="text-center">
          <form onSubmit={submit} className="space-y-6">
            {/* Dynamic content based on scenario */}
            {trackingScenario === 'not-period' && (
              <div className="space-y-4">
                <h3 className="font-display text-lg text-rose-200/95">Tell me how you're feeling today</h3>
                <p className="text-sm text-zinc-400">Even when you're not on your period, I care about how you're feeling. Share anything you'd like me to remember.</p>
                
                {/* Mood Selection */}
                <div className="text-left">
                  <label className="block text-sm font-medium text-zinc-300 mb-3">How are you feeling emotionally?</label>
                  <div className="grid grid-cols-5 gap-2">
                    {MOOD_OPTIONS.map((mood) => (
                      <button
                        key={mood.value}
                        type="button"
                        onClick={() => handleMoodSelect(mood.value)}
                        className={`p-3 rounded-xl border transition-all ${
                          selectedMood === mood.value
                            ? 'border-rose-400 bg-rose-400/20 text-rose-300'
                            : 'border-white/10 bg-black/35 text-zinc-400 hover:border-rose-400/35'
                        }`}
                        title={mood.label}
                      >
                        <div className="text-2xl">{mood.emoji}</div>
                        <div className="text-xs mt-1 capitalize">{mood.label}</div>
                      </button>
                    ))}
                  </div>
                </div>

                {/* General Symptoms */}
                <div className="text-left">
                  <label className="block text-sm font-medium text-zinc-300 mb-3">Any symptoms or feelings you've noticed?</label>
                  <div className="flex flex-wrap gap-2">
                    {["headache", "fatigue", "bloating", "mood_swings", "cramps", "breast_tenderness"].map((symptom) => (
                      <button
                        key={symptom}
                        type="button"
                        onClick={() => toggleCommonSymptom(symptom)}
                        className={`px-3 py-1 rounded-full text-xs border transition-all ${
                          selectedSymptoms.includes(symptom)
                            ? 'border-rose-400 bg-rose-400/20 text-rose-300'
                            : 'border-white/10 bg-black/35 text-zinc-400 hover:border-rose-400/35'
                        }`}
                      >
                        {symptom.replace(/_/g, ' ')}
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {trackingScenario === 'on-period' && (
              <div className="space-y-4">
                <h3 className="font-display text-lg text-rose-200/95">Tell me about your period today</h3>
                <p className="text-sm text-zinc-400">How is your flow today? I'm here to listen and help you track your patterns.</p>
                
                {/* Period Day */}
                <div className="text-left">
                  <label className="block text-sm font-medium text-zinc-300 mb-2">Which day of your period is this?</label>
                  <input
                    type="number"
                    min="1"
                    max="10"
                    className={input}
                    placeholder="e.g., Day 1, Day 2..."
                  />
                </div>

                {/* Flow Intensity */}
                <div className="text-left">
                  <label className="block text-sm font-medium text-zinc-300 mb-2">How is your flow today?</label>
                  <div className="grid grid-cols-3 gap-2">
                    {["light", "medium", "heavy"].map((flow) => (
                      <button
                        key={flow}
                        type="button"
                        onClick={() => setForm((f) => ({ ...f, flow }))}
                        className={`p-3 rounded-xl border transition-all ${
                          form.flow === flow
                            ? 'border-rose-400 bg-rose-400/20 text-rose-300'
                            : 'border-white/10 bg-black/35 text-zinc-400 hover:border-rose-400/35'
                        }`}
                      >
                        <div className="capitalize">{flow}</div>
                      </button>
                    ))}
                  </div>
                </div>

                {/* Period Symptoms */}
                <div className="text-left">
                  <label className="block text-sm font-medium text-zinc-300 mb-3">Any symptoms today?</label>
                  <div className="flex flex-wrap gap-2">
                    {["cramps", "bloating", "headache", "back_pain", "fatigue", "nausea"].map((symptom) => (
                      <button
                        key={symptom}
                        type="button"
                        onClick={() => toggleCommonSymptom(symptom)}
                        className={`px-3 py-1 rounded-full text-xs border transition-all ${
                          selectedSymptoms.includes(symptom)
                            ? 'border-rose-400 bg-rose-400/20 text-rose-300'
                            : 'border-white/10 bg-black/35 text-zinc-400 hover:border-rose-400/35'
                        }`}
                      >
                        {symptom.replace(/_/g, ' ')}
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {trackingScenario === 'post-period' && (
              <div className="space-y-4">
                <h3 className="font-display text-lg text-rose-200/95">Tell me how your period went</h3>
                <p className="text-sm text-zinc-400">Share your overall experience so I can help you understand your patterns better.</p>
                
                {/* Date Range */}
                <div className="grid gap-4 sm:grid-cols-2">
                  <div className="text-left">
                    <label className="block text-sm font-medium text-zinc-300 mb-2">When did your period start?</label>
                    <input
                      type="date"
                      className={input}
                      value={form.start_date}
                      onChange={(e) => setForm((f) => ({ ...f, start_date: e.target.value }))}
                      required
                    />
                  </div>
                  <div className="text-left">
                    <label className="block text-sm font-medium text-zinc-300 mb-2">When did it end?</label>
                    <input
                      type="date"
                      className={input}
                      value={form.end_date}
                      onChange={(e) => setForm((f) => ({ ...f, end_date: e.target.value }))}
                    />
                  </div>
                </div>

                {/* Overall Flow */}
                <div className="text-left">
                  <label className="block text-sm font-medium text-zinc-300 mb-2">How would you describe your overall flow?</label>
                  <div className="grid grid-cols-3 gap-2">
                    {["light", "medium", "heavy"].map((flow) => (
                      <button
                        key={flow}
                        type="button"
                        onClick={() => setForm((f) => ({ ...f, flow }))}
                        className={`p-3 rounded-xl border transition-all ${
                          form.flow === flow
                            ? 'border-rose-400 bg-rose-400/20 text-rose-300'
                            : 'border-white/10 bg-black/35 text-zinc-400 hover:border-rose-400/35'
                        }`}
                      >
                        <div className="capitalize">{flow}</div>
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {/* Common sections for all scenarios */}
            {/* Mood Selection */}
            <div className="text-left">
              <label className="block text-sm font-medium text-zinc-300 mb-3">How are you feeling emotionally?</label>
              <div className="grid grid-cols-5 gap-2">
                {MOOD_OPTIONS.map((mood) => (
                  <button
                    key={mood.value}
                    type="button"
                    onClick={() => handleMoodSelect(mood.value)}
                    className={`p-3 rounded-xl border transition-all ${
                      selectedMood === mood.value
                        ? 'border-rose-400 bg-rose-400/20 text-rose-300'
                        : 'border-white/10 bg-black/35 text-zinc-400 hover:border-rose-400/35'
                    }`}
                    title={mood.label}
                  >
                    <div className="text-2xl">{mood.emoji}</div>
                    <div className="text-xs mt-1 capitalize">{mood.label}</div>
                  </button>
                ))}
              </div>
            </div>

            {/* Wellness Metrics */}
            <div className="grid gap-4 sm:grid-cols-3">
              <div className="text-left">
                <label className="block text-sm font-medium text-zinc-300 mb-2">How many hours did you sleep?</label>
                <input
                  type="number"
                  step="0.5"
                  className={input}
                  value={form.sleep_hours ?? ""}
                  onChange={(e) => {
                    const v = e.target.value;
                    const n = v === "" ? undefined : Number(v);
                    setForm((f) => ({ ...f, sleep_hours: Number.isFinite(n as number) ? (n as number) : undefined }));
                  }}
                />
              </div>
              <div className="text-left">
                <label className="block text-sm font-medium text-zinc-300 mb-2">Stress level (0-10)?</label>
                <input
                  type="number"
                  min={0}
                  max={10}
                  className={input}
                  value={form.stress ?? ""}
                  onChange={(e) => {
                    const v = e.target.value;
                    const n = v === "" ? undefined : Number(v);
                    setForm((f) => ({ ...f, stress: Number.isFinite(n as number) ? (n as number) : undefined }));
                  }}
                />
              </div>
              <div className="text-left">
                <label className="block text-sm font-medium text-zinc-300 mb-2">Exercise today?</label>
                <select
                  className={input}
                  value={form.exercise ?? ""}
                  onChange={(e) => setForm((f) => ({ ...f, exercise: e.target.value || undefined }))}
                >
                  {[
                    { v: "", label: "—" },
                    { v: "none", label: "none" },
                    { v: "light", label: "light" },
                    { v: "moderate", label: "moderate" },
                    { v: "heavy", label: "heavy" },
                  ].map((o) => (
                    <option key={o.v} value={o.v}>
                      {o.label}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            {/* Personal Notes */}
            <div className="text-left">
              <label className="block text-sm font-medium text-zinc-300 mb-2">Anything else you'd like to share with me?</label>
              <textarea
                className={input + " min-h-[90px] resize-y"}
                value={form.notes ?? ""}
                onChange={(e) => setForm((f) => ({ ...f, notes: e.target.value }))}
                placeholder="Tell me anything that's on your mind... I'm here to listen and care about you."
              />
            </div>

            <button
              type="submit"
              className="w-full rounded-2xl bg-gradient-to-r from-rose-500 to-pink-600 py-3.5 text-sm font-semibold text-white shadow-[0_0_24px_-8px_rgba(236,72,153,0.5)] transition hover:brightness-110 sm:w-auto sm:px-10"
            >
              Share with me 💝
            </button>
          </form>
        </GlassCard>

        {/* Recent Entries */}
        <GlassCard className="text-center">
          <h3 className="font-display text-lg text-rose-200/95 mb-4">Your health journey</h3>
          <p className="text-sm text-zinc-400 mb-6">Here's what you've shared with me recently</p>
          
          {isLoading ? (
            <div className="mt-4 space-y-3">
              {[...Array(3)].map((_, i) => (
                <div key={i} className="text-left rounded-xl border border-white/10 bg-black/25 p-4">
                  <div className="flex items-center justify-between mb-3">
                    <div className="h-5 bg-white/20 rounded w-32"></div>
                    <div className="h-4 bg-white/20 rounded w-20"></div>
                  </div>
                  <div className="space-y-2">
                    <div className="h-3 bg-white/20 rounded w-24"></div>
                    <div className="h-3 bg-white/20 rounded w-28"></div>
                    <div className="h-3 bg-white/20 rounded w-20"></div>
                  </div>
                </div>
              ))}
            </div>
          ) : rows.length === 0 ? (
            <div className="text-center py-8">
              <div className="text-4xl mb-4">🌸</div>
              <p className="text-zinc-400">No entries yet. Start sharing your journey with me!</p>
            </div>
          ) : (
            <div className="space-y-4">
              {rows
                .slice()
                .reverse()
                .slice(0, 5)
                .map((c) => {
                  const entryDate = new Date(c.start_date);
                  const isPeriodEntry = c.flow && c.flow !== 'none';
                  const hasSymptoms = c.symptoms && c.symptoms.length > 0;
                  const hasMood = c.mood;
                  const daysAgo = Math.floor((Date.now() - entryDate.getTime()) / (1000 * 60 * 60 * 24));
                  
                  return (
                    <div key={c.id} className="text-left rounded-xl border border-white/10 bg-black/25 p-4 hover:border-rose-400/30 transition-all">
                      <div className="flex items-center justify-between mb-3">
                        <div className="flex items-center gap-3">
                          <div className="text-2xl">
                            {isPeriodEntry ? '🩸' : hasMood ? '😊' : '🌸'}
                          </div>
                          <div>
                            <div className="font-medium text-white">
                              {isPeriodEntry ? 'Period Day' : hasMood ? 'Mood Check-in' : 'Daily Entry'}
                            </div>
                            <div className="text-xs text-zinc-400">
                              {daysAgo === 0 ? 'Today' : daysAgo === 1 ? 'Yesterday' : `${daysAgo} days ago`}
                            </div>
                          </div>
                        </div>
                        <button
                          type="button"
                          className="shrink-0 text-xs text-rose-400/80 hover:text-rose-300 transition-colors"
                          onClick={() => void cyclesApi.del(c.id).then(() => load())}
                        >
                          Remove
                        </button>
                      </div>
                      
                      <div className="space-y-2">
                        {isPeriodEntry && (
                          <div className="flex items-center gap-2 text-sm">
                            <span className="px-2 py-1 rounded-full bg-rose-400/20 text-rose-300 text-xs">
                              {c.flow} flow
                            </span>
                            {c.end_date && c.end_date !== c.start_date && (
                              <span className="text-zinc-400 text-xs">
                                {c.start_date} → {c.end_date}
                              </span>
                            )}
                          </div>
                        )}
                        
                        {hasMood && (
                          <div className="flex items-center gap-2 text-sm">
                            <span className="text-zinc-300">Feeling:</span>
                            <span className="px-2 py-1 rounded-full bg-violet-400/20 text-violet-300 text-xs capitalize">
                              {c.mood}
                            </span>
                          </div>
                        )}
                        
                        {hasSymptoms && (
                          <div className="flex flex-wrap gap-1">
                            <span className="text-zinc-300 text-sm">Symptoms:</span>
                            {c.symptoms.slice(0, 3).map((symptom, idx) => (
                              <span key={idx} className="px-2 py-1 rounded-full bg-amber-400/20 text-amber-300 text-xs">
                                {symptom.replace(/_/g, ' ')}
                              </span>
                            ))}
                            {c.symptoms.length > 3 && (
                              <span className="px-2 py-1 rounded-full bg-zinc-400/20 text-zinc-300 text-xs">
                                +{c.symptoms.length - 3} more
                              </span>
                            )}
                          </div>
                        )}
                        
                        {c.notes && (
                          <div className="text-sm text-zinc-400 italic">
                            "{c.notes}"
                          </div>
                        )}
                        
                        {(c.sleep_hours || c.stress || c.exercise) && (
                          <div className="flex flex-wrap gap-3 text-xs text-zinc-500">
                            {c.sleep_hours && (
                              <span>💤 {c.sleep_hours}h sleep</span>
                            )}
                            {c.stress && (
                              <span>😰 Stress: {c.stress}/10</span>
                            )}
                            {c.exercise && (
                              <span>🏃 {c.exercise} exercise</span>
                            )}
                          </div>
                        )}
                      </div>
                    </div>
                  );
                })}
            </div>
          )}
        </GlassCard>
      </div>
    </>
  );
}
