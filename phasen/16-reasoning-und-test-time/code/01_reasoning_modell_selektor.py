# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "marimo",
#   "pydantic>=2.9",
# ]
# ///

"""Reasoning-Modell-Selektor — wählt Modell basierend auf Task-Profil + Cost.

Smoke-Test-tauglich: keine externen API-Calls. Pricing-Daten Stand 28.04.2026
(GPT-5.5, Opus 4.7, Sonnet 4.6, R1-Distill lokal). Vor Produktiv-Einsatz im
Anbieter-Portal re-verifizieren.
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
        # 🧠 Reasoning-Modell-Selektor · Phase 16

        Dieses Notebook hilft dir, das **richtige Reasoning-Modell** für deinen
        Use-Case zu wählen — basierend auf:

        - Task-Typ (Math / Code / Recht / Conversation)
        - Compliance-Tier (Standard / DSGVO-strict / KRITIS)
        - Volume (Calls/Tag)
        - Verifizierbarkeit (Verifier verfügbar?)

        Pricing Stand 28.04.2026.

        Smoke-Test-tauglich (keine API-Calls).
        """
    )
    return


@app.cell
def _():
    """Pydantic-Modelle: Modell, Profil, Empfehlung."""
    from typing import Literal

    from pydantic import BaseModel, Field

    class ReasoningModell(BaseModel):
        name: str
        anbieter: str
        modus: Literal["api", "self-hosted-eu", "lokal"]
        eur_pro_call_einfach: float
        eur_pro_call_komplex: float
        max_reasoning_tokens: int
        compliance_tier: Literal["standard", "dsgvo-strict", "lokal-only"]
        latenz_p50_ms_einfach: int
        latenz_p50_ms_komplex: int

    class TaskProfil(BaseModel):
        task_typ: Literal["math", "code", "recht", "conversation", "rag"]
        verifier_verfuegbar: bool
        compliance_tier: Literal["standard", "dsgvo-strict", "kritis", "lokal-only"]
        calls_pro_tag: int = Field(ge=1, le=1_000_000)
        latenz_budget_ms: int = Field(ge=100, le=60_000)

    class Empfehlung(BaseModel):
        empfehlung: list[str]
        begruendung: str
        geschaetzte_kosten_pro_tag_eur: float
        warnungen: list[str]

    return Empfehlung, ReasoningModell, TaskProfil


@app.cell
def _(ReasoningModell):
    """Modell-Katalog Stand 28.04.2026."""
    modelle = [
        ReasoningModell(
            name="GPT-5.5",
            anbieter="OpenAI",
            modus="api",
            eur_pro_call_einfach=0.0042,  # 500 input + 200 output (low effort)
            eur_pro_call_komplex=0.018,  # mit xhigh Reasoning-Tokens
            max_reasoning_tokens=20_000,
            compliance_tier="standard",
            latenz_p50_ms_einfach=800,
            latenz_p50_ms_komplex=4500,
        ),
        ReasoningModell(
            name="GPT-5.5 Pro",
            anbieter="OpenAI",
            modus="api",
            eur_pro_call_einfach=0.025,
            eur_pro_call_komplex=0.10,
            max_reasoning_tokens=40_000,
            compliance_tier="standard",
            latenz_p50_ms_einfach=2500,
            latenz_p50_ms_komplex=15_000,
        ),
        ReasoningModell(
            name="Claude Opus 4.7",
            anbieter="Anthropic München",
            modus="api",
            eur_pro_call_einfach=0.005,
            eur_pro_call_komplex=0.022,
            max_reasoning_tokens=64_000,
            compliance_tier="dsgvo-strict",
            latenz_p50_ms_einfach=900,
            latenz_p50_ms_komplex=5500,
        ),
        ReasoningModell(
            name="Claude Sonnet 4.6",
            anbieter="Anthropic München",
            modus="api",
            eur_pro_call_einfach=0.0028,
            eur_pro_call_komplex=0.011,
            max_reasoning_tokens=32_000,
            compliance_tier="dsgvo-strict",
            latenz_p50_ms_einfach=600,
            latenz_p50_ms_komplex=3000,
        ),
        ReasoningModell(
            name="DeepSeek-R1 (CN-API)",
            anbieter="DeepSeek",
            modus="api",
            eur_pro_call_einfach=0.0008,
            eur_pro_call_komplex=0.0035,
            max_reasoning_tokens=32_000,
            compliance_tier="standard",  # DSGVO-problematisch — nicht für strict
            latenz_p50_ms_einfach=700,
            latenz_p50_ms_komplex=4000,
        ),
        ReasoningModell(
            name="R1-Distill-Qwen-32B (lokal)",
            anbieter="self-hosted",
            modus="lokal",
            eur_pro_call_einfach=0.0,
            eur_pro_call_komplex=0.0,  # nur GPU-Strom
            max_reasoning_tokens=8_000,
            compliance_tier="lokal-only",
            latenz_p50_ms_einfach=2000,
            latenz_p50_ms_komplex=15_000,
        ),
        ReasoningModell(
            name="R1-Distill-Llama-70B (vLLM auf STACKIT)",
            anbieter="self-hosted-eu",
            modus="self-hosted-eu",
            eur_pro_call_einfach=0.0001,  # nur Compute-Anteil
            eur_pro_call_komplex=0.0008,
            max_reasoning_tokens=16_000,
            compliance_tier="dsgvo-strict",
            latenz_p50_ms_einfach=600,
            latenz_p50_ms_komplex=4500,
        ),
    ]
    return (modelle,)


