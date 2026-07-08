# MatBrief — landing page (matbrief.com)

The "Site en construction" landing page for **matbrief.com**, hosted free on GitHub Pages.

- **Live site:** https://matbrief.com (also http → https, and https://www.matbrief.com)
- **Repo:** https://github.com/dsekkat/matbrief-site (public)
- **Hosting:** GitHub Pages, built from the `main` branch, root folder
- **Domain registrar / DNS:** Squarespace

## What's in this folder

| File | Purpose |
|------|---------|
| `index.html` | The entire landing page — self-contained (only external dependency is Google Fonts). Edit this to change the page. |
| `CNAME` | Tells GitHub Pages the custom domain is `matbrief.com`. **Do not delete or rename** — removing it breaks the custom domain. |
| `.gitignore` | Ignores macOS `.DS_Store` clutter. |
| `README.md` | This file. |

## How to update the page later

1. Edit `index.html` (open it in any text editor — it's plain HTML/CSS).
2. From this folder, run:
   ```bash
   git add index.html
   git commit -m "Update landing page"
   git push
   ```
3. GitHub Pages rebuilds automatically within ~1 minute. Refresh https://matbrief.com to see the change (do a hard refresh — Cmd+Shift+R — if the old version is cached).

## DNS setup (already done — for reference)

At **Squarespace → Domains → matbrief.com → DNS**, the website points to GitHub via:

- **A** records on host `@`: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
- **AAAA** records on host `@`: `2606:50c0:8000::153`, `2606:50c0:8001::153`, `2606:50c0:8002::153`, `2606:50c0:8003::153`
- **CNAME** on host `www` → `dsekkat.github.io`

### ⚠️ DNS records that must NOT be touched (email + Resend)

These have nothing to do with the website; deleting them breaks email:

- **MX** `@` → `smtp.google.com` — Google Workspace email delivery
- **TXT** `google._domainkey` — Google email signing (DKIM)
- **MX** `send` → `feedback-smtp.eu-west-1.amazonses.com` — Resend bounce handling
- **TXT** `send` → `v=spf1 include:amazonses.com ~all` — Resend SPF
- **TXT** `resend._domainkey` — Resend email signing (DKIM)

**Rule of thumb:** only ever change records of type **A / AAAA / CNAME** for the website. Never touch **MX** or **TXT** records, and never touch anything on the `send` or `_domainkey` hosts.

## HTTPS

GitHub Pages provides a free auto-renewing Let's Encrypt certificate for the domain, with "Enforce HTTPS" enabled (Settings → Pages). No maintenance required.

## Note

This folder (`~/Claude/Projects/MatBrief-Site`) is **separate** from `~/Claude/Projects/MatBrief`, which is an unrelated daily-automation project. Changes here do not affect that project.
