const search = document.querySelector("#search");
const filter = document.querySelector("#review-filter");
const rows = [...document.querySelectorAll("tbody tr")];
const count = document.querySelector("#result-count");
const empty = document.querySelector("#no-results");
const dialog = document.querySelector("#review-dialog");

function updateResults() {
  const query = search.value.trim().toLocaleLowerCase();
  const reviewOnly = filter.getAttribute("aria-pressed") === "true";
  let visible = 0;
  for (const row of rows) {
    const text = `${row.cells[0].textContent} ${row.cells[1].textContent}`.toLocaleLowerCase();
    row.hidden = !text.includes(query) || (reviewOnly && row.dataset.state !== "review");
    if (!row.hidden) visible += 1;
  }
  count.textContent = `${visible} ${visible === 1 ? "item" : "items"}`;
  empty.hidden = visible !== 0;
}

function resetFilters() {
  search.value = "";
  filter.setAttribute("aria-pressed", "false");
  updateResults();
  search.focus();
}

search.addEventListener("input", updateResults);
filter.addEventListener("click", () => {
  filter.setAttribute("aria-pressed", String(filter.getAttribute("aria-pressed") !== "true"));
  updateResults();
});
document.querySelector("#reset").addEventListener("click", resetFilters);
document.querySelector("#empty-reset").addEventListener("click", resetFilters);

function openReview(title) {
  document.querySelector("#dialog-title").textContent = title;
  document.querySelector("#dialog-description").textContent =
    `${title} is a fictional example of a bounded review task.`;
  dialog.showModal();
}

for (const button of document.querySelectorAll("[data-review]")) {
  button.addEventListener("click", () => openReview(button.dataset.review));
}
document.querySelector("#sample-open").addEventListener("click", () => openReview("Review example"));
document.querySelector("#dialog-close").addEventListener("click", () => dialog.close());

const links = [...document.querySelectorAll(".masthead nav a")];
function updateNavigation() {
  const current = links.find(link => link.hash === location.hash) || links[0];
  for (const link of links) {
    if (link === current) link.setAttribute("aria-current", "location");
    else link.removeAttribute("aria-current");
  }
}
window.addEventListener("hashchange", updateNavigation);
updateNavigation();
