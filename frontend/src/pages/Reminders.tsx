import { useEffect, useState } from "react";
import { GlassCard } from "../components/GlassCard";
import { predictApi, remindersApi, insightsApi } from "../lib/api";

// LocalStorage keys
const LOCAL_STORAGE_KEYS = {
  REMINDERS: 'eliteher-reminders',
  LAST_SYNC: 'eliteher-reminders-last-sync'
};

interface Reminder {
  id?: string;
  type: "period" | "symptom" | "medicine" | "appointment" | "custom";
  title: string;
  frequency: "daily" | "weekly" | "monthly" | "cycle_based";
  enabled: boolean;
  nextDue?: string;
  time?: string;
}

interface SmartSuggestion {
  type: "period" | "symptom" | "health";
  message: string;
  actionable: boolean;
}

export default function Reminders() {
  const [reminders, setReminders] = useState<Reminder[]>([]);
  const [suggestions, setSuggestions] = useState<SmartSuggestion[]>([]);
  const [showAddForm, setShowAddForm] = useState(false);
  const [newReminder, setNewReminder] = useState<Partial<Reminder>>({
    type: "custom",
    title: "",
    frequency: "daily",
    enabled: true,
    time: "09:00"
  });

  // LocalStorage helper functions
  const saveToLocalStorage = (remindersData: Reminder[]) => {
    try {
      localStorage.setItem(LOCAL_STORAGE_KEYS.REMINDERS, JSON.stringify(remindersData));
      localStorage.setItem(LOCAL_STORAGE_KEYS.LAST_SYNC, new Date().toISOString());
    } catch (error) {
      console.warn('Failed to save reminders to localStorage:', error);
    }
  };

  const loadFromLocalStorage = (): Reminder[] | null => {
    try {
      const stored = localStorage.getItem(LOCAL_STORAGE_KEYS.REMINDERS);
      if (stored) {
        return JSON.parse(stored);
      }
      return null;
    } catch (error) {
      console.warn('Failed to load reminders from localStorage:', error);
      return null;
    }
  };

  const syncWithAPI = async (localReminders: Reminder[]) => {
    try {
      const apiData = localReminders.map(r => ({
        id: r.id,
        kind: r.type === 'period' ? 'period_prediction' : 
              r.type === 'symptom' ? 'health_alert' : 'custom',
        title: r.title,
        active: r.enabled,
        next_due: r.nextDue
      }));
      await remindersApi.put(apiData);
    } catch (error) {
      console.warn('Failed to sync reminders with API:', error);
    }
  };

  const loadReminders = async () => {
    // First, try to load from localStorage
    const localReminders = loadFromLocalStorage();
    
    if (localReminders && localReminders.length > 0) {
      setReminders(localReminders);
      // Sync with API in background
      syncWithAPI(localReminders);
    } else {
      // Fallback to API if no local data
      try {
        const r = await remindersApi.get();
        const data = r.data as any[];
        const apiReminders = data.map(item =>({
          id: item.id,
          type: item.kind === 'period_prediction' ? 'period' : 
                item.kind === 'health_alert' ? 'symptom' : 'custom' as Reminder['type'],
          title: item.title,
          frequency: 'daily' as const,
          enabled: item.active,
          nextDue: item.nextDue
        }));
        setReminders(apiReminders);
        saveToLocalStorage(apiReminders);
      } catch (error) {
        console.warn('Failed to load reminders from API:', error);
        // Keep empty state if both localStorage and API fail
        setReminders([]);
      }
    }
  };

  useEffect(() => {
    loadReminders();
    
    // Load smart suggestions
    Promise.all([predictApi.cycles(), insightsApi.smart()])
      .then(([p, s]) => {
        const sug: SmartSuggestion[] = [];
        const smart = s.data as any;
        
        if (smart.next_period_estimate) {
          sug.push({
            type: "period",
            message: `Period expected around ${smart.next_period_estimate}`,
            actionable: true
          });
        }
        
        const pred = p.data as any;
        (pred?.next_cycles || []).slice(0, 2).forEach(
          (c: { cycle_index: number; predicted_length_days: number }) => {
            sug.push({
              type: "health",
              message: `Cycle ${c.cycle_index}: ~${c.predicted_length_days} days`,
              actionable: false
            });
          }
        );
        
        const alerts = (smart as any)?.alerts;
        (alerts || []).slice(0, 2).forEach((a: { text: string }) => {
          sug.push({
            type: "symptom",
            message: a.text,
            actionable: true
          });
        });
        
        setSuggestions(sug);
      })
      .catch(() => setSuggestions([]));
  }, []);

  // Save reminders to localStorage whenever they change
  useEffect(() => {
    if (reminders.length > 0) {
      saveToLocalStorage(reminders);
    }
  }, [reminders]);

  const addReminder = async () => {
    if (!newReminder.title?.trim()) return;
    
    const reminder: Reminder = {
      id: `reminder-${Date.now()}`,
      type: newReminder.type || 'custom',
      title: newReminder.title.trim(),
      frequency: newReminder.frequency || 'daily',
      enabled: true,
      time: newReminder.time || '09:00'
    };
    
    const updatedReminders = [...reminders, reminder];
    setReminders(updatedReminders);
    
    // Save to localStorage immediately
    saveToLocalStorage(updatedReminders);
    
    // Sync with API in background
    try {
      const apiData = updatedReminders.map(r => ({
        id: r.id,
        kind: r.type === 'period' ? 'period_prediction' : 
              r.type === 'symptom' ? 'health_alert' : 'custom',
        title: r.title,
        active: r.enabled,
        next_due: r.nextDue
      }));
      await remindersApi.put(apiData);
    } catch (error) {
      console.warn('Failed to sync new reminder with API:', error);
    }
    
    setShowAddForm(false);
    setNewReminder({
      type: "custom",
      title: "",
      frequency: "daily",
      enabled: true,
      time: "09:00"
    });
  };

  const toggleReminder = async (id: string) => {
    const updatedReminders = reminders.map(r => 
      r.id === id ? { ...r, enabled: !r.enabled } : r
    );
    setReminders(updatedReminders);
    
    // Save to localStorage immediately
    saveToLocalStorage(updatedReminders);
    
    // Sync with API in background
    try {
      const apiData = updatedReminders.map(r => ({
        id: r.id,
        kind: r.type === 'period' ? 'period_prediction' : 
              r.type === 'symptom' ? 'health_alert' : 'custom',
        title: r.title,
        active: r.enabled,
        next_due: r.nextDue
      }));
      await remindersApi.put(apiData);
    } catch (error) {
      console.warn('Failed to sync reminder toggle with API:', error);
    }
  };

  const deleteReminder = async (id: string) => {
    const updatedReminders = reminders.filter(r => r.id !== id);
    setReminders(updatedReminders);
    
    // Save to localStorage immediately
    saveToLocalStorage(updatedReminders);
    
    // Sync with API in background
    try {
      const apiData = updatedReminders.map(r => ({
        id: r.id,
        kind: r.type === 'period' ? 'period_prediction' : 
              r.type === 'symptom' ? 'health_alert' : 'custom',
        title: r.title,
        active: r.enabled,
        next_due: r.nextDue
      }));
      await remindersApi.put(apiData);
    } catch (error) {
      console.warn('Failed to sync reminder deletion with API:', error);
    }
  };

  const createReminderFromSuggestion = (suggestion: SmartSuggestion) => {
    setNewReminder({
      type: suggestion.type === 'period' ? 'period' : 
            suggestion.type === 'symptom' ? 'symptom' : 'custom',
      title: suggestion.message,
      frequency: 'cycle_based',
      enabled: true,
      time: '09:00'
    });
    setShowAddForm(true);
  };

  const getReminderIcon = (type: Reminder['type']) => {
    switch (type) {
      case 'period': return '🩸';
      case 'symptom': return '⚠️';
      case 'medicine': return '💊';
      case 'appointment': return '📅';
      default: return '📝';
    }
  };

  const getSuggestionIcon = (type: SmartSuggestion['type']) => {
    switch (type) {
      case 'period': return '🩸';
      case 'symptom': return '⚠️';
      case 'health': return '💡';
    }
  };

  return (
    <div className="max-w-4xl space-y-6">
      {/* Header */}
      <div className="text-center space-y-2">
        <h2 className="font-display text-3xl text-rose-50">Health Reminders</h2>
        <p className="text-rose-200/70">Stay on track with personalized menstrual health reminders</p>
      </div>

      {/* Smart Suggestions */}
      {suggestions.length > 0 && (
        <GlassCard className="border-amber-500/20 bg-amber-950/15">
          <div className="flex items-center gap-2 mb-4">
            <span className="text-2xl">💡</span>
            <h3 className="font-display text-lg text-amber-200/95">Smart Suggestions</h3>
          </div>
          <div className="space-y-3">
            {suggestions.map((suggestion, index) => (
              <div key={index} className="flex items-center justify-between p-3 rounded-lg bg-amber-900/20 border border-amber-700/30">
                <div className="flex items-center gap-3">
                  <span className="text-xl">{getSuggestionIcon(suggestion.type)}</span>
                  <span className="text-amber-100 text-sm">{suggestion.message}</span>
                </div>
                {suggestion.actionable && (
                  <button
                    onClick={() => createReminderFromSuggestion(suggestion)}
                    className="px-3 py-1 text-xs bg-amber-600 hover:bg-amber-500 text-white rounded-full transition-colors"
                  >
                    Create Reminder
                  </button>
                )}
              </div>
            ))}
          </div>
        </GlassCard>
      )}

      {/* Quick Add Buttons */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        {[
          { type: 'period' as const, title: 'Period Start', icon: '🩸' },
          { type: 'symptom' as const, title: 'Symptom Check', icon: '⚠️' },
          { type: 'medicine' as const, title: 'Medicine', icon: '💊' },
          { type: 'appointment' as const, title: 'Doctor Visit', icon: '📅' }
        ].map((quick) => (
          <button
            key={quick.type}
            onClick={() => {
              setNewReminder({
                type: quick.type,
                title: quick.title,
                frequency: quick.type === 'period' ? 'cycle_based' : 'daily',
                enabled: true,
                time: '09:00'
              });
              setShowAddForm(true);
            }}
            className="p-4 rounded-xl bg-gradient-to-br from-rose-600/20 to-violet-600/20 border border-rose-500/30 hover:border-rose-400/50 transition-all hover:scale-105"
          >
            <div className="text-2xl mb-1">{quick.icon}</div>
            <div className="text-xs text-rose-100">{quick.title}</div>
          </button>
        ))}
      </div>

      {/* Add Reminder Form */}
      {showAddForm && (
        <GlassCard glow>
          <h3 className="font-display text-lg text-rose-200/95 mb-4">Add New Reminder</h3>
          <div className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm text-rose-200/70 mb-2">Reminder Type</label>
                <select
                  className="w-full rounded-xl border border-white/10 bg-black/35 px-4 py-2.5 text-sm text-zinc-200"
                  value={newReminder.type}
                  onChange={(e) => setNewReminder({ ...newReminder, type: e.target.value as Reminder['type'] })}
                >
                  <option value="period">Period Related</option>
                  <option value="symptom">Symptom Tracking</option>
                  <option value="medicine">Medicine</option>
                  <option value="appointment">Appointment</option>
                  <option value="custom">Custom</option>
                </select>
              </div>
              <div>
                <label className="block text-sm text-rose-200/70 mb-2">Frequency</label>
                <select
                  className="w-full rounded-xl border border-white/10 bg-black/35 px-4 py-2.5 text-sm text-zinc-200"
                  value={newReminder.frequency}
                  onChange={(e) => setNewReminder({ ...newReminder, frequency: e.target.value as Reminder['frequency'] })}
                >
                  <option value="daily">Daily</option>
                  <option value="weekly">Weekly</option>
                  <option value="monthly">Monthly</option>
                  <option value="cycle_based">Cycle Based</option>
                </select>
              </div>
            </div>
            <div>
              <label className="block text-sm text-rose-200/70 mb-2">Title</label>
              <input
                className="w-full rounded-xl border border-white/10 bg-black/35 px-4 py-2.5 text-sm text-zinc-100"
                value={newReminder.title}
                onChange={(e) => setNewReminder({ ...newReminder, title: e.target.value })}
                placeholder="e.g., Take iron supplements"
              />
            </div>
            <div>
              <label className="block text-sm text-rose-200/70 mb-2">Time</label>
              <input
                type="time"
                className="w-full rounded-xl border border-white/10 bg-black/35 px-4 py-2.5 text-sm text-zinc-100"
                value={newReminder.time}
                onChange={(e) => setNewReminder({ ...newReminder, time: e.target.value })}
              />
            </div>
            <div className="flex gap-3">
              <button
                onClick={addReminder}
                className="rounded-2xl bg-gradient-to-r from-rose-500 to-violet-600 px-6 py-2.5 text-sm font-semibold text-white shadow-lg shadow-rose-900/30"
              >
                Add Reminder
              </button>
              <button
                onClick={() => {
                  setShowAddForm(false);
                  setNewReminder({
                    type: "custom",
                    title: "",
                    frequency: "daily",
                    enabled: true,
                    time: "09:00"
                  });
                }}
                className="rounded-2xl border border-white/20 px-6 py-2.5 text-sm font-semibold text-rose-200/70 hover:text-rose-100"
              >
                Cancel
              </button>
            </div>
          </div>
        </GlassCard>
      )}

      {/* Active Reminders */}
      <GlassCard>
        <div className="flex items-center justify-between mb-4">
          <h3 className="font-display text-lg text-rose-200/95">Your Reminders</h3>
          <span className="text-sm text-rose-300/60">{reminders.filter(r => r.enabled).length} active</span>
        </div>
        {reminders.length === 0 ? (
          <div className="text-center py-8">
            <div className="text-4xl mb-3">🔔</div>
            <p className="text-rose-200/60">No reminders set yet</p>
            <p className="text-rose-200/40 text-sm mt-1">Create your first reminder to stay on track</p>
          </div>
        ) : (
          <div className="space-y-3">
            {reminders.map((reminder) => (
              <div
                key={reminder.id}
                className={`flex items-center justify-between p-4 rounded-xl border transition-all ${
                  reminder.enabled 
                    ? 'bg-rose-950/20 border-rose-500/30' 
                    : 'bg-black/20 border-white/10 opacity-60'
                }`}
              >
                <div className="flex items-center gap-3">
                  <span className="text-2xl">{getReminderIcon(reminder.type)}</span>
                  <div>
                    <div className="text-rose-100 font-medium">{reminder.title}</div>
                    <div className="text-rose-300/60 text-sm">
                      {reminder.frequency === 'cycle_based' ? 'Based on cycle' : 
                       reminder.frequency === 'daily' ? 'Daily' :
                       reminder.frequency === 'weekly' ? 'Weekly' : 'Monthly'}
                      {reminder.time && ` at ${reminder.time}`}
                    </div>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => toggleReminder(reminder.id!)}
                    className={`px-3 py-1 text-xs rounded-full transition-colors ${
                      reminder.enabled
                        ? 'bg-green-600/20 text-green-400 hover:bg-green-600/30'
                        : 'bg-gray-600/20 text-gray-400 hover:bg-gray-600/30'
                    }`}
                  >
                    {reminder.enabled ? 'Active' : 'Paused'}
                  </button>
                  <button
                    onClick={() => deleteReminder(reminder.id!)}
                    className="text-xs font-medium text-rose-400/90 hover:text-rose-300"
                  >
                    Delete
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </GlassCard>

      {/* Tips Section */}
      <GlassCard className="border-rose-500/10 bg-rose-950/10">
        <h3 className="font-display text-lg text-rose-200/95 mb-3">💡 Tips for Effective Reminders</h3>
        <div className="space-y-2 text-sm text-rose-200/70">
          <div>• Set period reminders 2-3 days before your expected date</div>
          <div>• Track symptoms regularly to identify patterns</div>
          <div>• Set medicine reminders at consistent times</div>
          <div>• Use cycle-based reminders for predictable events</div>
        </div>
      </GlassCard>
    </div>
  );
}
