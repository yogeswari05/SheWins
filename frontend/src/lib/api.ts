import axios from "axios";
import { getAccessToken, clearSession } from "./authStorage";

const base = import.meta.env.DEV ? "" : (import.meta.env.VITE_API_URL as string) || "";

export const api = axios.create({
  baseURL: base,
  headers: { "Content-Type": "application/json" },
});

api.interceptors.request.use((config) => {
  const t = getAccessToken();
  if (t) {
    config.headers.Authorization = `Bearer ${t}`;
  }
  return config;
});

api.interceptors.response.use(
  (r) => r,
  (err) => {
    const url = String(err?.config?.url || "");
    if (err?.response?.status === 401 && !url.includes("/api/auth/")) {
      clearSession();
      if (typeof window !== "undefined" && !window.location.pathname.startsWith("/login")) {
        window.location.assign("/login");
      }
    }
    return Promise.reject(err);
  }
);

export type CycleIn = {
  start_date: string;
  end_date?: string;
  flow: string;
  symptoms: string[];
  mood: string;
  sleep_hours?: number;
  stress?: number;
  exercise?: string;
  notes?: string;
};

export const cyclesApi = {
  list: () => api.get("/api/cycles"),
  create: (b: CycleIn) => api.post("/api/cycles", b),
  update: (id: string, b: CycleIn) => api.patch(`/api/cycles/${id}`, b),
  del: (id: string) => api.delete(`/api/cycles/${id}`),
  pcod: () => api.get("/api/cycles/assessment/pcod"),
};

export const predictApi = {
  cycles: () => api.get("/api/predict/cycles"),
};

export const analyticsApi = {
  dashboard: () => api.get("/api/analytics/dashboard"),
};

export const insightsApi = {
  smart: () => api.get("/api/insights/smart"),
};

export const chatApi = {
  message: (message: string, language: string) =>
    api.post("/api/chat/message", { message, language }),
};

export const remindersApi = {
  get: () => api.get("/api/reminders"),
  put: (items: unknown[]) => api.put("/api/reminders", items),
};

export const userApi = {
  me: () => api.get("/api/user/me"),
  init: (locale: string) => api.post(`/api/user/init?locale=${encodeURIComponent(locale)}`),
  settings: (body: { locale?: string; opt_in_analytics?: boolean; reminder_preferences?: object }) =>
    api.patch("/api/user/settings", body),
};

export const wellnessApi = {
  score: () => api.get("/api/wellness/score"),
  trend: () => api.get("/api/wellness/trend"),
  insights: () => api.get("/api/wellness/insights"),
  stressAnalysis: () => api.get("/api/wellness/stress-analysis"),
  moodAnalysis: () => api.get("/api/wellness/mood-analysis"),
  sleepAnalysis: () => api.get("/api/wellness/sleep-analysis"),
  symptomAnalysis: () => api.get("/api/wellness/symptom-analysis"),
  comprehensive: () => api.get("/api/wellness/comprehensive"),
};
