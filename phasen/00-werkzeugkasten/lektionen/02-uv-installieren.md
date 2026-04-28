---
id: 0.02
titel: uv installieren und ein Projekt anlegen
phase: 00-werkzeugkasten
dauer_minuten: 30
schwierigkeit: einsteiger
stand: 2026-04-28
voraussetzungen: [0.01]
lernziele:
  - uv (Astral) installieren auf macOS / Linux / Windows
  - Mit `uv init` ein Projekt anlegen, mit `uv add` Dependencies setzen
  - Den Unterschied zwischen `--extra` (PyPI-Extras) und `--group` (Dev-Groups, PEP 735) verstehen
  - `uv.lock` als reproducible-build-Garantie einsetzen
compliance_anker:
  - keys-niemals-im-code
colab_badge: false
---

## Worum es geht

> Stop juggling `pip`, `poetry`, `pyenv`, `virtualenv`, `pip-tools`. — uv macht alles in einem Tool, **10–100× schneller**.

`uv` ist der 2026 etablierte Python-Paket-Manager. Geschrieben in Rust, gemacht von Astral (denselben Leuten, die Ruff bauen). Standalone-Binary, keine Python-Abhängigkeit zum Bootstrappen.

**Aktuelle stable Version** (Stand 28.04.2026): `0.11.8`.

## Voraussetzungen

- Phase 00.01 durchgegangen (du kennst deine Hardware-Klasse)
- Funktionierende Internet-Verbindung
- Optional: `git` ist installiert (für `uv init --vcs git`)

## Konzept

### Was uv kann (das pip / poetry nicht in einem Tool kann)

| Aufgabe | klassisch | uv |
|---|---|---|
| Python installieren | `pyenv install 3.13` | `uv python install 3.13` |
| venv erstellen | `python -m venv .venv` | automatisch |
| Dependencies | `pip install -r req.txt` | `uv add ...` + `uv sync` |
| Lockfile | `pip-compile` | `uv.lock` (built-in) |
| Dev-Dependencies | extra requirements-dev.txt | `uv add --group dev` |
| Skript-Runner | `python -m foo` (mit aktivem venv) | `uv run foo` (auto-resolve) |
| Skript mit Inline-Dependencies | n/a | `uv run script.py` mit PEP 723 |

### Installation

**macOS / Linux** (offizielle Astral-Installer):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell)**:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Alternative (alle Plattformen)**:

```bash
# Über Homebrew (macOS / Linux)
brew install uv

# Über pipx (überall)
pipx install uv
```

**Verifizieren**:

```bash
uv --version
# → uv 0.11.8 (Homebrew 2026-04-27) oder ähnlich
```

### Dein erstes Projekt

```bash
# 1. Projekt anlegen (im aktuellen Verzeichnis)
uv init mein-erstes-ki-projekt
cd mein-erstes-ki-projekt

# 2. Was wurde erstellt?
ls -la
# → .python-version       (z. B. "3.13")
# → .gitignore            (Standard Python-gitignore)
# → README.md
# → main.py               (Hello-World)
# → pyproject.toml        (Projekt-Konfiguration)

# 3. Python sicherstellen (uv installiert es bei Bedarf)
uv python install 3.13

# 4. Erste Dependency hinzufügen
uv add httpx

# 5. Code ausführen — uv aktiviert venv automatisch
uv run main.py
```

Was hier passiert ist:

1. `uv init` hat einen `pyproject.toml`-Stub mit dem aktuellen Python-Standard erzeugt.
2. `uv add httpx` hat:
   - eine virtuelle Umgebung in `.venv/` erstellt,
   - `httpx` und seine Dependencies installiert,
   - die exakten Versionen in `uv.lock` geschrieben,
   - `pyproject.toml` ergänzt.
3. `uv run main.py` hat den Code im venv ausgeführt — kein `source .venv/bin/activate` nötig.

### Extras vs. Groups (wichtig für KI-Projekte!)

Python-Pakete können zwei Arten optionaler Dependencies haben. Verwechseln führt zu Verwirrung — du **musst** den Unterschied kennen:

