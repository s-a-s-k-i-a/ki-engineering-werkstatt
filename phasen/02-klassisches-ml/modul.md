---
id: 2
titel: Klassisches ML — sklearn, XGBoost/LightGBM, SHAP für AI-Act-Hochrisiko
dauer_stunden: 6
schwierigkeit: leicht
stand: 2026-04-29
lernziele:
  - 70 % aller KMU-KI-Probleme ohne Deep Learning lösen
  - Train/Val/Test sauber splitten, Leakage erkennen
  - Logistic Regression vs. RF/XGBoost/LightGBM einordnen
  - SHAP für AI-Act Art. 13 + DSGVO Art. 22
  - Bias-Audit (Demographic Parity, Equalized Odds) durchführen
---

# Phase 02 · Klassisches ML

> **Don't bring an LLM to a Random-Forest fight.** — Tabular Data, < 1M Samples, gemischte Features → Boosting schlägt Deep Learning konsistent (Grinsztajn et al. 2022). Klassisches ML ist günstiger, erklärbarer und meist AI-Act-konformer.

**Status**: ✅ vollständig ausgearbeitet · **Dauer**: ~ 6 h · **Schwierigkeit**: leicht

## 🎯 Was du in diesem Modul lernst

- **Splitting-Disziplin**: Stratified-K-Fold, fünf Leakage-Patterns
- **Modell-Familie**: LogReg → RF → XGBoost / LightGBM / CatBoost
- **Hyperparameter-Tuning**: GridSearchCV → Optuna
- **SHAP-Erklärbarkeit**: Lokal + global, DSGVO-Art-22-konform
- **Bias-Audit**: Demographic Parity + Equalized Odds, AGG-Pflicht

## 📚 Inhalts-Übersicht

| Lektion | Titel | Datei |
|---|---|---|
| 02.01 | Train/Val/Test, K-Fold-CV, Leakage | [`lektionen/01-train-val-test-und-leakage.md`](lektionen/01-train-val-test-und-leakage.md) ✅ |
| 02.02 | Modell-Auswahl: LogReg → RF → XGBoost/LightGBM | [`lektionen/02-modellauswahl-baseline-bis-boosting.md`](lektionen/02-modellauswahl-baseline-bis-boosting.md) ✅ |
| 02.03 | SHAP & Bias-Audit für AI-Act-Hochrisiko | [`lektionen/03-shap-und-bias-audit.md`](lektionen/03-shap-und-bias-audit.md) ✅ |

## 💻 Hands-on-Projekt

**Kreditrisiko-Klassifikator**: synthetisches deutsches Bonitäts-Dataset (5 % Default-Rate), Stratified-K-Fold-Vergleich von LogReg / RF / Gradient Boosting, Permutation-Importance + Bias-Audit.

```bash
uv run marimo edit phasen/02-klassisches-ml/code/01_kreditrisiko_klassifikator.py
```

## 🧱 Faustregeln 2026

| Frage | Antwort |
|---|---|
| Tabular < 1M Samples? | XGBoost oder LightGBM |
| Tabular > 10M Samples? | LightGBM (Memory + Speed) |
| Viele kategoriale Features? | CatBoost |
| Erste Modell-Runde? | Immer mit Logistic Regression starten |
| AI-Act-Hochrisiko (Anhang III)? | SHAP + Bias-Audit + DSFA + Konformitätsbewertung |

## ⚖️ DACH-Compliance-Anker

→ [`compliance.md`](compliance.md): AI-Act Anhang III Nr. 5b (Kreditscoring), Art. 9-15 (alle Hochrisiko-Pflichten), DSGVO Art. 22 (Automatisierte Entscheidung), DSGVO Art. 35 (DSFA), AGG (Allgemeines Gleichbehandlungsgesetz).

## 🔄 Wartung

Stand: 29.04.2026 · Reviewer: Saskia Teichmann ([@s-a-s-k-i-a](https://github.com/s-a-s-k-i-a)) · Nächster Review: 10/2026 (BaFin-Fokusrisiken-Update Q3/2026 erwartet).
