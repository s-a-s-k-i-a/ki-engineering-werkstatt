# Asiatische LLMs aus DACH-Compliance-Sicht

> 2026 findet ein erheblicher Teil der LLM-Innovation in Asien statt. Wer das ignoriert, verpasst aktuelle State-of-the-Art-Modelle. Wer es naiv nutzt, riskiert DSGVO- und Sicherheits-Probleme. Hier der Mittelweg.

**Stand: 2026-04-27.** Modelle entwickeln sich rasant, Lizenzen ändern sich.

## Top-7 für DACH-Curricula

| Familie | Anbieter | Land | Lizenz | Stärken | DACH-Compliance-Risiko |
|---|---|---|---|---|---|
| **Qwen3** | Alibaba | CN | **Apache 2.0** | 119 Sprachen, Hybrid-Reasoning, VL/Omni | mittel-hoch + Self-Censorship |
| **DeepSeek-R1** | DeepSeek | CN | **MIT** | GRPO-Referenz, Reasoning, Nature-publiziert | hoch + 88 % Self-Censorship |
| **DeepSeek V4** | DeepSeek | CN | custom | „GPT-5.4-Niveau" Coding | hoch (Lizenz prüfen!) |
| **GLM-5** | Zhipu AI | CN | **MIT** | SOTA Coding 02/2026 | mittel-hoch |
| **Kimi K2.6** | Moonshot AI | CN | Modified MIT | 256K Context, Agent-Swarm 300 Subagenten | mittel-hoch |
| **MiniCPM-o / V** | OpenBMB | CN | Apache 2.0 | Edge-Multimodal (Phone-tauglich) | niedrig-mittel |
| **EXAONE 4.5** | LG AI Research | KR | EXAONE 1.2-NC ⚠️ | STEM-Avg. 77.3, multimodal | niedrig (Lizenz: nicht kommerziell) |

Zusätzlich erwähnt: **AI21 Jamba** (IL, Hybrid-Architektur), **Hunyuan-TurboS** (CN, Mamba-Hybrid 560B), **SEA-LION** (Singapur, Apache 2.0).

## Drei Compliance-Schichten

### 1. Lokale Inferenz auf eigener/EU-Hardware

> ✅ DSGVO-vertraeglich. Modell-Weights sind Mathematik, kein Datentransfer.

- Ollama, llama.cpp, vLLM, MLX
- Cloud auf EU-Servern (Nebius, Scaleway, OVH AI Endpoints, IONOS, StackIT)

### 2. Offizielle CN-API

> ❌ DSGVO-problematisch.

- DeepSeek API (`api.deepseek.com`)
- Alibaba Dashscope (`dashscope.aliyun.com`)
- Moonshot Kimi (`api.moonshot.cn`)
- Zhipu (`open.bigmodel.cn`)

Probleme:

- Kein EU-Vertreter
- Kein durchsetzbarer Auskunfts-/Löschanspruch
- Datentransfer in Drittland ohne adequacy decision
- **Präzedenz**: TikTok 530 Mio. EUR Bußgeld 2025

### 3. Drittanbieter-Hoster

> 🟡 Hoster-Standort entscheidet.

- **EU-Region** (Nebius, Scaleway, Mistral La Plateforme, OVH AI): DSGVO-konform
- **US-Provider** (Together, Fireworks, DeepInfra): SCC + TIA + Zero-Retention nötig

## Self-Censorship-Bedenken

Die wichtigste DACH-Frage: **Trainings-Bias**.

### Was wurde gemessen?

