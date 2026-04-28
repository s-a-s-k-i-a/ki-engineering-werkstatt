---
id: 11.05
titel: Anbieter-Vergleich mit echten Token-Kosten (April 2026)
phase: 11-llm-engineering
dauer_minuten: 90
schwierigkeit: mittel
stand: 2026-04-28
voraussetzungen: [11.02]
lernziele:
  - Aktuelle USD-Pricing-Tabellen aller großen LLM-Anbieter kennen
  - Total Cost of Ownership (TCO) für realen Use-Case berechnen
  - DSGVO-Aufpreis vs. EU-Hosting-Bonus einkalkulieren
  - Caching-Effekte richtig in TCO einbeziehen
compliance_anker:
  - eu-cloud-bevorzugen
  - kostenmonitoring-art-13
ai_act_artikel:
  - art-13
dsgvo_artikel:
  - art-28
  - art-44
---

## Worum es geht

> Stop comparing LLM-Anbieter at sticker price. — Tokenizer-Effizienz, Caching, EU-Hosting, AVV, Output-Verhältnis verschieben die echten Kosten oft um Faktor 3–10.

Wer LLM-Apps in Production betreibt, muss die Kosten **pro Anfrage** kennen, nicht nur pro 1M Tokens. Diese Lektion zeigt aktuelle Listenpreise (Stand 28.04.2026) und einen TCO-Rechner.

> ⚠️ **Wichtig**: Pricing ändert sich. Vor Produktiv-Entscheidung jedes Pricing auf der Anbieter-Seite re-verifizieren. Diese Tabelle ist **Stand 28.04.2026**.

## Voraussetzungen

- Lektion 11.02 (Pydantic AI) — für die Multi-Provider-Aufrufe
- Optional: Phase 05 (Tokenizer) — für deutsche Tokenisierungs-Effizienz

## Anbieter-Pricing (Stand 28.04.2026)

Alle Preise in **USD** pro 1 Mio. Tokens (sofern nicht anders angegeben). Wechselkurs USD/EUR im April 2026: ~ 0,93 (für Umrechnung).

### Anthropic (offizielle Pricing-Page)

| Modell | Input | Output | Cache 5min Write | Cache Read | Use-Case |
|---|---|---|---|---|---|
| **Claude Opus 4.7** | $5,00 | $25,00 | $6,25 | $0,50 | Frontier-Reasoning |
| Claude Opus 4.6 | $5,00 | $25,00 | $6,25 | $0,50 | Reasoning |
| **Claude Sonnet 4.6** | $3,00 | $15,00 | $3,75 | $0,30 | Standard-Workhorse |
| Claude Sonnet 4.5 | $3,00 | $15,00 | $3,75 | $0,30 | Standard |
| **Claude Haiku 4.5** | $1,00 | $5,00 | $1,25 | $0,10 | Schnell, günstig |

Cache-Multiplikatoren: 5min-Write = 1,25 ×, 1h-Write = 2 ×, **Read = 0,1 ×** Input-Preis. Batch-API = 50 % Rabatt. EU-Datenresidenz +10 % (`inference_geo`).

> ⚠️ Opus 4.7 nutzt einen neuen Tokenizer mit bis zu 35 % mehr Tokens pro Text. Sticker-Preis identisch zu 4.6, **echte** Kosten höher.

### OpenAI (Stand: aus Search-Snippets, vor Produktiv-Einsatz re-verifizieren)

| Modell | Input | Cached Input | Output | Use-Case |
|---|---|---|---|---|
| **GPT-5.5** | $5,00 | $0,50 | $30,00 | Frontier |
| **GPT-5.4** | $2,50 | $0,25 | $15,00 | Standard |
| **GPT-5.4-mini** | $0,75 | $0,075 | $4,50 | günstig |
| **GPT-5.4-nano** | $0,20 | $0,02 | $1,25 | sehr günstig |
| GPT-5.5-pro (o3-Reasoning) | $30,00 | n/a | $180,00 | Premium-Reasoning |

Caching: automatisch bei Prefix-Reuse ≥ 1.024 Tokens, ~ 10 % des Input-Preises. Batch = 50 % Rabatt. EU-Region +10 %.

### Google Gemini

