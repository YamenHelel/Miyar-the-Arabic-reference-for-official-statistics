// Render the Open Graph / Twitter social cards (1200×630 PNG) listed in _site/static/social/cards.json.
// Usage: node tools/build_social_cards.mjs [_site]
// Needs Playwright + Chromium (preinstalled in the Claude sandbox; in CI: `npx playwright install chromium`).
// Design: the Miʿyar gold sheet on bottle green (ADR-0008), Amiri from Google Fonts.
import { readFileSync } from "node:fs";
import { join, resolve } from "node:path";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
let chromium;
try { ({ chromium } = require("playwright")); } catch { ({ chromium } = await import("playwright")); }

const site = resolve(process.argv[2] || "_site");
const dir = join(site, "static", "social");
const cards = JSON.parse(readFileSync(join(dir, "cards.json"), "utf8"));
const hallmark = readFileSync(resolve("tools/site/templates/hallmark.svg"), "utf8");
const esc = (s) => String(s || "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

const page = (c) => `<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&display=block">
<style>
  html,body{margin:0;width:1200px;height:630px;background:#133621;font-family:Amiri,serif;color:#133621}
  .sheet{position:absolute;inset:56px 64px 56px 64px;background:#f4d96c;padding:48px 60px;display:grid;grid-template-rows:auto 1fr auto;
         clip-path:polygon(0 0,calc(100% - 44px) 0,100% 44px,100% 100%,0 100%)}
  .kind{font-size:30px;color:#3e5a33}
  h1{margin:0;align-self:center;font-size:${c.title.length > 22 ? 78 : 104}px;line-height:1.2;font-weight:700}
  .sub{font-size:34px;direction:ltr;text-align:right;color:#3e5a33}
  .foot{display:flex;justify-content:space-between;align-items:flex-end}
  .brand{font-size:44px;font-weight:700}
  svg{width:70px;height:91px}
</style></head><body><div class="sheet">
  <div class="kind">${esc(c.kind)}</div>
  <h1>${esc(c.title)}</h1>
  <div class="foot"><div><div class="brand">مِعيار</div><div class="sub">${esc(c.sub)}</div></div>
  <svg viewBox="0 0 100 130">${hallmark}</svg></div>
</div></body></html>`;

const browser = await chromium.launch();
const p = await browser.newPage({ viewport: { width: 1200, height: 630 } });
for (const c of cards) {
  await p.setContent(page(c), { waitUntil: "networkidle" });
  await p.evaluate(() => document.fonts.ready);
  await p.screenshot({ path: join(dir, c.file) });
}
await browser.close();
console.log(`Rendered ${cards.length} social cards into ${dir}`);
