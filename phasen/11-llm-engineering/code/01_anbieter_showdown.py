# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "marimo",
#   "rich>=13.9",
# ]
# ///

"""Anbieter-Showdown — vergleicht aktuelle LLM-Anbieter mit echten Pricing-Daten.

Smoke-Test-tauglich: nutzt eingebettete Pricing-Tabelle (Stand 28.04.2026)
und keine echten API-Calls. Für die produktive Version siehe Lektion 11.05.
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
        # 💸 Anbieter-Showdown · Phase 11

        Vergleich aktueller LLM-Anbieter mit echten USD/EUR-Pricing-Daten.
        **Stand: 28.04.2026** — bei produktivem Einsatz auf Anbieter-Seite re-verifizieren.

        Dieses Notebook zeigt:

        1. **Pricing-Tabelle** (USD pro 1M Tokens)
        2. **TCO-Rechner** für realen Use-Case (Newsletter-Beispiel)
        3. **Cache-Effekt-Berechnung** mit Anthropic-Multiplikatoren
        4. **EU-Cloud-Vergleich** (STACKIT, IONOS, OVHcloud, Scaleway)
        """
    )
    return


@app.cell
def _():
    """Pricing-Tabelle Stand 28.04.2026 (USD/1M Tokens)."""
    pricing = {
        # Anthropic
        "Claude Opus 4.7": {
            "anbieter": "Anthropic",
            "input": 5.00,
            "output": 25.00,
            "cache_read": 0.50,
            "land": "🇺🇸 US",
            "eu_avv": "DPA + EU-Datazone (+10%)",
        },
        "Claude Sonnet 4.6": {
            "anbieter": "Anthropic",
            "input": 3.00,
            "output": 15.00,
            "cache_read": 0.30,
            "land": "🇺🇸 US",
            "eu_avv": "DPA + EU-Datazone (+10%)",
        },
        "Claude Haiku 4.5": {
            "anbieter": "Anthropic",
            "input": 1.00,
            "output": 5.00,
            "cache_read": 0.10,
            "land": "🇺🇸 US",
            "eu_avv": "DPA + EU-Datazone (+10%)",
        },
        # OpenAI
        "GPT-5.5": {
            "anbieter": "OpenAI",
            "input": 5.00,
            "output": 30.00,
            "cache_read": 0.50,
            "land": "🇺🇸 US",
            "eu_avv": "DPA + EU-Region (+10%)",
        },
        "GPT-5.4": {
            "anbieter": "OpenAI",
            "input": 2.50,
            "output": 15.00,
            "cache_read": 0.25,
            "land": "🇺🇸 US",
            "eu_avv": "DPA + EU-Region (+10%)",
        },
        "GPT-5.4-mini": {
            "anbieter": "OpenAI",
            "input": 0.75,
            "output": 4.50,
            "cache_read": 0.075,
            "land": "🇺🇸 US",
            "eu_avv": "DPA + EU-Region (+10%)",
        },
        # Google
        "Gemini 3.1 Pro Preview": {
            "anbieter": "Google",
            "input": 2.00,
            "output": 12.00,
            "cache_read": 0.20,
            "land": "🇺🇸 US",
            "eu_avv": "DPA + EU-Region",
        },
        "Gemini 3 Flash Preview": {
            "anbieter": "Google",
            "input": 0.50,
            "output": 3.00,
            "cache_read": 0.05,
            "land": "🇺🇸 US",
            "eu_avv": "DPA + EU-Region",
        },
        # Mistral (FR — EU)
        "Mistral Large 3": {
            "anbieter": "Mistral",
            "input": 2.00,
            "output": 6.00,
            "cache_read": 0.20,
            "land": "🇫🇷 FR",
            "eu_avv": "AVV im Standard-Vertrag",
        },
        "Mistral Small 4": {
            "anbieter": "Mistral",
            "input": 0.20,
            "output": 0.60,
            "cache_read": 0.02,
            "land": "🇫🇷 FR",
            "eu_avv": "AVV im Standard-Vertrag",
        },
    }
    return (pricing,)


