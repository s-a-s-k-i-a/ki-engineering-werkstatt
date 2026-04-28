# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "marimo",
# ]
# ///

"""Lösungs-Skelett — Übung 00.01 — eigene Werkstatt dokumentieren.

Dieses Notebook ist eine Vorlage. Trage deine eigenen Werte ein, dann läuft es
lokal und dokumentiert deine spezifische Werkstatt-Konfiguration.

Smoke-Test-tauglich: keine externen Aufrufe, keine API-Keys nötig.
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
        # 📋 Meine Werkstatt — Lösung Übung 00.01

        **Stand**: _hier dein Datum eintragen_
        **Ort**: _z. B. Hannover_
        **Werkstatt-Version**: ki-engineering-werkstatt 0.1.0
        """
    )
    return


@app.cell
def _(mo):
    """1. Hardware-Klasse."""
    hardware = {
        "OS": "macOS 25.2 Tahoe",  # ← anpassen
        "Architektur": "Apple Silicon M3 Pro",  # ← anpassen
        "RAM": "32 GB Unified Memory",  # ← anpassen
        "GPU": "n/a (Unified Memory)",  # ← anpassen
        "Hardware-Klasse": "32 GB Apple Silicon → bis ~ 30B q4",  # ← anpassen
    }

    rows_hardware = "\n".join(f"| {k} | {v} |" for k, v in hardware.items())
    mo.md(
        f"## 1. Hardware-Klasse\n\n"
        f"| Eigenschaft | Wert |\n|---|---|\n{rows_hardware}\n\n"
        "→ Laut Lektion 00.01 kann ich Modelle bis ca. 30B q4 lokal laufen lassen "
        "(z. B. Qwen 3 30B-A3B-MoE, Gemma 3 27B)."
    )
    return (hardware,)


@app.cell
def _(mo):
    """2. Tool-Versionen."""
    tools = {
        "Python": "3.13.0",  # ← `python --version`
        "uv": "0.11.8",  # ← `uv --version`
        "Marimo": "0.23.4",  # ← `marimo --version` (oder pyproject.toml)
        "Ollama": "0.22.0",  # ← `ollama --version`
        "Just": "1.40.0",  # ← `just --version` (optional)
        "Docker": "27.5.1",  # ← `docker --version` (optional)
    }

    rows_tools = "\n".join(f"| {k} | `{v}` |" for k, v in tools.items())
    mo.md(f"## 2. Tool-Versionen\n\n| Tool | Version |\n|---|---|\n{rows_tools}")
    return (tools,)


@app.cell
def _(mo):
    """3. Lokales Modell — was läuft, wie schnell, mit welchem Output?"""
    modell_info = {
        "Modell": "qwen3:8b",  # ← anpassen
        "Größe": "~ 4,8 GB (q4_K_M)",
        "RAM-Verbrauch": "~ 6 GB inkl. Context",
        "Tokens / Sekunde": "~ 45 (auf M3 Pro 32 GB)",  # ← messen
        "Pull-Zeit": "~ 2 Min. bei 100 Mbit/s",
    }

    rows_modell = "\n".join(f"| {k} | {v} |" for k, v in modell_info.items())

    test_prompt = "Was ist der AI Act in zwei Sätzen?"
    test_antwort = (
        "Der AI Act (Verordnung (EU) 2024/1689) ist die EU-weite Regelung von "
        "KI-Systemen mit gestaffeltem Inkrafttreten zwischen 2025 und 2027. "
        "Er klassifiziert Systeme in vier Risikoklassen (verboten, hochrisiko, "
        "begrenzt, minimal) und legt entsprechende Pflichten für Anbieter und "
        "Bereitsteller fest."
    )

    mo.md(
        f"## 3. Lokales LLM-Setup\n\n| Eigenschaft | Wert |\n|---|---|\n{rows_modell}\n\n"
        f"### Test-Prompt\n\n> {test_prompt}\n\n"
        f"### Antwort\n\n> {test_antwort}\n\n"
        "→ Antwort kommt in unter 10 Sekunden, fachlich korrekt, auf Deutsch."
    )
    return modell_info, test_antwort, test_prompt


@app.cell
def _(mo):
    """4. EU-Cloud-Wahl (optional)."""
    cloud = {
        "Anbieter": "Scaleway Generative APIs",  # ← anpassen
        "Standort": "Paris (FR)",
        "AVV-Status": "Self-Service signiert (im Customer Portal)",
        "Modell-Test": "mistral-small-3.2",
        "Pricing": "€ 0,15 In / € 0,35 Out per 1M Token",
        "Free-Tier": "1M Token kostenlos zum Start",
        "Zertifikate": "ISO 27001, HDS",
    }

    rows_cloud = "\n".join(f"| {k} | {v} |" for k, v in cloud.items())
    mo.md(f"## 4. EU-Cloud (optional)\n\n| Eigenschaft | Wert |\n|---|---|\n{rows_cloud}")
    return (cloud,)


@app.cell
def _(mo):
    """5. Reflexion."""
    reflexion = """
    ### Was war einfach?

    - `uv` ist überraschend schnell. Ich war Pip-Resolver-Wartezeiten gewöhnt; mit
      uv geht das in Sekunden statt Minuten.
    - Marimo zu starten war ein Befehl. Ich hatte „noch ein Notebook-Tool"
      erwartet, aber die reaktive Auto-Run-Logik hat sofort Sinn ergeben.

    ### Was war schwer?

    - Ich hatte einen Moment Verwirrung mit `--extra` vs. `--group` (PEP 735).
      Lektion 00.02 hat das geklärt — Extras sind PyPI-public, Groups sind nur
      lokal.
    - Bei Ollama war die Auswahl an Modellen anfangs überfordernd. Die Tabelle
      in Lektion 00.04 hat sehr geholfen, schnell ein passendes für meine
      Hardware zu finden.

    ### Was nehme ich mit?

    - Lokal-erst entwickeln spart erheblich Token-Kosten und vermeidet AVV-Stress
      während der Lehr-Phase.
    - EU-Cloud (z. B. Scaleway Free-Tier) ist günstig genug, um auch Production-
      ähnliche Tests zu machen, ohne erst US-Provider anlegen zu müssen.
    """
    mo.md(f"## 5. Reflexion\n{reflexion}")
    return


@app.cell
def _(mo):
    """6. Ergebnis."""
    mo.md(
        r"""
        ---

        ## ✅ Werkstatt eingerichtet — bereit für Phase 05

        Nächste Schritte:

        1. `uv run marimo edit phasen/05-deutsche-tokenizer/code/01_tokenizer_showdown.py`
        2. Token-Showdown auf 10kGNAD durchspielen
        3. Eigene Tokenizer-Empfehlung für meinen Use-Case herleiten

        Bei Problemen: [Discussions](https://github.com/s-a-s-k-i-a/ki-engineering-werkstatt/discussions).
        """
    )
    return


if __name__ == "__main__":
    app.run()
