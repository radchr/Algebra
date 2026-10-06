import os
import shutil
import subprocess

PROJECT_ROOT = r"c:\Users\taxco\Dev\Algebra"
BOOK_DIR = os.path.join(PROJECT_ROOT, "book_geometry")
BUILD_DIR = os.path.join(BOOK_DIR, "build")
DOCS_ASSETS = os.path.join(PROJECT_ROOT, "docs", "assets")
os.makedirs(BUILD_DIR, exist_ok=True)
os.makedirs(DOCS_ASSETS, exist_ok=True)

# 1. Clean PATH from any entries that end with .exe (MiKTeX Windows bug fix)
env = os.environ.copy()
clean_paths = [p for p in env.get("PATH", "").split(";") if not p.lower().endswith(".exe")]
env["PATH"] = ";".join(clean_paths)

print("Starting XeLaTeX compilation pass 1...")
res1 = subprocess.run(
    ["xelatex", "-interaction=nonstopmode", "-output-directory=build", "main.tex"],
    cwd=BOOK_DIR,
    env=env,
    capture_output=True,
)
print("Pass 1 finished, exit code:", res1.returncode)

print("Starting XeLaTeX compilation pass 2 (TOC & cross-refs)...")
res2 = subprocess.run(
    ["xelatex", "-interaction=nonstopmode", "-output-directory=build", "main.tex"],
    cwd=BOOK_DIR,
    env=env,
    capture_output=True,
)
print("Pass 2 finished, exit code:", res2.returncode)

pdf_source = os.path.join(BUILD_DIR, "main.pdf")
if os.path.exists(pdf_source):
    target_docs = os.path.join(DOCS_ASSETS, "kiselev_geometry_7_pilot.pdf")
    shutil.copy2(pdf_source, target_docs)
    size_kb = os.path.getsize(target_docs) / 1024
    print(f"SUCCESS: Generated {target_docs} ({size_kb:.1f} KB)")
else:
    print("ERROR: main.pdf was not produced.")