| Modell | Input ≤ 200k | Cached | Output ≤ 200k | Use-Case |
|---|---|---|---|---|
| **Gemini 3.1 Pro Preview** | $2,00 | $0,20 | $12,00 | starkes Reasoning + Vision |
| **Gemini 3 Flash Preview** | $0,50 | $0,05 | $3,00 | schnell + günstig |

Batch-Tier = 50 % Rabatt.

### Mistral (vorbehaltlich Re-Verifikation)

| Modell | Input | Output | Use-Case |
|---|---|---|---|
| **Mistral Large 3** | $2,00 | $6,00 | Premium |
| **Mistral Medium 3.1** | $1,00 | $3,00 | Standard |
| **Mistral Small 4** | $0,20 | $0,60 | günstig |
| Codestral | $0,30 | $0,90 | Code-spezifisch |
| Ministral 8B | $0,10 | $0,10 | Edge / on-device |

Server: Frankreich (FR). DSGVO-konform mit AVV.

### EU-Cloud-Anbieter (Hosted Open-Weights)

| Anbieter | Modelle | EUR / 1M In | Server | AVV im Dashboard |
|---|---|---|---|---|
| **STACKIT** | Llama 3.1 8B, Mistral Nemo | ~ 0,45 € / 0,65 € (in/out) | Neckarsulm (DE) | ✅ |
| **IONOS AI Model Hub** | Llama, Mistral, Qwen3 | $ 0,17–1,93 / 1M | Karlsruhe (DE) | ✅ |
| **OVHcloud AI Endpoints** | Llama 3.3 70B, Qwen, Mistral | € 0,01–0,67 / 1M | Frankreich | ✅ |
| **Scaleway Generative APIs** | Qwen3, Llama 3.3, Mistral | € 0,15 / 0,35 (Mistral Small) | Paris (FR) | ✅ |

**1M Free-Tier** bei Scaleway, gut zum Testen.

### Aleph Alpha / Pharia

Enterprise-Pricing on Request. Keine öffentliche Token-Liste 2026 (nach Cohere-Übernahme im April 2026 unklar). Empfehlung: für Sovereign-Use-Cases direkt Vertrieb anschreiben.

## TCO-Rechnung — ein Newsletter-Beispiel

Ein KMU verschickt wöchentlich personalisierte Newsletter an **8.000 Empfänger:innen**:

- System-Prompt: 1.500 Tokens (gleich für alle)
- User-Daten: 200 Tokens (variabel pro Empfänger)
- Generierter Text: 800 Tokens Output

**Pro Empfänger:** 1.700 Input + 800 Output. Für 8.000 Empfänger pro Woche, 52 Wochen pro Jahr:

```text
Input/Jahr  = 8.000 × 1.700 × 52 = 707,2 Mio. Tokens
Output/Jahr = 8.000 × 800   × 52 = 332,8 Mio. Tokens
```

### Ohne Caching

| Anbieter | Modell | Input-Kosten | Output-Kosten | Summe USD/Jahr | Summe EUR/Jahr |
|---|---|---|---|---|---|
| Anthropic | Sonnet 4.6 | 707 × $3 = $2.121 | 333 × $15 = $4.995 | **$7.116** | ~ €6.620 |
| OpenAI | GPT-5.4 | 707 × $2,50 = $1.768 | 333 × $15 = $4.995 | **$6.763** | ~ €6.290 |
| OpenAI | GPT-5.4-mini | 707 × $0,75 = $530 | 333 × $4,50 = $1.498 | **$2.028** | ~ €1.886 |
| Google | Gemini 3 Flash | 707 × $0,50 = $354 | 333 × $3 = $999 | **$1.353** | ~ €1.258 |
| Mistral | Small 4 | 707 × $0,20 = $141 | 333 × $0,60 = $200 | **$341** | ~ €317 |
| Scaleway | Mistral Small (EU) | EUR-Preis 0,15/0,35 | | | **~ €222** |

### Mit Prefix-Cache (System-Prompt = 1.500 Tokens, identisch über alle Calls)

Anthropic Sonnet 4.6 mit 5min-Cache (1,25 × Write, 0,1 × Read):

- Erstmaliger Cache-Write: 1.500 × $3 × 1,25 = ~ $0,006 pro Cache-Refresh
- Read pro Call: 1.500 × $3 × 0,1 = $0,00045 statt $0,0045 → **$1.500-Ersparnis pro Jahr** auf der System-Prompt-Komponente.

