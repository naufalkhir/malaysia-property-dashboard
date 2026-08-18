# `@nuxt/ui` v2 → v4 upgrade

Date: 2026-08-17
Status: Approved (writing-only pass — no code changes made under this spec yet)

## Context

`@nuxt/ui` is pinned to `^2.22.3` in `nuxt-frontend/package.json`. Upgrading to
v4 closes the last remaining (moderate) npm vulnerability out of the original
23 found 2026-08-11 (22 already fixed via `npm audit fix`, non-breaking) —
see `CLAUDE.md` Sprint 6.

**Verified: zero `@nuxt/ui` components are in use anywhere today.**
```
grep -rn "<U[A-Z]" app/                                    → no matches
grep -rn "from ['\"]#components['\"]\|from ['\"]@nuxt/ui['\"]" app/  → no matches
grep -rnE "useToast|useOverlay|useModal\(|appConfig\.ui" app/        → no matches
find . -iname "app.config.ts"                              → no file
```
Every page is 100% inline `style="..."`. `@nuxt/ui` currently exists purely
as a dependency silently providing Tailwind under the hood — nothing else.
This means the upgrade has no component-migration surface; the risk is
entirely in *Tailwind and global CSS wiring*, not in broken `UButton`/`UCard`
usage.

### What `3676ff5` (the original v2 pin) actually fixed — confirmed, not assumed

Traced the full history rather than trusting the commit message alone:

```
git log --oneline -- nuxt-frontend/package.json nuxt-frontend/app.vue \
  nuxt-frontend/nuxt.config.ts nuxt-frontend/app/assets/css/main.css
  ...
  e50f959  fix: remove unused @nuxtjs/tailwindcss causing prod build crash
  3676ff5  fix: downgrade @nuxt/ui to v2 for Tailwind compatibility
```

At the initial commit, the project had **both** `@nuxt/ui@^4.6.0` *and* a
separate `@nuxtjs/tailwindcss@^6.14.0` module registered simultaneously —
two competing Tailwind integrations (v4's own bundled Vite plugin vs. the
older module's own PostCSS pipeline) in the same Nuxt app. `e50f959` removed
the redundant `@nuxtjs/tailwindcss` module 23 minutes before the downgrade.

Checked out `nuxt-frontend/{app.vue,nuxt.config.ts,app/assets/css/main.css}`
**at `e50f959`** — i.e. the brief window where the project ran `@nuxt/ui@4.6.0`
alone, without the conflicting module:
- `app.vue` **already had** `<UApp><NuxtPage /></UApp>` — correctly done.
- `nuxt.config.ts` had **no `css: [...]` array**.
- `main.css` had **no `@import "tailwindcss"; @import "@nuxt/ui";`** — same
  plain CSS-variables file as today, no Tailwind directives at all.

**Conclusion:** v4's required CSS wiring (the `@import` directives + `css:`
registration) was never actually added. Without it, Tailwind v4 generates no
utility CSS at all — the app would have built (after the conflicting module
was removed) but rendered completely unstyled. Rather than diagnose the
missing import step, the pragmatic fix at the time was downgrading to v2's
self-contained zero-config setup.

**This means today's planned migration — which explicitly adds the missing
`@import` directives and `css:` registration — fixes the actual root cause,
not just the symptom.** The `<UApp>` wrapper doesn't need to be re-verified;
it was already done correctly before and never changed.

## Full audit of `app/assets/css/main.css`

