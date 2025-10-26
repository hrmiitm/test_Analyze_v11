# Analyze_v11

This repository contains a small data analysis script and CI workflow that publishes the analysis result to GitHub Pages.

What is included
- execute.py — Python 3.11 compatible script which reads data.csv (falls back to data.xlsx) and prints JSON to stdout.
- data.csv — CSV converted from the provided data.xlsx (committed so execute.py can run locally).
- .github/workflows/ci.yml — GitHub Actions workflow that:
  - Runs ruff (output is visible in the CI logs)
  - Runs `python execute.py > result.json`
  - Publishes `result.json` to GitHub Pages (the workflow uploads it as the Pages artifact)
- index.html, style.css, script.js — a minimal GitHub Pages site that can display the deployed `result.json`.

Notes
- Do NOT commit result.json. The CI generates it and publishes it to GitHub Pages.
- The workflow pins Pandas 2.3.x and uses Python 3.11.

How to run locally

1. Install dependencies (recommended in a venv):

   pip install "pandas==2.3.*" openpyxl

2. Run the analysis and capture output:

   python execute.py > result.json

You can then open `result.json` or use the included `index.html` to load it when hosted.