@app.cell
def _(Empfehlung, modelle):
    """Empfehlungs-Logik."""

    def empfehle(profil: dict) -> Empfehlung:
        warnungen = []
        kandidaten = list(modelle)

        # Compliance-Filter
        if profil["compliance_tier"] in ("dsgvo-strict", "kritis"):
            kandidaten = [
                m for m in kandidaten if m.compliance_tier in ("dsgvo-strict", "lokal-only")
            ]
            if profil["compliance_tier"] == "kritis":
                kandidaten = [m for m in kandidaten if m.modus != "api"]
        if profil["compliance_tier"] == "lokal-only":
            kandidaten = [m for m in kandidaten if m.modus == "lokal"]

        # Latenz-Filter
        ist_komplex = profil["task_typ"] in ("math", "code", "recht")

        def latenz_check(m):
            return m.latenz_p50_ms_komplex if ist_komplex else m.latenz_p50_ms_einfach

        kandidaten = [m for m in kandidaten if latenz_check(m) <= profil["latenz_budget_ms"]]

        if not kandidaten:
            return Empfehlung(
                empfehlung=[],
                begruendung="Kein Modell erfüllt Compliance + Latenz.",
                geschaetzte_kosten_pro_tag_eur=0,
                warnungen=["Latenz-Budget oder Compliance relaxen."],
            )

        # Verifier-Bonus: bei verfügbarem Verifier kannst du günstigere Modelle mit
        # GRPO-Training nutzen (lokal R1-Distill)
        if profil["verifier_verfuegbar"] and any(m.modus == "lokal" for m in kandidaten):
            warnungen.append(
                "Verifier verfügbar: lokales R1-Distill mit GRPO-Training "
                "(Phase 16.07) kann produktiv günstiger sein als API."
            )

        # Sortiere nach Cost (komplex bei komplexen Tasks, einfach sonst)
        cost_field = "eur_pro_call_komplex" if ist_komplex else "eur_pro_call_einfach"
        sorted_kandidaten = sorted(kandidaten, key=lambda m: getattr(m, cost_field))

        top3 = sorted_kandidaten[:3]
        guenstigster = top3[0]
        cost_per_call = getattr(guenstigster, cost_field)
        cost_pro_tag = cost_per_call * profil["calls_pro_tag"]

        if profil["compliance_tier"] == "standard" and any(
            m.compliance_tier != "dsgvo-strict" for m in top3
        ):
            warnungen.append(
                "Compliance 'standard' lässt CN-APIs zu — bei DACH-Mittelstand "
                "tier 'dsgvo-strict' empfohlen (Anthropic München / EU-self-hosted)."
            )

        return Empfehlung(
            empfehlung=[m.name for m in top3],
            begruendung=(
                f"Compliance {profil['compliance_tier']} erfüllt von "
                f"{len(kandidaten)} Modellen, sortiert nach Cost (komplex={ist_komplex})."
            ),
            geschaetzte_kosten_pro_tag_eur=cost_pro_tag,
            warnungen=warnungen,
        )

    return (empfehle,)


