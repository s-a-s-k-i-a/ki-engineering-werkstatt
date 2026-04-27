---
id: 17
phase: 17-production-und-eu-hosting
stand: 2026-04-27
anker:
  - server-standort-dokumentation
  - bsi-c5-iso-27001
  - nis2-incident-response
  - cost-monitoring-pflicht
dsgvo_artikel:
  - art-32
  - art-44
  - art-46
ai_act_artikel:
  - art-12
  - art-15
  - art-17
---

# Compliance-Anker — Phase 17

## Server-Standort-Dokumentation

Pro Modell-Aufruf: log Server-Standort. Bei Audit muss pro Anfrage rekonstruierbar sein, wo verarbeitet wurde.

## Zertifizierungen

EU-Hosting-Anbieter mit AVV + Compliance-Frameworks:

- **StackIT (Schwarz IT)**: BSI C5, ISO 27001, deutsche RZ
- **IONOS**: BSI C5, ISO 27001, EU-Cloud-Code-of-Conduct
- **OVH**: ISO 27001, SOC 2, EU-Sovereign-Tier
- **Scaleway**: ISO 27001, SOC 2, EU-Sovereign
- **Hetzner**: ISO 27001 (Helsinki, Falkenstein, Nürnberg)

## NIS2 + KritisDachG (in Kraft 12/2025, operativ ab 04/2026)

Wer KRITIS-relevante KI-Systeme betreibt: NIS2 + Cybersecurity-Pflichten:

- 24h-Frist für Incident-Notification
- 72h-Frist für detaillierten Bericht
- 30-Tage-Frist für Final Report
- Geschäftsleitung haftet persönlich (bis 10 Mio. €)

Templates in `phasen/20-recht-und-governance/vorlagen/incident-runbook.md`.

## Cost-Monitoring (Art. 17)

AI-Act fordert Quality Management — dazu gehört Cost-Effektivität. Pflicht-Dashboard:

- Token-Kosten pro Tag/User/Use-Case
- Modell-Wahl-Auditing (warum nicht ein günstigeres Modell?)
- Anomalie-Alerts

## Drittland-Routing-Disziplin

LiteLLM erlaubt Provider-Switch. Compliance-Pattern:

- **Default = EU-Region** (Pharia, Mistral, IONOS, EU-OpenAI-Route)
- **Fallback nur mit AVV** + Logging-Marker

## Quellen

- [BSI C5-Katalog](https://www.bsi.bund.de/DE/Themen/Unternehmen-und-Organisationen/Informationen-und-Empfehlungen/Empfehlungen-nach-Angriffszielen/Cloud-Computing/Kriterienkatalog-C5/kriterienkatalog-c5_node.html)
- [vLLM Docs](https://docs.vllm.ai/)
- [LiteLLM Docs](https://docs.litellm.ai/)
- [BSI NIS2-regulierte Unternehmen](https://www.bsi.bund.de/DE/Themen/Regulierte-Wirtschaft/NIS-2-regulierte-Unternehmen/nis-2-regulierte-unternehmen_node.html)