This file is **currently dead** — nothing in `nuxt.config.ts` loads it (no
`css: [...]` array exists today), confirmed independently by `predict.vue`'s
own inline `background: white` workarounds on its inputs (comments literally
say "FIX 1/2/3" — evidence someone already hit the fact that this file's
`input[type=...] { background: white !important }` rule wasn't taking
effect, and worked around it with inline styles instead of noticing the file
wasn't loaded). Once `main.css` is wired up as part of this migration, it
activates **sitewide, for the first time, on every page** — not just wherever
new Tailwind classes are added. Every rule needs to be assessed for what
happens when it goes live, not just the already-known-dead input rule:

| Rule | Current usage (verified via grep) | Risk once live |
|---|---|---|
| `:root { --color-*: ... }` | `grep -rn "var(--color-" app/pages/` → **no matches anywhere** | None — inert, nothing references these variables outside this file itself |
| `* { box-sizing: border-box; margin: 0; padding: 0; }` | N/A (universal selector) | **Highest risk in this file.** `app.vue`'s own active `<style>` block already has its own `* { box-sizing: border-box; }`, but does **not** zero margin/padding. This rule newly zeroes margin/padding on **every element on every page for the first time**. Elements with explicit inline `margin`/`padding` are unaffected (inline styles win over this regardless of specificity), but anything currently relying on browser-default spacing (default `<p>`/`<ul>`/`<li>`/heading margins, default button/input padding not explicitly set inline) could visibly shift. This is exactly why a real per-page visual check is required, not just a build check. |
| `body { font-family, background-color: var(--color-bg), color: var(--color-text), line-height: 1.6 }` | `app.vue`'s own `<style>` block already sets body to the same resolved values (`#f8fafc` bg, `#1e293b` text, same font, same line-height) directly (not via variables) | None — fully redundant with what's already active, same computed values, no visual change |
| `.container` | `grep -rn 'class="container"' app/pages/` → **no matches** | None — inert |
| `.card` | `grep -rn 'class="card"' app/pages/` → no exact matches (the only hits were unrelated page-local classes in `analytics.vue` like `.chart-card`/`.card-header`/`.card-title`, which are different selectors defined in that page's own styling, not this rule) | None — inert |
| `.btn-primary` | `grep -rl 'btn-primary' app/pages/` → **`index.vue` only** | None — `app.vue`'s own active `<style>` block already defines `.btn-primary` with the same resolved values (`#2563eb` / `#1d4ed8` hover). Two rules will now target the same class with matching values: redundant CSS, zero visual change. |
| `input[type="number"\|"text"\|"email"\|"password"\|"search"] { background: white !important; color: #1e293b !important; }` | `predict.vue`: 4 inputs, **all already have explicit inline `background: white`** (the "FIX 1/2/3" comments) — no visible change. `listings/index.vue`: 2 `type="number"` inputs (min/max price) with **no explicit inline `background` set today** — these will get a forced white background for the first time. Likely already renders white by default in most browsers, but not guaranteed (OS/browser dark-mode form-control defaults vary) | Low-moderate — the one rule in this file with a real (if probably subtle) chance of an observable change. Specifically called out in the verification plan below. |

**Net assessment:** the only two rules with any real chance of a visible
change are the universal margin/padding reset (real risk, sitewide) and the
input background rule on `listings/index.vue`'s two price filter inputs (low
risk, narrow scope). Everything else in this file is either already
redundant with `app.vue`'s own active styles or completely unused. Not
deduping `app.vue`'s duplicate rules against `main.css` as part of this
migration — that belongs in the later systematic page-rebuild pass, per the
"pure upgrade only" scope already agreed for this piece of work.

## Design

### Scope (unchanged from prior discussion)

Pure dependency upgrade — bump `@nuxt/ui` to `^4.10.0`, wire up the required
config changes, verify nothing breaks. No new `@nuxt/ui` components adopted;
that's future page-by-page work. Does **not** touch `pages/dashboard/map.vue`
or any other page content — this spec covers `package.json`,
`package-lock.json`, `nuxt.config.ts`, `app/assets/css/main.css`, and
`app.vue` only.

### Changes required

1. **`package.json`**: bump `"@nuxt/ui": "^2.22.3"` → `"^4.10.0"`, add
   `"tailwindcss"` as an explicit dependency (v2 bundled it invisibly; v4
   requires it declared per the official install docs).
2. **`app/assets/css/main.css`**: add to the very top, before the existing
   `:root` block:
   ```css
   @import "tailwindcss";
   @import "@nuxt/ui";
   ```
   Leave every existing rule in the file untouched (see audit table above —
   nothing here needs to change, only the two new import lines are added).
3. **`nuxt.config.ts`**: add `css: ['~/assets/css/main.css']` to actually
   load the file for the first time.
4. **`app.vue`**: no change needed — `<UApp><NuxtPage /></UApp>` wrapping
   already exists today (confirmed identical to what `e50f959` had) and was
   never part of what broke originally.
5. **`package-lock.json`**: regenerate via `npm install` (not `npm ci` —
   learned this lesson from the prediction_logs deploy incident on
   2026-08-13, where a lock file left out of sync with `package.json` broke
   both `Deploy to VPS` and every PR's `nuxt-checks` job for days
   undetected). Verify the regenerated lock file passes `npm ci` in an
   isolated directory before committing, the same way that incident's fix
   was verified.

### Verification plan

**Automated (can run in this environment):**
1. `npm install` in `nuxt-frontend/`, then verify the regenerated lock file
   passes `npm ci` in an isolated temp copy (not the working directory —
   avoids polluting the actual install).
2. `npm run lint` (ESLint via `@nuxt/eslint`).
3. `npm run build`.
4. Static-HTML check of the prerendered `/` route only (`.output/public/index.html`)
   — confirm the hero's Tailwind utility classes (`bg-[#050807]`,
   `blur-[90px]`, `mix-blend-screen`, the `aurora-drift`/`hero-headline-glow`
   keyframes) still generate correctly. This is the same method used to
   verify the hero originally, and it remains valid **for `/` only** — see
   below for why it's insufficient for everything else.