@app.cell
def _(empfehle, mo):
    """Drei Test-Profile durchspielen."""
    profile = [
        {
            "name": "Math-Tutor (verifizierbar)",
            "task_typ": "math",
            "verifier_verfuegbar": True,
            "compliance_tier": "standard",
            "calls_pro_tag": 1000,
            "latenz_budget_ms": 8000,
        },
        {
            "name": "Recht-Auskunft (DSGVO-strict)",
            "task_typ": "recht",
            "verifier_verfuegbar": False,
            "compliance_tier": "dsgvo-strict",
            "calls_pro_tag": 500,
            "latenz_budget_ms": 6000,
        },
        {
            "name": "Code-Assistent intern (KRITIS)",
            "task_typ": "code",
            "verifier_verfuegbar": True,
            "compliance_tier": "kritis",
            "calls_pro_tag": 5000,
            "latenz_budget_ms": 5000,
        },
    ]

    rows_profile = []
    for p in profile:
        e = empfehle(p)
        warn_kurz = " · ".join(e.warnungen)[:50] if e.warnungen else "—"
        rows_profile.append(
            f"| {p['name']} | {p['compliance_tier']} | {p['calls_pro_tag']:,} | "
            f"{', '.join(e.empfehlung[:2])} | "
            f"€ {e.geschaetzte_kosten_pro_tag_eur:.2f}/Tag | {warn_kurz} |"
        )

    mo.md(
        "## Test-Profile + Empfehlungen\n\n"
        "| Profil | Compliance | Calls/Tag | Top-2-Modelle | Cost/Tag | Warnung |\n"
        "|---|---|---|---|---|---|\n" + "\n".join(rows_profile)
    )
    return


@app.cell
def _(mo, modelle):
    """Modell-Katalog anzeigen."""
    rows_kat = []
    for m in modelle:
        rows_kat.append(
            f"| **{m.name}** | {m.anbieter} | {m.modus} | "
            f"€ {m.eur_pro_call_einfach:.4f} | € {m.eur_pro_call_komplex:.4f} | "
            f"{m.max_reasoning_tokens:,} | {m.compliance_tier} |"
        )

    mo.md(
        "## Reasoning-Modell-Katalog (Stand 28.04.2026)\n\n"
        "| Modell | Anbieter | Modus | € einfach | € komplex | Max Reasoning Tokens | Compliance |\n"
        "|---|---|---|---|---|---|---|\n" + "\n".join(rows_kat)
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Wie du das nutzt

        1. Pass `profile` mit deinen Werten an
        2. Schau auf Top-3-Modelle und Cost
        3. Verifier-Bonus prüfen — eigenes R1-Distill mit GRPO oft günstiger als API

        ## Annahmen + Limitierungen

        - Pricing volatil — vor Produktiv-Einsatz im Anbieter-Portal re-verifizieren
        - Cost-per-Call basiert auf 500-Token-Input + 200-Token-Output
        - Latenz-Werte sind p50, real ± 30 %

        ## Compliance-Anker

        - **DSGVO Art. 44**: 'kritis'-Tier filtert API-Modelle aus
        - **AI-Act Art. 13 (Cost-Transparenz)**: Cost/Tag-Schätzung als Pre-Production-Hinweis
        - **AI-Act Art. 15**: Verifier-verfügbar = höhere Robustheit-Anforderung erfüllbar

        ## Quellen

        - GPT-5.5 Pricing — <https://openai.com/index/introducing-gpt-5-5/>
        - Anthropic Pricing — <https://platform.claude.com/docs/en/build-with-claude/pricing>
        - DeepSeek Pricing — <https://api-docs.deepseek.com/quick_start/pricing>
        - R1-Distill HF — <https://huggingface.co/deepseek-ai>
        """
    )
    return


if __name__ == "__main__":
    app.run()
