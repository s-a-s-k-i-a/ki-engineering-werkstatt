---
id: 17.04
titel: EU-Cloud-Stack — STACKIT, IONOS, OVH, Scaleway, Hetzner im Detail
phase: 17-production-und-eu-hosting
dauer_minuten: 75
schwierigkeit: mittel
stand: 2026-04-28
voraussetzungen: [00.05, 11.05]
lernziele:
  - Die fünf wichtigsten EU-Cloud-Anbieter abgrenzen (Compliance + Pricing + GPU-Optionen)
  - AI-Model-Serving-APIs (managed) vs. IaaS-GPU-Server unterscheiden
  - Aleph-Alpha-Pharia post-Cohere-Übernahme realistisch einschätzen
  - Stack-Wahl-Tabelle nach Use-Case bedienen
compliance_anker:
  - eu-rz-standort-pflicht
  - bsi-c5-iso-27001
  - secnumcloud-fr
ai_act_artikel:
  - art-12
dsgvo_artikel:
  - art-32
  - art-44
  - art-46
---

## Worum es geht

> Stop defaulting to AWS Frankfurt. — die EU hat 2026 fünf produktiv-reife Cloud-Anbieter mit AI-Stack: STACKIT (BSI C5 Type 2), IONOS (BSI C5 + GAIA-X), OVHcloud (SecNumCloud läuft), Scaleway (HDS), Hetzner (klassisch günstig, aber kein H100). Plus: das Aleph-Alpha-Pharia-Ökosystem nach der Cohere-Übernahme im April 2026.

## Voraussetzungen

- Phase 00.05 (EU-Cloud-Stack-Überblick aus Werkzeugkasten)
- Phase 11.05 (Anbieter-Vergleich mit Token-Pricing)

## Konzept

### Die Compliance-Differenzierung 2026

Die DSGVO-Frage „dürfen wir hier deployen?" beantwortet sich über drei Layer:

| Layer | Was zählt | Beleg |
|---|---|---|
| **Land** | EU/EEA für „kein Drittland" | Server-Standort im AVV |
| **Zertifizierung** | BSI C5, ISO 27001, SecNumCloud (FR) | Audit-Reports |
| **AVV** | DSGVO Art. 28-Vertrag, Sub-Processors | Self-Service oder Anwalt |

### STACKIT (Schwarz IT, Heilbronn / Neckarsulm)

**Lage**: deutsche Public Cloud der Schwarz-Gruppe (Lidl/Kaufland-Mutter). 100 % deutsche RZ.

| Feld | Wert |
|---|---|
| RZ-Standorte | Neckarsulm (DE), Lübbenau (DE) |
| Compliance | **BSI C5 Type 2**, ISO 27001, ISAE 3000/3402 |
| AVV | Self-Service im Customer Portal |
| AI Model Serving | Llama 3.1 8B, Mistral Nemo, E5 Mistral 7B |
| Pricing AI Serving | ~ 0,45 € In / 0,65 € Out per 1M Tokens (Llama-Beispiel) |
| GPU IaaS | nicht eindeutig öffentlich — bei Bedarf Vertrieb anschreiben |
| K8s | STACKIT Kubernetes Engine (SKE) mit dokumentiertem NVIDIA-GPU-Operator-Support |

**Wann STACKIT**: wenn Mandanten BSI-C5-Type-2 verlangen (z. B. öffentliche Hand, kritische Infrastruktur). Plus: deutsche Firma → AVV in DE-Vertragsrecht.

URL: <https://stackit.com/en/products/data-ai/stackit-ai-model-serving>

### IONOS Cloud + AI Model Hub

**Lage**: deutscher Mittelstandscloud-Pionier, Karlsruhe / Berlin / Frankfurt.

