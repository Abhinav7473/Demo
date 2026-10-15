export type Source = "nielsen" | "wickens";

export interface Principle {
  id: number;
  code: string;
  source: Source;
  category: string;
  title: string;
  summary: string;
  example: string;
}

export async function listPrinciples(): Promise<Principle[]> {
  const res = await fetch("/api/principles");
  if (!res.ok) throw new Error(`GET /api/principles failed: ${res.status}`);
  return res.json();
}
