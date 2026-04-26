import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { Link } from "react-router-dom";
import { GlassCard } from "../components/GlassCard";
import { insightsApi, wellnessApi } from "../lib/api";
import { downloadDoctorReport } from "../lib/report";
import { BubbleCursor } from "../components/BubbleCursor";
import { AmbientBackground } from "../components/AmbientBackground";

type Pred = {
  predicted_length_days?: number;
  confidence?: number;
  cycle_index: number;
  interval_low?: number;
  interval_high?: number;
};

export default function Home() {
  const { t } = useTranslation();
  const [data, setData] = useState<{
    pcod: { risk_score: number; level: string; recommendation: string };
    prediction: { next_cycles: Pred[]; method?: string; overall_confidence?: number };
    alerts: { text: string; severity: string }[];
    next_period_estimate?: string | null;
    wellness?: {
      score: {
        wellness_score: number;
        factors: any;
        recommendations: any[];
        trend: string;
        data_points: number;
      };
      trend: string;
      insights: any[];
    };
    stress?: {
      current: any;
      trend: any;
    };
    mood?: {
      current: string;
      trends: any;
    };
    sleep?: {
      current: number;
      trends: any;
    };
  } | null>(null);
  const [err, setErr] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadAllData = async () => {
      try {
        // Load insights data
        const insightsResponse = await insightsApi.smart();
        const insightsData = insightsResponse.data;
        
        // Load comprehensive wellness data
        const wellnessResponse = await wellnessApi.comprehensive();
        const wellnessData = wellnessResponse.data;
        
        // Combine all data
        setData({
          ...insightsData,
          wellness: wellnessData.overall_wellness,
          stress: wellnessData.stress,
          mood: wellnessData.mood,
          sleep: wellnessData.sleep,
        });
      } catch (e) {
        setErr((e as Error)?.message || "load failed");
      } finally {
        setLoading(false);
      }
    };
    
    loadAllData();
  }, []);

  if (loading) {
    return (
      <p className="text-center text-sm tracking-wide text-rose-200/60">{t("analytics.loading")}</p>
    );
  }
  if (err) return <p className="text-center text-rose-300">{err}</p>;
  if (!data) return null;

  return (
    <>
      <BubbleCursor />
      <AmbientBackground />
      <div className="max-w-4xl mx-auto px-4 space-y-8 text-center">
        {/* Welcome Header */}
        <div className="text-center mb-8">
          <h1 className="font-display text-4xl font-bold text-transparent bg-gradient-to-r from-rose-200 via-pink-200 to-violet-200 bg-clip-text mb-4">
            Welcome to your personal health dashboard
          </h1>
          <p className="text-lg text-zinc-300 max-w-2xl mx-auto">
            Track your cycle patterns and get helpful insights about your body with SheWins.
          </p>
        </div>

        {/* Wellness Score */}
        {data.wellness && (
          <GlassCard className="group relative overflow-hidden text-center">
            {/* Animated background pattern */}
            <div className="absolute inset-0 bg-gradient-to-br from-emerald-500/5 via-green-500/5 to-teal-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
            
            <div className="relative">
              <h2 className="font-display text-lg text-emerald-200/95 flex items-center gap-2">
                Your Wellness Score
                <div className="w-2 h-2 bg-emerald-400 rounded-full animate-pulse"></div>
              </h2>
              <p className="mt-0.5 text-[11px] uppercase tracking-wider text-zinc-500">Overall health & wellness</p>
              
              {/* Wellness Score with animated ring */}
              <div className="relative inline-block mt-4">
                <div className="absolute inset-0 rounded-full border-4 border-emerald-400/20 animate-ping"></div>
                <p className="relative text-5xl font-bold tabular-nums text-transparent bg-gradient-to-r from-emerald-200 via-green-200 to-teal-200 bg-clip-text group-hover:scale-110 transition-transform duration-300">
                  {data.wellness?.score?.wellness_score || 0}%
                </p>
              </div>
              
              <div className="mt-4 space-y-2">
                <p className="text-sm capitalize text-emerald-200/90 inline-flex items-center gap-2">
                  <span>Trend:</span>
                  <span className="px-2 py-1 rounded-full bg-emerald-500/20 text-emerald-200 text-xs font-medium">
                    {data.wellness?.score?.trend || 'Stable'}
                  </span>
                </p>
                <div className="text-xs text-zinc-400">
                  {data.sleep?.current && (
                    <div className="grid grid-cols-3 gap-2 mt-2">
                      <div>Sleep: {data.sleep.current}h</div>
                      <div>Stress: {data.stress?.current?.stress_score || 'N/A'}/10</div>
                      <div>Mood: {data.mood?.current || 'N/A'}</div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </GlassCard>
        )}

        {/* Health Risk Score */}
        <GlassCard className="group relative overflow-hidden text-center">
            {/* Animated background pattern */}
            <div className="absolute inset-0 bg-gradient-to-br from-rose-500/5 via-pink-500/5 to-violet-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
            
            <div className="relative">
              <h2 className="font-display text-lg text-rose-200/95 flex items-center gap-2">
                {t("home.riskTitle")}
                <div className="w-2 h-2 bg-amber-400 rounded-full animate-pulse"></div>
              </h2>
              <p className="mt-0.5 text-[11px] uppercase tracking-wider text-zinc-500">{t("home.riskSub")}</p>
              
              {/* Risk Score with animated ring */}
              <div className="relative inline-block mt-4">
                <div className="absolute inset-0 rounded-full border-4 border-rose-400/20 animate-ping"></div>
                <p className="relative text-5xl font-bold tabular-nums text-transparent bg-gradient-to-r from-rose-200 via-pink-200 to-violet-200 bg-clip-text group-hover:scale-110 transition-transform duration-300">
                  {data.pcod.risk_score}%
                </p>
              </div>
              
              <div className="mt-4 space-y-2">
                <p className="text-sm capitalize text-amber-200/90 inline-flex items-center gap-2">
                  <span>{t("home.level")}:</span>
                  <span className="px-2 py-1 rounded-full bg-amber-500/20 text-amber-200 text-xs font-medium animate-pulse">
                    {data.pcod.level}
                  </span>
                </p>
                <p className="text-sm leading-relaxed text-zinc-300 group-hover:text-white/90 transition-colors duration-300">{data.pcod.recommendation}</p>
              </div>
            </div>
          </GlassCard>

        {/* Your Upcoming Cycle Predictions */}
        <GlassCard glow className="text-center">
            <div className="mb-6">
              <h2 className="font-display text-2xl text-transparent bg-gradient-to-r from-rose-200 via-pink-200 to-violet-200 bg-clip-text mb-3">
                Your upcoming cycle predictions
              </h2>
              <p className="text-sm text-zinc-400 italic">
                {t("home.method")}: {data.prediction?.method || "—"}
              </p>
            </div>
            
            <div className="relative">
              {(data.prediction?.next_cycles || []).length > 0 ? (
                <div className="space-y-4">
                  {data.prediction.next_cycles.map((c, index) => (
                    <div key={c.cycle_index} className="relative group">
                      {/* Timeline Connection Line */}
                      {index < data.prediction.next_cycles.length - 1 && (
                        <div className="absolute left-6 top-12 w-0.5 h-16 bg-gradient-to-b from-rose-400/30 to-violet-400/30"></div>
                      )}
                      {/* Cycle Card */}
                      <div className="relative flex items-start gap-4 p-4 rounded-2xl border border-white/10 bg-gradient-to-r from-rose-500/5 via-pink-500/5 to-violet-500/5 hover:from-rose-500/10 hover:via-pink-500/10 hover:to-violet-500/10 transition-all duration-300">
                        {/* Cycle Number Badge */}
                        <div className="flex-shrink-0 w-12 h-12 rounded-full bg-gradient-to-br from-rose-500 to-violet-600 flex items-center justify-center text-white font-bold text-sm shadow-lg group-hover:scale-110 transition-transform">
                          {c.cycle_index}
                        </div>
                        {/* Cycle Details */}
                        <div className="flex-1 space-y-2">
                          <div className="flex items-center gap-3">
                            <span className="text-lg font-semibold text-white/90">
                              ~{c.predicted_length_days} days
                            </span>
                            {c.confidence != null && (
                              <div className="px-2 py-1 rounded-full bg-violet-500/20 text-violet-300 text-xs font-medium">
                                {c.confidence}% confidence
                              </div>
                            )}
                          </div>
                          {c.interval_low != null && c.interval_high != null && (
                            <div className="flex items-center gap-2 text-sm text-zinc-400">
                              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                              </svg>
                              <span>Range: {c.interval_low}–{c.interval_high} days</span>
                            </div>
                          )}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-8">
                  <div className="inline-flex items-center gap-3 px-6 py-3 rounded-full border border-white/20 bg-white/5">
                    <svg className="w-5 h-5 text-zinc-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                    <span className="text-zinc-400">{t("home.noPred")}</span>
                  </div>
                </div>
              )}
            </div>

            {/* Next Period Estimate */}
            {data.next_period_estimate && (
              <div className="mt-6 p-4 rounded-2xl border border-emerald-500/20 bg-emerald-500/5">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-full bg-gradient-to-br from-emerald-400 to-emerald-600 flex items-center justify-center">
                    <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                  </div>
                  <div>
                    <p className="text-sm text-emerald-300/80 mb-2 font-medium">Next Period</p>
                    <p className="text-lg font-semibold text-emerald-200/95">{data.next_period_estimate}</p>
                  </div>
                </div>
              </div>
            )}
          </GlassCard>

        {/* Alerts Section */}
        {data.alerts.length > 0 && (
          <GlassCard className="relative overflow-hidden border-amber-500/25 bg-amber-950/20 group text-center">
            {/* Alert animation background */}
            <div className="absolute inset-0 bg-gradient-to-br from-amber-500/10 via-orange-500/10 to-red-500/10 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
            
            <div className="relative">
              <h3 className="font-display text-amber-200/95 flex items-center gap-2">
                {t("home.alertsTitle")}
                <div className="flex items-center gap-1">
                  <div className="w-2 h-2 bg-amber-400 rounded-full animate-pulse"></div>
                  <span className="text-xs text-amber-300/80">{data.alerts.length} active</span>
                </div>
              </h3>
              
              <ul className="mt-3 space-y-2">
                {data.alerts.map((a, i) => (
                  <li 
                    key={i} 
                    className="flex items-start gap-3 p-3 rounded-xl border border-amber-400/20 bg-amber-500/5 hover:bg-amber-500/10 transition-all duration-300 group-hover:scale-102"
                  >
                    <div className="flex-shrink-0 mt-0.5">
                      <div className={`w-2 h-2 rounded-full ${
                        a.severity === 'high' ? 'bg-red-400 animate-ping' :
                        a.severity === 'medium' ? 'bg-amber-400 animate-pulse' :
                        'bg-yellow-400 animate-pulse'
                      }`}></div>
                    </div>
                    <p className="text-sm text-amber-100/90 leading-relaxed group-hover:text-amber-50 transition-colors duration-300">
                      {a.text}
                    </p>
                  </li>
                ))}
              </ul>
            </div>
          </GlassCard>
        )}

        {/* How are you feeling today? */}
        <GlassCard className="text-center">
          <div className="mb-4">
            <h2 className="font-display text-xl text-transparent bg-gradient-to-r from-rose-200 via-pink-200 to-violet-200 bg-clip-text mb-3">
              How are you feeling today?
            </h2>
            <p className="text-sm text-zinc-400 italic mb-4">
              Tell me about your day. Whether you're having your period, feeling different moods, or noticing changes in your body - I'm here to listen and care about you.
            </p>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-left">
              <div className="p-3 rounded-xl border border-rose-200/20 bg-rose-500/5">
                <h4 className="font-medium text-rose-200 mb-2 flex items-center gap-2">
                  <span className="w-2 h-2 bg-rose-400 rounded-full"></span>
                  Period Status
                </h4>
                <p className="text-xs text-rose-100/80">
                  Track your period flow, cramps, and physical symptoms
                </p>
              </div>
              
              <div className="p-3 rounded-xl border border-violet-200/20 bg-violet-500/5">
                <h4 className="font-medium text-violet-200 mb-2 flex items-center gap-2">
                  <span className="w-2 h-2 bg-violet-400 rounded-full"></span>
                  Mood & Emotions
                </h4>
                <p className="text-xs text-violet-100/80">
                  Share how you're feeling emotionally - happy, anxious, tired, or depressed
                </p>
              </div>
              
              <div className="p-3 rounded-xl border border-amber-200/20 bg-amber-500/5">
                <h4 className="font-medium text-amber-200 mb-2 flex items-center gap-2">
                  <span className="w-2 h-2 bg-amber-400 rounded-full"></span>
                  Body Changes
                </h4>
                <p className="text-xs text-amber-100/80">
                  Notice hunger levels, energy, sleep patterns, and other changes
                </p>
              </div>
              
              <div className="p-3 rounded-xl border border-emerald-200/20 bg-emerald-500/5">
                <h4 className="font-medium text-emerald-200 mb-2 flex items-center gap-2">
                  <span className="w-2 h-2 bg-emerald-400 rounded-full"></span>
                  Pattern Insights
                </h4>
                <p className="text-xs text-emerald-100/80">
                  I'll help you see patterns before periods and mood connections
                </p>
              </div>
            </div>
          </div>
          
          <Link
            to="/track"
            className="group inline-flex items-center justify-center rounded-2xl bg-gradient-to-r from-rose-500 to-violet-600 px-8 py-4 text-base font-medium text-white shadow-lg transition-all duration-300 hover:brightness-110 hover:scale-105"
          >
            <span className="mr-2">Share today's experience</span>
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
            </svg>
          </Link>
        </GlassCard>

        {/* Action Buttons */}
        <div className="flex flex-wrap gap-4 justify-center">
          <Link
            to="/analytics"
            className="group relative inline-flex items-center justify-center rounded-2xl border border-white/15 bg-white/5 px-6 py-3 text-sm font-medium text-zinc-200 backdrop-blur transition-all duration-300 hover:border-rose-400/40 hover:bg-rose-500/10 hover:scale-105 hover:shadow-[0_0_20px_-8px_rgba(139,92,246,0.3)]"
          >
            {/* Button icon with animation */}
            <div className="absolute -top-1 -right-1 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
              <svg className="w-4 h-4 text-violet-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h6l-2 2V9a2 2 0 00-2-2H7a2 2 0 00-2 2v6z" />
              </svg>
            </div>
            {t("home.ctaPatterns")}
          </Link>
          
          <button
            type="button"
            onClick={() => void downloadDoctorReport().catch((e) => alert(String(e)))}
            className="group relative inline-flex items-center justify-center rounded-2xl border border-rose-400/35 bg-rose-500/5 px-6 py-3 text-sm font-medium text-rose-100 transition-all duration-300 hover:bg-rose-500/15 hover:scale-105 hover:shadow-[0_0_20px_-8px_rgba(236,72,153,0.4)]"
          >
            {/* Button icon with animation */}
            <div className="absolute -top-1 -right-1 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
              <svg className="w-4 h-4 text-rose-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-6-6m6 6v6m0 0l-6-6m6 6v6m0 0l-6-6" />
              </svg>
            </div>
            {t("common.exportPdf")}
          </button>
        </div>
      </div>
    </>
  );
}