| Feld | Wert |
|---|---|
| RZ-Standorte | Karlsruhe, Berlin, Frankfurt (DE) |
| Compliance | **BSI C5**, ISO 27001, ISO 50001, ISO 27018, GAIA-X, EU-Cloud-CoC |
| AVV | Self-Service im Cloud-Portal |
| AI Model Hub | Llama 3.1 8B/70B/405B, Mistral Nemo/Small, gpt-oss-120b, Qwen3-Coder-Next 80B, FLUX, LightOnOCR |
| Pricing | $ 0,17–1,93 / 1M Tokens (Range) |
| API | OpenAI-kompatibel: `https://openai.inference.de-txl.ionos.com/v1` |
| GPU IaaS | verfügbar (NVIDIA), Detail-Pricing über Vertrieb / Cloud-Portal |
| K8s | Managed K8s; H100/H200-Self-Service-Verfügbarkeit ist 2026 ausbaufähig |

**Wann IONOS**: breitestes EU-AI-Modell-Angebot 2026 (inkl. Qwen3-Coder, gpt-oss, FLUX). GAIA-X-Compatibility plus EU-Cloud-Code-of-Conduct.

URL: <https://cloud.ionos.com/managed/ai-model-hub>

### OVHcloud (Roubaix / Limburg)

**Lage**: französischer Cloud-Riese mit eigenem RZ in Deutschland, attraktive Preise.

| Feld | Wert |
|---|---|
| RZ-Standorte | Frankreich (Roubaix, Gravelines, Strasbourg), Deutschland (Limburg) |
| Compliance | ISO 27001/27017/27018/27701, BSI C5, **SecNumCloud-Erweiterung läuft**, HDS |
| AVV | Self-Service |
| AI Endpoints | Llama 3.3 70B, Mistral 7B / Nemo, Qwen3-32B, Qwen3.5-9B Vision, Qwen3-Coder-30B, gpt-oss-20B/120B, Whisper, NVIDIA Riva, Stable Diffusion |
| Pricing | € 0,01–0,67 / 1M Tokens; Llama 3.3 70B ≈ € 0,67 / 1M (günstigster 70B-EU-Preis 2026) |
| GPU IaaS | H100, A100, V100 verfügbar; Detail-Pricing auf Anbieter-Seite re-verifizieren |
| K8s | Managed K8s mit GPU-Nodes |

**Wann OVHcloud**: günstigster EU-anbieter-Preis pro 1M Token bei 70B-Klasse. Französische Datensouveränität (SecNumCloud) — wichtig für FR-Kund:innen.

URL: <https://www.ovhcloud.com/en/public-cloud/ai-endpoints/catalog/>

### Scaleway (Paris)

**Lage**: Pariser Sovereign-Cloud mit Generative APIs und attraktivem Free-Tier.

| Feld | Wert |
|---|---|
| RZ-Standorte | Paris (FR) |
| Compliance | ISO 27001, **HDS** (Health Data Host), SecNumCloud-Qualifikation läuft |
| Generative APIs | Qwen3.5-397B, Llama 3.3-70B, Mistral Small 4, Pixtral-12B, Qwen 3 Embedding, Whisper-large-v3, Voxtral |
| Pricing | Mistral Small: € 0,15 In / € 0,35 Out per 1M Tokens; **1M Free-Tier** inklusive |
| GPU IaaS | H100, L40S verfügbar (Stunden-Pricing auf Anbieter-Seite verifizieren) |
| K8s | Kapsule (Managed K8s) |

**Wann Scaleway**: günstige Token-Preise + großzügiges Free-Tier für Prototyping. Health-Data-Tier (HDS) für Gesundheits-Use-Cases.

URL: <https://www.scaleway.com/en/generative-apis/>

### Hetzner (Falkenstein / Nürnberg / Helsinki)

**Lage**: klassisch günstigster EU-Anbieter, Fokus auf dedizierte Server, **kein H100/H200-Cloud-Angebot** 2026.

