# AFMS ServicePal — Deployment Notes

## What was wrong
GitHub Pages rejects any site over **1 GB**. Your folder was **~3 GB**, almost
all of it images inside the three HTML help systems (Panther Service Manual,
Parts Library, Troubleshooting Guide) plus the manual PDFs.

## What I changed
- Recompressed ~7,000 images inside the three help folders (large PNGs/JPGs and
  the 353 uncompressed BMPs) to JPEG-quality data. Filenames and extensions are
  unchanged, so every HTML link still resolves — browsers render them fine.
- Downsampled the biggest manual PDFs (cl900 70→28 MB, cl1200 34→27 MB, etc.).
- Moved non-website scratch/source into `_deploy_ignore/` (kept locally, not for
  the site) and added it to `.gitignore`.

**Result: the site is now ~884 MB — under the 1 GB limit.**

## To deploy
1. Commit the compressed files **and** the moves (git will see many changes).
2. Do **not** upload the `_deploy_ignore/` folder. If you deploy with git it's
   already excluded via `.gitignore`. If you upload the folder manually, delete
   or skip `_deploy_ignore/` first.
3. Push, then let the Pages workflow run.

## About the second error in your log
`Invalid actions OIDC token ... No keys from key endpoint match the id token`
is a **transient GitHub Actions infrastructure issue**, not something in your
repo. If it recurs after the size is fixed, just **re-run the failed workflow**
(Actions tab → the run → "Re-run all jobs"). It almost always clears on retry.

## Quality note
Images and PDFs are now lower resolution to fit the limit. They remain clearly
readable for field reference. Full-resolution originals are still on your machine
(the help-system source folders were compressed in place — if you want pristine
copies preserved, keep a backup of the originals before your next sync).