```toml
[project.optional-dependencies]
# "Extras" = werden mit auf PyPI publiziert
# Andere Nutzer können sie via `pip install paket[extra]` installieren
tokenizer = ["tokenizers>=0.20", "tiktoken>=0.8"]
rag = ["qdrant-client>=1.12", "rank-bm25>=0.2"]

[dependency-groups]
# "Groups" (PEP 735) = lokal-only, nie auf PyPI
# Nur für deine eigene Entwicklung gedacht
dev = ["ruff>=0.7", "pytest>=8.3"]
```

Aufruf:

```bash
uv sync --extra tokenizer       # PyPI-Extra
uv sync --group dev             # PEP 735 Dev-Group
uv sync --all-extras --all-groups
```

**Faustregel**:

- **User-facing optional features** (z. B. „mit GPU-Support") → `[project.optional-dependencies]`
- **Dev-Workflow** (Lint, Test, Format) → `[dependency-groups]`

In **diesem Repo** (`ki-engineering-werkstatt`) nutzen wir aktuell `[project.optional-dependencies]` für alles, weil das pip-kompatibel ist und die User-Tooling-Etikette einfacher hält. Das könnte sich in einem späteren Refactor ändern.

### Reproduzierbarkeit: das `uv.lock`

Wenn du `uv add httpx` machst, wird **die exakt aufgelöste Version** mit Hash in `uv.lock` geschrieben. Das committest du. Wenn jemand anders `uv sync` macht, bekommt er **die identischen Versionen, byte-genau**.

Das ist der wichtige Unterschied zu `pip install -r requirements.txt`: Letzteres re-resolved ggf. auf neuere Versionen — ein Update von einer Transitiv-Dependency kann dein Setup brechen.

> **In diesem Repo** ist `uv.lock` committet. Beim `uv sync` bekommst du genau die Umgebung, die ich beim Schreiben getestet habe.

## Hands-on (15 Min.)

```bash
# 1. uv installieren (siehe oben), dann
uv --version

# 2. Test-Projekt anlegen (irgendwo außerhalb des Werkstatt-Repos)
cd /tmp
uv init uv-test
cd uv-test

# 3. Marimo hinzufügen — du wirst es in 00.03 nutzen
uv add marimo

# 4. uv.lock anschauen (bewusst!)
cat uv.lock | head -30
# Beachte: jede Dependency mit pinned Version + Hash

# 5. Marimo starten
uv run marimo edit
# → öffnet Browser auf http://localhost:2718
# → Strg+C zum Beenden
```

Wenn das geklappt hat: du hast das Standard-Werkstatt-Setup.

## Selbstcheck

- [ ] Du kannst `uv --version` ausführen und siehst eine Versionsnummer.
- [ ] Du verstehst, warum `uv add` schneller ist als `pip install` (Rust-basierter Resolver).
- [ ] Du kennst den Unterschied zwischen `--extra` und `--group`.
- [ ] Du erklärst, warum `uv.lock` committet wird.
- [ ] Du brauchst kein `source .venv/bin/activate` mehr — `uv run` macht das.

## Compliance-Anker

- **`uv.lock` ist Pflicht** für reproduzierbare Builds nach AI-Act Art. 11 (Tech-Doku) — du kannst jederzeit beweisen, mit welcher Dependency-Version du gearbeitet hast.
- **Keine API-Keys in `pyproject.toml`** oder anderen committeten Dateien. Nur in `.env`-Files (siehe `.env.example` im Repo-Root).

## Quellen

- uv Docs (Astral) — <https://docs.astral.sh/uv/> (Zugriff 2026-04-28)
- uv Releases — <https://github.com/astral-sh/uv/releases> (aktuell 0.11.8)
- uv Versioning Policy — <https://docs.astral.sh/uv/reference/policies/versioning/>
- uv Concepts: Dependencies — <https://docs.astral.sh/uv/concepts/projects/dependencies/>
- PEP 735 (Dependency Groups) — <https://peps.python.org/pep-0735/>

## Weiterführend

→ Lektion **00.03** (Marimo statt Jupyter) — jetzt nutzt du `uv` für Notebooks
→ Lektion **00.04** (Ollama lokal) — dein erster lokaler LLM-Aufruf
