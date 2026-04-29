# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "marimo",
#   "pydantic>=2.9",
# ]
# ///

"""Long-Context-Kalkulator — wann Long-Context vs. RAG vs. Standard-LLM.

Smoke-Test-tauglich. Effektive Context-Länge nach RULER (Stand 04/2026).
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
        # 📚 Long-Context-Kalkulator · Phase 09

        Empfiehlt Long-Context vs. RAG vs. Standard-LLM basierend auf:

        - Token-Volumen pro Call
        - Frequenz (einmalig vs. wiederkehrend)
        - Cost-Budget

        Stand: 29.04.2026.
        """
    )
    return


@app.cell
def _():
    """Pydantic-Schemas."""

    from pydantic import BaseModel, Field

    class LangContextModell(BaseModel):
        name: str
        behauptet_tokens: int
        effektiv_ruler_tokens: int
        cost_pro_1m_input_eur: float
        wann: str

    class UseCaseProfil(BaseModel):
        tokens_pro_call: int = Field(ge=1000, le=2_000_000)
        calls_pro_tag: int = Field(ge=1, le=100_000)
        wiederkehrend: bool

    return LangContextModell, UseCaseProfil


@app.cell
def _(LangContextModell):
    """Long-Context-Modell-Katalog Stand 29.04.2026."""
    katalog = [
        LangContextModell(
            name="Llama 3.3 70B",
            behauptet_tokens=128_000,
            effektiv_ruler_tokens=32_000,
            cost_pro_1m_input_eur=0.65,  # via OVHcloud
            wann="Marketing 128k, real ~ 32k",
        ),
        LangContextModell(
            name="Mistral Large 3",
            behauptet_tokens=128_000,
            effektiv_ruler_tokens=64_000,
            cost_pro_1m_input_eur=1.85,
            wann="solid bis ~ 64k",
        ),
        LangContextModell(
            name="Claude Opus 4.7",
            behauptet_tokens=200_000,
            effektiv_ruler_tokens=200_000,
            cost_pro_1m_input_eur=4.50,
            wann="real ~ 200k, Premium-Cost",
        ),
        LangContextModell(
            name="GPT-5.5",
            behauptet_tokens=256_000,
            effektiv_ruler_tokens=200_000,
            cost_pro_1m_input_eur=4.60,
            wann="real ~ 200k",
        ),
        LangContextModell(
            name="Jamba 1.5 Mini (Hybrid)",
            behauptet_tokens=256_000,
            effektiv_ruler_tokens=200_000,
            cost_pro_1m_input_eur=0.20,  # self-hosted Compute
            wann="Open-Weights-Hybrid, self-hosted",
        ),
        LangContextModell(
            name="Jamba 1.5 Large",
            behauptet_tokens=256_000,
            effektiv_ruler_tokens=200_000,
            cost_pro_1m_input_eur=0.50,
            wann="größere Variante",
        ),
        LangContextModell(
            name="DeepSeek-V4 (1M)",
            behauptet_tokens=1_000_000,
            effektiv_ruler_tokens=600_000,
            cost_pro_1m_input_eur=0.50,  # CN-API, DSGVO-problematisch
            wann="Mega-Context, ⚠️ CN-API",
        ),
    ]
    return (katalog,)


@app.cell
def _(katalog):
    """Empfehlungs-Logik."""

    def empfehle(profil: dict) -> dict:
        tokens = profil["tokens_pro_call"]
        wiederkehrend = profil["wiederkehrend"]

        # Entscheidung: RAG vs. Long-Context vs. Standard
        if tokens < 32_000:
            ansatz = "Standard-LLM (Phase 11)"
            modelle = ["Claude Sonnet 4.6", "GPT-5.5", "Pharia-1"]
        elif wiederkehrend:
            ansatz = "RAG (Phase 13) + Standard-LLM"
            modelle = ["Sonnet 4.6 + Qdrant", "Mistral Large 3 + RAG"]
        else:
            # Einmaliger Long-Doc — Long-Context-Modell
            passende = [m for m in katalog if m.effektiv_ruler_tokens >= tokens]
            passende.sort(key=lambda m: m.cost_pro_1m_input_eur)
            ansatz = "Long-Context-Modell"
            modelle = [m.name for m in passende[:3]] if passende else ["⚠️ keines passt"]

        # Cost-Schätzung pro Tag
        if ansatz.startswith("Standard"):
            cost_pro_tag = profil["calls_pro_tag"] * tokens / 1_000_000 * 1.0  # ~ 1 €/1M
        elif ansatz.startswith("RAG"):
            cost_pro_tag = profil["calls_pro_tag"] * 5_000 / 1_000_000 * 1.0  # nur Top-5-Retrieval
        else:
            best = next((m for m in katalog if m.name == modelle[0]), katalog[0])
            cost_pro_tag = profil["calls_pro_tag"] * tokens / 1_000_000 * best.cost_pro_1m_input_eur

        return {
            "ansatz": ansatz,
            "modelle": modelle,
            "cost_pro_tag_eur": cost_pro_tag,
            "cost_pro_monat_eur": cost_pro_tag * 30,
        }

    return (empfehle,)


