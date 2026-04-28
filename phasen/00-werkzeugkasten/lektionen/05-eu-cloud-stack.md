---
id: 0.05
titel: EU-Cloud-Stack im Vergleich (StackIT, IONOS, OVHcloud, Scaleway)
phase: 00-werkzeugkasten
dauer_minuten: 60
schwierigkeit: einsteiger
stand: 2026-04-28
voraussetzungen: [0.04]
lernziele:
  - Vier produktive EU-Cloud-LLM-Anbieter mit AVV im Dashboard kennen
  - Pricing in EUR / 1M Tokens vergleichen
  - Compliance-Zertifikate (BSI C5, ISO 27001, SecNumCloud, HDS) einordnen
  - Wann lokale Inferenz endet und Cloud anfängt
compliance_anker:
  - eu-cloud-bevorzugen
  - avv-art-28
  - bsi-c5
dsgvo_artikel:
  - art-28
  - art-44
  - art-46
ai_act_artikel:
  - art-13
---

## Worum es geht

> Stop reaching for OpenAI as default. — die EU hat 2026 einen produktiven Cloud-LLM-Stack mit AVV im Dashboard.

Wenn lokale Inferenz nicht reicht (zu großes Modell, hoher QPS, mehrere User parallel), brauchst du Cloud. **Du musst nicht US-Cloud nehmen.** Vier EU-Anbieter haben 2026 einen produktiven LLM-Stack mit Self-Service-AVV und EU-Hosting.

## Voraussetzungen

- Phase 00.04 (Ollama lokal — du verstehst die OpenAI-API-Form)
- Eine Kreditkarte und 5 Min. für Account-Anlage (eine kostenlose Variante bei Scaleway)

## Konzept

### Die vier Hauptanbieter im Vergleich

| Anbieter | Standort | Modelle | EUR / 1M Tok (Beispiel) | Zertifikate | OpenAI-kompatibel |
|---|---|---|---|---|---|
| **STACKIT** (Schwarz IT) | DE (Neckarsulm, Lübbenau) | Llama 3.1 8B, Mistral Nemo, E5 Mistral 7B | ~ 0,45 In / 0,65 Out (Llama) | **BSI C5 Type 2**, ISO 27001, ISAE 3000/3402 | ✅ |
| **IONOS AI Model Hub** | DE | Llama 3.1 8B/70B/405B, Mistral Nemo / Small, gpt-oss-120b, Qwen3-Coder-Next 80B, FLUX, LightOnOCR | $ 0,17–1,93 / 1M (€-Preise auf DE-Seite) | **BSI C5, ISO 27001, ISO 50001, GAIA-X**, DSGVO | ✅ (`api.ionos.com/docs/inference-openai/v1`) |
| **OVHcloud AI Endpoints** | FR / DE | Llama 3.3 70B (€ 0,67 / 1M), Mistral 7B/Nemo, Qwen3-32B, Qwen3.5-9B Vision, Qwen3-Coder-30B, gpt-oss-20B/120B, Whisper, NVIDIA Riva, Stable Diffusion | € 0,01–0,67 / 1M | ISO 27001/27017/27018/27701, BSI C5, **SecNumCloud (Erweiterung läuft)**, HDS | ✅ |
| **Scaleway Generative APIs** | FR (Paris) | Qwen 3.5-397B, Llama 3.3-70B, Mistral Small 3.2-24B, Pixtral-12B, Qwen 3 Embedding, Whisper-large-v3, Voxtral | Mistral Small € 0,15 In / € 0,35 Out per 1M; **1M Free-Tier** | ISO 27001, **HDS** (Health Data Host); SecNumCloud-Qualifikation läuft | ✅ |

> Quellen: STACKIT, IONOS, OVHcloud, Scaleway offizielle Pricing-Seiten, Stand 28.04.2026. Pricing kann sich ändern — vor produktivem Einsatz auf Anbieter-Seite verifizieren.

### Vergleich nach Use-Case

