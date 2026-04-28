# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "marimo",
#   "pydantic>=2.9",
# ]
# ///

"""Lösungs-Skelett — Übung 17.01 — Production-Stack-Architektur (Profil A: Bürger-Service-Bot).

Dieses Notebook ist eine Vorlage. Bau drumherum dein BERICHT.md, deine
docker-compose.yml und deine litellm-config.yaml. Smoke-Test-tauglich (keine
externen API-Calls). Echte Werte trägst du über die `MeinProfil`-Cell ein.
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
        # 🎯 Lösung Übung 17.01 — Stack-Architektur (Beispiel: Profil A — Bürger-Service-Bot)

        Du erstellst:

        1. Ein `UseCaseProfil` mit deinen Werten
        2. Eine `Empfehlung` aus dem Selector (`code/01_eu_hosting_selector.py`)
        3. Ein TCO-Modell mit Cache-Hit-Rate-Sensitivität
        4. Eine Compliance-Checkliste mit Status

        Smoke-Test-tauglich: keine API-Calls, keine externen Daten.
        """
    )
    return


@app.cell
def _():
    """Profil A — Bürger-Service-Bot (Beispiel)."""
    from typing import Literal

    from pydantic import BaseModel, Field

    class UseCaseProfil(BaseModel):
        projekt_name: str
        token_volumen_pro_monat: int = Field(ge=0)
        cache_hit_rate_erwartet: float = Field(ge=0.0, le=1.0)
        latenz_p95_ms: int = Field(ge=50, le=10_000)
        compliance_tier: Literal["standard", "bsi_c5", "bsi_c5_t2", "kritis"]
        modell_klasse: Literal["7-8b", "70b", "397b_plus"]
        budget_eur_pro_monat: float = Field(ge=0)
        avv_signiert: list[str]
        dsfa_status: Literal["fehlt", "in_arbeit", "abgeschlossen"]
        ai_act_klasse: Literal["minimal", "begrenzt", "hoch", "unzulaessig"]

    profil = UseCaseProfil(
        projekt_name="Bürger-Service-Bot Stadtverwaltung",
        token_volumen_pro_monat=15_000_000,
        cache_hit_rate_erwartet=0.55,
        latenz_p95_ms=1500,
        compliance_tier="bsi_c5_t2",
        modell_klasse="7-8b",
        budget_eur_pro_monat=250.0,
        avv_signiert=["STACKIT", "Anthropic Enterprise", "Langfuse"],
        dsfa_status="in_arbeit",
        ai_act_klasse="begrenzt",
    )

    return UseCaseProfil, profil


@app.cell
def _(profil):
    """Architektur-Entscheidung: STACKIT AI Model Serving + Anthropic Sonnet 4.6 als Premium-Tier."""

    architektur = {
        "default": {
            "anbieter": "STACKIT AI Model Serving",
            "modell": "Mistral Nemo 12B (Llama-3.1-8B als Backup)",
            "rz_standort": "Neckarsulm (DE)",
            "compliance": "BSI C5 Type 2",
            "input_eur_1m": 0.45,
            "output_eur_1m": 0.65,
            "begruendung": "BSI C5 Type 2 ist für öffentliche Hand Pflicht. STACKIT ist der einzige Anbieter mit Type 2 explizit.",
        },
        "premium": {
            "anbieter": "Anthropic Claude Sonnet 4.6",
            "modell": "claude-sonnet-4-6",
            "rz_standort": "EU-Datazone (München-Office)",
            "compliance": "ISO 42001 + DPA",
            "input_eur_1m": 2.80,
            "output_eur_1m": 14.00,
            "cache_read_rabatt": 0.90,
            "begruendung": "Für komplexe Bürger-Anfragen (Multi-Hop, Recht). Anthropic München-Office + EU-Datazone = ausreichende DSGVO-Beleglage.",
        },
        "fallback": {
            "anbieter": "Mistral Large 3",
            "modell": "mistral-large-3",
            "rz_standort": "Paris (FR)",
            "compliance": "ISO 27001",
            "input_eur_1m": 1.85,
            "output_eur_1m": 5.55,
            "begruendung": "Reine EU-Anbieter-Backbone bei Anthropic-Outage.",
        },
    }
    return (architektur,)


