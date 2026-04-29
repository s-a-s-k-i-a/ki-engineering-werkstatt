# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "marimo",
#   "pydantic>=2.9",
# ]
# ///

"""Lösungs-Skelett — Übung 09.01 — Long-Context vs. RAG vs. Hybrid.

Smoke-test-tauglich. Reine Pydantic-Logik.
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
        # 🎯 Lösung Übung 09.01 — Long-Context-Architektur-Entscheidung

        Drei Use-Cases → Long-Context vs. RAG vs. Hybrid.
        """
    )
    return


@app.cell
def _():
    """Pydantic-Profil-Schema."""
    from pydantic import BaseModel, Field

    class LongContextProfil(BaseModel):
        name: str
        tokens_pro_call: int = Field(ge=1_000, le=10_000_000)
        calls_pro_tag: int = Field(ge=1)
        wiederkehrend: bool
        latenz_budget_ms: int = Field(ge=100)
        dsgvo_sensibel: bool

    return (LongContextProfil,)


@app.cell
def _():
    """Architektur-Entscheidungs-Logik."""

    def empfehle_architektur(p) -> dict:
        if p.tokens_pro_call < 32_000:
            return {
                "architektur": "Standard-LLM (Phase 11)",
                "modell": "Claude Sonnet 4.6 / Mistral Large 3 / Pharia-1",
                "grund": "< 32k → Standard-LLM",
            }
        if p.wiederkehrend and p.calls_pro_tag > 10:
            return {
                "architektur": "RAG (Phase 13) mit Standard-LLM",
                "modell": "Mistral Large 3 oder Sonnet 4.6 + Qdrant",
                "grund": "wiederkehrend → RAG 30-100× günstiger als Long-Context",
            }
        if p.tokens_pro_call > 200_000:
            return {
                "architektur": "Hybrid-Modell (Mamba-Transformer)",
                "modell": "Jamba 1.5 (256k) oder Hunyuan-TurboS (256k)",
                "grund": "> 200k einmalig → Hybrid effizienter als Vanilla Transformer",
            }
        return {
            "architektur": "Long-Context-Transformer",
            "modell": "Claude Opus 4.7 (echte 200k) oder Mistral Large 3",
            "grund": "32k-200k einmalig → Long-Context",
        }

    def ruler_eval_pflicht(p) -> bool:
        return p.tokens_pro_call > 32_000

    def kosten_pro_monat(p) -> dict:
        a = empfehle_architektur(p)
        if a["architektur"].startswith("Standard"):
            cost_pro_call = p.tokens_pro_call / 1_000_000 * 1.0
        elif a["architektur"].startswith("RAG"):
            cost_pro_call = 5_000 / 1_000_000 * 1.0  # nur Top-5-Retrieval
        elif a["architektur"].startswith("Long-Context"):
            cost_pro_call = p.tokens_pro_call / 1_000_000 * 4.5  # Opus 4.7 / 1M Input
        else:  # Hybrid
            cost_pro_call = p.tokens_pro_call / 1_000_000 * 0.50  # Jamba self-hosted
        cost_pro_tag = cost_pro_call * p.calls_pro_tag
        return {
            "pro_call_eur": cost_pro_call,
            "pro_tag_eur": cost_pro_tag,
            "pro_monat_eur": cost_pro_tag * 30,
        }

    def dsgvo_pflichten(p) -> list[str]:
        a = empfehle_architektur(p)
        pflichten = []
        if p.dsgvo_sensibel and "DeepSeek" in a["modell"]:
            pflichten.append("⚠️ DeepSeek-V4-API (CN) → SCC + TIA + DPIA")
            pflichten.append("Alternative: Open-Weights-Self-Hosted auf EU-Server")
        if p.dsgvo_sensibel:
            pflichten.append("AVV mit Cloud-Anbieter (IONOS / OVH / Scaleway / STACKIT)")
            pflichten.append("DSFA falls Hochrisiko (Phase 20.03)")
        return pflichten

    return (
        dsgvo_pflichten,
        empfehle_architektur,
        kosten_pro_monat,
        ruler_eval_pflicht,
    )


