---
id: 9
phase: 09-state-space-und-hybride
stand: 2026-04-27
anker:
  - hunyuan-china-disclaimer
  - energieeffizienz-art-13
  - jamba-license
dsgvo_artikel:
  - art-44
ai_act_artikel:
  - art-13
---

# Compliance-Anker — Phase 09

## Hunyuan-TurboS (Tencent, China)

Open Weights, technisch beeindruckend (560B/56B aktiv, 256K Context, Mamba-Hybrid). Aber:

> **⚠️ DACH-Compliance**: lokale Inferenz auf EU-Hardware = ok; offizielle Tencent-Cloud-API = DSGVO-problematisch; Self-Censorship-Risiko bei sensiblen Themen identisch zu DeepSeek/Qwen.

Siehe `docs/rechtliche-perspektive/asiatische-llms.md`.

## Jamba (AI21 Labs, Israel)

Lizenz: **Jamba Open Model License** — eigene Bedingungen, nicht Apache/MIT. Vor produktiver Nutzung Lizenz prüfen.

## Energieeffizienz-Argument (Art. 13)

Mamba/Hybrid-Modelle haben besseres Throughput-pro-Watt. Für Hochrisiko-Systeme nach AI-Act Art. 13: dokumentierter geringerer Energieverbrauch ist Compliance-Plus.

## Quellen

- [Mamba Paper](https://arxiv.org/abs/2312.00752)
- [Jamba Tech Report](https://arxiv.org/abs/2403.19887)
- [Hunyuan-TurboS Paper](https://arxiv.org/abs/2503.05447)