Bei sehr stabilem Prompt (= Cache-Hit-Rate hoch) reduziert das die Anthropic-Rechnung um ~ 30–50 % auf der Input-Seite.

### EU-Aufpreis ist real

OpenAI / Anthropic mit EU-Datenresidenz: + 10 %. Für Newsletter mit Personenbezug: kein Verzicht möglich.

→ Bei niedrigem Volumen rechnet sich **EU-Cloud** (Scaleway, OVH, IONOS) oft besser, weil dort EU-Hosting im Standard-Preis enthalten ist.

## Mit Pydantic AI: Anbieter wechseln in 1 Zeile

```python
# Standard
agent = Agent("anthropic:claude-sonnet-4-6", output_type=...)

# Test günstigere Alternative
agent = Agent("openai:gpt-5-4-mini", output_type=...)

# EU-Hosted
agent = Agent(
    "openai:meta-llama/Llama-3.1-8B-Instruct",
    output_type=...,
    api_key=os.environ["IONOS_AI_API_KEY"],
    base_url="https://openai.inference.de-txl.ionos.com/v1",
)
```

→ Der Anbieter-Showdown im Notebook (siehe `code/01_anbieter_showdown.py`) zeigt dieselben 5 Test-Prompts gegen 5 Anbieter, mit Token-Anzahl + EUR-Kosten.

## Selbstcheck

- [ ] Du kennst die ungefähre USD-Reihenfolge der wichtigsten Modelle (Premium → günstig).
- [ ] Du erklärst, warum Output ~ 5 × teurer als Input ist (das gilt bei fast allen Anbietern).
- [ ] Du verstehst Cache-Hit-Rate und ihren TCO-Impact.
- [ ] Du wechselst Provider in einer Pydantic-AI-Zeile, ohne Geschäftslogik anzufassen.
- [ ] Du erkennst, dass EU-Aufpreis (+ 10 %) bei US-Anbietern manchmal teurer ist als ein Wechsel zu EU-Cloud.

## Compliance-Anker

- **Kostenmonitoring (AI-Act Art. 13)**: Hochrisiko-Systeme verlangen Kosten-Doku. LiteLLM-Proxy (Phase 17) bietet das out-of-the-box.
- **AVV-Pflicht (Art. 28 DSGVO)** bei jedem Cloud-Aufruf. Bei US-Anbietern zusätzlich SCC + TIA.
- **Caching und PII**: Wenn dein System-Prompt PII enthält (z. B. Mandanten-Namen), wird der Prompt **gecacht und u. U. an verschiedene User serviert**. Cache nur für **personen-unabhängige** Prefixes nutzen.

## Quellen

- Anthropic Pricing — <https://platform.claude.com/docs/en/about-claude/pricing> (Zugriff 2026-04-28)
- Anthropic Prompt Cache — <https://docs.claude.com/en/docs/build-with-claude/prompt-caching>
- OpenAI Pricing — <https://platform.openai.com/docs/pricing> (Zugriff 2026-04-28)
- OpenAI Prompt Caching — <https://platform.openai.com/docs/guides/prompt-caching>
- Google Gemini Pricing — <https://ai.google.dev/pricing>
- Mistral Pricing — <https://mistral.ai/pricing>
- STACKIT AI Model Serving — <https://stackit.com/en/products/data-ai/stackit-ai-model-serving>
- IONOS AI Model Hub — <https://cloud.ionos.com/managed/ai-model-hub>
- OVHcloud AI Endpoints — <https://www.ovhcloud.com/en/public-cloud/ai-endpoints/catalog/>
- Scaleway Generative APIs — <https://www.scaleway.com/en/generative-apis/>

## Weiterführend

→ **Hands-on**: Notebook [`code/01_anbieter_showdown.py`](../code/01_anbieter_showdown.py) (in dieser Phase) — direkter Vergleich
→ Lektion **11.07** (Caching) — wie du Prompt-Caching maximal ausnutzt
→ Lektion **11.10** (Observability) — wie du Kosten in Production trackst
→ Phase **17** (Production EU-Hosting) — LiteLLM-Proxy für Cost-Tracking + Provider-Switching
