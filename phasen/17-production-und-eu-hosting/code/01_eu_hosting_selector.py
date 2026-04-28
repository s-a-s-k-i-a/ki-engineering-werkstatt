# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "marimo",
#   "pydantic>=2.9",
# ]
# ///

"""EU-Hosting-Stack-Selector — empfiehlt Stack basierend auf Use-Case-Profil.

Smoke-Test-tauglich: keine externen API-Calls. Pricing-Daten Stand 28.04.2026
aus Anbieter-Pages (verifiziert in Lektion 17.04). Vor Produktiv-Einsatz im
Anbieter-Portal re-verifizieren — Pricing ist volatil.
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
        # 🧱 EU-Hosting-Stack-Selector · Phase 17

        Dieses Notebook hilft dir, den **richtigen EU-Cloud-Stack** für deinen
        Use-Case zu wählen — basierend auf:

        - **Token-Volumen / Monat**
        - **Latenz-Budget**
        - **Compliance-Tier** (Standard / BSI-C5-Type-2 / KRITIS)
        - **Modell-Klasse** (8B / 70B / 397B+)

        **Pricing-Stand**: 28.04.2026. Volatil — vor Produktiv-Einsatz im
        Anbieter-Portal re-verifizieren. Quellen pro Anbieter siehe Lektion 17.04.

        Smoke-Test-tauglich (keine externen API-Calls).
        """
    )
    return


@app.cell
def _():
    """Pydantic-Modelle: Anbieter, Profil, Empfehlung."""
    from typing import Literal

    from pydantic import BaseModel, Field

    class Anbieter(BaseModel):
        name: str
        rz_standort: str
        compliance: list[str]
        modelle: list[str]
        pricing_modus: Literal["managed_token", "iaas_gpu", "self_hosted_gguf"]
        eur_pro_1m_input: float | None = None
        eur_pro_1m_output: float | None = None
        verfuegbarkeit: Literal["managed_api", "managed_k8s", "iaas_gpu", "dedicated"]

    class UseCaseProfil(BaseModel):
        token_volumen_pro_monat: int = Field(ge=0)
        latenz_p95_ms: int = Field(ge=50, le=10_000)
        compliance_tier: Literal["standard", "bsi_c5", "bsi_c5_t2", "kritis"]
        modell_klasse: Literal["7-8b", "70b", "397b_plus", "egal"]
        budget_eur_pro_monat: float = Field(ge=0)

    class Empfehlung(BaseModel):
        anbieter: list[str]
        modus: str
        begruendung: str
        geschaetzte_kosten_eur: float
        compliance_match: bool
        warnungen: list[str]

    return Anbieter, Empfehlung, UseCaseProfil


@app.cell
def _(Anbieter):
    """Anbieter-Katalog (Stand 28.04.2026)."""
    katalog = [
        Anbieter(
            name="STACKIT AI Model Serving",
            rz_standort="Neckarsulm / Lübbenau (DE)",
            compliance=["BSI C5 Type 2", "ISO 27001", "ISAE 3000"],
            modelle=["Llama 3.1 8B", "Mistral Nemo", "E5 Mistral 7B (Embed)"],
            pricing_modus="managed_token",
            eur_pro_1m_input=0.45,
            eur_pro_1m_output=0.65,
            verfuegbarkeit="managed_api",
        ),
        Anbieter(
            name="STACKIT SKE + vLLM",
            rz_standort="Neckarsulm (DE)",
            compliance=["BSI C5 Type 2", "ISO 27001"],
            modelle=["Pharia-1-7B", "Llama 3.3 70B", "Custom"],
            pricing_modus="iaas_gpu",
            verfuegbarkeit="managed_k8s",
        ),
        Anbieter(
            name="IONOS AI Model Hub",
            rz_standort="Frankfurt / Karlsruhe / Berlin (DE)",
            compliance=["BSI C5", "ISO 27001", "GAIA-X", "EU-Cloud-CoC"],
            modelle=[
                "Llama 3.1 8B/70B/405B",
                "Mistral Nemo/Small",
                "Qwen3-Coder 80B",
                "gpt-oss-120b",
            ],
            pricing_modus="managed_token",
            eur_pro_1m_input=0.40,
            eur_pro_1m_output=1.20,
            verfuegbarkeit="managed_api",
        ),
        Anbieter(
            name="OVHcloud AI Endpoints",
            rz_standort="Roubaix / Limburg (FR/DE)",
            compliance=["ISO 27001", "BSI C5", "SecNumCloud (laufend)", "HDS"],
            modelle=[
                "Llama 3.3 70B",
                "Qwen3-32B",
                "Qwen3-Coder 30B",
                "Mistral Nemo",
                "gpt-oss-120b",
            ],
            pricing_modus="managed_token",
            eur_pro_1m_input=0.18,
            eur_pro_1m_output=0.67,
            verfuegbarkeit="managed_api",
        ),
        Anbieter(
            name="Scaleway Generative APIs",
            rz_standort="Paris (FR)",
            compliance=["ISO 27001", "HDS", "SecNumCloud (laufend)"],
            modelle=[
                "Mistral Small 4",
                "Llama 3.3 70B",
                "Qwen3.5-397B",
                "Pixtral-12B",
            ],
            pricing_modus="managed_token",
            eur_pro_1m_input=0.15,
            eur_pro_1m_output=0.35,
            verfuegbarkeit="managed_api",
        ),
        Anbieter(
            name="Hetzner GEX131 (dediziert)",
            rz_standort="Falkenstein / Nürnberg (DE)",
            compliance=["ISO 27001"],
            modelle=["beliebig (GGUF / vLLM lokal)"],
            pricing_modus="self_hosted_gguf",
            verfuegbarkeit="dedicated",
        ),
        Anbieter(
            name="Anthropic Claude (München-Office)",
            rz_standort="EU-Datazone (DPA)",
            compliance=["ISO 42001", "DPA", "EU-Datazone Enterprise"],
            modelle=["Claude Opus 4.7", "Sonnet 4.6", "Haiku 4.5"],
            pricing_modus="managed_token",
            eur_pro_1m_input=2.80,
            eur_pro_1m_output=14.00,
            verfuegbarkeit="managed_api",
        ),
        Anbieter(
            name="Mistral La Plateforme",
            rz_standort="Paris (FR)",
            compliance=["ISO 27001", "AVV im Standard"],
            modelle=["Mistral Large 3", "Medium 3.1", "Small 4"],
            pricing_modus="managed_token",
            eur_pro_1m_input=1.85,
            eur_pro_1m_output=5.55,
            verfuegbarkeit="managed_api",
        ),
    ]
    return (katalog,)


