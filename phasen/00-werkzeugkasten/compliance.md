---
id: 0
phase: 00-werkzeugkasten
stand: 2026-04-28
anker:
  - eu-cloud-bevorzugen
  - keys-niemals-im-code
  - hardware-co2-bewusstsein
  - avv-art-28
  - ai-literacy-art-4
  - lokale-inferenz-dsgvo-bonus
  - reproducible-environment
dsgvo_artikel:
  - art-28
  - art-44
  - art-46
ai_act_artikel:
  - art-4
  - art-11
  - art-13
---

# Compliance-Anker — Phase 00

## Auftragsverarbeitungsvertrag (AVV) ab Tag 1

Sobald du eine Cloud-LLM-API aufrufst und auch nur indirekt personenbezogene Daten verarbeitest (User-Prompts können Namen, E-Mails, Kontodaten enthalten — auch wenn nur „Test"-Daten), brauchst du einen AVV nach **Art. 28 DSGVO**.

| Anbieter-Klasse | AVV-Pfad |
|---|---|
| **EU-Anbieter** (STACKIT, IONOS, OVHcloud, Scaleway, Aleph Alpha, Mistral) | meist Self-Service im Dashboard signierbar |
| **US-Anbieter** (OpenAI, Anthropic, Google) | Enterprise- / Team- / Zero-Retention-Tier nötig + zusätzlich SCC + TIA |
| **Free-Tier-Web-UIs** (chatgpt.com, claude.ai Free, gemini.google.com Free) | **kein AVV → für berufliche Nutzung mit Realdaten unzulässig** |

→ Lektion **00.05** zeigt die vier wichtigsten EU-Anbieter im Vergleich.

## Art. 4 AI Literacy ab 02.02.2025

Schon in Phase 00 startet die Pflicht. Wenn du Kolleg:innen anlernst, dokumentiere die Schulungseinheit (Datum, Inhalt, Teilnehmende) — auch ein 30-Min-Onboarding zählt. → Phase 20 hat eine 4-Stunden-Onboarding-Vorlage.

**Sanktionsfähig ab 02.08.2026**: bis 15 Mio. € oder 3 % weltweiter Jahresumsatz.

## Datenresidenz

Wähle bewusst:

- **EU / DACH-Region** für regulierte Daten (Mandanten, HR, Patient:innen, Kreditdaten)
- **Lokale Inferenz** (Ollama, MLX, vLLM on-prem) für maximale Datenhoheit — **keine** AVV-Pflicht
- **US-Region** nur, wenn Output keinen Personenbezug hat **oder** Daten anonymisiert sind **und** EU-Datazone aktiviert ist + SCC + TIA

## Reproduzierbarkeit (AI-Act Art. 11)

Hochrisiko-Systeme verlangen lückenlose Tech-Doku. Die Werkstatt-Kombination liefert das von Tag 1:

- `pyproject.toml` + `uv.lock` (alle Versionen byte-genau gepinnt)
- Marimo-Notebooks als `.py`-Dateien (Git-Diff-tauglich)
- Pre-commit-Hooks (Ruff, gitleaks, codespell)
- Dev-Container (siehe Lektion 00.06)

## Energie & CO₂ (AI-Act Art. 13)

GPU-Inferenz ist nicht „kostenlos". Faustwerte (Stand 2025):

| Hosting | Strommix | Hinweis |
|---|---|---|
| Aleph Alpha Pharia in Heidelberg | ~ 370 g CO₂ / kWh (deutscher Strommix) | mittel |
| AWS Frankfurt (FLUX, etc.) | ~ 320 g CO₂ / kWh (laut AWS-Region-Doku) | etwas besser |
| OVHcloud Beauharnois (Hydro) | ~ 30 g CO₂ / kWh | sehr gut |
| Scaleway Paris (DC2/3, Free Cooling) | ~ 220 g CO₂ / kWh | mittel |
| Lokale Inferenz auf Mac M4 | ~ 30 W × Strommix | sehr gut, kleine Workloads |

Hochrisiko-Systeme nach AI-Act Art. 13: **Energieverbrauch dokumentieren**. Gewöhne dich von Anfang an daran, auch wenn dein Use-Case noch nicht Hochrisiko ist.

## Schlüssel & Geheimnisse

- **Niemals API-Keys im Code** committen
- `.env`-Datei lokal halten, `.env.example` committen
- `gitleaks` als Pre-commit-Hook (siehe `.pre-commit-config.yaml`)
- GitHub Push-Protection ist im Repo aktiv (auch beim Klon!)

## Markt-Entwicklung April 2026 (relevant für Anbieter-Wahl)

> **Cohere übernimmt Aleph Alpha** (angekündigt 25.04.2026, $ 20 Mrd. Sovereign-AI-Deal mit Schwarz-Backing).

Wenn dein Use-Case Pharia-1 spezifisch braucht (z. B. wegen BAFA-Vertrauensdienst-Zertifizierung für Behörden), prüfe vor produktivem Einsatz, ob Pharia-Pricing und -Verfügbarkeit sich nach dem Merger geändert haben.

Quellen:

- TechCrunch, „Why Cohere is merging with Aleph Alpha", 25.04.2026 — <https://techcrunch.com/2026/04/25/why-cohere-is-merging-with-aleph-alpha/>
- Implicator: $ 20B Sovereign-AI-Deal — <https://www.implicator.ai/cohere-buys-aleph-alpha-in-20bn-sovereign-ai-deal-backed-by-schwarz/>

## Quellen (Recht & Compliance)

- BfDI Kurzpapier KI — <https://www.bfdi.bund.de/SharedDocs/Kurzmeldungen/DE/2024/AI-Act.html> (Stand 2025)
- EDPB Opinion 28/2024 zu LLMs / Trainingsdaten — <https://www.edpb.europa.eu/system/files/2024-12/edpb_opinion_202428_ai-models_en.pdf>
- AI Act Art. 4 (AI Literacy) — <https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:32024R1689>
- Bitkom Leitfaden KI & Datenschutz 2.0 (08/2025) — <https://www.bitkom.org/sites/main/files/2025-08/bitkom-leitfaden-kuenstliche-intelligenz-und-datenschutz-auflage-2.pdf>