@app.cell
def _(LongContextProfil):
    """Drei Use-Cases."""
    profile = [
        LongContextProfil(
            name="Bundestag-Protokoll-Analyse",
            tokens_pro_call=500_000,
            calls_pro_tag=2,
            wiederkehrend=False,
            latenz_budget_ms=10_000,
            dsgvo_sensibel=False,
        ),
        LongContextProfil(
            name="Vertrags-DB-Q&A (Kanzlei)",
            tokens_pro_call=60_000,
            calls_pro_tag=50,
            wiederkehrend=True,
            latenz_budget_ms=3_000,
            dsgvo_sensibel=True,
        ),
        LongContextProfil(
            name="Code-Repo-Assistent",
            tokens_pro_call=30_000,  # nicht ganzes Repo, RAG-Retrieval
            calls_pro_tag=300,  # 10 Devs × 30 Queries
            wiederkehrend=True,
            latenz_budget_ms=3_000,
            dsgvo_sensibel=False,
        ),
    ]
    return (profile,)


@app.cell
def _(
    dsgvo_pflichten,
    empfehle_architektur,
    kosten_pro_monat,
    mo,
    profile,
    ruler_eval_pflicht,
):
    """Detail pro Use-Case."""
    blocks = []
    for p in profile:
        a = empfehle_architektur(p)
        k = kosten_pro_monat(p)
        ruler = "✅ RULER-Eval-Pflicht" if ruler_eval_pflicht(p) else "—"
        pflichten = dsgvo_pflichten(p)
        pflichten_str = (
            "\n".join(f"  - {x}" for x in pflichten)
            if pflichten
            else "  - keine zusätzlichen DSGVO-Pflichten"
        )
        blocks.append(
            f"### {p.name}\n\n"
            f"- **Architektur**: {a['architektur']}\n"
            f"- **Modell**: {a['modell']}\n"
            f"- **Grund**: {a['grund']}\n"
            f"- **Kosten/Monat**: € {k['pro_monat_eur']:.0f}\n"
            f"- **Long-Context-Eval**: {ruler}\n"
            f"- **DSGVO-Pflichten**:\n{pflichten_str}\n"
        )
    mo.md("## Detail pro Use-Case\n\n" + "\n".join(blocks))
    return


@app.cell
def _(empfehle_architektur, profile, ruler_eval_pflicht):
    """Smoke-Test: 5 Akzeptanz-Asserts."""
    p_bundestag = profile[0]
    p_vertrag = profile[1]
    p_code = profile[2]

    # 1. Bundestag-Analyse → Long-Context oder Hybrid
    bun_arch = empfehle_architektur(p_bundestag)["architektur"]
    assert "Long-Context" in bun_arch or "Hybrid" in bun_arch

    # 2. Vertrags-DB-Q&A → RAG (wiederkehrend)
    vertrag_arch = empfehle_architektur(p_vertrag)["architektur"]
    assert "RAG" in vertrag_arch

    # 3. Code-Repo → RAG oder Standard-LLM (30k Tokens)
    code_arch = empfehle_architektur(p_code)["architektur"]
    assert "RAG" in code_arch or "Standard" in code_arch

    # 4. RULER-Pflicht für > 32k
    assert ruler_eval_pflicht(p_bundestag)
    assert ruler_eval_pflicht(p_vertrag)
    assert not ruler_eval_pflicht(p_code)  # 30k < 32k

    # 5. Bundestag-Modell ist Opus 4.7 oder Jamba (echte Long-Context)
    bun_modell = empfehle_architektur(p_bundestag)["modell"]
    assert "Opus" in bun_modell or "Jamba" in bun_modell or "Hunyuan" in bun_modell

    print("✅ Übung 09.01 — alle 5 Asserts grün")
    return


if __name__ == "__main__":
    app.run()