@app.cell
def _(Empfehlung, UseCaseProfil, katalog):
    """Empfehlungs-Logik."""

    def empfehle(profil: UseCaseProfil) -> Empfehlung:
        warnungen = []

        kandidaten = []
        for a in katalog:
            # Compliance-Filter
            if profil.compliance_tier == "bsi_c5_t2" and "BSI C5 Type 2" not in a.compliance:
                continue
            if profil.compliance_tier == "bsi_c5" and not any("BSI C5" in c for c in a.compliance):
                continue
            if profil.compliance_tier == "kritis" and "BSI C5 Type 2" not in a.compliance:
                continue

            # Modell-Klasse-Filter
            if (
                profil.modell_klasse == "70b"
                and not any("70" in m or "397" in m or "120" in m for m in a.modelle)
                and a.pricing_modus not in ("self_hosted_gguf", "iaas_gpu")
            ):
                continue
            if profil.modell_klasse == "397b_plus" and not any(
                "397" in m or "405" in m or "Opus" in m for m in a.modelle
            ):
                continue

            kandidaten.append(a)

        if not kandidaten:
            return Empfehlung(
                anbieter=[],
                modus="kein-match",
                begruendung="Kein Anbieter erfüllt deine Compliance + Modell-Anforderungen.",
                geschaetzte_kosten_eur=0,
                compliance_match=False,
                warnungen=["Compliance-Anforderung relaxen oder Modell-Klasse anpassen."],
            )

        # Token-Volumen → bevorzuge managed_token bei < 50M Tokens
        if profil.token_volumen_pro_monat < 50_000_000:
            preferred = [k for k in kandidaten if k.pricing_modus == "managed_token"]
        else:
            preferred = [k for k in kandidaten if k.pricing_modus == "iaas_gpu"]

        if not preferred:
            preferred = kandidaten

        # Sortiere nach Output-Pricing aufsteigend
        preferred_sorted = sorted(
            preferred,
            key=lambda x: x.eur_pro_1m_output or 999.0,
        )

        top3 = preferred_sorted[:3]

        # Kostenschätzung mit dem günstigsten
        guenstigster = top3[0]
        if guenstigster.eur_pro_1m_input is not None and guenstigster.eur_pro_1m_output is not None:
            # 70 % Input, 30 % Output (typisches Mittel)
            est_kosten = (
                profil.token_volumen_pro_monat * 0.7 / 1_000_000 * guenstigster.eur_pro_1m_input
                + profil.token_volumen_pro_monat * 0.3 / 1_000_000 * guenstigster.eur_pro_1m_output
            )
        else:
            est_kosten = -1  # Self-Hosted: monatliche GPU-Miete, separat

        if est_kosten > profil.budget_eur_pro_monat and est_kosten >= 0:
            warnungen.append(
                f"Geschätzte Kosten ({est_kosten:.0f} €) übersteigen Budget "
                f"({profil.budget_eur_pro_monat:.0f} €) — Cache-Strategie + "
                f"Routing-Disziplin nötig (Lektion 17.07, 17.10)."
            )

        if profil.modell_klasse == "70b" and profil.latenz_p95_ms < 500:
            warnungen.append(
                "70B-Klasse mit p95 < 500 ms ist anspruchsvoll — vLLM auf H100 + "
                "Prefix Caching nötig (Lektion 17.02)."
            )

        return Empfehlung(
            anbieter=[k.name for k in top3],
            modus=guenstigster.pricing_modus,
            begruendung=(
                f"Compliance-Tier {profil.compliance_tier} erfüllt von "
                f"{len(kandidaten)} Anbietern; nach Output-Pricing sortiert."
            ),
            geschaetzte_kosten_eur=max(est_kosten, 0),
            compliance_match=True,
            warnungen=warnungen,
        )

    return (empfehle,)


