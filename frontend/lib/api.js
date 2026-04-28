const API_BASE = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";

export async function fetchHealth() {
  const res = await fetch(`${API_BASE}/health`, { cache: "no-store" });
  if (!res.ok) throw new Error("Health check failed");
  return res.json();
}

export async function fetchConfig() {
  const res = await fetch(`${API_BASE}/config`, { cache: "no-store" });
  if (!res.ok) throw new Error("Config fetch failed");
  return res.json();
}

export async function saveConfig(payload) {
  const res = await fetch(`${API_BASE}/config`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  if (!res.ok) throw new Error("Config update failed");
  return res.json();
}

export async function runScan() {
  const res = await fetch(`${API_BASE}/scan`, { method: "POST" });
  if (!res.ok) throw new Error("Scan failed");
  return res.json();
}
