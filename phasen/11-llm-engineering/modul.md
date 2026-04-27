---
id: 11
titel: LLM-Engineering — Pydantic AI, MCP, Anbieter-Vergleich mit EUR-Kosten
dauer_stunden: 14
schwierigkeit: mittel
stand: 2026-04-27
lernziele:
  - Production-reife LLM-Apps mit Type-Safety bauen (Pydantic AI)
  - Structured Outputs robust mit Validierung + Retry handhaben
  - MCP-Tools anbinden (Tool-Use, Function Calling)
  - Anbieter-Vergleich Aleph Alpha / Mistral / OpenAI / Anthropic / IONOS / DeepSeek / Qwen mit echten EUR-Token-Kosten
  - Caching, Eval (Promptfoo, Ragas), Observability (OpenTelemetry GenAI)
---

# LLM-Engineering

> Stop building production apps without types. — Pydantic AI macht LLM-Outputs zu validierten Schemata.

## Inhalts-Übersicht

| Lektion | Titel |
|---|---|
| 11.01 | Prompt-Patterns: Zero/Few-Shot, CoT, Self-Consistency |
| 11.02 | Structured Outputs mit Pydantic AI |
| 11.03 | Function Calling / Tool Use |
| 11.04 | MCP-Basics — USB-C der Agents (Phase 14 vertieft) |
| 11.05 | Anbieter-Vergleich mit echten EUR-Kosten |
| 11.06 | Asiatische Open-Weights (Qwen3, DeepSeek-R1) — mit DACH-Disclaimer |
| 11.07 | Caching: Anthropic Prompt-Cache, OpenAI Cached-Input, semantischer Cache |
| 11.08 | Eval mit Promptfoo (CI-tauglich) |
| 11.09 | Eval mit Ragas (Retrieval-Tasks) |
| 11.10 | Observability: OpenTelemetry GenAI + Phoenix/Langfuse (EU-self-hosted) |

## Anbieter-Vergleich Tabelle (Stand April 2026)

| Anbieter | Modell | Input EUR/1M Tok | Output EUR/1M Tok | DSGVO/AVV | Server EU |
|---|---|---|---|---|---|
| Aleph Alpha | Pharia-1-LLM-7B-control | ~5,00 | ~10,00 | ✓ | Heidelberg |
| Mistral | Mistral Large 2 | ~2,00 | ~6,00 | ✓ (FR) | Frankreich |
| OpenAI | GPT-5 | ~10,00 | ~30,00 | DPA, EU-Datazone | USA (EU-Routing optional) |
| Anthropic | Claude 4.7 Sonnet | ~2,80 | ~14,00 | DPA | USA (EU-Datazone Q1/26) |
| IONOS | Llama-4-Maverick | ~0,80 | ~1,60 | ✓ | Deutschland |
| StackIT | Teuken-7B | gehostet (Flatrate) | – | ✓ | Deutschland |
| DeepSeek (over EU host) | R1-Distill-70B | ~0,50 | ~1,50 | je nach Hoster | varies |
| Qwen (over EU host) | Qwen3-235B | ~0,40 | ~1,20 | je nach Hoster | varies |

## Status

🚧 Im Aufbau. Anbieter-Tabelle ist gepflegt, Lektionen folgen.
