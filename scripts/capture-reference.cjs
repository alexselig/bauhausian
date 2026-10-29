/* Capture the deployed public demo, not a reconstruction or authenticated data. */
const assert = require("node:assert/strict");
const crypto = require("node:crypto");
const fs = require("node:fs/promises");
const path = require("node:path");
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || "playwright");

const screens = [
  { id: "public-landing", title: "Public landing", route: "/", heading: "Ship a Skill" },
  { id: "demo-overview", title: "Demo introduction", route: "/demo", heading: "See Ship a Skill" },
  { id: "dashboard", title: "All Skills dashboard", route: "/demo/app?view=all", heading: "Skills" },
  { id: "dashboard-filter", title: "Dashboard filters", route: "/demo/app?view=all", heading: "Skills", action: "filter" },
  { id: "my-skills", title: "My Skills dashboard", route: "/demo/app?view=mine", heading: "Skills" },
  { id: "add-skill", title: "Add Skill", route: "/demo/app/skills/new?from=all", heading: "Add" },
  { id: "skill-details", title: "Skill Details", route: "/demo/app/skills/skill-5663f389?stage=skill-details", heading: "Skill details" },
  { id: "bridge-setup", title: "Copilot bridge setup", route: "/demo/app/skills/skill-3f20feab?stage=bridge-setup", heading: "bridge" },
  { id: "create-audit", title: "Create / audit results", route: "/demo/app/skills/skill-3f20feab?stage=create", heading: "Create" },
  { id: "create-upload", title: "Create / package upload", route: "/demo/app/skills/skill-3f20feab?stage=create", heading: "Create", action: "upload" },
  { id: "provide-evals", title: "Provide Evals", route: "/demo/app/skills/skill-3d213822?stage=provide-evals", heading: "Provide evals" },
  { id: "eval-results", title: "Eval Results Review", route: "/demo/app/skills/skill-765e9f44?stage=eval-results-review", heading: "Eval results" },
  { id: "create-pr", title: "Create PR", route: "/demo/app/skills/skill-6cc1214d?stage=create-pr", heading: "Create PR" },
  { id: "ship", title: "Ship", route: "/demo/app/skills/skill-f6b3baac?stage=create-pr-ship", heading: "Ship" },
  { id: "dogfood", title: "Dogfood", route: "/demo/app/skills/skill-3c3a4b52?stage=dogfood", heading: "Dogfood" },
  { id: "submit-review", title: "Submit for review", route: "/demo/app/skills/skill-c393a8c1?stage=submit", heading: "review" },
  { id: "final-review-queue", title: "Final review queue", route: "/demo/app/review", heading: "review" },
  { id: "final-review-decision", title: "Final review decision", route: "/demo/app/review/submission-e2e-0001", heading: "customer-story-slides" },
  { id: "settings-menu", title: "Settings menu", route: "/demo/app?view=all", heading: "Skills", action: "settings" },
  { id: "admin-reviewers", title: "Admin reviewers", route: "/demo/app/settings/reviewers", heading: "Review Settings" },
  { id: "admin-engineers", title: "Admin engineers", route: "/demo/app/settings/engineers", heading: "engineers" },
  { id: "process-configuration", title: "Process configuration", route: "/demo/app/settings/process", heading: "engineers" },
];
const viewports = [
  { width: 1440, height: 1000 },
  { width: 768, height: 1024 },
  { width: 390, height: 844 },
];

