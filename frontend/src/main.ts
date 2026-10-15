import { createHabit, listHabits } from "./api";

const list = document.querySelector<HTMLUListElement>("#habits")!;
const form = document.querySelector<HTMLFormElement>("#habit-form")!;
const input = document.querySelector<HTMLInputElement>("#habit-name")!;

async function render() {
  const habits = await listHabits();
  list.replaceChildren(
    ...habits.map((h) => {
      const li = document.createElement("li");
      li.textContent = h.name;
      return li;
    }),
  );
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  await createHabit(input.value);
  input.value = "";
  await render();
});

render();