@app.cell
def _(architektur, mo, profil):
    """TCO-Modell mit Sensitivität auf Cache-Hit-Rate."""

    def schaetze_kosten(volumen_total: int, cache_rate: float, mix_default: float = 0.7) -> dict:
        """Mix: 70 % Default-Tier, 25 % Premium, 5 % Fallback."""
        cache_savings = (
            cache_rate * 0.5
        )  # ~50 % Ersparnis-Effekt durch Cache (gemittelt über Schichten)

        # 70 % via STACKIT
        v_default = volumen_total * mix_default
        eur_default = (
            v_default * 0.7 / 1_000_000 * architektur["default"]["input_eur_1m"]
            + v_default * 0.3 / 1_000_000 * architektur["default"]["output_eur_1m"]
        ) * (1 - cache_savings)

        # 25 % via Anthropic Premium
        v_premium = volumen_total * 0.25
        eur_premium = (
            v_premium * 0.7 / 1_000_000 * architektur["premium"]["input_eur_1m"]
            + v_premium * 0.3 / 1_000_000 * architektur["premium"]["output_eur_1m"]
        ) * (1 - cache_savings)

        # 5 % Fallback Mistral
        v_fallback = volumen_total * 0.05
        eur_fallback = (
            v_fallback * 0.7 / 1_000_000 * architektur["fallback"]["input_eur_1m"]
            + v_fallback * 0.3 / 1_000_000 * architektur["fallback"]["output_eur_1m"]
        ) * (1 - cache_savings)

        return {
            "default": eur_default,
            "premium": eur_premium,
            "fallback": eur_fallback,
            "total": eur_default + eur_premium + eur_fallback,
        }

    sensitivitaet = []
    for cache_rate in [0.30, 0.40, 0.55, 0.70]:
        k = schaetze_kosten(profil.token_volumen_pro_monat, cache_rate)
        within_budget = "✅" if k["total"] <= profil.budget_eur_pro_monat else "⚠️"
        sensitivitaet.append(
            f"| {cache_rate * 100:.0f} % | "
            f"{k['default']:.1f} | {k['premium']:.1f} | "
            f"{k['fallback']:.1f} | **{k['total']:.1f}** | {within_budget} |"
        )

    mo.md(
        f"## TCO-Sensitivität (Profil: {profil.projekt_name})\n\n"
        f"Token-Volumen: {profil.token_volumen_pro_monat:,} / Monat. "
        f"Mix: 70 % Default / 25 % Premium / 5 % Fallback. Budget: "
        f"**{profil.budget_eur_pro_monat:.0f} €/Monat**.\n\n"
        "| Cache-Hit-Rate | Default (€) | Premium (€) | Fallback (€) | Total (€) | Budget? |\n"
        "|---|---|---|---|---|---|\n" + "\n".join(sensitivitaet)
    )
    return (schaetze_kosten,)


@app.cell
def _(architektur, mo):
    """Architektur-Diagramm + Routing-Logik."""

    rows_arch = []
    for tier, info in architektur.items():
        cache_info = (
            f"-{info.get('cache_read_rabatt', 0) * 100:.0f}%"
            if info.get("cache_read_rabatt")
            else "—"
        )
        rows_arch.append(
            f"| **{tier}** | {info['anbieter']} | {info['modell']} | "
            f"{info['rz_standort']} | {info['compliance']} | "
            f"€ {info['input_eur_1m']:.2f} / € {info['output_eur_1m']:.2f} | "
            f"{cache_info} |"
        )

    mo.md(
        "## Architektur — Drei Tiers\n\n"
        "| Tier | Anbieter | Modell | RZ-Standort | Compliance | Input/Output €/1M | Cache-Read |\n"
        "|---|---|---|---|---|---|---|\n" + "\n".join(rows_arch)
    )
    return


