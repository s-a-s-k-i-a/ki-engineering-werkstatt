---
id: 02.03
titel: SHAP-Erklärbarkeit + Bias-Audit für AI-Act-Hochrisiko-Systeme
phase: 02-klassisches-ml
dauer_minuten: 90
schwierigkeit: leicht
stand: 2026-04-29
voraussetzungen: [02.02]
lernziele:
  - SHAP-Werte als Pflicht-Erklärung für AI-Act Art. 13 + DSGVO Art. 22
  - Globale vs. lokale Erklärungen unterscheiden
  - Bias-Audit auf geschützte Merkmale (AGG, AI-Act Art. 10)
  - Demographic Parity vs. Equalized Odds verstehen
compliance_anker:
  - shap-erklaerbarkeit-pflicht
  - bias-test-pflicht
  - dsgvo-art-22-automatisierte-entscheidung
ai_act_artikel:
  - art-10
  - art-13
  - art-14
dsgvo_artikel:
  - art-22
---

## Worum es geht

> Stop saying "the model decided". — Wenn Mensch X einen Kredit nicht bekommt, hat sie nach DSGVO Art. 22 ein Recht auf **menschliches Eingreifen, Information über die Logik und Anfechtung**. AI-Act Art. 13 fordert zusätzlich **Transparenz** über die Output-Generierung. Beides bekommst du mit SHAP — und das ist 2026 Industrie-Standard.

Diese Lektion zeigt zwei Pflicht-Schritte vor jedem Hochrisiko-Deployment: **SHAP-Erklärungen** (lokal + global) und **Bias-Audit** auf geschützte Merkmale.

## Voraussetzungen

- Lektion 02.02 (Modell-Auswahl)

## Konzept

### Schritt 1: SHAP — Shapley-Werte für ML

**SHAP** (SHapley Additive exPlanations, Lundberg & Lee 2017) basiert auf Shapley-Werten aus der Spieltheorie und liefert für jede Vorhersage **pro Feature**:

- **Beitrag** zum Output (positiv = pushte Richtung Klasse 1, negativ = pushte Richtung Klasse 0)
- **Konsistenz**: Summe aller SHAP-Werte = `f(x) - E[f(x)]` (Vorhersage minus Mittelwert)

```python
import shap
import xgboost as xgb

modell = xgb.XGBClassifier(...).fit(X_train, y_train)
explainer = shap.TreeExplainer(modell)
shap_werte = explainer.shap_values(X_test)

# Lokale Erklärung für Sample 0:
shap.force_plot(explainer.expected_value, shap_werte[0], X_test.iloc[0])
```

### Schritt 2: Globale vs. lokale Erklärungen

| Erklärungs-Typ | Frage | SHAP-Werkzeug |
|---|---|---|
| **Lokal** | „Warum hat **dieser** Antragsteller abgelehnt?" | `force_plot`, `waterfall_plot` |
| **Global** | „Welche Features sind im Modell **insgesamt** wichtig?" | `summary_plot`, `bar_plot` |

**DSGVO Art. 22-Pflicht**: Lokale Erklärung pro Entscheidung muss zur Verfügung stehen — die betroffene Person hat Anspruch darauf.

**AI-Act Art. 13**: globale Transparenz — die Behörde muss verstehen können, was das System tut.

### Schritt 3: Bias-Audit — Demographic Parity & Equalized Odds

Für AI-Act-Hochrisiko-Systeme (z.B. Kreditscoring) ist Bias-Audit Pflicht (Art. 10). Zwei Standard-Metriken:

**Demographic Parity (DP)**:

```text
DP = | P(ŷ=1 | Geschlecht=m) - P(ŷ=1 | Geschlecht=f) |
```

Misst: Werden Männer und Frauen **gleich häufig** akzeptiert?

**Equalized Odds (EOpp)**:

```text
EOpp = | TPR(m) - TPR(f) | + | FPR(m) - FPR(f) |
```

Misst: Sind die **Fehler-Raten** über Gruppen gleich?

**Welche Metrik wann?**

- **DP** ist intuitiv, aber strikt: schließt aus, dass Gruppen unterschiedliche Basis-Risiken haben
- **EOpp** erlaubt unterschiedliche Basis-Raten, fordert aber gleich-faire Behandlung **innerhalb** der wahren Klasse

**AI-Act gibt keine** harte Schwelle vor — aber 2026 ist in der Praxis: DP/EOpp-Differenz < 5 % gilt als „akzeptabel", > 10 % wird als „bias-verdächtig" markiert.

### Schritt 4: Geschützte Merkmale nach AGG

Das Allgemeine Gleichbehandlungsgesetz (Deutschland) verbietet Diskriminierung wegen:

- Rasse / ethnische Herkunft
- Geschlecht
- Religion / Weltanschauung
- Behinderung
- Alter
- Sexuelle Identität

Bei Bonitäts-Daten **typische Proxies**:

- Postleitzahl → ethnische Herkunft / sozioökonomischer Status
- Vorname → Geschlecht / Migrationshintergrund (Namens-Heuristik)
- Geburtsjahr → Alter

Auch wenn das Modell „nur" Postleitzahl nutzt, kann es indirekt diskriminieren (**proxy bias**). Bias-Audit muss das erkennen.