@app.cell
def _(mo, pricing):
    """Pricing-Tabelle als Markdown."""
    rows_pricing = []
    for modell_p, daten_p in pricing.items():
        rows_pricing.append(
            f"| **{modell_p}** | {daten_p['anbieter']} | {daten_p['land']} | "
            f"${daten_p['input']:.2f} | ${daten_p['output']:.2f} | "
            f"${daten_p['cache_read']:.2f} | {daten_p['eu_avv']} |"
        )
    table_pricing = (
        "| Modell | Anbieter | Land | Input | Output | Cache Read | DSGVO/AVV |\n"
        "|---|---|---|---|---|---|---|\n" + "\n".join(rows_pricing)
    )
    mo.md(f"### 1. Pricing-Tabelle (USD pro 1M Tokens)\n\n{table_pricing}")
    return (table_pricing,)


@app.cell
def _():
    """TCO-Rechner: Newsletter-Beispiel."""
    # 8000 Empfänger, 1x/Woche, 52 Wochen/Jahr
    n_empfaenger = 8_000
    versande_pro_jahr = 52
    system_prompt_tokens = 1_500
    user_prompt_tokens = 200
    output_tokens = 800

    n_calls = n_empfaenger * versande_pro_jahr
    input_pro_call = system_prompt_tokens + user_prompt_tokens
    total_input_tokens = n_calls * input_pro_call
    total_output_tokens = n_calls * output_tokens

    return (
        input_pro_call,
        n_calls,
        output_tokens,
        system_prompt_tokens,
        total_input_tokens,
        total_output_tokens,
    )


@app.cell
def _(mo, n_calls, pricing, total_input_tokens, total_output_tokens):
    """TCO ohne Caching, USD/Jahr."""
    rows_tco = []
    for modell_t, daten_t in pricing.items():
        in_kosten = total_input_tokens * daten_t["input"] / 1_000_000
        out_kosten = total_output_tokens * daten_t["output"] / 1_000_000
        gesamt_t = in_kosten + out_kosten
        rows_tco.append(
            f"| **{modell_t}** | ${in_kosten:>7.0f} | ${out_kosten:>7.0f} | **${gesamt_t:>7.0f}** | ~ €{gesamt_t * 0.93:.0f} |"
        )
    table_tco = (
        f"| Modell | Input ({total_input_tokens / 1_000_000:.0f}M Tokens) "
        f"| Output ({total_output_tokens / 1_000_000:.0f}M Tokens) "
        f"| Summe USD/Jahr | Summe EUR (~0,93×) |\n"
        "|---|---|---|---|---|\n" + "\n".join(rows_tco)
    )
    mo.md(
        f"### 2. TCO ohne Caching\n\n"
        f"**Use-Case**: 8.000 Empfänger × 52 Versände × ({1500 + 200} Input + 800 Output) Tokens"
        f" = **{n_calls:,} Calls/Jahr**\n\n{table_tco}\n\n"
        f"→ Faktor zwischen Premium (Opus 4.7) und günstig (Mistral Small 4): **~ 30 ×**"
    )
    return (table_tco,)


@app.cell
def _(mo, n_calls, pricing, system_prompt_tokens):
    """Cache-Effekt: stabiler System-Prompt → 1h-Cache.

    Anthropic-Multiplikatoren: 1h-Write = 2x Input, Read = 0.1x Input.
    """
    # Annahme: Cache wird einmal pro Stunde refreshed = 8.760 Refreshs/Jahr
    cache_refreshs = 8_760

    rows_cache = []
    for modell_c, daten_c in pricing.items():
        if daten_c["anbieter"] != "Anthropic":
            continue  # nur Anthropic für dieses Beispiel
        write_kosten = cache_refreshs * system_prompt_tokens * daten_c["input"] * 2 / 1_000_000
        read_kosten = n_calls * system_prompt_tokens * daten_c["cache_read"] / 1_000_000
        # Variabler Input bleibt voll bezahlt
        var_input_kosten = (n_calls * 200) * daten_c["input"] / 1_000_000
        # Output bleibt voll bezahlt
        out_kosten_c = (n_calls * 800) * daten_c["output"] / 1_000_000
        gesamt_c = write_kosten + read_kosten + var_input_kosten + out_kosten_c
        rows_cache.append(
            f"| **{modell_c}** | ${write_kosten:>5.0f} | ${read_kosten:>5.0f} | "
            f"${var_input_kosten:>5.0f} | ${out_kosten_c:>5.0f} | **${gesamt_c:>6.0f}** |"
        )
    table_cache = (
        "| Modell | Cache-Writes | Cache-Reads | Var-Input | Output | Σ USD/Jahr |\n"
        "|---|---|---|---|---|---|\n" + "\n".join(rows_cache)
    )
    mo.md(
        f"### 3. Cache-Effekt (1h-Cache, Anthropic-Modelle)\n\n"
        f"**Annahme**: System-Prompt ({system_prompt_tokens} Tokens) wird "
        f"1× pro Stunde refreshed = {cache_refreshs:,} Cache-Writes/Jahr.\n\n"
        f"{table_cache}\n\n"
        f"→ Caching spart ~ 25 % auf Sonnet 4.6, mehr bei stabileren Prompts."
    )
    return (table_cache,)