@app.cell
def _(mo, profil):
    """Compliance-Checkliste mit Status."""
    checkliste = [
        ("AVV STACKIT signiert", "STACKIT" in profil.avv_signiert),
        ("AVV Anthropic Enterprise", "Anthropic Enterprise" in profil.avv_signiert),
        ("AVV Langfuse DPA", "Langfuse" in profil.avv_signiert),
        ("DSFA durchgeführt", profil.dsfa_status == "abgeschlossen"),
        (
            "AI-Act-Klassifizierung dokumentiert",
            profil.ai_act_klasse in ("begrenzt", "minimal", "hoch"),
        ),
        ("PII-Filter im OTel-Span-Processor", False),  # Pattern: zu implementieren
        ("Pseudonymisierung User-IDs", False),
        ("Audit-Aufbewahrung ≥ 6 Monate", False),
        ("Cost-Caps pro Mandant aktiv", False),
        ("NIS2-Incident-Runbook (KRITIS)", False),
        ("Backup-Pipeline Postgres", False),
        ("gitleaks + trufflehog in CI", False),
    ]

    rows_chk = []
    erledigt = 0
    for name, ok in checkliste:
        marker = "✅" if ok else "⏳"
        if ok:
            erledigt += 1
        rows_chk.append(f"| {marker} | {name} |")

    mo.md(
        f"## Compliance-Checkliste — {erledigt}/{len(checkliste)} erledigt\n\n"
        "| Status | Pflicht-Punkt |\n|---|---|\n" + "\n".join(rows_chk)
    )
    return (checkliste,)


@app.cell
def _(mo):
    """LiteLLM-Config-Vorlage."""
    litellm_config = """model_list:
  - model_name: "default"
    litellm_params:
      model: "openai/mistral-nemo-12b"
      api_base: "https://api.stackit.cloud/ai-model-serving/v1"
      api_key: os.environ/STACKIT_API_KEY
    metadata:
      eu_compliant: true
      bsi_c5_type_2: true
      rz_standort: "Neckarsulm"

  - model_name: "premium"
    litellm_params:
      model: "anthropic/claude-sonnet-4-6"
      api_key: os.environ/ANTHROPIC_API_KEY
    metadata:
      eu_compliant: true
      provider_office: "München"

  - model_name: "fallback"
    litellm_params:
      model: "mistral/mistral-large-3"
      api_key: os.environ/MISTRAL_API_KEY
    metadata:
      eu_compliant: true
      rz_standort: "Paris"

router_settings:
  routing_strategy: "simple-shuffle"
  fallbacks:
    - "default": ["premium", "fallback"]
    - "premium": ["fallback"]
    - "fallback": ["default"]
  num_retries: 2
  timeout: 30

litellm_settings:
  cache: true
  cache_params:
    type: "redis-semantic"
    similarity_threshold: 0.92
    embedding_model: "openai/text-embedding-3-small"
    host: "redis"
    port: 6379
    ttl: 3600
  success_callback: ["langfuse"]
  failure_callback: ["langfuse", "slack"]
  drop_params: true

general_settings:
  master_key: os.environ/LITELLM_MASTER_KEY
  database_url: os.environ/DATABASE_URL
  global_max_parallel_requests: 100
  alerting: ["slack"]
"""

    mo.md(f"## `litellm-config.yaml` (Vorlage)\n\n```yaml\n{litellm_config}```")
    return (litellm_config,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Reflexion — drei Sätze

        - **Schwierigste Architektur-Entscheidung**: BSI C5 Type 2 schließt 4 von 8 Anbietern aus. STACKIT ist faktisch alternativlos für die öffentliche Hand 2026.
        - **Compliance-Stolperfalle**: DSFA für „rein automatisierte Entscheidung" (DSGVO Art. 22) ist beim Bürger-Service-Bot relevant — Mitarbeiter-Approval-Schritt für kritische Auskünfte (Recht, Bauantrag) ist Pflicht.
        - **Skalierung 5×**: bei 75M Tokens/Monat würde ich vom managed AI Model Serving zur eigenen STACKIT-SKE-vLLM-Instance wechseln (Lektion 17.11), spart bei Volumen ab ~ 50M Tokens.

        ## Wie du das auf dein Profil anwendest

        1. Pass `UseCaseProfil` mit deinen Werten an
        2. Lass die `architektur`-Cell die drei Tiers automatisch ableiten (oder manuell)
        3. Nutze `schaetze_kosten` für deine TCO-Sensitivität
        4. Hak die `checkliste` mit deinem Status ab
        5. Bau `BERICHT.md` mit den vier Tabellen + 3-Satz-Reflexion

        ## Compliance-Anker (Quervweis)

        - **Phase 20.01** — AI-Act-Risikoklassifizierung
        - **Phase 20.03** — DSFA-Workflow
        - **Phase 20.05** — Audit-Logging-Pattern
        - **Lektion 17.11** — Hands-on Pharia-1 auf STACKIT mit voller Compliance-Verifikation
        """
    )
    return


if __name__ == "__main__":
    app.run()
