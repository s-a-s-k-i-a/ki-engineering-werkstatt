# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "marimo",
#   "pydantic>=2.9",
# ]
# ///

"""Lösungs-Skelett — Übung 18.01 — Bias + Self-Censorship + Red-Team + Safety-Stack.

Smoke-Test-tauglich: keine echten API-Calls, keine GPU-Abhängigkeit. Stub-Reports
zeigen das Audit-Pattern. Vollversion mit Garak + PyRIT + Llama Guard siehe
Lektionen 18.07 + 18.09.
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
        # 🎯 Lösung Übung 18.01 — Audit-Paket (Beispiel: Profil B — Internes QA mit Qwen3-32B)

        Du erstellst:

        1. Bias-Audit-Report (Stub)
        2. Self-Censorship-Audit-Report (Stub)
        3. Red-Team-Report (Stub)
        4. Safety-Stack-Performance (Stub)
        5. Konformitätserklärung als YAML

        Smoke-Test-tauglich (Stub-Werte) — Reproduzierbarkeit über separate Reports.
        """
    )
    return


@app.cell
def _():
    """Pydantic-Schemas."""
    from typing import Literal

    from pydantic import BaseModel, Field

    class BiasReport(BaseModel):
        modell: str
        dir_pro_dimension: dict[str, float]  # Disparate Impact Ratio
        bias_score_open_end: float = Field(ge=0.0, le=1.0)
        problematische_dimensionen: list[str]

    class SelfCensReport(BaseModel):
        modell: str
        zensur_rate_gesamt: float = Field(ge=0.0, le=1.0)
        pro_kategorie: dict[str, float]
        disclaimer_pflicht: bool

    class RedTeamReport(BaseModel):
        modell: str
        refusal_rate_jailbreak: float = Field(ge=0.0, le=1.0)
        prompt_injection_resistenz: float = Field(ge=0.0, le=1.0)
        kritische_luecken: list[str]

    class SafetyStackReport(BaseModel):
        nemo_config: str
        llama_guard_version: str
        ttft_ms_ohne_safety: int
        ttft_ms_mit_safety: int
        false_positive_rate: float

    class Konformitaet(BaseModel):
        anbieter: str
        system_name: str
        version: str
        klassifikation: Literal["minimal", "begrenzt", "hoch", "unzulaessig"]
        konformitaetspfad: Literal["Anhang VI", "Anhang VII"]
        anhang_iv_punkte_erfuellt: int = Field(ge=0, le=9)
        luecken: list[str]

    return (
        BiasReport,
        Konformitaet,
        RedTeamReport,
        SafetyStackReport,
        SelfCensReport,
    )


@app.cell
def _(BiasReport):
    """Stub-Bias-Audit für Qwen3-32B (lokal)."""
    bias_report = BiasReport(
        modell="Qwen3-32B (Ollama, deutsch)",
        dir_pro_dimension={
            "geschlecht": 0.72,  # signifikanter Bias (< 0.8)
            "migration": 0.78,  # auch problematisch
            "region": 0.92,
            "alter": 1.05,
            "religion": 0.85,
            "beruf": 0.83,
        },
        bias_score_open_end=0.31,  # 31 % der Open-End-Outputs enthielten Stereotype
        problematische_dimensionen=["geschlecht", "migration"],
    )
    return (bias_report,)


@app.cell
def _(SelfCensReport):
    """Stub-Self-Censorship für Qwen3-32B."""
    self_cens = SelfCensReport(
        modell="Qwen3-32B (Ollama, deutsch)",
        zensur_rate_gesamt=0.35,
        pro_kategorie={
            "tiananmen": 0.40,
            "taiwan": 0.30,
            "xinjiang": 0.40,
            "xi_jinping": 0.20,
            "hongkong": 0.45,
        },
        disclaimer_pflicht=True,
    )
    return (self_cens,)


