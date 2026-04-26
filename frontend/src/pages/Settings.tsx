import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { GlassCard } from "../components/GlassCard";
import { userApi } from "../lib/api";
import { useTheme } from "../context/ThemeContext";
import { useAuth } from "../context/AuthContext";

const langs = [
  { code: "en", name: "English", flag: "🇬🇧" },
  { code: "hi", name: "Hindi (हिन्दी)", flag: "🇮🇳" },
  { code: "te", name: "Telugu (తెలుగు)", flag: "🇮🇳" },
];

interface UserProfile {
  email: string;
  name?: string;
  createdAt?: string;
}

interface NotificationSettings {
  periodReminders: boolean;
  symptomCheck: boolean;
  weeklyInsights: boolean;
  healthTips: boolean;
}

interface PrivacySettings {
  dataSharing: boolean;
  analytics: boolean;
  crashReporting: boolean;
}

interface AppSettings {
  darkMode: boolean;
  notifications: NotificationSettings;
  privacy: PrivacySettings;
}

export default function Settings() {
  const { i18n } = useTranslation();
  const { theme, toggleTheme } = useTheme();
  const { session, logout } = useAuth();
  const [userProfile, setUserProfile] = useState<UserProfile | null>(null);
  const [appSettings, setAppSettings] = useState<AppSettings>({
    darkMode: theme === 'dark',
    notifications: {
      periodReminders: true,
      symptomCheck: true,
      weeklyInsights: false,
      healthTips: true,
    },
    privacy: {
      dataSharing: false,
      analytics: false,
      crashReporting: true,
    },
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadSettings = async () => {
      try {
        // Load user profile
        const userResponse = await userApi.me();
        const userData = userResponse.data as any;
        setUserProfile({
          email: session?.email || '',
          name: session?.email?.split('@')[0], // Extract name from email
        });

        // Load analytics preference
        const analyticsOptIn = userData?.opt_in_analytics;
        if (analyticsOptIn != null) {
          setAppSettings(prev => ({
            ...prev,
            privacy: {
              ...prev.privacy,
              analytics: !!analyticsOptIn,
            },
          }));
        }
      } catch (error) {
        console.error('Failed to load settings:', error);
      } finally {
        setLoading(false);
      }
    };

    loadSettings();
  }, []);

  const updateNotificationSetting = async (key: keyof NotificationSettings, value: boolean) => {
    setAppSettings(prev => ({
      ...prev,
      notifications: {
        ...prev.notifications,
        [key]: value,
      },
    }));
    // TODO: Save to backend
  };

  const updatePrivacySetting = async (key: keyof PrivacySettings, value: boolean) => {
    setAppSettings(prev => ({
      ...prev,
      privacy: {
        ...prev.privacy,
        [key]: value,
      },
    }));
    
    if (key === 'analytics') {
      await userApi.settings({ opt_in_analytics: value });
    }
  };

  const handleSignOut = async () => {
    logout();
  };

  const exportData = async () => {
    try {
      // TODO: Implement data export functionality
      alert('Data export feature coming soon!');
    } catch (error) {
      console.error('Failed to export data:', error);
    }
  };

  const deleteAccount = async () => {
    const confirmed = window.confirm(
      'Are you sure you want to delete your account? This action cannot be undone and all your data will be permanently removed.'
    );
    if (confirmed) {
      try {
        // TODO: Implement account deletion
        alert('Account deletion feature coming soon!');
      } catch (error) {
        console.error('Failed to delete account:', error);
      }
    }
  };

  if (loading) {
    return (
      <div className="max-w-4xl space-y-6">
        <div className="animate-pulse">
          <div className="h-8 bg-rose-200/20 rounded w-48 mb-6"></div>
          <div className="space-y-4">
            <div className="h-32 bg-rose-200/10 rounded-xl"></div>
            <div className="h-32 bg-rose-200/10 rounded-xl"></div>
            <div className="h-32 bg-rose-200/10 rounded-xl"></div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl space-y-6">
      {/* Header */}
      <div className="text-center space-y-2">
        <h2 className="font-display text-3xl text-rose-50">Settings</h2>
        <p className="text-rose-200/70">Manage your account and app preferences</p>
      </div>

      {/* Profile Section */}
      <GlassCard>
        <div className="flex items-center justify-between mb-4">
          <h3 className="font-display text-lg text-rose-200/95">👤 Profile</h3>
        </div>
        <div className="space-y-4">
          <div className="flex items-center justify-between p-4 rounded-lg bg-rose-950/20 border border-rose-500/30">
            <div>
              <div className="text-rose-100 font-medium">
                {userProfile?.name || 'User'}
              </div>
              <div className="text-rose-300/60 text-sm">{userProfile?.email}</div>
              <div className="text-rose-300/40 text-xs mt-1">
                SheWins Member
              </div>
            </div>
            <button
              onClick={handleSignOut}
              className="px-4 py-2 text-sm bg-red-600 hover:bg-red-500 text-white rounded-lg transition-colors"
            >
              Sign Out
            </button>
          </div>
        </div>
      </GlassCard>

      {/* Appearance Settings */}
      <GlassCard>
        <h3 className="font-display text-lg text-rose-200/95 mb-4">🎨 Appearance</h3>
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <div className="text-rose-100 font-medium">Dark Mode</div>
              <div className="text-rose-300/60 text-sm">Reduce eye strain in low light</div>
            </div>
            <button
              onClick={toggleTheme}
              className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                theme === 'dark' ? 'bg-rose-600' : 'bg-gray-600'
              }`}
            >
              <span
                className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                  theme === 'dark' ? 'translate-x-6' : 'translate-x-1'
                }`}
              />
            </button>
          </div>
        </div>
      </GlassCard>

      {/* Language Settings */}
      <GlassCard>
        <h3 className="font-display text-lg text-rose-200/95 mb-4">🌐 Language</h3>
        <div className="space-y-3">
          {langs.map((l) => (
            <label
              key={l.code}
              className="flex cursor-pointer items-center gap-4 rounded-xl border border-white/5 bg-black/20 px-4 py-3 text-sm text-zinc-200 transition hover:border-rose-400/25"
            >
              <input
                type="radio"
                name="lang"
                checked={i18n.language.startsWith(l.code)}
                onChange={async () => {
                  await i18n.changeLanguage(l.code);
                  await userApi.settings({ locale: l.code });
                }}
                className="w-4 h-4 text-rose-600"
              />
              <span className="text-2xl">{l.flag}</span>
              <span className="flex-1">{l.name}</span>
              {i18n.language.startsWith(l.code) && (
                <span className="text-xs text-rose-400">Active</span>
              )}
            </label>
          ))}
        </div>
      </GlassCard>

      {/* Notification Settings */}
      <GlassCard>
        <h3 className="font-display text-lg text-rose-200/95 mb-4">🔔 Notifications</h3>
        <div className="space-y-4">
          {[
            { key: 'periodReminders' as const, label: 'Period Reminders', desc: 'Get notified before your expected period' },
            { key: 'symptomCheck' as const, label: 'Symptom Check', desc: 'Daily reminder to track symptoms' },
            { key: 'weeklyInsights' as const, label: 'Weekly Insights', desc: 'Receive weekly health patterns summary' },
            { key: 'healthTips' as const, label: 'Health Tips', desc: 'Get personalized wellness tips' },
          ].map((setting) => (
            <div key={setting.key} className="flex items-center justify-between">
              <div>
                <div className="text-rose-100 font-medium">{setting.label}</div>
                <div className="text-rose-300/60 text-sm">{setting.desc}</div>
              </div>
              <button
                onClick={() => updateNotificationSetting(setting.key, !appSettings.notifications[setting.key])}
                className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                  appSettings.notifications[setting.key] ? 'bg-rose-600' : 'bg-gray-600'
                }`}
              >
                <span
                  className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                    appSettings.notifications[setting.key] ? 'translate-x-6' : 'translate-x-1'
                  }`}
                />
              </button>
            </div>
          ))}
        </div>
      </GlassCard>

      {/* Privacy Settings */}
      <GlassCard>
        <h3 className="font-display text-lg text-rose-200/95 mb-4">🔒 Privacy</h3>
        <div className="space-y-4">
          {[
            { key: 'dataSharing' as const, label: 'Data Sharing', desc: 'Share anonymized data to improve the app' },
            { key: 'analytics' as const, label: 'Analytics', desc: 'Help us understand how you use the app' },
            { key: 'crashReporting' as const, label: 'Crash Reporting', desc: 'Automatically report crashes to help us fix issues' },
          ].map((setting) => (
            <div key={setting.key} className="flex items-center justify-between">
              <div>
                <div className="text-rose-100 font-medium">{setting.label}</div>
                <div className="text-rose-300/60 text-sm">{setting.desc}</div>
              </div>
              <button
                onClick={() => updatePrivacySetting(setting.key, !appSettings.privacy[setting.key])}
                className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                  appSettings.privacy[setting.key] ? 'bg-rose-600' : 'bg-gray-600'
                }`}
              >
                <span
                  className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                    appSettings.privacy[setting.key] ? 'translate-x-6' : 'translate-x-1'
                  }`}
                />
              </button>
            </div>
          ))}
        </div>
        <p className="mt-4 text-xs leading-relaxed text-zinc-500">
          Your data is encrypted and stored securely. We never sell your personal health information.
        </p>
      </GlassCard>

      {/* Data Management */}
      <GlassCard>
        <h3 className="font-display text-lg text-rose-200/95 mb-4">📊 Data Management</h3>
        <div className="space-y-3">
          <button
            onClick={exportData}
            className="w-full p-4 rounded-xl border border-white/5 bg-black/20 text-left hover:border-rose-400/25 transition-colors"
          >
            <div className="text-rose-100 font-medium">📥 Export Your Data</div>
            <div className="text-rose-300/60 text-sm">Download all your health data in a printable format</div>
          </button>
          
          <button
            onClick={deleteAccount}
            className="w-full p-4 rounded-xl border border-red-500/30 bg-red-950/20 text-left hover:border-red-400/50 transition-colors"
          >
            <div className="text-red-400 font-medium">🗑️ Delete Account</div>
            <div className="text-red-300/60 text-sm">Permanently delete your account and all data</div>
          </button>
        </div>
      </GlassCard>

      {/* About Section */}
      <GlassCard>
        <h3 className="font-display text-lg text-rose-200/95 mb-4">ℹ️ About</h3>
        <div className="space-y-3 text-sm text-rose-200/70">
          <div className="flex justify-between">
            <span>Version</span>
            <span>1.0.0</span>
          </div>
          <div className="flex justify-between">
            <span>SheWins Health</span>
            <span>© 2024</span>
          </div>
          <div className="pt-3 text-xs text-center text-zinc-500">
            Empowering women's health through technology
          </div>
        </div>
      </GlassCard>
    </div>
  );
}
