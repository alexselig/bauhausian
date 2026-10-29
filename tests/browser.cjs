const assert = require("node:assert/strict");
const path = require("node:path");
const { pathToFileURL } = require("node:url");
const fs = require("node:fs/promises");
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || "playwright");

async function main() {
  const root = path.resolve(__dirname, "..");
  const output = path.join(root, "test-results");
  await fs.mkdir(output, { recursive: true });
  const browser = await chromium.launch({ headless: true });
  try {
    const page = await browser.newPage();
    const errors = [];
    const remote = [];
    page.on("pageerror", error => errors.push(error.message));
    page.on("request", request => {
      if (/^https?:/.test(request.url())) remote.push(request.url());
    });
    await page.goto(pathToFileURL(path.join(root, "index.html")).href);
    await page.keyboard.press("Tab");
    assert.equal(await page.locator(":focus").textContent(), "Skip to content");
    await page.keyboard.press("Enter");
    assert.equal(await page.locator(":focus").getAttribute("id"), "main");
    for (const width of [390, 768, 1024, 1440, 1920]) {
      await page.setViewportSize({ width, height: 1000 });
      assert.equal(await page.evaluate(() =>
        document.documentElement.scrollWidth <= innerWidth), true, `Overflow at ${width}`);
      const sheet = await page.locator(".sheet").boundingBox();
      assert.ok(sheet.width <= 1680, "Capped sheet");
      for (const button of await page.locator("button:visible").all()) {
        assert.ok((await button.boundingBox()).height >= 44, `Touch target at ${width}`);
      }
      await page.screenshot({ path: path.join(output, `showcase-${width}.png`), fullPage: true });
    }
    await page.locator("#search").fill("material");
    assert.equal(await page.locator("tbody tr:visible").count(), 1);
    assert.equal(await page.locator("#result-count").textContent(), "1 item");
    await page.locator("#review-filter").click();
    assert.equal(await page.locator("#no-results").isVisible(), true);
    await page.locator("#empty-reset").click();
    assert.equal(await page.locator("tbody tr:visible").count(), 4);
    assert.equal(await page.locator(":focus").getAttribute("id"), "search");
    await page.locator("#review-filter").click();
    assert.equal(await page.locator("tbody tr:visible").count(), 2);
    await page.locator("#reset").click();
    await page.locator("[data-review]").first().click();
    assert.equal(await page.locator("#review-dialog").isVisible(), true);
    assert.equal(await page.locator("#dialog-title").textContent(), "Workshop inventory");
    assert.equal(await page.locator(":focus").getAttribute("id"), "dialog-close");
    await page.keyboard.press("Escape");
    assert.equal(await page.locator("#review-dialog").isVisible(), false);
    assert.equal(await page.locator(":focus").getAttribute("data-review"), "Workshop inventory");
    await page.locator("#sample-open").click();
    await page.locator("#dialog-close").click();
    assert.equal(await page.locator(":focus").getAttribute("id"), "sample-open");
    await page.locator("#sample-open").click();
    await page.getByRole("button", { name: "Return to workbench" }).click();
    assert.equal(await page.locator("#review-dialog").isVisible(), false);
    await page.setViewportSize({ width: 390, height: 380 });
    await page.locator("#sample-open").click();
    const modal = await page.locator("#review-dialog").boundingBox();
    assert.ok(modal.height <= 348, "Dialog respects short viewport");
    await page.keyboard.press("Escape");
    await page.locator('nav a[href="#foundations"]').click();
    await page.waitForFunction(() =>
      document.querySelector("nav a[aria-current]")?.getAttribute("href") === "#foundations");
    assert.equal(await page.locator('nav a[aria-current]').getAttribute("href"), "#foundations");
    await page.emulateMedia({ reducedMotion: "reduce" });
    assert.equal(await page.locator("html").evaluate(el => getComputedStyle(el).scrollBehavior), "auto");
    assert.equal(await page.locator("#sample-open").evaluate(el => getComputedStyle(el).transitionDuration), "0s");
    assert.deepEqual(errors, []);
    assert.deepEqual(remote, []);
    console.log("PASS: widths, sheet cap, touch targets, keyboard, filters, dialog, reduced motion and offline assets.");
  } finally {
    await browser.close();
  }
}

main().catch(error => {
  console.error(error);
  process.exitCode = 1;
});