| Du willst... | Empfehlung | Warum |
|---|---|---|
| günstigste 70B-Inferenz im EU-Raum | **OVHcloud** Llama 3.3 70B | € 0,67 / 1M Output ist 2026 der günstigste 70B-EU-Preis |
| BSI-C5-zertifizierte deutsche Cloud | **STACKIT** oder **IONOS** | beide BSI C5 Type 2, deutsches Hosting |
| Kostenlos starten / Free-Tier | **Scaleway** | 1M Free-Tier auf Generative APIs |
| Multimodal (Text + Bild + Audio) | **OVHcloud** oder **Scaleway** | Whisper, Pixtral, Voxtral, FLUX (IONOS auch) |
| Sovereign-AI für Behörden | **IONOS** + GAIA-X | mit ISO 50001 Energie-Zertifikat |
| Reine GPU-Bare-Metal (eigene Modelle) | **Hetzner** | GEX44 (RTX 4000 SFF Ada 20 GB), GEX131 (RTX PRO 6000 Blackwell Max-Q 96 GB) |

### Self-Service-AVV (Art. 28 DSGVO) — wer hat das?

**STACKIT, IONOS, OVHcloud, Scaleway**: Auftragsverarbeitungsvertrag direkt im Customer Portal signierbar, üblicherweise als Self-Service-Klick-Workflow.

**Hetzner**: AVV als PDF im Konto-Bereich.

**Aleph Alpha / PhariaAI**: Enterprise-Vertrag, individuell verhandelt (siehe Hinweis unten).

> ⚠️ AVV-Workflows ändern sich häufig. Vor produktivem Einsatz im jeweiligen Kunden-Portal prüfen.

### Aleph Alpha — wichtige Markt-Entwicklung 2026

Im April 2026 wurde **Cohere übernimmt Aleph Alpha** angekündigt ($ 20 Mrd. Sovereign-AI-Deal mit Schwarz-Backing). Auswirkung auf das Pharia-LLM-Roadmap noch offen.

→ Wenn dein Use-Case auf Pharia-1 spezifisch angewiesen ist (z. B. weil du BAFA-Vertrauensdienst-Zertifizierung für Behörden brauchst), prüfe vor produktivem Einsatz, ob Pharia-Pricing und -Verfügbarkeit sich nach dem Merger geändert haben.

Quellen: [TechCrunch, 25.04.2026](https://techcrunch.com/2026/04/25/why-cohere-is-merging-with-aleph-alpha/) · [Implicator](https://www.implicator.ai/cohere-buys-aleph-alpha-in-20bn-sovereign-ai-deal-backed-by-schwarz/).

### Beispiel-Aufruf gegen IONOS AI Model Hub

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["IONOS_AI_API_KEY"],
    base_url="https://openai.inference.de-txl.ionos.com/v1",  # de-txl = Frankfurt
)

