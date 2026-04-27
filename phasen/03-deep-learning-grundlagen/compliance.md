---
id: 3
phase: 03-deep-learning-grundlagen
stand: 2026-04-27
anker:
  - mlflow-lokal-statt-wandb-us
  - reproducibility-seeds
dsgvo_artikel:
  - art-44
ai_act_artikel:
  - art-11
---

# Compliance-Anker — Phase 03

## Tracking-Dienste

W&B (Weights & Biases) ist beliebt, hostet aber primär in den USA. Empfehlung:

- **Lokal**: MLflow self-hosted (Docker-Compose-Setup in `infrastruktur/observability/`)
- **EU-Cloud**: Comet (mit EU-Region) oder Self-Hosted Aim

Für Lehr-/Demo-Zwecke ohne PII: W&B-Nutzung ok, aber dokumentieren.

## Reproduzierbarkeit (Art. 11 AI Act)

Tech-Doku für Hochrisiko-Systeme verlangt nachvollziehbare Trainings-Läufe:

- Random-Seeds setzen
- Daten-Hash dokumentieren
- Modell-Checksummen archivieren
- Hyperparameter logging

## Drittland-Transfer (Art. 44 DSGVO)

Datasets von Hugging Face werden über USA-CDNs verteilt. Bei rohen Daten ohne Personenbezug unkritisch; bei selbst-hochgeladenen mit Personenbezug → SCC-Pflicht plus TIA.
