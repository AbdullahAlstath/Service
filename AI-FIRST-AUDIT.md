# AI-Firstify Assessment Report

**Project:** AFMS ServicePal — biomedical service-engineer web app (index.html PWA + pdf-editor.html)
**Date:** 2026-07-17
**Mode:** Audit (read-only)

> Context note: the AI-Firstify framework is designed for *AI-first projects* (repos an AI agent works inside — CLAUDE.md, skills, git discipline). AFMS is a **shipped end-user web app**, so a few dimensions (Skills, Agent Architecture) apply only loosely. Scores below are honest against the rubric, and recommendations are filtered to what genuinely helps this project.

## Overall Score

| Dimension | Score | Summary |
|-----------|-------|---------|
| 1. Project Structure | RED | No git, no CLAUDE.md, no .gitignore; 70 root files incl. 378 MB of manual .bak copies |
| 2. Agent Architecture | YELLOW | Optional in-app Anthropic chat via a server-side Cloudflare proxy; key not in client; defaults offline |
| 3. Skill Usage | RED | No .claude/skills (largely N/A for a product app, but no reusable automation captured) |
| 4. Scope & Complexity | YELLOW | Broad but focused domain; the 39 MB single-file monolith is the main complexity risk |
| 5. Context Hygiene | RED | One 39 MB HTML mixes code + data + base64 images; working folder cluttered with scratch/backup files |
| 6. Safety | YELLOW | No secrets in client code, offline by default; but client-side password "gate" is not real security |
| 7. Workflow Design | RED | No version control, no validation/review pipeline; backups are manual .bak files |

## Priority Recommendations

1. **[HIGH]** Put the project under **git** and delete the 10 manual `.bak` copies (≈378 MB) once history exists — effort ~15 min.
2. **[HIGH]** **Clean the working folder**: remove 34 stray calibration PNG/PDFs, `ppm_pages_tmp/`, `test_marks/`, `_mnt_sync_test.txt` — effort ~10 min.
3. **[HIGH]** Restore the **missing `manifest.webmanifest`** — index.html links it but the file is absent, breaking PWA install/icon — effort ~10 min.
4. **[MEDIUM]** Add a **`.gitignore`** (scratch outputs, \*.bak, OS files) and a short **README/CLAUDE.md** describing structure, how to run, and how it's deployed — effort ~20 min.
5. **[MEDIUM]** Split the **39 MB single-file** index.html: move the part-image data / per-device datasets into separate files loaded on demand (also fixes slow load) — effort: larger, staged.
6. **[LOW]** Label or strengthen the **client-side password gate** — treat it as a soft lock, not security; anything sensitive must live behind the server proxy — effort ~varies.

## Detailed Findings

### Dimension 1: Project Structure
RED. No `.git`, no `CLAUDE.md`, no `.gitignore`, no `README`. The root holds 70 entries (226 files total). Version history is being kept as **10 `index.html.bak_*` files totalling ~378 MB** plus a `pdf-editor.html.bak` — this is what git is for. Deliverables (index.html, pdf-editor.html, manuals/) are mixed with dozens of throwaway calibration artifacts.

### Dimension 2: Agent Architecture
YELLOW. The app offers an optional AI assistant ("Ask Notebook" / quick chat / troubleshooting) that calls the Anthropic API **through `proxy-worker.js` (a Cloudflare Worker)** so the API key stays server-side. `API_PROXY_URL` defaults to `''` (100% offline; a built-in offline responder is used). This is a reasonable, safe pattern for a shipped product — the LLM is a feature, not core plumbing, and no key is exposed client-side. Not "AI-first" in the framework's sense, but not a red flag either.

### Dimension 3: Skill Usage
RED (mostly N/A). There is no `.claude/skills/` directory. For a distributed web app this is expected, so treat this as informational rather than a defect. If you keep iterating with an AI assistant, the repeated **PPM PDF-calibration workflow** (extract template → detect cells → transform coordinates → verify) is a strong candidate to capture as a reusable script/skill.

### Dimension 4: Scope & Complexity
YELLOW. The product is coherent (one audience: field service engineers) but wide: 7 device workspaces, parts catalogs, manual viewers, PPM checklist generators, an AI chat, notebook links, a lab-module reference, plus a new standalone PDF editor. The real complexity issue is **structural, not featural**: index.html is a single 39 MB file embedding code, data, and ~1,200 base64 images. That is hard to diff, edit safely, and load quickly.

### Dimension 5: Context Hygiene
RED. Everything lives in one 39 MB HTML file, so code, per-device datasets, and image blobs are all interleaved — the opposite of progressive disclosure. The working folder compounds it with backup copies, scratch renders, and temp directories. There is no top-level doc explaining what's what.

### Dimension 6: Safety
YELLOW. Positives: no API keys or tokens in the client (the proxy holds the secret), offline-by-default, no committed `.env`. Watch-items: the password gate is **client-side only** (bypassable — fine as a soft deterrent, not access control); the many scratch/backup files in the folder could inadvertently be shared; `proxy-worker.js` ships with placeholder origins (`yourusername.github.io`) that must be locked down before real deployment.

### Dimension 7: Workflow Design
RED. No git means no commit discipline, no diff-based review, and no rollback except manual `.bak` files. There is no validation/test harness in the repo (`build-search-index.py` is a one-off generator). Adding version control + a tiny "does index.html still parse / open a device" smoke check would remove most of the risk we've hit during edits.

## Recommended Next Steps

1. `git init`, commit the current index.html + pdf-editor.html + manuals/, then delete the `.bak` files and scratch artifacts.
2. Add `.gitignore` and a short `README.md` (what it is, how to open, how it deploys, where the proxy lives).
3. Restore `manifest.webmanifest` so the PWA install/icons work again.
4. Plan a staged split of index.html (externalize part images/data) to shrink load time and make edits safe.
5. Before any public deploy, lock the proxy's `ALLOWED_ORIGINS` and treat the password gate as non-security.
