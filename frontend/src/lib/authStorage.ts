const KEY = "elite-her-session";

export type Session = {
  access_token: string;
  email: string;
  user_id: string;
};

export function loadSession(): Session | null {
  try {
    const raw = localStorage.getItem(KEY);
    if (!raw) return null;
    const j = JSON.parse(raw) as Session;
    if (j?.access_token && j?.user_id) return j;
    return null;
  } catch {
    return null;
  }
}

export function saveSession(s: Session): void {
  localStorage.setItem(KEY, JSON.stringify(s));
}

export function clearSession(): void {
  localStorage.removeItem(KEY);
}

export function getAccessToken(): string | null {
  return loadSession()?.access_token ?? null;
}
