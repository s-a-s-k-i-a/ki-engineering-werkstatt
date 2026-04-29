# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "marimo",
#   "pydantic>=2.9",
# ]
# ///

"""Lösungs-Skelett — Übung 16.01 — TTC-Strategien-Vergleich auf dt. Mathe.

Smoke-Test-tauglich: keine echten API-Calls, keine GPU-Abhängigkeit. Stub-
Strategien zeigen das Vergleichs-Pattern. Vollversion mit Unsloth+TRL siehe
Lektionen 16.04 + 16.07.
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
        # 🎯 Lösung Übung 16.01 — TTC-Strategien-Vergleich

        Drei Strategien auf 50 Test-Aufgaben:

        1. **Self-Consistency N=8** auf Qwen2.5-Math-7B (Standard-Modell)
        2. **Eingebautes Reasoning** mit GPT-5.5 (effort=medium)
        3. **Eigenes GRPO-Mini** auf Qwen2.5-Math-1.5B + 100 Trainings-Aufgaben

        Smoke-Test-tauglich (Stub-Werte) — Reproduzierbarkeit über Manifest.
        """
    )
    return


@app.cell
def _():
    """Pydantic-Schemas."""
    from typing import Literal

    from pydantic import BaseModel, Field

    class Aufgabe(BaseModel):
        frage: str = Field(min_length=10, max_length=2000)
        loesung: str  # exakte Endlösung — für Verifier
        schwierigkeit: Literal["leicht", "mittel", "schwer"]

    class StrategieResult(BaseModel):
        strategie: str
        accuracy: float = Field(ge=0.0, le=1.0)
        avg_latenz_ms: int
        avg_tokens_pro_call: int
        eur_pro_50_aufgaben: float
        eur_einmalig_setup: float = 0.0
        warnungen: list[str] = []

    return Aufgabe, StrategieResult


@app.cell
def _(Aufgabe):
    """Stub-Test-Set — 5 Aufgaben für Smoke."""
    test_set = [
        Aufgabe(frage="Was ist 12 % von 3.700.000?", loesung="444000", schwierigkeit="leicht"),
        Aufgabe(
            frage="Wenn ein Auto 80 km/h fährt, wieviel km in 3:30 h?",
            loesung="280",
            schwierigkeit="leicht",
        ),
        Aufgabe(
            frage="Wenn ich 25.000 € auf 5 % p.a. anlege, wieviel nach 4 Jahren mit Zinseszins?",
            loesung="30387.66",
            schwierigkeit="mittel",
        ),
        Aufgabe(
            frage="Bei Brutto 4.500 € + Steuersatz 38 %, was ist netto?",
            loesung="2790",
            schwierigkeit="mittel",
        ),
        Aufgabe(
            frage="Lös: x² - 6x + 9 = 0",
            loesung="3",
            schwierigkeit="schwer",
        ),
    ]
    return (test_set,)


@app.cell
def _(StrategieResult, test_set):
    """Stub-Strategien — würden in der Vollversion echte API-Calls / GPU-Inferenz machen."""
    n_aufgaben = len(test_set)

    # Strategie 1: Self-Consistency N=8 auf Qwen2.5-Math-7B
    s1 = StrategieResult(
        strategie="Self-Consistency N=8 (Qwen2.5-Math-7B)",
        accuracy=0.74,
        avg_latenz_ms=8500,  # 8 calls parallel
        avg_tokens_pro_call=1800,  # 8 × 225 tokens
        eur_pro_50_aufgaben=0.45,  # 8× Standard-Cost
        warnungen=[
            "8× API-Cost vs. Single-Pass.",
            "Bei nicht-numerischen Tasks (Recht, Konversation) ungeeignet.",
        ],
    )

    # Strategie 2: GPT-5.5 effort=medium
    s2 = StrategieResult(
        strategie="GPT-5.5 (effort=medium)",
        accuracy=0.84,
        avg_latenz_ms=2800,
        avg_tokens_pro_call=900,  # ~ 700 reasoning + 200 visible
        eur_pro_50_aufgaben=0.85,  # höhere Per-Token-Cost
        warnungen=[
            "Reasoning-Tokens versteckt aber bezahlt.",
            "Drittland (US) — DSGVO-strict braucht alternative Anbieter.",
        ],
    )

    # Strategie 3: GRPO-Mini auf Qwen2.5-Math-1.5B (lokal RTX 4090)
    s3 = StrategieResult(
        strategie="GRPO-Mini auf Qwen2.5-Math-1.5B (lokal)",
        accuracy=0.66,
        avg_latenz_ms=1200,
        avg_tokens_pro_call=600,
        eur_pro_50_aufgaben=0.05,  # nur Strom-Anteil
        eur_einmalig_setup=14.40,  # 4 h × 3.60 € (RTX 4090 inkl. Storage)
        warnungen=[
            "Trainings-Setup-Cost bei kleiner Aufgabe nicht amortisiert.",
            "Bei OOD-Verteilung (AIME-DE) Drop-off möglich — Eval pflicht.",
        ],
    )

    return n_aufgaben, s1, s2, s3


