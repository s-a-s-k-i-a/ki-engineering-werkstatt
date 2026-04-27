---
id: 0
phase: 00-werkzeugkasten
stand: 2026-04-27
anker:
  - eu-cloud-bevorzugen
  - keys-niemals-im-code
  - hardware-co2-bewusstsein
dsgvo_artikel:
  - art-28
  - art-44
  - art-46
ai_act_artikel:
  - art-4
---

# Compliance-Anker — Phase 00

## Auftragsverarbeitungsvertrag (AVV) ab Tag 1

Sobald du eine Cloud-LLM-API anrufst und auch nur indirekt personenbezogene Daten verarbeitest (User-Prompts können Namen, E-Mails, Kontodaten enthalten — auch wenn nur „Test"-Daten), brauchst du einen AVV nach **Art. 28 DSGVO**.

- **EU-Anbieter mit AVV** (StackIT, IONOS, OVH, Scaleway, Aleph Alpha, Mistral): meist online im Dashboard signierbar.
- **US-Anbieter** (OpenAI, Anthropic, Google): Enterprise-/Team-/Zero-Retention-Tier nötig + zusätzlich Standardvertragsklauseln (SCC) + Transfer-Impact-Assessment (TIA).
- **Kostenlose Web-UIs** (chatgpt.com Free, claude.ai Free): kein AVV → für jede berufliche Nutzung mit Realdaten unzulässig.

## Art. 4 AI Literacy ab 02.02.2025

Schon in Phase 00 startet die Pflicht. Wenn du Kolleg:innen anlernst, dokumentiere die Schulungseinheit (Datum, Inhalt, Teilnehmende) — auch ein 30-Min-Onboarding zählt.

## Datenresidenz

Wähle bewusst:

- **EU/DACH-Region** für regulierte Daten (Mandanten, HR, Patient:innen)
- **Lokale Inferenz** (Ollama, MLX, vLLM on-prem) für maximale Datenhoheit
- **US-Region** nur, wenn Output keinen Personenbezug hat oder Daten anonymisiert sind

## Energie & CO₂

GPU-Inferenz ist nicht „kostenlos". Pharia-1 in Heidelberg läuft mit deutschem Strommix (~370 g CO₂/kWh, 2025). FLUX bei AWS Frankfurt liegt höher; vLLM auf einer eigenen Renewable-Cloud niedriger. AI-Act Art. 13 fordert für Hochrisiko-Systeme Energieverbrauch-Doku — gewöhne dich von Anfang an daran.

## Quellen

- [BfDI Kurzpapier KI](https://www.bfdi.bund.de/SharedDocs/Kurzmeldungen/DE/2024/AI-Act.html) (Stand 2025)
- [EDPB Opinion 28/2024 zu LLMs/Trainingsdaten](https://www.edpb.europa.eu/system/files/2024-12/edpb_opinion_202428_ai-models_en.pdf)
- [AI Act Art. 4 (AI Literacy)](https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:32024R1689) — Stand 2024
- [Bitkom Leitfaden KI & Datenschutz 2.0 (08/2025)](https://www.bitkom.org/sites/main/files/2025-08/bitkom-leitfaden-kuenstliche-intelligenz-und-datenschutz-auflage-2.pdf)