| Feld | Wert |
|---|---|
| RZ-Standorte | Falkenstein, Nürnberg (DE), Helsinki (FI) |
| Compliance | ISO 27001 |
| AVV | PDF im Konto-Bereich |
| GPU-Server (dediziert) | **GEX44** (RTX 4000 SFF Ada, 20 GB VRAM), **GEX131** (RTX PRO 6000 Blackwell Max-Q, 96 GB VRAM) |
| H100/H200 | nicht im Angebot |
| K8s | Cloud Native Kubernetes Engine (CCM); GPU-Self-Service eingeschränkt |

**Wann Hetzner**: Single-User-Inferenz mittlerer Modelle (70B Q4 läuft auf einer GEX131 mit 96 GB VRAM), monatliche Miete statt stündlich. Für Multi-GPU-Production ist Hetzner 2026 **nicht** der richtige Partner — nimm STACKIT, IONOS oder OVH.

URL: <https://www.hetzner.com/dedicated-rootserver/matrix-gpu/>

### Aleph Alpha Pharia post-Cohere-Übernahme (Stand 04/2026)

**Status**: am 25.04.2026 wurde der **Cohere-Aleph-Alpha-Merger** angekündigt — ein US$ 20 Mrd. Sovereign-AI-Deal mit Schwarz-Backing ([TechCrunch 25.04.2026](https://techcrunch.com/2026/04/25/why-cohere-is-merging-with-aleph-alpha/), [Implicator.ai](https://www.implicator.ai/cohere-buys-aleph-alpha-in-20bn-sovereign-ai-deal-backed-by-schwarz/)). Die Merger-Roadmap ist offen.

| Feld | Wert |
|---|---|
| Pharia-1-LLM-7B-control | weiterhin auf Hugging Face (Open Weights, MIT-ähnlich) |
| Pharia-API (`api.aleph-alpha.com`) | aktiv, Pricing Enterprise-on-Request |
| Indirekt via STACKIT / IONOS | zur Verifikation, Roadmap nach Merger offen |
| Compliance | ISO 27001, BSI C5, BAFA-Vertrauensdienst, RZ Heidelberg |

> **Empfehlung 04/2026**: bei Pharia-Abhängigkeit für aktuelle Projekte das Tech-Team **direkt anschreiben**. Die Open-Weights-Pharia-1-7B läuft weiterhin auf eigener vLLM-Instance — siehe Lektion 17.11 (Hands-on).

URL: <https://aleph-alpha.com/phariaai/>

### Stack-Wahl-Tabelle nach Use-Case

| Use-Case | Empfohlener Stack |
|---|---|
| Kleine SaaS-App, < 5M Tokens/Monat | **Scaleway Generative APIs** (Free-Tier + günstig) |
| DACH-Mittelstand, AVV-Pflicht | **STACKIT AI Model Serving** oder **IONOS AI Model Hub** |
| 70B-Klasse + günstigster EU-Preis | **OVHcloud AI Endpoints** (Llama 3.3 70B ≈ 0,67 € / 1M) |
| Self-Hosted vLLM auf K8s | **STACKIT SKE** + GPU-Operator + production-stack-Helm |
| Health-Data, HDS-Pflicht | **Scaleway HDS** |
| Single-User-Inferenz auf eigener Box | **Hetzner GEX131** + Llama 3.3 70B Q4 lokal |
| Pharia-1 Open-Weights | **eigene STACKIT-/IONOS-vLLM-Instance** mit GGUF-Import |
| BSI-C5-Type-2-Pflicht | **STACKIT** (einziger Anbieter mit Type 2 explizit ausgewiesen) |

### Token-Pricing-Realitäts-Check (Stand 28.04.2026)

| Anbieter | Modell | Input / 1M | Output / 1M | Cache (in) |
|---|---|---|---|---|
| STACKIT | Llama 3.1 8B | € 0,45 | € 0,65 | ⏳ |
| IONOS | Llama 3.1 70B | $ 0,40 | $ 1,20 | ⏳ |
| IONOS | gpt-oss-120b | $ 1,30 | $ 1,93 | ⏳ |
| OVHcloud | Llama 3.3 70B | € 0,67 | € 0,67 | ⏳ |
| OVHcloud | Qwen3-Coder-30B | € 0,18 | € 0,18 | ⏳ |
| Scaleway | Mistral Small 4 | € 0,15 | € 0,35 | ⏳ |
| Scaleway | Llama 3.3 70B | € 0,90 | € 0,90 | ⏳ |

> Pricing volatil — vor Produktiv-Einsatz **immer im Anbieter-Portal re-verifizieren**. Cache-Pricing war bei den EU-Anbietern Stand 04/2026 noch nicht konsolidiert (im Gegensatz zu Anthropic/OpenAI, siehe Lektion 11.05).

## Hands-on

1. Bei zwei der fünf Anbieter einen Test-Account aufsetzen (kostenlose Tier wo verfügbar)
2. Denselben Prompt (5 deutsche Test-Sätze) gegen beide Anbieter laufen lassen
3. Latenz + EUR-Kosten dokumentieren — Tabelle bauen
4. AVV-Status für deine Organisation prüfen (Self-Service vs. Anwalt)

## Selbstcheck

- [ ] Du nennst die Compliance-Tier der fünf wichtigsten EU-Anbieter (BSI C5, SecNumCloud, HDS).
- [ ] Du wählst den richtigen Anbieter pro Use-Case-Profil.
- [ ] Du verstehst die Aleph-Alpha-Pharia-Situation post-Cohere-Merger.
- [ ] Du re-verifizierst Token-Preise vor Produktiv-Einsatz selbst auf der Anbieter-Seite.

## Compliance-Anker

- **EU-RZ-Pflicht (DSGVO Art. 44)**: alle fünf Anbieter erfüllen das.
- **AVV (DSGVO Art. 28)**: Self-Service bei STACKIT / IONOS / OVH / Scaleway / Hetzner.
- **NIS2-Pflicht (ab 04/2026 operativ)**: bei KRITIS-Zulieferung trifft NIS2 — siehe Phase 17 `compliance.md`.

## Quellen

- STACKIT Zertifikate — <https://stackit.com/en/why-stackit/benefits/certificates>
- STACKIT AI Model Serving — <https://stackit.com/en/products/data-ai/stackit-ai-model-serving>
- STACKIT SKE GPU-Operator — <https://docs.stackit.cloud/products/runtime/kubernetes-engine/how-tos/use-nvidia-gpus/>
- IONOS AI Model Hub — <https://cloud.ionos.com/managed/ai-model-hub>
- IONOS Compliance — <https://www.ionos.de/digitalguide/server/security/iso-und-c5-zertifizierungen-im-it-bereich/>
- OVHcloud AI Endpoints — <https://www.ovhcloud.com/en/public-cloud/ai-endpoints/catalog/>
- OVHcloud SecNumCloud — <https://www.ovhcloud.com/en/compliance/secnumcloud/>
- Scaleway Generative APIs — <https://www.scaleway.com/en/generative-apis/>
- Scaleway Compliance — <https://www.scaleway.com/en/security-and-resilience/>
- Hetzner GPU-Server — <https://www.hetzner.com/dedicated-rootserver/matrix-gpu/>
- Cohere-Aleph-Alpha-Merger — <https://techcrunch.com/2026/04/25/why-cohere-is-merging-with-aleph-alpha/>
- Aleph Alpha Pharia — <https://aleph-alpha.com/phariaai/>

## Weiterführend

→ Lektion **17.06** (Helm-Charts auf STACKIT SKE / OVH Managed K8s)
→ Lektion **17.11** (Hands-on Pharia-1 auf STACKIT mit vLLM)
→ Phase **00.05** (EU-Cloud-Stack-Überblick aus dem Werkzeugkasten)
→ Phase **20.06** (`ai.txt`-Generator pro Domain)