@app.cell
def _(UseCaseProfil, empfehle, mo):
    """Drei Beispiel-Profile durchspielen."""
    profile = [
        UseCaseProfil(
            token_volumen_pro_monat=2_000_000,
            latenz_p95_ms=2000,
            compliance_tier="standard",
            modell_klasse="7-8b",
            budget_eur_pro_monat=50.0,
        ),
        UseCaseProfil(
            token_volumen_pro_monat=20_000_000,
            latenz_p95_ms=1000,
            compliance_tier="bsi_c5",
            modell_klasse="70b",
            budget_eur_pro_monat=300.0,
        ),
        UseCaseProfil(
            token_volumen_pro_monat=80_000_000,
            latenz_p95_ms=500,
            compliance_tier="bsi_c5_t2",
            modell_klasse="70b",
            budget_eur_pro_monat=1500.0,
        ),
    ]

    rows = []
    for i, p in enumerate(profile, 1):
        e = empfehle(p)
        warn = " · ".join(e.warnungen) if e.warnungen else "—"
        rows.append(
            f"| {i} | {p.token_volumen_pro_monat:,} | {p.compliance_tier} | "
            f"{p.modell_klasse} | {', '.join(e.anbieter[:2])} | "
            f"{e.geschaetzte_kosten_eur:.0f} € | {warn[:60]} |"
        )

    mo.md(
        "## Beispiel-Profile + Empfehlungen\n\n"
        "| # | Tokens/Monat | Compliance | Modell | Top-2-Anbieter | Est. EUR | Warnungen |\n"
        "|---|---|---|---|---|---|---|\n" + "\n".join(rows)
    )
    return (profile,)


@app.cell
def _(katalog, mo):
    """Anbieter-Übersicht als Tabelle."""
    rows_kat = []
    for a in katalog:
        pricing = (
            f"€ {a.eur_pro_1m_input:.2f} / € {a.eur_pro_1m_output:.2f}"
            if a.eur_pro_1m_input is not None
            else "Self-Host"
        )
        comp = ", ".join(a.compliance[:2])
        modelle_kurz = ", ".join(a.modelle[:2])
        rows_kat.append(f"| **{a.name}** | {a.rz_standort} | {comp} | {modelle_kurz} | {pricing} |")

    mo.md(
        "## Anbieter-Katalog (Stand 28.04.2026)\n\n"
        "| Anbieter | RZ-Standort | Compliance | Modelle (Auswahl) | Input / Output €/1M |\n"
        "|---|---|---|---|---|\n" + "\n".join(rows_kat)
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Wie du das selbst nutzt

        Pass die `UseCaseProfil`-Werte in der Beispiel-Cell an dein eigenes Profil an:

        ```python
        mein_profil = UseCaseProfil(
            token_volumen_pro_monat=10_000_000,
            latenz_p95_ms=1500,
            compliance_tier="bsi_c5",
            modell_klasse="70b",
            budget_eur_pro_monat=200,
        )
        empfehlung = empfehle(mein_profil)
        ```

        ## Kosten-Realitäts-Check

        Diese Schätzung nimmt 70 % Input / 30 % Output an. Realistische
        Cache-Hit-Rate (Anthropic Prompt-Cache + Redis-Semantic) drückt die Kosten
        um weitere **40–60 %** — siehe Lektion 17.10.

        ## Compliance-Anker

        - **AVV (DSGVO Art. 28)**: vor Produktiv-Einsatz mit jedem Anbieter
          Self-Service-AVV signieren.
        - **Drittland (Art. 44)**: alle Anbieter im Katalog sind EU/EEA — kein
          Drittland-Transfer.
        - **NIS2** (operativ ab 04/2026): bei KRITIS-Use-Cases zusätzlich
          Incident-Runbook (Phase 17 `compliance.md`).

        ## Quellen

        - Pricing-Daten verifiziert in Lektion 17.04 mit URLs pro Anbieter.
        - Pricing volatil — vor Produktiv-Einsatz im Anbieter-Portal re-verifizieren.
        """
    )
    return


if __name__ == "__main__":
    app.run()
