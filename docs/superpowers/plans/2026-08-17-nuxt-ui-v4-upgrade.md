# @nuxt/ui v2->v4 Upgrade Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Upgrade `@nuxt/ui` from `^2.22.3` to `^4.10.0`, wiring up the CSS/config it actually requires (which was never finished the first time this project tried it — see spec), without adopting any new components.

**Architecture:** Four files change together as one atomic unit (bump the dependency, add the two required `@import` lines to `main.css`, register that file via `nuxt.config.ts`'s `css:` array, regenerate the lock file correctly). `app.vue` needs no change — its `<UApp>` wrapper already exists. This is not a multi-task feature; it's one cohesive config change, so it's structured as one implementation task plus a separate, explicitly-flagged manual verification task that requires a real browser this session cannot provide.

**Tech Stack:** Nuxt 3, `@nuxt/ui` v4, Tailwind CSS v4, npm.

**Spec:** `docs/superpowers/specs/2026-08-17-nuxt-ui-v4-upgrade-design.md`

---

## File Structure

- Modify: `nuxt-frontend/package.json` — bump `@nuxt/ui`, add `tailwindcss` as an explicit dependency.
- Modify: `nuxt-frontend/package-lock.json` — regenerated via `npm install`, never hand-edited.
- Modify: `nuxt-frontend/app/assets/css/main.css` — add two `@import` lines at the top only; every existing rule stays untouched (see spec's audit table for why).
- Modify: `nuxt-frontend/nuxt.config.ts` — add `css: ['~/assets/css/main.css']`.
- No change: `nuxt-frontend/app/app.vue` (already has `<UApp>`, confirmed in the spec).

---

### Task 1: Bump the dependency and wire up the required config

**Files:**
- Modify: `nuxt-frontend/package.json`
- Modify: `nuxt-frontend/package-lock.json`
- Modify: `nuxt-frontend/app/assets/css/main.css:1`
- Modify: `nuxt-frontend/nuxt.config.ts`

- [ ] **Step 1: Bump `@nuxt/ui`**

In `nuxt-frontend/package.json`, change:
```json
    "@nuxt/ui": "^2.22.3",
```
to:
```json
    "@nuxt/ui": "^4.10.0",
```
(`4.10.0` is the exact target already confirmed via the open Dependabot PR — "chore(deps): bump @nuxt/ui from 2.22.3 to 4.10.0 in /nuxt-frontend".)

- [ ] **Step 2: Add `tailwindcss` as an explicit dependency**

Don't hand-write a version guess into `package.json` — let npm resolve the actual current version:
```bash
cd nuxt-frontend && npm install tailwindcss
```
Expected: `tailwindcss` now appears in `nuxt-frontend/package.json`'s `dependencies` with whatever version npm actually resolved.

- [ ] **Step 3: Add the required CSS imports**

At the very top of `nuxt-frontend/app/assets/css/main.css` (before the existing `/* Global CSS variables */` comment), add:
```css
@import "tailwindcss";
@import "@nuxt/ui";

```
Nothing else in this file changes — every existing rule (`:root`, `*`, `body`, `.container`, `.card`, `.btn-primary`, the `input[type=...]` override) stays exactly as-is. The spec's audit table already covers what each one does once this file is actually loaded for the first time.

- [ ] **Step 4: Register the CSS file in `nuxt.config.ts`**

In `nuxt-frontend/nuxt.config.ts`, add a top-level `css` array. The file currently starts:
```ts
export default defineNuxtConfig({
  modules: ["@pinia/nuxt", "@nuxt/ui", "@nuxt/eslint"],
```
Change to:
```ts
export default defineNuxtConfig({
  modules: ["@pinia/nuxt", "@nuxt/ui", "@nuxt/eslint"],
  css: ["~/assets/css/main.css"],
```

- [ ] **Step 5: Regenerate the lock file**

Run: `cd nuxt-frontend && npm install`
Expected: completes without error. This will show `EBADENGINE` warnings about Node version mismatches (pre-existing, unrelated to this change — same warnings seen throughout this project's build logs already) — those are not failures, ignore them.

- [ ] **Step 6: Verify the regenerated lock file is actually in sync**

This is the exact check that would have caught the incident on 2026-08-13 (a lock file left out of sync broke `Deploy to VPS` and every PR's `nuxt-checks` job for days undetected). Run in an isolated copy, not the working directory:
```bash
mkdir -p /tmp/nuxt-ui-v4-lockcheck
cp nuxt-frontend/package.json nuxt-frontend/package-lock.json /tmp/nuxt-ui-v4-lockcheck/
cd /tmp/nuxt-ui-v4-lockcheck && npm ci
```
Expected: `npm ci` completes without an `EUSAGE`/"lock file out of sync" error. If it fails, do not proceed — re-run `npm install` in the real `nuxt-frontend/` directory and re-check.

- [ ] **Step 7: Run the automated checks**

```bash
cd nuxt-frontend
npm run lint
npm run build
```
Expected: both exit 0.

- [ ] **Step 8: Confirm the hero's Tailwind classes still generate**

```bash
grep -o 'mix-blend-screen' .output/public/index.html | wc -l
```
Expected: `4` (one per aurora-glow layer div on the landing page hero — same check used when the hero was first verified).

- [ ] **Step 9: Commit**

```bash
git add nuxt-frontend/package.json nuxt-frontend/package-lock.json nuxt-frontend/app/assets/css/main.css nuxt-frontend/nuxt.config.ts
git commit -m "feat: upgrade @nuxt/ui to v4, wire up its required Tailwind CSS imports"
```

**Do not push yet.** Task 2 (manual verification) has to happen first — see below for why.

---

### Task 2: Manual verification (requires a real browser — cannot be automated in this session)

**Why this is its own task, not a step skipped or merged into Task 1:** `nuxt.config.ts`'s `routeRules` mark `/dashboard/**` as `ssr: false` (client-side-rendered only) and `/listings*` as `ssr: true` (server-rendered per-request, not statically prerendered). Neither produces meaningful output in `.output/public/` for a static grep to check — the spec's audit table flags the universal `* { margin: 0; padding: 0; }` reset in `main.css` (now active for the first time, sitewide) as the one rule in this migration with a real chance of a visible layout regression, and a static-HTML check is structurally incapable of catching it on these routes. This has to be eyes-on, in a browser, after Task 1 is committed.

- [ ] **Step 1: Start the app**

Whichever matches normal local dev — `docker compose up` from the repo root, or `npm run dev`/`npm run preview` in `nuxt-frontend/`.

- [ ] **Step 2: Load every page and check for layout shifts**

Specifically watch for elements that lost spacing they previously had from browser defaults (default `<p>`/`<ul>`/`<li>`/heading margins, default button/input padding) — anything currently set via inline `style` is unaffected, this is only about elements that were relying on browser defaults.

- `/` — re-confirm visually (the aurora hero, stats bar, feature cards, footer)
- `/listings` — **specifically check the min/max price number inputs** (the one rule in the spec's audit table with a real chance of a visible change — they never had an explicit inline `background` set, so they'll get a forced white background for the first time; confirm they still look right)
- `/listings/[id]` (any existing listing)
- `/dashboard` (Overview)
- `/dashboard/analytics`
- `/dashboard/map` (today's redesign — confirm the dark aurora-glow theme still renders correctly alongside the new Tailwind version)
- `/dashboard/predict` — including its 4 inputs and the Recent Predictions widget
- `/dashboard/compare`

- [ ] **Step 3: If everything looks right, push**

```bash
git push
```

- [ ] **Step 4: If something broke**

Per the spec's rollback plan: revert `package.json`/`package-lock.json`/`nuxt.config.ts`/`main.css` together as one unit (`git revert` the Task 1 commit) rather than trying to partially unwind — they only make sense as a set. Report back what broke before re-attempting.

---

## Post-implementation

None — this migration deliberately doesn't touch `CLAUDE.md`'s Sprint 6 list beyond what's already there (item 11's `@nuxt/ui` bullet already describes this as the open item; once Task 2 confirms it's live, update that bullet to DONE, matching the pattern used for the `prediction_logs` item).
