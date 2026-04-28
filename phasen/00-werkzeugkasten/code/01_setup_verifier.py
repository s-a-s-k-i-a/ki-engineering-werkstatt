# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "marimo",
#   "rich>=13.9",
#   "httpx>=0.27",
# ]
# ///

"""Setup-Verifier — prüft, dass deine Werkstatt sauber aufgesetzt ist.

Smoke-Test-tauglich: alle Checks sind read-only, keine API-Keys nötig.
Ollama-Check ist optional (wird nur ausgeführt, wenn Daemon läuft).
"""

import marimo

__generated_with = "0.23.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    mo.md(
        r"""
        # 🛠️ Setup-Verifier · Phase 00

        Dieses Notebook prüft systematisch, ob deine Werkstatt-Umgebung sauber aufgesetzt ist:

        1. **Python-Version** (sollte ≥ 3.13 sein)
        2. **uv-Version** (sollte aktuell sein)
        3. **Marimo-Version** (du läufst gerade in Marimo, also OK)
        4. **Ollama-Daemon** (optional — wird geprüft, ob läuft)
        5. **Deutsche Sprach-Tokenisierung** (eine Zeile)

        Wenn alles grün ist, kannst du mit Phase 05 (Tokenizer) starten.
        """
    )
    return


@app.cell
def _(mo):
    """1. Python-Version."""
    import sys

    py_version = sys.version_info
    py_str = f"{py_version.major}.{py_version.minor}.{py_version.micro}"
    py_ok = py_version >= (3, 13)

    mark_py = "✅" if py_ok else "❌"
    msg_py = "" if py_ok else " — Bitte auf Python 3.13+ aktualisieren!"
    mo.md(f"### 1. Python-Version\n\n{mark_py} `{py_str}`{msg_py}")
    return py_ok, py_str


@app.cell
def _(mo):
    """2. uv-Version (Subprozess-Aufruf)."""
    import subprocess

    try:
        res = subprocess.run(
            ["uv", "--version"], capture_output=True, text=True, check=False, timeout=5
        )
        uv_str = res.stdout.strip() if res.returncode == 0 else "uv nicht gefunden"
        uv_ok = res.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        uv_str = "uv nicht gefunden"
        uv_ok = False

    mark_uv = "✅" if uv_ok else "❌"
    hinweis_uv = (
        "" if uv_ok else " — Installation: `curl -LsSf https://astral.sh/uv/install.sh | sh`"
    )
    mo.md(f"### 2. uv-Version\n\n{mark_uv} `{uv_str}`{hinweis_uv}")
    return uv_ok, uv_str


@app.cell
def _(mo):
    """3. Marimo-Version."""
    import marimo

    marimo_version = marimo.__version__
    marimo_ok = True  # wenn dieser Code läuft, ist Marimo offensichtlich da

    mo.md(f"### 3. Marimo-Version\n\n✅ `{marimo_version}`")
    return marimo_ok, marimo_version


@app.cell
def _(mo):
    """4. Ollama-Daemon (optional, fail-soft)."""
    import httpx

    try:
        # Default-Port 11434
        r = httpx.get("http://localhost:11434/api/tags", timeout=2)
        if r.status_code == 200:
            data = r.json()
            modelle = data.get("models", [])
            ollama_state = f"läuft, {len(modelle)} Modell(e) installiert"
            if modelle:
                ollama_state += f" — z. B. `{modelle[0]['name']}`"
            ollama_ok = True
        else:
            ollama_state = f"antwortet mit Status {r.status_code}"
            ollama_ok = False
    except (httpx.ConnectError, httpx.TimeoutException):
        ollama_state = "nicht erreichbar (optional — siehe Lektion 00.04)"
        ollama_ok = None  # neutral, nicht „failed"
    except Exception as e:
        ollama_state = f"Fehler: {type(e).__name__}"
        ollama_ok = None

    mark_ollama = "✅" if ollama_ok else ("⚪" if ollama_ok is None else "❌")
    mo.md(f"### 4. Ollama-Daemon (optional)\n\n{mark_ollama} `{ollama_state}`")
    return ollama_ok, ollama_state


@app.cell
def _(mo):
    """5. Eine Zeile deutsche Tokenisierung — keine externen Modelle nötig."""
    import re
    from collections import Counter

    beispiel = (
        "Donaudampfschifffahrtsgesellschaftskapitän erinnert "
        "die Mitarbeiter:innen an die Generalversammlung in München."
    )

    woerter = re.findall(r"\w+", beispiel.lower())
    n_woerter = len(woerter)
    n_zeichen = len(beispiel)
    n_unique = len(set(woerter))
    haeufigste = Counter(woerter).most_common(3)

    laengstes = max(woerter, key=len)
    mo.md(
        f"### 5. Deutsche Sprach-Statistik\n\n"
        f"**Beispiel-Satz**: *{beispiel}*\n\n"
        f"- {n_zeichen} Zeichen, {n_woerter} Wörter, {n_unique} unique\n"
        f"- Häufigste Tokens: `{haeufigste}`\n"
        f"- Längstes Wort: `{laengstes}` ({len(laengstes)} Zeichen)\n\n"
        f"→ Phase 05 zeigt, wie unterschiedlich Tokenizer dieses Wort behandeln."
    )
    return beispiel, n_unique, n_woerter, n_zeichen


@app.cell
def _(mo, ollama_ok, py_ok, uv_ok):
    """6. Zusammenfassung."""
    pflicht = py_ok and uv_ok  # Marimo läuft = OK, das ist klar
    optional_ok = ollama_ok is True
    optional_msg = (
        "✅ Bonus: Ollama läuft."
        if optional_ok
        else "⚪ Bonus: Ollama optional. Für lokale LLMs siehe Lektion 00.04."
    )

    if pflicht:
        verdict = (
            "## ✅ Werkstatt einsatzbereit\n\n"
            "Alle Pflicht-Checks grün. Du kannst mit Phase 05 (Deutsche Tokenizer) starten:\n\n"
            "```bash\n"
            "uv run marimo edit phasen/05-deutsche-tokenizer/code/01_tokenizer_showdown.py\n"
            "```\n\n"
            f"{optional_msg}"
        )
    else:
        verdict = (
            "## ❌ Werkstatt unvollständig\n\n"
            "Mindestens ein Pflicht-Check ist rot. Bitte oben prüfen und Phase 00 "
            "(Lektionen 00.01 bis 00.04) durchgehen, bis alle grün sind."
        )
    mo.md(verdict)
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ### Was du als Nächstes machen kannst

        - **Phase 05 (Deutsche Tokenizer)** — der Token-Effizienz-Showdown mit GPT-5, Claude 4.7, Llama 4, Mistral, Pharia, Teuken auf 10kGNAD
        - **Phase 13 (RAG-Tiefenmodul)** — von Vanilla bis Agentic mit Pharia-1 + Qdrant
        - **Phase 20 (Recht & Governance)** — AI-Act-Klassifizierung, AVV-Checkliste, DSFA-Workflow

        Alle 21 Phasen: [`ROADMAP.md`](../../../ROADMAP.md)
        """
    )
    return


if __name__ == "__main__":
    app.run()
