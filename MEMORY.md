# MatBrief Site — Living Memory

> **Read this at the start of every session.** Update it whenever I say **"save progress to memory."**
> This is the durable state of the matbrief.com website project.

## What this project is
The public website for **MatBrief** — a daily bulletin of plastic raw-material prices for the Moroccan market (PVC, polyethylene, plasticizers; prices by origin, freight, customs, forecasts). French-language. Based in Casablanca, Morocco. Contact: dsekkat@matbrief.com.

⚠️ **Separate from** `~/Claude/Projects/MatBrief` — that is a different project (a live daily automation). Do **not** touch it.

## Current state (as of 2026-07-09)
- **Live & secure:** https://matbrief.com serves over HTTPS with a valid auto-renewing cert; "Enforce HTTPS" is on. `http://` and `www.` both 301-redirect to the apex.
- **Hosting:** GitHub Pages, repo **`dsekkat/matbrief-site`** (public), built from `main` branch root. `CNAME` file = `matbrief.com`.
- **DNS:** managed at **Squarespace** (nsc*.squarespacedns.com). Apex A → GitHub IPs `185.199.108–111.153`; `www` CNAME → `dsekkat.github.io`; AAAA → `2606:50c0:8000–8003::153`.
  - **Never touch these DNS records (email/deliverability):** MX `smtp.google.com` (Google Workspace); `google._domainkey` TXT; `send` MX `feedback-smtp.eu-west-1.amazonses.com` + TXT `v=spf1 include:amazonses.com ~all` (Resend); `resend._domainkey` TXT (Resend DKIM). Only ever edit A / AAAA / CNAME for the website.
- **Page:** single self-contained `index.html` — "Site en construction" landing page. **Black rebrand done** (wordmark `#111`, orange `#e8541f` dot; no navy anywhere) and **visual polish deployed** (tighter wordmark tracking, refined status pill with soft shadow, subtle background lift, crisper type, gentle fade-in).
- **Favicons in place:** `favicon.ico`, `favicon-512.png`, `apple-touch-icon.png` (black variants), linked in `<head>`.

## Tooling
- **UI UX Pro Max** plugin installed in Claude Code at **user scope** (works in any project). Provides 7 skills: `banner-design, brand, design, design-system, slides, ui-styling, ui-ux-pro-max`. Callable from the **next session onward** (not the session it was installed in). Keep it for the redesign work below. Manage via `claude plugin list|details|uninstall`.

## How to update the site
Edit `index.html` → `git add . && git commit && git push`. GitHub Pages rebuilds in ~1–3 min (note: the build runner has occasionally stalled — if a change isn't live after a few minutes, trigger a rebuild via `gh api -X POST repos/dsekkat/matbrief-site/pages/builds`). Browsers cache favicons hard — hard-refresh (Cmd+Shift+R) to see icon changes.

## Next step (planned, not started)
**Full homepage redesign** — replace the single "en construction" page with a real homepage. A draft mockup exists in the **Cowork chat**. Intended sections:
1. **Hero** with a clickable bulletin preview
2. **Blurred subscriber-only sections** (gated content teaser)
3. **Méthodologie** section
4. **Pricing card**

Use the UI UX Pro Max skill for this. Keep it a clean, premium financial-data brand aesthetic; keep the black `#111` + orange `#e8541f` palette, no navy.
