import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  LineChart,
  Line,
  CartesianGrid,
} from "recharts";
import { GlassCard } from "../components/GlassCard";
import { 
  CardSkeleton, 
  ChartSkeleton, 
  HeatmapSkeleton, 
  LoadingState 
} from "../components/LoadingSkeleton";
import { analyticsApi, wellnessApi } from "../lib/api";
import { useTheme } from "../context/ThemeContext";
import { BubbleCursor } from "../components/BubbleCursor";
import { AmbientBackground } from "../components/AmbientBackground";

export default function MyPatterns() {
  const { t } = useTranslation();
  const { theme, toggleTheme } = useTheme();
  const [d, setD] = useState<{
    irregularity_index: number;
    pcod: { risk_score: number; level: string; factors: { tier: string; label: string }[] };
    symptom_frequency: { symptom: string; count: number }[];
    cycle_length_trend: { index: number; length_days: number; period_start: string }[];
    calendar_heatmap_6m: { start: string; days: { date: string; in_period: boolean; intensity: number }[] };
    mood_patterns: { mood: string; count: number; avg_stress: number; avg_sleep: number }[];
    wellness_metrics: { avg_sleep: number; avg_stress: number; exercise_frequency: { type: string; count: number }[] };
    pre_period_patterns: { days_before: number; common_symptoms: string[]; common_moods: string[] }[];
    personal_insights: { type: string; message: string; confidence: number }[];
  } | null>(null);
  const [err, setErr] = useState<string | null>(null);

  useEffect(() => {
    const loadAllData = async () => {
      try {
        // Load analytics data
        const analyticsResponse = await analyticsApi.dashboard();
        const analyticsData = analyticsResponse.data;
        
        // Load comprehensive wellness data for enhanced insights
        const wellnessResponse = await wellnessApi.comprehensive();
        const wellnessData = wellnessResponse.data;
        
        // Combine data
        setD({
          ...analyticsData,
          wellness: wellnessData.overall_wellness,
          stress: wellnessData.stress,
          mood: wellnessData.mood,
          sleep: wellnessData.sleep,
        });
      } catch (e) {
        setErr((e as Error)?.message || "failed");
      }
    };
    
    loadAllData();
  }, []);

  if (err) return <p className="text-center text-rose-300">{err}</p>;
  if (!d) return (
    <>
      <BubbleCursor />
      <AmbientBackground />
      <div className="max-w-4xl mx-auto px-4 space-y-8 text-center">
        <div className="text-center mb-8">
          <h1 className="font-display text-3xl font-bold text-transparent bg-gradient-to-r from-rose-200 via-pink-200 to-violet-200 bg-clip-text mb-4">
            My Patterns
          </h1>
          <p className="text-lg text-zinc-300 max-w-2xl mx-auto">
            Understanding your body's rhythms helps you take better care of yourself. Let's explore your patterns together.
          </p>
        </div>
        <div className="grid gap-4 sm:grid-cols-3">
          <CardSkeleton />
          <CardSkeleton className="sm:col-span-2" />
        </div>
        <GlassCard>
          <p className="text-sm text-zinc-400">Loading your patterns...</p>
          <div className="mt-2">
            <ChartSkeleton />
          </div>
        </GlassCard>
      </div>
    </>
  );

  const trend = d.cycle_length_trend || [];
  const barData = d.symptom_frequency?.slice(0, 8) || [];
  const heat = d.calendar_heatmap_6m?.days || [];
  
  // Group days by month for horizontal layout
  const monthsData: { month: string; year: number; days: typeof heat }[] = [];
  const monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  
  if (heat.length > 0) {
    const startDate = new Date(heat[0].date);
    const currentMonth = startDate.getMonth();
    const currentYear = startDate.getFullYear();
    
    // Group by month
    for (let monthOffset = 0; monthOffset < 6; monthOffset++) {
      const targetDate = new Date(currentYear, currentMonth + monthOffset, 1);
      const monthName = monthNames[targetDate.getMonth()];
      const year = targetDate.getFullYear();
      
      const monthDays = heat.filter(day => {
        const dayDate = new Date(day.date);
        return dayDate.getMonth() === targetDate.getMonth() && dayDate.getFullYear() === targetDate.getFullYear();
      });
      
      monthsData.push({ month: monthName, year, days: monthDays });
    }
  }

  // Enhanced data processing for comprehensive insights
  const moodData = d?.mood_patterns || [];
  const wellnessData = d?.wellness_metrics || {};
  const prePeriodData = d?.pre_period_patterns || [];
  const insightsData = d?.personal_insights || [];

  // Calculate comprehensive wellness score using all metrics
  const calculateWellnessScore = () => {
    if (!d) return 0;
    
    let score = 100;
    
    // Deduct for irregular cycles
    score -= d.irregularity_index * 0.3;
    
    // Deduct for PCOD risk
    score -= d.pcod.risk_score * 0.4;
    
    // Bonus for good sleep (if data available)
    if (wellnessData.avg_sleep && wellnessData.avg_sleep >= 7) {
      score += 5;
    } else if (wellnessData.avg_sleep && wellnessData.avg_sleep < 6) {
      score -= 5;
    }
    
    // Bonus for low stress (if data available)
    if (wellnessData.avg_stress && wellnessData.avg_stress <= 3) {
      score += 5;
    } else if (wellnessData.avg_stress && wellnessData.avg_stress >= 7) {
      score -= 5;
    }
    
    return Math.max(0, Math.min(100, Math.round(score)));
  };

  // Generate mood-symptom correlations
  const getMoodSymptomInsights = () => {
    if (!moodData.length || !barData.length) return [];
    
    const insights = [];
    
    // Find most common mood
    const topMood = moodData.reduce((prev, current) => 
      (prev.count > current.count) ? prev : current
    );
    
    // Correlate with symptoms
    const moodRelatedSymptoms = barData.filter(symptom => 
      symptom.symptom.toLowerCase().includes('mood') || 
      symptom.symptom.toLowerCase().includes('anxious') ||
      symptom.symptom.toLowerCase().includes('irritable')
    );
    
    if (topMood && moodRelatedSymptoms.length > 0) {
      insights.push({
        type: 'mood-symptom',
        message: `Your dominant mood is ${topMood.mood}, which directly triggers ${moodRelatedSymptoms[0]?.symptom?.replace(/_/g, ' ')}. Solution: Address mood first to prevent physical symptoms.`,
        confidence: 0.8
      });
    }
    
    return insights;
  };

  // Generate sleep-stress insights
  const getSleepStressInsights = () => {
    if (!wellnessData.avg_sleep || !wellnessData.avg_stress) return [];
    
    const insights = [];
    
    if (wellnessData.avg_sleep < 6 && wellnessData.avg_stress > 6) {
      insights.push({
        type: 'sleep-stress',
        message: `CRITICAL: You're averaging ${wellnessData.avg_sleep.toFixed(1)}h sleep with ${wellnessData.avg_stress.toFixed(1)}/10 stress. Fix: Go to bed 1 hour earlier + no screens 30min before bed.`,
        confidence: 0.9
      });
    } else if (wellnessData.avg_sleep >= 8 && wellnessData.avg_stress <= 4) {
      insights.push({
        type: 'sleep-stress',
        message: `EXCELLENT: ${wellnessData.avg_sleep.toFixed(1)}h sleep with ${wellnessData.avg_stress.toFixed(1)}/10 stress. Maintain this routine - it's working perfectly.`,
        confidence: 0.9
      });
    }
    
    return insights;
  };

  // Generate exercise-mood insights
  const getExerciseMoodInsights = () => {
    if (!wellnessData.exercise_frequency || !moodData.length) return [];
    
    const insights = [];
    const exerciseFreq = wellnessData.exercise_frequency.find(e => e.type === 'moderate' || e.type === 'heavy');
    
    if (exerciseFreq && exerciseFreq.count > 0) {
      const positiveMoods = moodData.filter(m => 
        m.mood === 'happy' || m.mood === 'calm' || m.mood === 'energetic'
      );
      
      if (positiveMoods.length > moodData.length * 0.6) {
        insights.push({
          type: 'exercise-mood',
          message: `Your ${exerciseFreq.type} exercise is directly improving your mood. Continue: ${exerciseFreq.count} sessions/week + add 1 more session for better results.`,
          confidence: 0.7
        });
      } else {
        insights.push({
          type: 'exercise-mood',
          message: `You're exercising but mood isn't improving. Solution: Try morning exercise + add mood tracking before/after workouts.`,
          confidence: 0.7
        });
      }
    } else {
      insights.push({
        type: 'exercise-mood',
        message: "NO EXERCISE RECORDED. Start with 10-minute walks daily + track mood changes. Exercise is essential for mood regulation.",
        confidence: 0.8
      });
    }
    
    return insights;
  };

  // Generate pre-period predictions
  const getPrePeriodInsights = () => {
    if (!prePeriodData.length) return [];
    
    const insights = [];
    const mostCommonPattern = prePeriodData[0]; // Assuming sorted by frequency
    
    if (mostCommonPattern && mostCommonPattern.common_symptoms.length > 0) {
      insights.push({
        type: 'pre-period',
        message: `${mostCommonPattern.days_before} days before period: Expect ${mostCommonPattern.common_symptoms.slice(0, 2).join(' + ')}. Prepare: Start self-care 2 days earlier + track symptoms.`,
        confidence: 0.8
      });
    }
    
    return insights;
  };

  // Combine all insights
  const allInsights = [
    ...getMoodSymptomInsights(),
    ...getSleepStressInsights(),
    ...getExerciseMoodInsights(),
    ...getPrePeriodInsights(),
    ...(insightsData || [])
  ].slice(0, 3); // Top 3 most relevant insights

  return (
    <>
      <BubbleCursor />
      <AmbientBackground />
      <div className="max-w-4xl mx-auto px-4 space-y-8 text-center">
        {/* Welcome Header */}
        <div className="text-center mb-8">
          <h1 className="font-display text-3xl font-bold text-transparent bg-gradient-to-r from-rose-200 via-pink-200 to-violet-200 bg-clip-text mb-4">
            My Patterns
          </h1>
          <p className="text-lg text-zinc-300 max-w-2xl mx-auto">
            Understanding your body's rhythms helps you take better care of yourself. Let's explore your patterns together.
          </p>
        </div>

        {/* Health Overview Cards */}
        <div className="grid gap-4 sm:grid-cols-3">
          <GlassCard className="text-center">
            <div className="text-3xl mb-2">🌸</div>
            <h3 className="font-display text-lg text-transparent bg-gradient-to-r from-rose-200 via-pink-200 to-violet-200 bg-clip-text mb-2">
              Cycle Regularity
            </h3>
            <div className="space-y-2">
              <div className="text-2xl font-bold text-rose-100">
                {d.irregularity_index < 30 ? 'Very Regular' : d.irregularity_index < 60 ? 'Moderately Regular' : 'Irregular'}
              </div>
              <div className="text-xs text-zinc-400">
                Score: {d.irregularity_index}/100
              </div>
              <div className="text-xs text-zinc-500 mt-2">
                {d.irregularity_index < 30 ? 'Your cycles are very predictable! 🎉' : 
                 d.irregularity_index < 60 ? 'Your cycles have some variation, which is normal.' :
                 'Your cycles vary quite a bit. This is common and worth tracking.'}
              </div>
            </div>
          </GlassCard>
          
          <GlassCard glow className="sm:col-span-2 text-center">
            <div className="text-3xl mb-2">💝</div>
            <h3 className="font-display text-lg text-transparent bg-gradient-to-r from-rose-200 via-pink-200 to-violet-200 bg-clip-text mb-2">
              Your Wellness Score
            </h3>
            <div className="space-y-2">
              <div className="text-2xl font-bold text-rose-100">
                {calculateWellnessScore()}%
              </div>
              <div className="text-xs text-zinc-400">
                Based on your cycles, mood, sleep, stress & exercise patterns
              </div>
              <div className="text-xs text-zinc-500 mt-2">
                {calculateWellnessScore() >= 85 ? 'Excellent! Your body is thriving with your care! 🌟' :
                 calculateWellnessScore() >= 70 ? 'Great progress! You\'re building healthy habits. 💪' :
                 calculateWellnessScore() >= 50 ? 'Good foundation! Let\'s enhance your wellness journey. 🌱' :
                 'You\'re taking the first step - I\'m here to support you! 💝'}
              </div>
            </div>
          </GlassCard>
        </div>

        {/* Cycle Length Trends */}
        <GlassCard className="text-center">
          <h3 className="font-display text-xl text-transparent bg-gradient-to-r from-rose-200 via-pink-200 to-violet-200 bg-clip-text mb-4">
            Your Cycle Journey
          </h3>
          <p className="text-sm text-zinc-400 mb-6">How your cycle lengths have changed over time</p>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={trend} margin={{ left: 0, right: 8 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#ffffff18" />
                <XAxis dataKey="index" tick={{ fill: "#a1a1aa" }} fontSize={11} />
                <YAxis tick={{ fill: "#a1a1aa" }} fontSize={11} />
                <Tooltip contentStyle={{ background: "#120810", border: "1px solid rgba(255,255,255,0.12)" }} />
                <Line type="monotone" dataKey="length_days" stroke="#f9a8d4" strokeWidth={2} dot={{ fill: "#fbcfe8" }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
          <div className="mt-4 text-xs text-zinc-500">
            Typical cycle length: {trend.length > 0 ? Math.round(trend.reduce((sum, t) => sum + t.length_days, 0) / trend.length) : '--'} days
          </div>
        </GlassCard>

        {/* Common Symptoms */}
        <GlassCard className="text-center">
          <h3 className="font-display text-xl text-transparent bg-gradient-to-r from-rose-200 via-pink-200 to-violet-200 bg-clip-text mb-4">
            Your Body's Signals
          </h3>
          <p className="text-sm text-zinc-400 mb-6">What your body tells you most often</p>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={barData.map(item => ({
                ...item,
                symptom: item.symptom.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
              }))} margin={{ left: 0, right: 8, top: 20, bottom: 60 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#ffffff18" />
                <XAxis 
                  dataKey="symptom" 
                  tick={{ fill: "#a1a1aa", fontSize: 10 }} 
                  angle={-45}
                  textAnchor="end"
                  height={80}
                />
                <YAxis tick={{ fill: "#a1a1aa" }} fontSize={11} />
                <Tooltip 
                  contentStyle={{ 
                    background: "rgba(18, 8, 16, 0.95)", 
                    border: "1px solid rgba(244, 114, 182, 0.3)",
                    borderRadius: "8px"
                  }}
                  formatter={(value: any) => [`${value} times`, 'Frequency']}
                />
                <Bar 
                  dataKey="count" 
                  fill="#f9a8d4" 
                  radius={[8, 8, 0, 0]}
                  onMouseEnter={(data: any) => {
                    // Custom hover effect
                  }}
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
          
          {/* Direct Actionable Insights */}
          <div className="mt-6 space-y-3 text-left">
            {barData.length > 0 && (
              <>
                <div className="p-3 rounded-xl border border-amber-200/20 bg-amber-500/5">
                  <h4 className="font-medium text-amber-200 mb-1 text-sm">⚠️ Your Primary Issue</h4>
                  <p className="text-xs text-zinc-300">
                    <span className="font-semibold text-amber-100">{barData[0]?.symptom?.replace(/_/g, ' ')}</span> is your #1 problem - 
                    it appeared {barData[0]?.count} times. You need to address this consistently.
                  </p>
                </div>
                
                {barData.length > 1 && (
                  <div className="p-3 rounded-xl border border-violet-200/20 bg-violet-500/5">
                    <h4 className="font-medium text-violet-200 mb-1 text-sm">🔗 Connected Issue</h4>
                    <p className="text-xs text-zinc-300">
                      <span className="font-semibold text-violet-100">{barData[1]?.symptom?.replace(/_/g, ' ')}</span> often occurs with your main issue. 
                      Watch for this pattern - when one appears, the other usually follows.
                    </p>
                  </div>
                )}
                
                <div className="p-3 rounded-xl border border-emerald-200/20 bg-emerald-500/5">
                  <h4 className="font-medium text-emerald-200 mb-1 text-sm">✅ Your Action Plan</h4>
                  <p className="text-xs text-zinc-300">
                    {barData[0]?.symptom?.includes('cramp') ? 
                      "For cramps: Do 5 minutes of gentle stretching + apply warm compress for 15 minutes. Repeat 2x daily when cramps appear." :
                     barData[0]?.symptom?.includes('headache') ?
                      "For headaches: Drink 2 glasses water immediately + practice 4-7-8 breathing for 2 minutes. Track if stress is the trigger." :
                     barData[0]?.symptom?.includes('bloat') ?
                      "For bloating: Walk for 10 minutes after meals + drink 8oz water every hour. Avoid carbonated drinks during bloating." :
                     barData[0]?.symptom?.includes('fatigue') ?
                      "For fatigue: Go to bed 30 minutes earlier + take 5-minute movement breaks every 2 hours. Check your iron levels." :
                     barData[0]?.symptom?.includes('mood') || barData[0]?.symptom?.includes('anxious') ?
                      "For mood issues: Write down triggers + practice 5-minute morning meditation. Consider reducing caffeine intake." :
                     "Track this symptom for 7 days to identify your personal triggers and create a specific action plan."
                    }
                  </p>
                </div>
              </>
            )}
          </div>
        </GlassCard>

        {/* Six Month Calendar */}
        <GlassCard className="text-center p-6">
          <div className="mb-6">
            <h3 className="font-display text-xl text-transparent bg-gradient-to-r from-rose-200 via-pink-200 to-violet-200 bg-clip-text mb-2">
              Six Months at a Glance
            </h3>
            <p className="text-sm text-zinc-400">Rose days show when you had your period</p>
          </div>
          
          <div className="mt-6 overflow-x-auto">
            <div className="space-y-4">
              {monthsData.map((monthData) => (
                <div key={`${monthData.month}-${monthData.year}`} className="space-y-2">
                  <div className="flex items-center gap-4">
                    <h4 className="text-sm font-semibold text-rose-100 min-w-[60px]">
                      {monthData.month} {monthData.year}
                    </h4>
                    <div className="flex-1 h-px bg-white/10"></div>
                    <div className="text-xs text-zinc-500">
                      {monthData.days.filter(d => d.in_period).length} period days
                    </div>
                  </div>
                  
                  <div className="flex flex-wrap gap-1.5">
                    {monthData.days.map((day) => (
                      <div
                        key={day.date}
                        title={day.date}
                        className="w-4 h-4 rounded-md transition-all duration-200 hover:scale-110 cursor-pointer"
                        style={{
                          background: day.in_period
                            ? day.intensity >= 2 
                              ? "linear-gradient(135deg, #f43f5e, #ec4899)"
                              : day.intensity >= 1
                              ? "linear-gradient(135deg, #f472b6, #a78bfa)"
                              : "linear-gradient(135deg, #f9a8d4, #c084fc)"
                            : "rgba(255,255,255,0.08)",
                          boxShadow: day.in_period ? "0 0 8px rgba(244, 114, 182, 0.3)" : "none",
                          border: day.in_period ? "1px solid rgba(244, 114, 182, 0.2)" : "1px solid rgba(255,255,255,0.05)",
                        }}
                      />
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
          
          <div className="mt-6 flex items-center justify-center gap-6 text-xs text-zinc-500">
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-sm bg-gradient-to-br from-rose-400 to-violet-400"></div>
              <span>Period days</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-sm bg-white/10"></div>
              <span>Non-period days</span>
            </div>
          </div>
        </GlassCard>

        {/* Comprehensive Personal Insights */}
        <GlassCard className="text-center">
          <h3 className="font-display text-xl text-transparent bg-gradient-to-r from-rose-200 via-pink-200 to-violet-200 bg-clip-text mb-4">
            Your Personal Health Story
          </h3>
          <p className="text-sm text-zinc-400 mb-6">Insights from your cycles, mood, sleep, stress, and exercise patterns</p>
          
          <div className="space-y-4 text-left">
            {allInsights.map((insight, index) => (
              <div 
                key={index}
                className={`p-4 rounded-xl border ${
                  insight.type === 'mood-symptom' ? 'border-amber-200/20 bg-amber-500/5' :
                  insight.type === 'sleep-stress' ? 'border-blue-200/20 bg-blue-500/5' :
                  insight.type === 'exercise-mood' ? 'border-emerald-200/20 bg-emerald-500/5' :
                  insight.type === 'pre-period' ? 'border-purple-200/20 bg-purple-500/5' :
                  'border-rose-200/20 bg-rose-500/5'
                }`}
              >
                <h4 className={`font-medium mb-2 text-sm ${
                  insight.type === 'mood-symptom' ? 'text-amber-200' :
                  insight.type === 'sleep-stress' ? 'text-blue-200' :
                  insight.type === 'exercise-mood' ? 'text-emerald-200' :
                  insight.type === 'pre-period' ? 'text-purple-200' :
                  'text-rose-200'
                }`}>
                  {insight.type === 'mood-symptom' && '🧠 Mood & Symptom Connection'}
                  {insight.type === 'sleep-stress' && '😴 Sleep & Stress Balance'}
                  {insight.type === 'exercise-mood' && '🏃 Exercise & Mood Link'}
                  {insight.type === 'pre-period' && '🔮 Pre-Period Pattern'}
                  {insight.type === 'general' && '💝 Body Wisdom'}
                </h4>
                <p className="text-sm text-zinc-300">{insight.message}</p>
                <div className="mt-2 text-xs text-zinc-500">
                  Confidence: {Math.round(insight.confidence * 100)}%
                </div>
              </div>
            ))}
            
            {/* Wellness Summary */}
            <div className="p-4 rounded-xl border border-violet-200/20 bg-violet-500/5">
              <h4 className="font-medium text-violet-200 mb-2 text-sm">📊 Your Wellness Summary</h4>
              <div className="grid grid-cols-2 gap-4 text-xs">
                <div>
                  <span className="text-zinc-400">Average Sleep:</span>
                  <span className="text-violet-100 ml-2">{wellnessData.avg_sleep ? `${wellnessData.avg_sleep.toFixed(1)}h` : 'Not tracked'}</span>
                </div>
                <div>
                  <span className="text-zinc-400">Average Stress:</span>
                  <span className="text-violet-100 ml-2">{wellnessData.avg_stress ? `${wellnessData.avg_stress.toFixed(1)}/10` : 'Not tracked'}</span>
                </div>
                <div>
                  <span className="text-zinc-400">Most Common Mood:</span>
                  <span className="text-violet-100 ml-2">{moodData.length > 0 ? moodData[0]?.mood : 'Not tracked'}</span>
                </div>
                <div>
                  <span className="text-zinc-400">Exercise Pattern:</span>
                  <span className="text-violet-100 ml-2">
                    {wellnessData.exercise_frequency?.length > 0 ? 
                      `${wellnessData.exercise_frequency[0]?.type} intensity` : 
                      'Not tracked'
                    }
                  </span>
                </div>
              </div>
            </div>
            
            {/* Direct Action Plan */}
            <div className="p-4 rounded-xl border border-emerald-200/20 bg-emerald-500/5">
              <h4 className="font-medium text-emerald-200 mb-2 text-sm">� Your Required Actions</h4>
              <p className="text-sm text-zinc-300">
                {calculateWellnessScore() >= 85 ? 
                  "MAINTAIN EXCELLENCE: Your routine works perfectly. Add 1 new wellness habit this month + mentor someone else." :
                 calculateWellnessScore() >= 70 ?
                  "IMPROVE CONSISTENCY: Set phone reminders for sleep/water/exercise. Track compliance for 30 days." :
                 calculateWellnessScore() >= 50 ?
                  "PRIORITY: Fix sleep schedule. Bedtime: 10PM daily. No screens after 9:30PM. Wake: 6AM daily." :
                  "START NOW: 3 non-negotiable daily habits: 1) 8 glasses water, 2) 10-minute walk, 3) 7 hours sleep. Track for 21 days."
                }
              </p>
            </div>
          </div>
        </GlassCard>
      </div>
    </>
  );
}
