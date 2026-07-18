# AFMS ServicePal

A single-file, offline-capable web app for biomedical service engineers: spare-parts
catalogs, service manuals, troubleshooting, and PPM (preventive-maintenance) checklist
generators for several lab analyzers (LIAISON XL, CL-1200i/CL-900i, ETI-MAX, BIO-FLASH,
WADiana, Erytra Eflexis).

## Files

| File | Purpose |
|------|---------|
| `index.html` | The whole app (UI, data, and embedded images/PDF templates). Open directly in a browser. |
| `pdf-editor.html` | Standalone PDF editor tool (edit text, draw, add photos, OCR scanned PDFs). |
| `manuals/` | Service-manual PDFs linked from the app's "Manual" tabs. |
| `manifest.webmanifest`, `icon-*.png` | PWA install metadata + app icons. |
| `proxy-worker.js` | Optional Cloudflare Worker that proxies the in-app AI chat to the Anthropic API (keeps the API key server-side). Not required — the app runs fully offline with `API_PROXY_URL = ''`. |
| `build-search-index.py` | One-off helper that built the manual search index. |
| `AI-FIRST-AUDIT.md` | Project health audit report. |

## Run

Open `index.html` (or `pdf-editor.html`) in any modern browser. Installable as a PWA on
mobile via "Add to Home Screen". PDF rendering, the PDF editor, and the AI chat load
libraries from CDN, so those features need internet; the parts/manual/PPM core works offline.

## Deploy

Static hosting (e.g. GitHub Pages). To enable the AI chat, deploy `proxy-worker.js` as a
Cloudflare Worker, set its `ANTHROPIC_API_KEY` secret, lock `ALLOWED_ORIGINS` to your site,
and set `API_PROXY_URL` in `index.html` to the Worker URL.

## Notes

- The password gate in the app is a soft lock (client-side), not real access control.
- Manuals referenced but not yet present: `bioflash.pdf`, `etimax.pdf`, `liaison-xl.pdf`
  (their "Open Manual" buttons 404 until the PDFs are added).