**Manual, required, not optional (cannot be substituted with a static-HTML
grep):**

`nuxt.config.ts`'s `routeRules` mean `/dashboard/**` (Overview, Analytics,
Map, Predict, Compare) are `ssr: false` — client-side-rendered only. There is
no meaningful server-rendered HTML for these routes; the DOM only exists
after client-side JS mounts in an actual browser. Grepping `.output/public/`
for these routes would either find nothing or find an empty shell — it
cannot verify anything about whether the universal CSS reset broke their
layout. `/listings` and `/listings/[id]` are `ssr: true` (server-rendered
per-request, not statically prerendered), so they also aren't covered by a
prerendered-output grep.

5. Start the app for real (`docker compose up` or `npm run dev`/`preview` —
   whichever matches normal local dev) and **manually load every one of these
   pages in a real browser**, checking specifically for layout shifts from
   the newly-active `* { margin: 0; padding: 0; }` reset:
   - `/` (re-confirm visually, not just via the static grep)
   - `/listings` — including the min/max price number inputs specifically
     (the one rule in the audit table with a real chance of visible change)
   - `/listings/[id]` (any existing listing)
   - `/dashboard` (Overview)
   - `/dashboard/analytics`
   - `/dashboard/map`
   - `/dashboard/predict` — including its 4 inputs
   - `/dashboard/compare`

This step requires an actual browser and running app instance. It could not
be completed for the hero verification earlier (Docker wasn't running in
this sandboxed environment) — flagging now so whoever executes this plan
knows it's a hard requirement, not something to skip because the automated
checks passed.

### Rollback

If the manual check surfaces a real layout regression that isn't a quick
fix, revert `package.json`/`package-lock.json`/`nuxt.config.ts`/`main.css`
together as one unit (they only make sense as a set) rather than trying to
partially unwind. Low effort to revert since this is a small, isolated set
of file changes with no component-migration surface tangled into it.

## Out of scope

- Adopting any actual `@nuxt/ui` v4 component (`UButton`, `UCard`, etc.) —
  future page-by-page work, per the earlier "pure upgrade only" decision.
- Deduplicating `app.vue`'s `<style>` block against `main.css`'s now-active
  overlapping rules (`.btn-primary`, `body`) — cosmetic redundancy, zero
  visual impact, belongs in the later systematic page-rebuild pass.
- The `pages/dashboard/map.vue` redesign — separate, unrelated piece of work
  scoped to its own spec/plan, deliberately not touching `main.css`,
  `app.vue`, or `nuxt.config.ts` so it doesn't collide with this migration's
  execution.
