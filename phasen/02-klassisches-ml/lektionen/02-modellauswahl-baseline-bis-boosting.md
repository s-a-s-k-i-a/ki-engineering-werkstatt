---
id: 02.02
titel: Modell-Auswahl — Logistische Regression, Random Forest, XGBoost, LightGBM
phase: 02-klassisches-ml
dauer_minuten: 90
schwierigkeit: leicht
stand: 2026-04-29
voraussetzungen: [02.01]
lernziele:
  - Logistische Regression als Baseline-Pflicht setzen
  - Random Forest, XGBoost, LightGBM unterscheiden — und wann welches
  - Hyperparameter-Tuning mit GridSearchCV oder Optuna
  - Erkennen, wann KEIN Deep Learning nötig ist
compliance_anker:
  - hochrisiko-anhang-iii-5b
  - bias-test-pflicht
ai_act_artikel:
  - art-10
  - art-15
---

## Worum es geht

> Don't bring an LLM to a Random-Forest fight. — 2026 lösen sehr viele DACH-Mittelstand-Use-Cases (Customer-Churn, Predictive Maintenance, Kreditrisiko, Tarif-Klassifizierung) **ohne** Deep Learning. Klassisches ML ist günstiger, erklärbarer (SHAP), schneller in Production und meist AI-Act-konformer.

Diese Lektion zeigt die vier Standard-Werkzeuge: **Logistische Regression** als Baseline, **Random Forest** als „Schweizer Taschenmesser", **XGBoost** als Klassiker, **LightGBM** als 2026-Production-Wahl.

## Voraussetzungen

- Lektion 02.01 (Splitting + Leakage)

## Konzept

### Schritt 1: Logistische Regression als Pflicht-Baseline

Bevor du XGBoost trainierst, **immer** zuerst Logistische Regression. Gründe:

- Sehr schnell zu trainieren (Sekunden, nicht Minuten)
- Maximal interpretierbar (jeder Koeffizient ist eine Bedeutung)
- Wenn LogReg schon 85 % F1 schafft, ist dein Problem **linear separierbar** — keine Bäume nötig
- Setzt eine ehrliche untere Schranke: dein XGBoost muss mindestens das schlagen

```python
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

baseline = Pipeline([
    ("sc", StandardScaler()),
    ("lr", LogisticRegression(max_iter=1000, class_weight="balanced")),
])
```

`class_weight="balanced"` ist bei unbalancierten Klassen Pflicht, sonst optimiert das Modell auf die häufige Klasse.

### Schritt 2: Random Forest — der robuste Allrounder

**Random Forest** = viele Decision Trees mit Bagging (Random Subsets der Daten + Features). Eigenschaften:

- Funktioniert ootb für die meisten Probleme („Schweizer Taschenmesser")
- Robust gegen Hyperparameter (Default ist meist okay)
- Liefert Feature-Importance gratis
- **Skaliert nicht super** auf > 1M Samples — dann LightGBM

```python
from sklearn.ensemble import RandomForestClassifier

rf = RandomForestClassifier(
    n_estimators=200,
    max_depth=10,
    min_samples_leaf=20,
    n_jobs=-1,
    class_weight="balanced",
    random_state=42,
)
```

### Schritt 3: Gradient Boosting — XGBoost vs. LightGBM vs. CatBoost

Boosting-Modelle bauen Bäume **sequentiell** und korrigieren jeweils den Fehler des Vorgängers. Drei Varianten dominieren 2026:

| Bibliothek | Stärke | Schwäche |
|---|---|---|
| **XGBoost** (T. Chen et al., 2014, Apache 2.0) | seit 10+ Jahren bewährt, beste Tooling-Integration | Speicher-hungrig bei sehr großen Datasets |
| **LightGBM** (Microsoft, 2017, MIT) | sehr schnell auf Tabular > 1M Samples, geringer Memory-Footprint | Default-Hyperparameter weniger verzeihend |
| **CatBoost** (Yandex, 2017, Apache 2.0) | exzellent bei kategorialen Features ohne One-Hot | etwas langsamer als LightGBM |

**Faustregel 2026**:

- KMU-Datasets (< 100k Samples, gemischte Features): **XGBoost** ist die sichere Wahl
- Große Tabular-Production (Millionen Samples, Latenz-kritisch): **LightGBM**
- Viele kategoriale Features ohne Energie für Encoding: **CatBoost**

```python
import xgboost as xgb

xgb_model = xgb.XGBClassifier(
    n_estimators=300,
    max_depth=6,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    scale_pos_weight=20,   # bei 5 % Positiv-Rate: 95/5
    random_state=42,
    eval_metric="logloss",
)
```

### Schritt 4: Hyperparameter-Tuning — GridSearch vs. Optuna

Für klassisches ML reichen oft **drei Tuning-Stufen**:

1. **Default**: erste Modell-Vergleichsrunde mit Defaults — sieht klar, welche Familie überhaupt passt.
2. **GridSearchCV**: für 2-3 wichtige Hyperparameter eine kleine Grid (z.B. `max_depth ∈ {4, 6, 8}` × `learning_rate ∈ {0.01, 0.05, 0.1}`).
3. **Optuna** (Bayes/TPE-basiert): wenn man mehr als 3 HPs gleichzeitig tunen will. Standard in der Production 2026.

```python
import optuna

def objective(trial):
    params = {
        "max_depth": trial.suggest_int("max_depth", 3, 10),
        "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.3, log=True),
        "n_estimators": trial.suggest_int("n_estimators", 100, 500),
    }
    model = xgb.XGBClassifier(**params, random_state=42)
    return cross_val_score(model, X_train, y_train, scoring="f1", cv=5).mean()

study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=30)
```

### Schritt 5: Wann KEIN Deep Learning?

Für **tabular data** ist klassisches ML 2026 immer noch state-of-the-art bei < 1M Samples. Studien (z.B. „Why do tree-based models still outperform deep learning on typical tabular data?", Grinsztajn et al., NeurIPS 2022) bestätigen: bei strukturierten Tabellen schlagen Boosting-Modelle Deep-Learning-Tabular-Modelle (TabNet, FT-Transformer) konsistent.

**Entscheidungsregel**:

- **Bilder, Audio, Text, lange Sequenzen** → Deep Learning (Phase 03+)
- **Tabular, < 1M Samples, kategorisch+numerisch** → Boosting (XGBoost/LightGBM)
- **Tabular, > 10M Samples, niedrige Latenz** → LightGBM
- **Sehr kleine Daten (< 1k)** → Logistische Regression / einfacher Baum, oft besser als alles Komplexere

## Code-Walkthrough

```python
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score, roc_auc_score
import xgboost as xgb

modelle = {
    "Logistic Regression": LogisticRegression(max_iter=1000, class_weight="balanced"),
    "Random Forest": RandomForestClassifier(
        n_estimators=200, max_depth=10, class_weight="balanced", random_state=42
    ),
    "XGBoost": xgb.XGBClassifier(
        n_estimators=300, max_depth=6, learning_rate=0.05,
        scale_pos_weight=20, random_state=42, eval_metric="logloss"
    ),
}

for name, modell in modelle.items():
    modell.fit(X_train, y_train)
    y_pred = modell.predict(X_test)
    y_prob = modell.predict_proba(X_test)[:, 1]
    print(f"{name}: F1 = {f1_score(y_test, y_pred):.3f}, "
          f"AUC = {roc_auc_score(y_test, y_prob):.3f}")
```

## Hands-on

→ [`code/01_kreditrisiko_klassifikator.py`](../code/01_kreditrisiko_klassifikator.py)

Notebook führt alle drei Modelle auf synthetischen deutschen Bonitäts-Daten aus und vergleicht F1, ROC-AUC, Trainings-Zeit.

## Selbstcheck

- [ ] Wann nimmst du Logistische Regression statt XGBoost?
- [ ] Was bedeutet `scale_pos_weight=20` bei einer 5 %-Positiv-Klasse?
- [ ] Wann ist LightGBM einem XGBoost überlegen?
- [ ] Bei tabular data mit 50.000 Samples: würdest du Deep Learning probieren? Warum (nicht)?

## Compliance-Anker

- **AI-Act Anhang III Nr. 5b** (Hochrisiko: Kreditwürdigkeitsprüfung): wer ein Kreditscoring-Modell **produktiv** einsetzt, hat alle Hochrisiko-Pflichten zu erfüllen. Im Lehrkontext nicht relevant — aber für jeden Schritt sollst du wissen, was später dazugehört (Risk-Mgmt Art. 9, Daten-Governance Art. 10, Tech-Doku Art. 11, Logging Art. 12, Transparenz Art. 13, Human Oversight Art. 14, Accuracy/Robustness Art. 15). Phase 20 vertieft.
- **Bias-Test ist Pflicht** (Art. 10): bei deutschen Bonitäts-Modellen prüfe Bias gegen Postleitzahl, Geschlecht, Migrationshintergrund. AGG (Allgemeines Gleichbehandlungsgesetz) gilt parallel.

→ [`compliance.md`](../compliance.md)

## Quellen

- Chen & Guestrin (2016): „XGBoost: A Scalable Tree Boosting System" — <https://arxiv.org/abs/1603.02754>
- Ke et al. (2017): „LightGBM: A Highly Efficient Gradient Boosting Decision Tree" — <https://papers.nips.cc/paper/2017/hash/6449f44a102fde848669bdd9eb6b76fa-Abstract.html>
- Prokhorenkova et al. (2018): „CatBoost: unbiased boosting with categorical features" — <https://arxiv.org/abs/1706.09516>
- Grinsztajn et al. (2022): „Why do tree-based models still outperform deep learning on typical tabular data?" — <https://arxiv.org/abs/2207.08815>
- Optuna Docs — <https://optuna.org/>

## Weiterführend

- Lektion 02.03 (SHAP & Bias-Audit) — Erklärbarkeit + AGG
- Phase 17 (Production): wie Tabular-Modelle mit FastAPI deployt werden
