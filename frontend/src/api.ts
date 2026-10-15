export interface Habit {
  id: number;
  name: string;
}

export async function listHabits(): Promise<Habit[]> {
  const res = await fetch("/api/habits");
  if (!res.ok) throw new Error(`GET /api/habits failed: ${res.status}`);
  return res.json();
}

export async function createHabit(name: string): Promise<Habit> {
  const res = await fetch("/api/habits", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name }),
  });
  if (!res.ok) throw new Error(`POST /api/habits failed: ${res.status}`);
  return res.json();
}