- DeepSeek-Chat zensiert ~88 % geopolitischer CN-Fragen
- Tiananmen 1989: real-time Antwort-Löschung sichtbar
- Taiwan: Aussagen sind nicht historisch faktentreu („untrennbar Teil Chinas")
- Xi Jinping: kritische Aussagen werden umgeschrieben oder verweigert

### Was bedeutet das für deinen Use-Case?

| Use-Case | Self-Censorship-Risiko | Empfehlung |
|---|---|---|
| **B2B-Coding** | gering | ok mit Pflicht-Eval |
| **Mathematik / Formeln** | gering | ok |
| **Allgemeine Fakten** | mittel | Eval auf historisch-politische Fragen |
| **News / Politik** | sehr hoch | **nicht** ohne weitere Modelle |
| **Geschichte** | sehr hoch | **nicht** ohne weitere Modelle |
| **Journalismus** | inakzeptabel | nicht einsetzen |
| **Bildung** | hoch | nur mit Mehrmodell-Verifikation |

## Pflicht-Eval-Pipeline

Wenn du ein chinesisches Modell einsetzt: führe `phasen/18-ethik-safety-alignment` Self-Censorship-Audit durch:

1. 50 deutsche Prompts in 5 Kategorien (Tiananmen, Taiwan, Xinjiang, Xi, Hongkong)
2. Modell antworten lassen
3. Zensur-Rate pro Kategorie ausweisen
4. Vergleich mit Pharia-1 / Mistral / Llama-4

## Lizenz-Fallstricke

| Modell | Lizenz | Falle |
|---|---|---|
| Qwen3 (alle Open-Varianten) | Apache 2.0 | keine — sicher |
| DeepSeek-R1 | MIT | keine |
| DeepSeek V3/V4 | custom | Lizenz-Detail vor produktivem Einsatz prüfen |
| GLM-5 | MIT (seit 07/2025) | vorher: restriktiv — alte Versionen prüfen |
| Kimi K2.6 | Modified MIT | Modifikationen lesen |
| MiniCPM | Apache 2.0 | keine |
| **EXAONE 1.2-NC** | NC = nicht kommerziell ohne LG-Vertrag | **kommerzielle Nutzung verboten** ohne Vertrag |
| Hunyuan | open weights, custom | für kommerzielle Nutzung Detail prüfen |

## Chinesisches Recht extraterritorial?

**PIPL** (Personal Information Protection Law):

- Gilt extraterritorial **nur** für in CN lebende Personen
- → Bei DACH-Inferenz auf DACH-Daten: **nicht anwendbar**

**DSL/CSL** (Data Security / Cybersecurity Law):

- Novelle 01.01.2026: erweiterte Reichweite **nur** bei Schädigung von CN-Cybersicherheit/CII
- → Bei normaler EU-Inferenz: **nicht anwendbar**

**Konsequenz**: Open-Weights-Inference auf EU-Servern triggert **keine** chinesische Compliance.

## EU AI Act ab 02.08.2026

- GPAI-Pflichten gelten **dem Bereitsteller** (also deinem DACH-SaaS), nicht nur dem ursprünglichen Modell-Anbieter
- Bei Modellen >10²⁵ FLOPs (DeepSeek V4, Qwen3-235B): **Systemic-Risk-Regime** (Art. 51, 55)
- Eval, Cybersecurity, Incident-Reporting, Energie-Doku werden Pflicht

## Curriculum-Empfehlung

| Phase | Asiatisches Modell | Use-Case |
|---|---|---|
| 04 (CV) | Qwen3-VL, MiniCPM-o | Open-VLM-Spitze |
| 09 (Hybride) | Hunyuan-TurboS, AI21 Jamba | Mamba-Transformer |
| 11 (LLM-Eng) | Qwen3, DeepSeek-R1, GLM-5, Kimi, EXAONE | Provider-Vergleich + Kosten |
| 13 (RAG) | Kimi K2.6 (Long-Context) | 256K-Kontext-Pattern |
| 14 (Agents) | Kimi K2.6, Qwen3-Coder | Agent-Swarm |
| 16 (Reasoning) | DeepSeek-R1 (GRPO-Referenz) | RLHF-Praxis |
| 17 (Production) | MiniCPM auf Edge, Qwen3-7B/Ollama | DSGVO-Inferenz |
| 18 (Ethik) | Self-Censorship-Audit | Pflicht-Eval |

## Pflicht-Disclaimer-Block

Jede Lektion mit asiatischem Modell enthält:

```markdown
> **⚠️ DACH-Compliance-Hinweise zu chinesischen Open-Weight-Modellen** (Stand 04/2026):
> - Lokale Inferenz auf EU-Hardware = DSGVO-konform
> - Offizielle CN-API = DSGVO-problematisch
> - Self-Censorship: 88 % Zensur bei DeepSeek-Chat auf geopolitische Themen
> - Lizenz-Falle: EXAONE-NC nicht kommerziell, V3/V4 = custom
> - EU AI Act ab 02.08.2026: Bereitsteller-Pflichten bleiben bei dir
```

## Quellen

- [DeepSeek-R1 Nature 08/2025](https://www.nature.com/articles/s41586-025-09422-z)
- [Qwen3 Technical Report (HF)](https://huggingface.co/Qwen)
- [Aleph Alpha vs. Qwen-Vergleich (heise.de)](https://www.heise.de/)
- [Mayer Brown — China CSL-Novelle 01.01.2026](https://www.mayerbrown.com/)
- [Linux Foundation EU — AI Act für Open-Weights](https://linuxfoundation.eu/)
- [Enkrypt AI — DeepSeek Bias Audit](https://www.enkryptai.com/blog/deepseek-r1-redteaming)
- [EDPB — AI Privacy Risks](https://www.edpb.europa.eu/system/files/2024-12/edpb_opinion_202428_ai-models_en.pdf)
- [TikTok 530 Mio. EUR Bußgeld 2025](https://www.dataprotection.ie/en/news-media/data-protection-commission-announces-conclusion-tiktok-inquiry)
