import { getAccessToken } from "./authStorage";

export async function downloadDoctorReport(): Promise<void> {
  const base = import.meta.env.DEV ? "" : (import.meta.env.VITE_API_URL as string) || "";
  const t = getAccessToken();
  if (!t) throw new Error("Sign in to export your report.");
  const r = await fetch(`${base}/api/reports/doctor`, {
    headers: { Authorization: `Bearer ${t}` },
  });
  if (!r.ok) throw new Error("Report failed");
  const b = await r.blob();
  const u = URL.createObjectURL(b);
  const a = document.createElement("a");
  a.href = u;
  a.download = "elite-her-doctor-report.pdf";
  a.click();
  URL.revokeObjectURL(u);
}
