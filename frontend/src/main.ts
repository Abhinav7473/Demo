import { listPrinciples, type Principle, type Source } from "./api";
import "./style.css";

const SOURCES: { id: Source | "all"; label: string }[] = [
  { id: "all", label: "All" },
  { id: "nielsen", label: "Nielsen · 10 heuristics" },
  { id: "wickens", label: "Wickens · 13 principles" },
];

const $ = <T extends HTMLElement>(sel: string) => document.querySelector<T>(sel)!;
const grid = $<HTMLDivElement>("#grid");
const count = $<HTMLParagraphElement>("#count");
const sourcesEl = $<HTMLDivElement>("#sources");
const categoriesEl = $<HTMLDivElement>("#categories");
const search = $<HTMLInputElement>("#search");
const dialog = $<HTMLDialogElement>("#detail");

const state = { source: "all" as Source | "all", category: "", query: "" };
let all: Principle[] = [];

const chip = (active: boolean) =>
  [
    "rounded-full border px-3 py-1 text-sm text-left transition-colors cursor-pointer",
    active
      ? "border-beige-500 bg-beige-200 text-beige-900 dark:border-beige-500 dark:bg-beige-800 dark:text-beige-50"
      : "border-beige-200 bg-white text-stone-600 hover:border-beige-400 hover:bg-beige-100 dark:border-stone-700 dark:bg-stone-900 dark:text-stone-300 dark:hover:bg-stone-800",
  ].join(" ");

function el<K extends keyof HTMLElementTagNameMap>(tag: K, className: string, text?: string) {
  const node = document.createElement(tag);
  node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

function filtered() {
  const q = state.query.toLowerCase();
  return all.filter(
    (p) =>
      (state.source === "all" || p.source === state.source) &&
      (!state.category || p.category === state.category) &&
      (!q || [p.title, p.summary, p.example, p.category].some((s) => s.toLowerCase().includes(q))),
  );
}

function renderFilters() {
  sourcesEl.replaceChildren(
    ...SOURCES.map((s) => {
      const b = el("button", chip(state.source === s.id), s.label);
      b.onclick = () => {
        state.source = s.id;
        state.category = "";
        render();
      };
      return b;
    }),
  );

  const categories = [...new Set(all.filter((p) => state.source === "all" || p.source === state.source).map((p) => p.category))];
  categoriesEl.replaceChildren(
    ...["", ...categories].map((c) => {
      const b = el("button", chip(state.category === c), c || "Any");
      b.onclick = () => {
        state.category = c;
        render();
      };
      return b;
    }),
  );
}

function card(p: Principle) {
  const b = el(
    "button",
    "group flex flex-col rounded-xl border border-beige-200 bg-white p-5 text-left shadow-sm transition hover:-translate-y-0.5 hover:border-beige-400 hover:shadow-md focus-visible:ring-2 focus-visible:ring-beige-400 focus-visible:outline-none dark:border-stone-800 dark:bg-stone-900 dark:hover:border-beige-700 cursor-pointer",
  );
  const top = el("div", "flex items-center justify-between gap-2");
  top.append(
    el("span", "rounded-md bg-beige-100 px-2 py-0.5 font-mono text-xs font-semibold text-beige-700 dark:bg-beige-900 dark:text-beige-200", p.code),
    el("span", "text-xs text-stone-500", p.category),
  );
  b.append(
    top,
    el("h2", "mt-3 font-serif text-lg font-semibold text-stone-900 group-hover:text-beige-800 dark:text-beige-50 dark:group-hover:text-beige-300", p.title),
    el("p", "mt-2 text-sm leading-relaxed text-stone-600 dark:text-stone-400", p.summary),
  );
  b.onclick = () => openDetail(p);
  return b;
}

function openDetail(p: Principle) {
  const body = el("div", "p-6");
  const head = el("div", "flex items-start justify-between gap-4");
  const close = el("button", "rounded-md px-2 text-2xl leading-none text-stone-400 hover:text-stone-700 cursor-pointer", "×");
  close.setAttribute("aria-label", "Close");
  close.onclick = () => dialog.close();
  head.append(
    el("p", "text-xs font-semibold uppercase tracking-[0.2em] text-beige-600 dark:text-beige-400", `${p.code} · ${p.source === "nielsen" ? "Nielsen" : "Wickens"} · ${p.category}`),
    close,
  );
  const example = el("div", "mt-5 rounded-xl border-l-4 border-beige-400 bg-beige-50 p-4 dark:bg-stone-800");
  example.append(
    el("p", "text-xs font-semibold uppercase tracking-wider text-beige-700 dark:text-beige-300", "Example"),
    el("p", "mt-1 text-sm text-stone-700 dark:text-stone-300", p.example),
  );
  body.append(
    head,
    el("h2", "mt-2 font-serif text-2xl font-semibold text-stone-900 dark:text-beige-50", p.title),
    el("p", "mt-3 leading-relaxed text-stone-600 dark:text-stone-400", p.summary),
    example,
  );
  dialog.replaceChildren(body);
  dialog.showModal();
}

function render() {
  renderFilters();
  const items = filtered();
  count.textContent = `${items.length} of ${all.length} principles`;
  grid.replaceChildren(
    ...(items.length
      ? items.map(card)
      : [el("p", "col-span-full rounded-xl border border-dashed border-beige-300 p-8 text-center text-stone-500", "Nothing matches. Try a different search or filter.")]),
  );
}

dialog.addEventListener("click", (e) => e.target === dialog && dialog.close());
search.addEventListener("input", () => {
  state.query = search.value.trim();
  render();
});

listPrinciples()
  .then((data) => {
    all = data;
    render();
  })
  .catch((err) => {
    count.textContent = `Could not load principles: ${err.message}`;
  });