@app.cell
def _(mo):
    """EU-Cloud-Anbieter (Open-Weights gehostet)."""
    eu_cloud = {
        "STACKIT (DE)": {
            "modelle": "Llama 3.1 8B, Mistral Nemo",
            "in_eur": 0.45,
            "out_eur": 0.65,
            "avv": "Self-Service",
            "zertifikate": "BSI C5, ISO 27001",
        },
        "IONOS AI Model Hub (DE)": {
            "modelle": "Llama 3.1 8B/70B/405B, Mistral, Qwen3",
            "in_eur": 0.17,
            "out_eur": 1.93,
            "avv": "Self-Service",
            "zertifikate": "BSI C5, ISO 27001, ISO 50001, GAIA-X",
        },
        "OVHcloud AI Endpoints (FR)": {
            "modelle": "Llama 3.3 70B, Qwen3-32B, Mistral",
            "in_eur": 0.01,
            "out_eur": 0.67,
            "avv": "DPA-Anhang",
            "zertifikate": "ISO 27001, BSI C5, SecNumCloud (laufend)",
        },
        "Scaleway Generative APIs (FR)": {
            "modelle": "Qwen 3.5-397B, Llama 3.3-70B, Mistral Small 3.2",
            "in_eur": 0.15,
            "out_eur": 0.35,
            "avv": "Self-Service, **1M Free-Tier**",
            "zertifikate": "ISO 27001, HDS",
        },
    }

    rows_eu = []
    for anbieter_eu, daten_eu in eu_cloud.items():
        rows_eu.append(
            f"| **{anbieter_eu}** | {daten_eu['modelle']} | "
            f"€{daten_eu['in_eur']:.2f} | €{daten_eu['out_eur']:.2f} | "
            f"{daten_eu['avv']} | {daten_eu['zertifikate']} |"
        )

    table_eu = (
        "| Anbieter | Modelle | EUR Input | EUR Output | AVV | Zertifikate |\n"
        "|---|---|---|---|---|---|\n" + "\n".join(rows_eu)
    )

    mo.md(
        f"### 4. EU-Cloud-Anbieter (Open-Weights gehostet)\n\n{table_eu}\n\n"
        "→ EU-Hoster sparen den +10%-EU-Datenresidenz-Aufpreis der US-Anbieter "
        "und liefern AVV im Standard-Vertrag mit."
    )
    return eu_cloud, rows_eu, table_eu


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Was du in der Vollversion machst

        Mit **echten** API-Calls (statt Pricing-Tabelle):

        ```python
        from pydantic_ai import Agent
        from pydantic import BaseModel

        class Antwort(BaseModel):
            kurz: str
            tokens_input: int
            tokens_output: int

        # Identische Frage gegen alle Anbieter
        agents = {
            "Sonnet 4.6": Agent("anthropic:claude-sonnet-4-6", output_type=Antwort),
            "GPT-5.4-mini": Agent("openai:gpt-5-4-mini", output_type=Antwort),
            "Mistral Small 4": Agent("mistral:mistral-small-4", output_type=Antwort),
            "Qwen3-8B (lokal)": Agent("ollama:qwen3:8b", output_type=Antwort),
        }

        prompt = "Erkläre den AI Act in 2 Sätzen."
        for name, agent in agents.items():
            r = agent.run_sync(prompt)
            print(f"{name}: {r.output.kurz} ({r.usage().total_tokens} Tokens)")
        ```

        ### Quellen

        Alle Pricing-Werte aus offiziellen Anbieter-Pricing-Pages, Stand 28.04.2026.
        Vollständige Quellen-Liste in [`weiterfuehrend.md`](../weiterfuehrend.md).
        """
    )
    return


if __name__ == "__main__":
    app.run()
