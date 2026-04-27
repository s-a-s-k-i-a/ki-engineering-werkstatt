---
id: 20
titel: Recht & Governance — AI-Act, DSGVO, AVV, DSFA, AI-Literacy
dauer_stunden: 12
schwierigkeit: mittel
stand: 2026-04-27
lernziele:
  - KI-Systeme rechtssicher nach EU AI Act klassifizieren (CLI-Tool!)
  - AVV (Art. 28 DSGVO) und DSFA (Art. 35) für KI-Use-Cases praktisch erstellen
  - AI-Literacy-Curriculum (AI-Act Art. 4) für Mitarbeitende aufbauen
  - Audit-Logging-Code-Skelett (OpenTelemetry GenAI) implementieren
  - ai.txt / robots.txt für TDM-Opt-out generieren
  - Lizenz-Scanner für Modelle, Trainings-Daten und Dependencies
---

# Recht & Governance — der DACH-Layer

> Stop hoping no one notices. — Compliance ist 2026 das größte Risiko für KI-Projekte im Mittelstand.

Showcase-Modul der KI-Engineering-Werkstatt. Im Original (rohitg00) komplett fehlend — der größte Mehrwert des Repos.

**Dieser Block ist keine juristische Beratung.** Er macht Compliance praktisch — mit CLI-Tools, Templates und Pattern. Bei konkreten Fällen: Datenschutzbeauftragte:n oder Kanzlei einschalten.

## Was du danach kannst

- Ein KI-System nach AI-Act in unter 5 Min. klassifizieren (CLI: `ki-act-classifier`)
- Einen AVV anhand eines Mustertemplates für deinen Use-Case erstellen
- Eine DSFA-Light durchführen
- Ein 4-h-AI-Literacy-Onboarding für Mitarbeitende aufbauen
- Audit-Logs nach AI-Act Art. 12 strukturieren
- ai.txt / robots.txt für deine Domain generieren (CLI: `ki-ai-txt`)
- Lizenz-Scanner über deine Modelle und Datasets laufen lassen

## Inhalts-Übersicht

| Lektion | Titel | Dauer |
|---|---|---|
| 20.01 | AI-Act-Risk-Klassifizierung mit Entscheidungsbaum | 90 min |
| 20.02 | AVV-Muster für die wichtigsten Cloud-LLM-Anbieter | 60 min |
| 20.03 | DSFA-Workflow am Beispiel „Tierheim-Bot" | 90 min |
| 20.04 | AI-Literacy-Curriculum (Art. 4) | 60 min |
| 20.05 | Audit-Logging-Code-Skelett (OpenTelemetry GenAI) | 60 min |
| 20.06 | ai.txt + robots.txt-Generator (UrhG § 44b) | 30 min |
| 20.07 | Lizenz-Scanner für Modelle/Datasets/Deps | 60 min |
| 20.08 | Sektor-Special: BaFin (Finance), MDR (Medizin), KritisDachG (KRITIS) | 90 min |

## CLI-Werkzeuge (Pflicht-Demo)

```bash
# AI-Act-Risk-Klassifizierung
ki-act-classifier --modell-karte projekte/01-tierheim-bot/model-card.yaml

# ai.txt + robots.txt für eine Domain
ki-ai-txt --domain example.de -o ./output/

# Compliance-Schema-Validierung über alle Phasen
ki-compliance-lint phasen/
```

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/s-a-s-k-i-a/ki-engineering-werkstatt/blob/main/dist-notebooks/phasen/20-recht-und-governance/code/01_ai_act_demo.ipynb)

## Voraussetzungen

- Phase 0 (Werkstatt)
- Empfehlenswert: Phase 11 (LLM-Engineering) und Phase 18 (Ethik)

## Status

✅ Vollständig ausgearbeitet (Showcase-Modul Launch).