@app.cell
def _(empfehle, mo):
    """Test-Profile."""
    profile = [
        {
            "name": "Standard-Chat (4k)",
            "tokens_pro_call": 4_000,
            "calls_pro_tag": 1_000,
            "wiederkehrend": True,
        },
        {
            "name": "Vertrags-DB (50 Verträge, oft abgefragt)",
            "tokens_pro_call": 60_000,
            "calls_pro_tag": 100,
            "wiederkehrend": True,
        },
        {
            "name": "Einmaliger 200-Seiten-Vertrag",
            "tokens_pro_call": 80_000,
            "calls_pro_tag": 5,
            "wiederkehrend": False,
        },
        {
            "name": "Bundestag-Protokoll-Mega-Doc",
            "tokens_pro_call": 500_000,
            "calls_pro_tag": 2,
            "wiederkehrend": False,
        },
        {
            "name": "RAG für Mandanten-Bot",
            "tokens_pro_call": 30_000,  # 30k Snippets aus 1M Korpus
            "calls_pro_tag": 500,
            "wiederkehrend": True,
        },
    ]

    rows_p = []
    for p in profile:
        e = empfehle(p)
        rows_p.append(
            f"| {p['name']} | {p['tokens_pro_call']:,} | "
            f"{p['calls_pro_tag']} | {e['ansatz']} | "
            f"{', '.join(e['modelle'][:2])} | € {e['cost_pro_monat_eur']:.0f}/Mo |"
        )

    mo.md(
        "## Use-Case-Empfehlungen\n\n"
        "| Profil | Tokens/Call | Calls/Tag | Ansatz | Top-2 | € pro Monat |\n"
        "|---|---|---|---|---|---|\n" + "\n".join(rows_p)
    )
    return


@app.cell
def _(katalog, mo):
    """Modell-Katalog mit RULER-Diff."""
    rows_kat = []
    for m in katalog:
        diff = m.behauptet_tokens - m.effektiv_ruler_tokens
        diff_pct = diff / m.behauptet_tokens * 100
        rows_kat.append(
            f"| **{m.name}** | {m.behauptet_tokens:,} | {m.effektiv_ruler_tokens:,} | "
            f"-{diff_pct:.0f} % | € {m.cost_pro_1m_input_eur:.2f} | {m.wann} |"
        )

    mo.md(
        "## Long-Context-Modell-Katalog (Stand 29.04.2026)\n\n"
        "| Modell | Behauptet | RULER-Effektiv | Diff | €/1M Input | Wann |\n"
        "|---|---|---|---|---|---|\n" + "\n".join(rows_kat)
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Faustregeln 2026

        - **< 32k Tokens**: Standard-LLM (Phase 11) — günstig, schnell
        - **32k–200k, wiederkehrend**: **RAG** (Phase 13) — 30–100× günstiger als Long-Context
        - **32k–200k, einmalig**: Long-Context-Modell (Jamba 1.5 / Opus 4.7)
        - **> 200k**: Hybrid-Modelle (Jamba) oder DeepSeek-V4 (mit DSGVO-Vorbehalt)

        ## Wichtige Hinweise

        - **Behauptete Context-Länge ≠ effektive** — RULER-Eval pflicht
        - **DeepSeek-V4 CN-API**: DSGVO-problematisch, nur lokale R1-Distill ok
        - **Cost-Realität**: Long-Context oft 30–100× teurer als RAG

        ## Quellen

        - NIAH — <https://github.com/gkamradt/LLMTest_NeedleInAHaystack>
        - RULER — <https://github.com/hsiehjackson/RULER>
        - Jamba 1.5 — <https://www.ai21.com/jamba/>
        - DeepSeek-V4 — <https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro>
        """
    )
    return


if __name__ == "__main__":
    app.run()