response = client.chat.completions.create(
    model="meta-llama/Llama-3.1-8B-Instruct",
    messages=[
        {"role": "user", "content": "Was ist der AI Act in einem Satz?"}
    ],
)
print(response.choices[0].message.content)
```

Beachte:

- **Identische API zu Ollama und OpenAI**: nur `base_url` und `api_key` ändern sich.
- **API-Key kommt aus `.env`** — niemals im Code (siehe `.env.example` im Repo-Root).

### Wann nicht-EU-Cloud unvermeidbar ist

Fälle, in denen du US-Cloud (mit AVV + EU-Datazone + SCC + TIA) brauchst:

- Du brauchst **GPT-5** spezifisch (z. B. Reasoning-Power von o3, der in Europa nicht repliziert ist)
- Du brauchst **Claude 4.7 Opus** spezifisch (Münchener Anthropic-Office hilft bei DPA, Server bleibt aber USA mit EU-Routing)
- Multimodale State-of-the-Art (Sora-Video, Imagen-Bild) — diese Modelle gibt es 2026 nicht in EU-Cloud

Pattern für US-Cloud mit DSGVO-Schutz:

1. **EU-Datazone** explizit aktivieren (OpenAI Enterprise, Anthropic Enterprise Q1 / 2026)
2. **Zero-Data-Retention** Header setzen
3. **Standardvertragsklauseln (SCC)** zusätzlich abschließen
4. **Transfer-Impact-Assessment (TIA)** durchführen und dokumentieren

→ Phase 20 vertieft.

## Hands-on (20 Min., optional)

Wenn du jetzt schon einen EU-Anbieter testen willst:

**Variante A — Scaleway Free-Tier** (am schnellsten):

1. Account anlegen: <https://console.scaleway.com>
2. Im Dashboard: „Generative APIs" aktivieren — bekommst du 1M Free-Tier-Token
3. API-Key erstellen, in `.env` packen:

   ```bash
   SCW_GENERATIVE_API_KEY=dein-key-hier
   SCW_BASE_URL=https://api.scaleway.ai/v1
   ```

4. Testen:

   ```python
   from openai import OpenAI
   import os
   c = OpenAI(api_key=os.environ["SCW_GENERATIVE_API_KEY"], base_url=os.environ["SCW_BASE_URL"])
   r = c.chat.completions.create(model="mistral-small-3.2", messages=[{"role":"user","content":"Hallo!"}])
   print(r.choices[0].message.content)
   ```

**Variante B — IONOS AI Model Hub** (deutsches Hosting):

1. Account: <https://cloud.ionos.com>
2. „AI Model Hub" aktivieren
3. Im Dashboard AVV-Status prüfen
4. API-Key generieren

## Selbstcheck

- [ ] Du kannst die vier wichtigsten EU-LLM-Anbieter aufzählen (STACKIT, IONOS, OVHcloud, Scaleway).
- [ ] Du verstehst, dass alle vier OpenAI-API-kompatibel sind.
- [ ] Du weißt, wo du den AVV signierst (Self-Service im Dashboard).
- [ ] Du kennst zwei Anbieter mit BSI-C5-Zertifikat (STACKIT, IONOS).
- [ ] Du erklärst, wann US-Cloud unvermeidbar ist und welche zusätzlichen Schritte dann nötig sind (DPA + EU-Datazone + SCC + TIA).

## Compliance-Anker

- **AVV-Pflicht (Art. 28 DSGVO)**: gilt bei jedem Cloud-LLM-Aufruf, der personenbezogene Daten enthalten könnte.
- **EU-Hosting bevorzugen**: kein Drittland-Transfer, keine SCC-Akrobatik.
- **BSI C5 / ISO 27001**: Zertifikate sind keine 100 %-Garantie, aber harter Hinweis auf Mindeststandard.
- **Zukunfts­sicherheit**: AI-Act ab 02.08.2026 voll wirksam — EU-Cloud reduziert Auditing-Aufwand erheblich.

## Quellen

- STACKIT AI Model Serving — <https://stackit.com/en/products/data-ai/stackit-ai-model-serving>
- STACKIT Zertifikate — <https://stackit.com/en/why-stackit/benefits/certificates>
- IONOS AI Model Hub — <https://cloud.ionos.com/managed/ai-model-hub>
- OVHcloud AI Endpoints — <https://www.ovhcloud.com/en/public-cloud/ai-endpoints/catalog/>
- OVHcloud SecNumCloud — <https://www.ovhcloud.com/en/compliance/secnumcloud/>
- Scaleway Generative APIs — <https://www.scaleway.com/en/generative-apis/>
- Scaleway Compliance — <https://www.scaleway.com/en/security-and-resilience/>
- Hetzner GEX-Matrix (GPU) — <https://www.hetzner.com/dedicated-rootserver/matrix-gpu/>
- Aleph Alpha PhariaAI — <https://aleph-alpha.com/phariaai/>
- TechCrunch, „Why Cohere is merging with Aleph Alpha", 25.04.2026 — <https://techcrunch.com/2026/04/25/why-cohere-is-merging-with-aleph-alpha/>

Alle URLs Zugriff 2026-04-28. Pricing und AVV-Status können sich ändern — vor produktivem Einsatz im Anbieter-Portal verifizieren.

## Weiterführend

→ Lektion **00.06** (Dev-Container) — wenn du in einem Team arbeitest
→ Phase **11** (LLM-Engineering) — Anbieter-Vergleich mit echten Token-Kosten
→ Phase **17** (Production EU-Hosting) — vollständiger Production-Stack mit vLLM + LiteLLM
→ Phase **20** (Recht & Governance) — AVV-Checkliste, DSFA-Workflow