@app.cell
def _(RedTeamReport):
    """Stub-Red-Team."""
    red_team = RedTeamReport(
        modell="Qwen3-32B (Ollama, deutsch)",
        refusal_rate_jailbreak=0.92,  # 92 % Refusal — solid
        prompt_injection_resistenz=0.85,  # 85 % erkannt
        kritische_luecken=[
            "Code-Switch DE→EN umgeht Filter in 2/30 Fällen",
            "Du-Form mit emotionaler Bitte: 1/15 Fail",
            "Indirekte Injection in RAG-Quelle: 3/20 erfolgreich",
        ],
    )
    return (red_team,)


@app.cell
def _(SafetyStackReport):
    """Stub-Safety-Stack."""
    safety = SafetyStackReport(
        nemo_config="DACH-Custom mit StGB § 86a + § 130",
        llama_guard_version="3-8B",
        ttft_ms_ohne_safety=1100,
        ttft_ms_mit_safety=1850,  # +750 ms für Safety-Layer
        false_positive_rate=0.04,  # 4 % False-Positives auf harmlose Prompts
    )
    return (safety,)


@app.cell
def _(bias_report, mo, red_team, safety, self_cens):
    """4-Reports-Übersicht."""
    rows_summary = [
        f"| **Bias-Audit** | DIR Geschlecht: {bias_report.dir_pro_dimension['geschlecht']:.2f} ⚠️ | Migration: {bias_report.dir_pro_dimension['migration']:.2f} ⚠️ | Open-End: {bias_report.bias_score_open_end * 100:.0f} % stereotyp |",
        f"| **Self-Censorship** | Gesamt: {self_cens.zensur_rate_gesamt * 100:.0f} % | Tiananmen: {self_cens.pro_kategorie['tiananmen'] * 100:.0f} % | Disclaimer pflicht ✓ |",
        f"| **Red-Team** | Refusal: {red_team.refusal_rate_jailbreak * 100:.0f} % | PI-Resistenz: {red_team.prompt_injection_resistenz * 100:.0f} % | {len(red_team.kritische_luecken)} Lücken |",
        f"| **Safety-Stack** | TTFT +{safety.ttft_ms_mit_safety - safety.ttft_ms_ohne_safety} ms | FPR: {safety.false_positive_rate * 100:.0f} % | {safety.llama_guard_version} |",
    ]

    mo.md(
        "## Audit-Paket-Übersicht\n\n"
        "| Report | Wert 1 | Wert 2 | Status |\n|---|---|---|---|\n" + "\n".join(rows_summary)
    )
    return


@app.cell
def _(Konformitaet, bias_report, red_team, self_cens):
    """Konformitätserklärung (Stub)."""
    konformitaet = Konformitaet(
        anbieter="Beispiel GmbH",
        system_name="Internes QA-Tool",
        version="1.0",
        klassifikation="begrenzt",
        konformitaetspfad="Anhang VI",
        anhang_iv_punkte_erfuellt=7,  # 7 von 9 erfüllt
        luecken=[
            (
                f"Bias-Audit zeigt DIR < 0.8 in {len(bias_report.problematische_dimensionen)} "
                f"Dimensionen → DPO-Run mit Korrektur-Pairs nötig (Phase 18.04)"
            ),
            (
                "Self-Censorship-Disclaimer fehlt im UI → muss vor Go-Live "
                "prominent angezeigt werden (Lektion 18.08)"
            ),
            (
                f"Red-Team zeigt {len(red_team.kritische_luecken)} Lücken → NeMo-Config "
                f"erweitern + monatliches Re-Audit"
            ),
        ],
    )
    return (konformitaet,)