async function main() {
  assert.ok(process.env.REFERENCE_BASE_URL, "Set REFERENCE_BASE_URL to the deployed public site's origin.");
  assert.match(process.env.REFERENCE_EXPECTED_SHA || "", /^[a-f0-9]{40}$/, "Set REFERENCE_EXPECTED_SHA.");
  const base = new URL(process.env.REFERENCE_BASE_URL);
  assert.equal(base.protocol, "https:");
  assert.equal(base.pathname, "/");
  assert.equal(base.username + base.password + base.search + base.hash, "");
  const expected = process.env.REFERENCE_EXPECTED_SHA;
  const health = await fetch(new URL("/healthz", base));
  assert.equal(health.status, 200);
  const healthBefore = await health.json();
  assert.equal(healthBefore.commitSha, expected, "Live build differs from the intended reference revision.");
  const startedAt = new Date().toISOString();
  const version = `${startedAt.replace(/[:.]/g, "-")}-${expected.slice(0, 7)}`;
  const output = path.join(__dirname, "..", "references", "ship-a-skill", version);
  await fs.mkdir(path.dirname(output), { recursive: true });
  await fs.mkdir(output); // Exclusive capture directory: never overwrite previous evidence.
  const manifest = {
    schemaVersion: 1,
    title: "Ship a Skill implemented screen references",
    capturedAt: startedAt,
    source: { origin: base.origin, commitSha: expected, mode: "live-public-demo", authenticated: false },
    data: "Built-in public demo fixtures only. No production records or authenticated session.",
    imageTreatment: "Unmodified viewport captures. Reduced-motion preference; no layout, content or CSS replacement.",
    limitations: [
      "Demo/admin badges and sandbox footer are part of the live public demo and are intentionally retained.",
      "External integrations are simulated by the site's demo; captures are visual references, not integration evidence.",
      "Only the listed states and viewports are captured, not every possible empty, error or permission state.",
      "Viewport captures preserve the fixed shell and internal scrollers; content below the fold is not expanded.",
    ],
    viewports,
    screens: [],
  };
  const browser = await chromium.launch({ headless: true });
  try {
    for (const viewport of viewports) {
      const context = await browser.newContext({
        viewport, deviceScaleFactor: 1, colorScheme: "light", reducedMotion: "reduce",
        locale: "en-US", timezoneId: "UTC", serviceWorkers: "block",
      });
      const blockedRequests = [];
      await context.route("**/*", route => {
        const request = route.request();
        const url = new URL(request.url());
        const publicPath = url.pathname === "/" || url.pathname === "/demo" ||
          url.pathname.startsWith("/demo/") || url.pathname.startsWith("/_next/") ||
          ["/ship-a-skill-logo.png", "/favicon.ico"].includes(url.pathname);
        if (url.origin === base.origin && publicPath && request.method() === "GET") {
          return route.continue();
        }
        blockedRequests.push({ method: request.method(), pathname: url.pathname });
        return route.abort("blockedbyclient");
      });
      const page = await context.newPage();
      const errors = [];
      page.on("pageerror", error => errors.push(error.message));
      await page.goto(new URL("/demo/app?mode=sandbox", base).href);
      await page.locator('[data-tour="demo-footer"]').waitFor();
      for (const screen of screens) {
        await page.goto(new URL(screen.route, base).href, { waitUntil: "networkidle" });
        await page.locator("h1").first().waitFor();
        assert.ok((await page.locator("h1").allTextContents()).some(text =>
          text.toLowerCase().includes(screen.heading.toLowerCase())),
        `${screen.id}: unexpected heading ${await page.locator("h1").allTextContents()}`);
        if (screen.route.startsWith("/demo/app")) {
          await page.locator('[data-tour="demo-footer"]').waitFor();
          assert.equal(await page.getByText("Sample data", { exact: true }).count(), 1,
            `${screen.id}: public demo marker is missing`);
        }
        if (screen.action === "filter") await page.getByRole("button", { name: "Filter", exact: true }).click();
        if (screen.action === "settings") await page.getByRole("button", { name: "Settings", exact: true }).click();
        if (screen.action === "upload") await page.getByRole("button", { name: "2. Upload your package", exact: true }).click();
        await page.evaluate(async () => {
          await document.fonts.ready;
          await Promise.all([...document.images].map(image => image.decode()));
          await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));
        });
        assert.equal(await page.evaluate(() => document.fonts.status), "loaded");
        const observation = await page.evaluate(() => {
          const root = getComputedStyle(document.documentElement);
          const heading = document.querySelector("h1");
          const style = getComputedStyle(heading);
          return {
            headings: [...document.querySelectorAll("h1")].map(node => node.textContent.trim()),
            fonts: Object.fromEntries(["display", "sans", "mono"].map(role =>
              [role, root.getPropertyValue(`--font-${role}`).trim()])),
            headingStyle: {
              family: style.fontFamily, size: style.fontSize, weight: style.fontWeight,
              lineHeight: style.lineHeight, letterSpacing: style.letterSpacing,
              textTransform: style.textTransform,
            },
            pageOverflow: document.documentElement.scrollWidth > innerWidth,
          };
        });
        const file = `${screen.id}-${viewport.width}.png`;
        const bytes = await page.screenshot({ path: path.join(output, file), fullPage: false, animations: "disabled" });
        manifest.screens.push({
          id: `${screen.id}-${viewport.width}`, screen: screen.id, title: screen.title,
          path: new URL(page.url()).pathname + new URL(page.url()).search,
          interaction: screen.action || null, file, ...viewport, capturedAt: new Date().toISOString(),
          sha256: crypto.createHash("sha256").update(bytes).digest("hex"), ...observation,
        });
        await fs.writeFile(path.join(output, "manifest.partial.json"), `${JSON.stringify(manifest, null, 2)}\n`);
        console.log(`Captured ${screen.id} ${viewport.width}x${viewport.height}`);
      }
      assert.deepEqual(errors, [], "Live demo emitted browser errors");
      assert.deepEqual(blockedRequests, [], "Unexpected network requests were blocked; review before publishing");
      await context.close();
    }
    const after = await fetch(new URL("/healthz", base));
    assert.equal(after.status, 200);
    assert.equal((await after.json()).commitSha, expected, "Live build changed during capture");
    manifest.verifiedAt = new Date().toISOString();
    await fs.writeFile(path.join(output, "manifest.json"), `${JSON.stringify(manifest, null, 2)}\n`);
    await fs.unlink(path.join(output, "manifest.partial.json"));
    console.log(`Complete: ${manifest.screens.length} live references in ${output}`);
  } finally {
    await browser.close();
  }
}

main().catch(error => {
  console.error(error);
  process.exitCode = 1;
});
