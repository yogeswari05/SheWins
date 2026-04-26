import React, { createContext, useCallback, useContext, useMemo, useState } from "react";
import axios from "axios";
import {
  clearSession,
  loadSession,
  saveSession,
  type Session,
} from "../lib/authStorage";

type AuthContextValue = {
  session: Session | null;
  login: (email: string, password: string) => Promise<void>;
  signup: (email: string, password: string, displayName: string) => Promise<void>;
  logout: () => void;
  setSession: (s: Session | null) => void;
};

const AuthContext = createContext<AuthContextValue | null>(null);

const base = import.meta.env.DEV ? "" : (import.meta.env.VITE_API_URL as string) || "";

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [session, setSessionState] = useState<Session | null>(() => loadSession());
  const setSession = useCallback((s: Session | null) => {
    if (s) saveSession(s);
    else clearSession();
    setSessionState(s);
  }, []);

  const login = useCallback(async (email: string, password: string) => {
    const r = await axios.post(`${base}/api/auth/login`, { email, password });
    const d = r.data as Session;
    const s: Session = {
      access_token: d.access_token,
      email: d.email,
      user_id: d.user_id,
    };
    setSession(s);
  }, [setSession]);

  const signup = useCallback(
    async (email: string, password: string, displayName: string) => {
      const r = await axios.post(`${base}/api/auth/signup`, {
        email,
        password,
        display_name: displayName,
      });
      const d = r.data as Session;
      setSession({
        access_token: d.access_token,
        email: d.email,
        user_id: d.user_id,
      });
    },
    [setSession]
  );

  const logout = useCallback(() => {
    setSession(null);
  }, [setSession]);

  const value = useMemo(
    () => ({
      session,
      login,
      signup,
      logout,
      setSession,
    }),
    [session, login, signup, logout, setSession]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const v = useContext(AuthContext);
  if (!v) throw new Error("useAuth outside AuthProvider");
  return v;
}