### Schritt 5: Bias-Mitigation — Quick-Wins

| Strategie | Wie | Trade-off |
|---|---|---|
| **Reweighting** | Trainingssamples nach Gruppen-Verhältnis gewichten | einfach, kann Performance kosten |
| **Adversarial Debiasing** | parallel ein Diskriminator-Modell, das Gruppe vorhersagt | komplex |
| **Post-Processing** | Schwellenwerte pro Gruppe anpassen | Pragmatic, aber rechtlich heikel (= Diskriminierung umgekehrt?) |
| **Feature-Removal** | geschützte Merkmale + Proxies entfernen | reicht oft nicht (Korrelationen) |

> **Praxis-Tipp 2026**: SHAP + Bias-Audit als **Pflicht-Pipeline-Schritt** integrieren. `fairlearn` (Microsoft, Apache 2.0) ist die Standard-Bibliothek 2026.

## Code-Walkthrough

```python
import numpy as np
import pandas as pd
import shap
import xgboost as xgb
from sklearn.metrics import confusion_matrix

# Modell training (Voraussetzung)
modell = xgb.XGBClassifier(...).fit(X_train, y_train)
y_pred = modell.predict(X_test)

# SHAP-Erklärung
explainer = shap.TreeExplainer(modell)
shap_werte = explainer.shap_values(X_test)

# Globale Feature-Importance
feature_importance = pd.DataFrame({
    "feature": X_test.columns,
    "mean_abs_shap": np.abs(shap_werte).mean(axis=0)
}).sort_values("mean_abs_shap", ascending=False)
print(feature_importance.head(10))


# Bias-Audit auf "Geschlecht" (synthetische Spalte)
def gruppen_metrik(y_true, y_pred, gruppe):
    """Demographic Parity + Equalized Odds zwischen 2 Gruppen."""
    masken = {0: gruppe == 0, 1: gruppe == 1}
    pos_rate = {g: y_pred[m].mean() for g, m in masken.items()}
    tpr = {}
    fpr = {}
    for g, m in masken.items():
        tn, fp, fn, tp = confusion_matrix(y_true[m], y_pred[m]).ravel()
        tpr[g] = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        fpr[g] = fp / (fp + tn) if (fp + tn) > 0 else 0.0
    dp = abs(pos_rate[0] - pos_rate[1])
    eopp = abs(tpr[0] - tpr[1]) + abs(fpr[0] - fpr[1])
    return dp, eopp

dp, eopp = gruppen_metrik(y_test, y_pred, geschlecht_test)
print(f"Demographic Parity diff: {dp:.3f}  (< 0.05 = akzeptabel)")
print(f"Equalized Odds diff:     {eopp:.3f}  (< 0.10 = akzeptabel)")
```

## Hands-on

→ [`code/01_kreditrisiko_klassifikator.py`](../code/01_kreditrisiko_klassifikator.py)

Im Notebook gibt es einen **Bias-Audit-Tab**, der Demographic Parity + Equalized Odds für eine simulierte „Geschlechts"-Spalte berichtet, plus globale SHAP-Top-10-Features.

## Selbstcheck

- [ ] Was ist der Unterschied zwischen lokaler und globaler SHAP-Erklärung?
- [ ] Was ist eine „Proxy-Diskriminierung"? Beispiel?
- [ ] DP-Differenz von 0.12 — was machst du?
- [ ] Welche fairlearn-Funktionen kennst du?

## Compliance-Anker

- **AI-Act Art. 13** (Transparenz): Output-Logik muss verständlich sein. SHAP ist Industrie-Standard, **aber nicht alleiniger Beweis** für Transparenz — die ergänzende Modell-Karte (Phase 17 + Phase 18) bleibt Pflicht.
- **DSGVO Art. 22** (Automatisierte Entscheidungen im Einzelfall): Recht auf menschliches Eingreifen + Anfechtung + Information über Logik. Lokale SHAP-Erklärung deckt einen Teil davon ab.
- **AI-Act Art. 14** (Human Oversight): bei Kreditscoring-Entscheidungen ist menschliche Letzt-Entscheidung Pflicht.
- **AGG**: Bias-Audit auf Geschlecht/Alter/ethnische Herkunft ist Pflicht.

→ [`compliance.md`](../compliance.md)

## Quellen

- Lundberg & Lee (2017): „A Unified Approach to Interpreting Model Predictions" (SHAP) — <https://arxiv.org/abs/1705.07874>
- Hardt, Price & Srebro (2016): „Equality of Opportunity in Supervised Learning" — <https://arxiv.org/abs/1610.02413>
- Microsoft Fairlearn — <https://fairlearn.org/>
- BaFin (2025): Fokusrisiken Digitalisierung — <https://www.bafin.de/DE/Aufsicht/Fokusrisiken/Fokusrisiken_2026/RIF_Trend_1_digitalisierung/RIF_Trend_1_digitalisierung_node.html>

## Weiterführend

- Phase 17 (Production): SHAP in einer FastAPI-Inferenz-API
- Phase 18 (Ethik & Alignment): Bias-Detektion bei LLMs
- Phase 20 (Recht): vollständige AI-Act-Konformitätsbewertung