@app.cell
def _(mo, n_aufgaben, s1, s2, s3):
    """Cost / Accuracy / Latenz - Vergleich."""
    rows = []
    for s in [s1, s2, s3]:
        rows.append(
            f"| **{s.strategie}** | {s.accuracy:.0%} | {s.avg_latenz_ms} ms | "
            f"{s.avg_tokens_pro_call} | € {s.eur_pro_50_aufgaben:.2f} | "
            f"€ {s.eur_einmalig_setup:.2f} |"
        )

    mo.md(
        f"## Drei-Strategien-Vergleich auf {n_aufgaben} Aufgaben (Stub-Werte)\n\n"
        "| Strategie | Accuracy | Avg Latenz | Tokens/Call | € pro 50 | Setup € |\n"
        "|---|---|---|---|---|---|\n" + "\n".join(rows)
    )
    return


@app.cell
def _(mo, s1, s2, s3):
    """Break-Even-Analyse."""
    # Bei wieviel Calls amortisiert sich GRPO-Setup gegenüber GPT-5.5?
    eur_diff_pro_50 = s2.eur_pro_50_aufgaben - s3.eur_pro_50_aufgaben
    break_even_aufgaben = s3.eur_einmalig_setup / max(eur_diff_pro_50 / 50, 0.001)

    mo.md(
        f"""
        ## Break-Even GRPO vs. GPT-5.5

        - GRPO-Setup-Cost: € {s3.eur_einmalig_setup:.2f}
        - GPT-5.5 spart pro 50 Aufgaben: keine — GRPO ist günstiger
        - Cost-Differenz pro Aufgabe: € {eur_diff_pro_50 / 50:.4f}
        - **Break-Even**: nach **{break_even_aufgaben:.0f}** Aufgaben hat sich GRPO-Training amortisiert

        > Bei < {break_even_aufgaben:.0f} Calls/Tag: API-Reasoning günstiger.
        > Bei mehr: lokales GRPO lohnt sich.

        ## Aber: Accuracy-Differenz beachten

        - GPT-5.5: {s2.accuracy:.0%}
        - GRPO: {s3.accuracy:.0%}
        - **Δ {(s2.accuracy - s3.accuracy) * 100:.0f} pp** — bei kritischen Tasks
          wichtiger als Cost.

        Self-Consistency bei {s1.accuracy:.0%} mit 8× Cost — selten besser
        als ein eingebautes Reasoning-Modell.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Reflexion (Pflicht in `BERICHT.md`)

        - **Cost vs. Accuracy**: GPT-5.5 mit eingebautem Reasoning hat das beste
          Verhältnis bei mittleren Volumina (< 1.000 Calls/Tag).
        - **Self-Consistency** ist bei 8× Cost selten konkurrenzfähig — das
          eingebaute Reasoning der o-Series / Extended Thinking schlägt es fast immer.
        - **GRPO-Mini lohnt sich** ab ~ 5.000 Calls/Tag oder bei DSGVO-strict-Anforderung.
        - **Verifier**: alle drei Strategien profitieren von einem objektiven
          Verifier — bei freitext-Tasks (Recht, Konversation) sind die Patterns
          alle weniger nützlich.

        ## Wie du das auf dein Profil anwendest

        1. Pass `test_set` mit deinen 50 Aufgaben an
        2. Bau die Stub-Strategien zu echten Calls aus (Lektionen 16.01 / 16.04 / 16.07)
        3. Cost-Werte aus deiner Modell-/GPU-Konstellation einsetzen
        4. Reflexion in BERICHT.md mit konkreten Zahlen aus deinen Runs

        ## Compliance-Anker

        - **AI-Act Art. 13 (Cost-Transparenz)**: alle Strategien dokumentieren € / Call
        - **AI-Act Art. 12 (Audit-Trail)**: GRPO-Manifest committet, Reasoning-Tokens geloggt
        - **AI-Act Art. 15 (Robustness)**: Verifier + OOD-Eval pflichtbewusst
        - **DSGVO Art. 44**: lokales GRPO-Modell = kein Drittland-Transfer

        ## Quellen

        - Self-Consistency-Paper — <https://arxiv.org/abs/2203.11171>
        - DeepSeek-Math (GRPO) — <https://arxiv.org/abs/2402.03300>
        - GPT-5.5 (24.04.2026) — <https://developers.openai.com/api/docs/models/gpt-5.5>
        - Anthropic Extended Thinking — <https://platform.claude.com/docs/en/build-with-claude/extended-thinking>
        - TRL GRPOTrainer — <https://huggingface.co/docs/trl/grpo_trainer>
        """
    )
    return


if __name__ == "__main__":
    app.run()