@app.cell
def _(konformitaet, mo):
    """Konformitätserklärung anzeigen."""
    luecken_text = "\n".join(f"  - {item}" for item in konformitaet.luecken)
    yaml_text = f"""anbieter: {konformitaet.anbieter}
system_name: {konformitaet.system_name}
version: {konformitaet.version}
klassifikation: {konformitaet.klassifikation}
konformitaetspfad: {konformitaet.konformitaetspfad}
anhang_iv_punkte_erfuellt: {konformitaet.anhang_iv_punkte_erfuellt}/9
luecken:
{luecken_text}
"""

    mo.md(f"## Konformitätserklärung\n\n```yaml\n{yaml_text}```")
    return


@app.cell
def _(bias_report, mo, red_team, safety):
    """Mitigation-Plan."""
    mitigations = [
        (
            "DPO-Run mit 200 Bias-Korrektur-Pairs für Geschlecht + Migration "
            "(Lektion 18.04, ~ 2 h auf RTX 4090)"
        ),
        ("Self-Censorship-Disclaimer in UI prominent anzeigen (alle Hauptseiten)"),
        ("NeMo Guardrails mit Code-Switch-Filter + DACH-StGB-Policy aktivieren (Lektion 18.09)"),
        (f"Llama Guard {safety.llama_guard_version} als Output-Filter — TTFT-Penalty akzeptiert"),
        (
            f"Quartalsweise Re-Audit aller {len(bias_report.problematische_dimensionen)} "
            f"problematischen Bias-Dimensionen + Red-Team-Lücken"
        ),
    ]

    md_block = "## Mitigation-Plan\n\n"
    for i, m in enumerate(mitigations, 1):
        md_block += f"{i}. {m}\n"

    mo.md(
        md_block
        + (
            f"\n**Cost-Schätzung Mitigation**: ~ 8 h Engineering-Aufwand + "
            f"€ {2 * 0.80:.2f} GPU-Strom für DPO-Run."
        )
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Reflexion (Pflicht in `BERICHT.md`)

        - **Bias-Befund**: Geschlecht und Migration zeigen DIR < 0.8 — DPO-Run pflicht
        - **Self-Censorship**: 35 % Zensur-Rate auf 50 dt. Prompts — Disclaimer reicht
          nicht für News-Use-Case, aber für **internes** QA-Tool akzeptabel
        - **Red-Team**: Code-Switch-Lücke ist kritisch — sofortiger Filter-Patch nötig
        - **Safety-Stack**: +750 ms TTFT akzeptabel für QA-Tool, nicht für Echt-Zeit-Chat
        - **Konformität**: 7/9 Anhang-IV-Punkte erfüllt — Lücken-Plan dokumentiert,
          vor Go-Live geschlossen

        ## Wie du das auf dein Profil anwendest

        1. Pass `bias_report` mit deinen 30 Probes-Ergebnissen an
        2. `self_cens`-Cell nur bei asiatischen Modellen ausführen
        3. `red_team`-Cell mit deinen Garak/promptfoo-Outputs befüllen
        4. `safety`-Cell mit deinen NeMo+Llama-Guard-Latenz-Messungen
        5. `konformitaet`-Cell mit deiner Punkt-für-Punkt-Anhang-IV-Checkliste
        6. BERICHT.md mit den 5 Tabellen + 3-Satz-Reflexion

        ## Compliance-Anker

        - **AI-Act Art. 9 / 10 / 12 / 13 / 15**: alle 4 Audits decken Pflicht-Inhalte
        - **DSGVO Art. 22**: bei automatisierten Entscheidungen Mensch-Pfad pflichtbewusst
        - **AI-Act Anhang IV**: Konformitätserklärung committet ins Repo

        ## Quellen

        - BBQ-Paper — <https://arxiv.org/abs/2110.08193>
        - Garak — <https://github.com/leondz/garak>
        - NeMo Guardrails — <https://github.com/NVIDIA/NeMo-Guardrails>
        - Llama Guard 3 — <https://huggingface.co/meta-llama/Llama-Guard-3-8B>
        - AI-Act Anhang IV — <https://eur-lex.europa.eu/eli/reg/2024/1689/oj>
        """
    )
    return


if __name__ == "__main__":
    app.run()
