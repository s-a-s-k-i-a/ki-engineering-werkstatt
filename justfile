# KI-Engineering-Werkstatt — Lokaler Workflow-Runner
# Voraussetzung: just (https://github.com/casey/just) + uv (https://docs.astral.sh/uv/)

set shell := ["bash", "-uc"]

default:
    @just --list

# Erstinstallation: uv sync + pre-commit + Pflicht-Datasets
setup:
    uv sync --all-extras
    uv run pre-commit install
    @echo "✓ Setup fertig. Nächster Schritt: 'just smoke' oder 'marimo edit phasen/05-deutsche-tokenizer/code/01_tokenizer_showdown.py'"

# Lint + Format-Check + Codespell-DE + Markdownlint
lint:
    uv run ruff check .
    uv run ruff format --check .
    uv run codespell phasen/ docs/ werkzeuge/ tests/ README.md ROADMAP.md CHANGELOG.md CONTRIBUTING.md
    @echo "✓ Lint grün."

# Auto-Fix (formatieren + simple Ruff-Fixes)
fix:
    uv run ruff check --fix .
    uv run ruff format .
    @echo "✓ Fixes angewandt."

# Type-Check (Astral Ty)
typecheck:
    uv run ty check werkzeuge/ tests/
    @echo "✓ Typecheck grün."

# E2E Smoke-Tests: Marimo headless + CLI-Tools + Compliance-Schema + Link-Check (offline)
smoke:
    @echo "→ 1/5 ruff lint"
    @just lint
    @echo "→ 2/5 ty type-check"
    @just typecheck
    @echo "→ 3/5 pytest tests (Notebook-Smoke + Werkzeuge + Compliance)"
    uv run pytest tests/ -q
    @echo "→ 4/5 lychee offline link-check"
    @command -v lychee >/dev/null 2>&1 && lychee --offline --no-progress phasen/ docs/ README.md || echo "  (lychee nicht installiert, übersprungen — siehe README für Setup)"
    @echo "→ 5/5 gitleaks secret-scan"
    @command -v gitleaks >/dev/null 2>&1 && gitleaks detect --no-banner --redact -v --source . || echo "  (gitleaks nicht installiert, übersprungen)"
    @echo "✓ Smoke-Tests durch."

# Marimo .py → .ipynb-Konvertierung + Colab-Badges injizieren
notebooks:
    uv run python werkzeuge/build_notebooks.py
    uv run python werkzeuge/inject_colab_badges.py
    @echo "✓ Notebooks gebaut."

# Marimo-Notebook eines Showcase-Moduls direkt öffnen
edit phase:
    uv run marimo edit phasen/{{phase}}/code/

# Online-Linkcheck (alle externen Links — slow, weekly cron in CI)
link-check:
    @command -v lychee >/dev/null 2>&1 && lychee --no-progress --max-redirects 5 phasen/ docs/ README.md ROADMAP.md || echo "lychee nicht installiert"

# Compliance-Schema-Linter (jedes compliance.md valide?)
compliance-check:
    uv run python werkzeuge/compliance_lint.py phasen/

# Repo-Statistik (für Module-Coverage-Badge)
stats:
    @uv run python werkzeuge/stats.py

# Aufräumen (caches, build-Artefakte) — KEINE source-Files
clean:
    rm -rf .ruff_cache .ty_cache .pytest_cache .uv-cache build dist *.egg-info
    find . -type d -name __pycache__ -prune -exec rm -rf {} +
    @echo "✓ Cache leer."
