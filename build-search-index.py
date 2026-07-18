#!/usr/bin/env python3
"""
AFMS - WADiana Service Manual Search Index Builder
Run this ONCE to OCR all 78 service manual PDFs and produce a search index.

Requirements:
    pip install pdf2image pytesseract pillow
    Also needs: Tesseract OCR  (https://github.com/UB-Mannheim/tesseract/wiki for Windows)

Usage:
    python build-search-index.py

Output:
    manuals/wadiana-svc-index.json   (~300KB, used by index.html for search)

Time: ~20-30 minutes on first run. Leave it running in the background.
"""

import os, sys, json, time, re
from pathlib import Path

# ── Dependencies check ────────────────────────────────────────────────────────
try:
    from pdf2image import convert_from_path
    import pytesseract
    from PIL import Image
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("Run:  pip install pdf2image pytesseract pillow")
    sys.exit(1)

# ── Tesseract path (Windows default) ─────────────────────────────────────────
if sys.platform == 'win32':
    candidates = [
        r'C:\Program Files\Tesseract-OCR\tesseract.exe',
        r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
    ]
    for c in candidates:
        if os.path.exists(c):
            pytesseract.pytesseract.tesseract_cmd = c
            break

# ── Paths ─────────────────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).parent
PDF_FOLDER = SCRIPT_DIR / 'manuals' / 'wadiana-svc'
OUTPUT     = SCRIPT_DIR / 'manuals' / 'wadiana-svc-index.json'

def clean_text(t):
    """Remove OCR noise: excess whitespace, lone characters, etc."""
    t = re.sub(r'[ \t]+', ' ', t)
    t = re.sub(r'\n{3,}', '\n\n', t)
    # Remove lines that are just punctuation/noise (common OCR artifacts)
    lines = [l.strip() for l in t.splitlines()]
    lines = [l for l in lines if len(l) > 1 or l.isalnum()]
    return '\n'.join(lines).strip()

def ocr_pdf(pdf_path, dpi=120):
    """Convert PDF pages to images then OCR each page."""
    pages_text = []
    try:
        images = convert_from_path(str(pdf_path), dpi=dpi)
        for i, img in enumerate(images):
            txt = pytesseract.image_to_string(img, lang='eng')
            pages_text.append(clean_text(txt))
    except Exception as e:
        print(f"    ERROR: {e}", flush=True)
    return pages_text

def main():
    pdfs = sorted(f for f in os.listdir(PDF_FOLDER) if f.endswith('.pdf'))
    total = len(pdfs)
    print(f"Found {total} PDFs in {PDF_FOLDER}")
    print(f"Output will be saved to: {OUTPUT}")
    print("=" * 60)

    index = {}

    # Load existing index if present (allows resuming interrupted runs)
    if OUTPUT.exists():
        try:
            index = json.loads(OUTPUT.read_text(encoding='utf-8'))
            already = len(index)
            print(f"Resuming — {already} PDFs already indexed, {total-already} remaining.\n")
        except:
            pass

    t_start = time.time()
    for i, fname in enumerate(pdfs, 1):
        if fname in index:
            print(f"[{i:2d}/{total}] SKIP (cached): {fname[:60]}")
            continue

        pdf_path = PDF_FOLDER / fname
        print(f"[{i:2d}/{total}] OCR-ing: {fname[:60]}", end=' ... ', flush=True)
        t0 = time.time()
        pages = ocr_pdf(pdf_path)
        elapsed = time.time() - t0
        total_chars = sum(len(p) for p in pages)
        print(f"{len(pages)} pages, {total_chars} chars, {elapsed:.1f}s")

        index[fname] = {'pages': pages}

        # Save after each PDF so progress is never lost
        OUTPUT.write_text(json.dumps(index, ensure_ascii=False, separators=(',', ':')),
                          encoding='utf-8')

    total_time = time.time() - t_start
    total_pages = sum(len(v['pages']) for v in index.values())
    size_kb = OUTPUT.stat().st_size // 1024
    print()
    print("=" * 60)
    print(f"Done! {total} PDFs, {total_pages} pages indexed in {total_time/60:.1f} min")
    print(f"Index file: {OUTPUT}  ({size_kb} KB)")
    print()
    print("Reload index.html in your browser to enable full-text search.")

if __name__ == '__main__':
    main()
