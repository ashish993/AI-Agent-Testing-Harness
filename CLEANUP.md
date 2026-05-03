# CLEANUP.md — Repository Maintenance Guide

This document explains how to keep the codebase clean, remove temporary files,
and reset the environment between test runs.

---

## Remove Python cache files

```bash
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -name "*.pyc" -delete
find . -name "*.pyo" -delete
```

## Remove test output files

```bash
rm -f report_*.md
rm -f output_*.txt
```

## Reset virtual environment

```bash
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run linting and formatting

```bash
pip install ruff
ruff check .
ruff format .
```

## Run type checking

```bash
pip install mypy
mypy module_*.py examples/
```

## Full clean and reinstall

```bash
git clean -fdx          # removes all untracked files (careful!)
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## What to commit vs ignore

The `.gitignore` should include:

```
__pycache__/
*.pyc
.venv/
*.egg-info/
dist/
report_*.md
output_*.txt
.DS_Store
```

## Dependency audit

```bash
pip install pip-audit
pip-audit
```

Review any HIGH or CRITICAL CVEs before deploying to production.
