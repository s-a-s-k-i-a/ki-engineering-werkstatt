---
id: 02.01
titel: Train/Val/Test, K-Fold-CV und Leakage-Vermeidung
phase: 02-klassisches-ml
dauer_minuten: 60
schwierigkeit: leicht
stand: 2026-04-29
voraussetzungen: []
lernziele:
  - Train/Val/Test-Splits methodisch sauber anlegen
  - K-Fold-Cross-Validation einsetzen, wenn Daten knapp sind
  - Die häufigsten Leakage-Quellen erkennen und vermeiden
  - Stratified-Splitting bei unbalancierten Klassen
compliance_anker:
  - daten-governance-art-10
ai_act_artikel:
  - art-10
  - art-15
---

<!-- colab-badge:begin -->
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/s-a-s-k-i-a/ki-engineering-werkstatt/blob/main/dist-notebooks/phasen/02-klassisches-ml/code/01_kreditrisiko_klassifikator.ipynb)
<!-- colab-badge:end -->

## Worum es geht

> Stop benchmarking on your training data. — Das **größte** Eigentor in klassischem ML ist Daten-Leakage: das Modell sieht beim Training zufällig Information aus dem Test-Set, performt grandios in der Eval, fällt in Produktion auseinander.

Diese Lektion macht Splitting-Disziplin konkret: drei Splits, K-Fold-CV als Werkzeug-Erweiterung, und eine Checkliste für die häufigsten Leakage-Quellen — am Beispiel **deutscher Bonitäts-Daten**, weil das ein AI-Act-Hochrisiko-Use-Case ist (Anhang III Nr. 5b).

## Voraussetzungen

Keine.

## Konzept

### Drei Splits, drei Aufgaben

```text
Gesamt-Daten (z.B. 10.000 Samples)
   │
   ├── Train (60-80 %) ──── Modell lernt darauf
   │
   ├── Val (10-20 %)  ──── Hyperparameter-Tuning, Early Stopping
   │
   └── Test (10-20 %) ──── EINMAL ganz am Ende, nicht öfter!
```

**Goldene Regel**: Das Test-Set ist **heilig**. Wer es während Modell-Auswahl mehrfach benutzt, betreibt versehentlich Hyperparameter-Optimierung gegen das Test-Set — die Performance-Zahl ist dann optimistisch.

**Praxis**:

- Klein (< 10k): 60/20/20
- Mittel (10k-1M): 70/15/15 oder 80/10/10
- Groß (> 1M): 98/1/1 reicht oft

### Stratified-Splitting bei unbalancierten Klassen

Im Kreditscoring ist die Klasse „Default" oft 5-10 % der Daten. Bei naivem Random-Split kann ein Test-Set zufällig nur 2 % Defaults enthalten — Test-Metriken werden unzuverlässig. Lösung: **stratifizieren** = Klassenverteilung in jedem Split erhalten.

```python
from sklearn.model_selection import train_test_split

X_trainval, X_test, y_trainval, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42  # ← stratify=y!
)
X_train, X_val, y_train, y_val = train_test_split(
    X_trainval, y_trainval, test_size=0.25, stratify=y_trainval, random_state=42
)
```

### K-Fold-Cross-Validation — wenn Daten knapp sind

Bei < 10k Samples (typisch für KMU-Use-Cases) ist 80/10/10 manchmal zu wenig. Alternative: **K-Fold-CV** auf Train+Val:

```text
Daten in K=5 Folds geteilt:

Fold 1: Test-Fold | Rest = Training
Fold 2: Test-Fold | Rest = Training
... 5 Mal ...

Durchschnitt der Eval-Metriken über alle 5 Folds → robusterer Schätzwert
```

**Stratified K-Fold** für unbalancierte Klassen ist Standard 2026.

### Leakage — die fünf häufigsten Fallen

1. **Zeit-Leakage**: Bei Zeitreihen (Kreditrückzahlung, Aktien) **niemals** zufällig splitten. Zeit-Reihenfolge respektieren: alte Daten = Train, jüngere = Val/Test.
2. **Identitäts-Leakage**: Wenn dieselbe Person mehrfach in Daten ist (z.B. mehrere Kredite pro Kunde), darf sie **nicht** sowohl in Train als auch Test sein. Lösung: Group-Aware-Splitting (`GroupKFold`).
3. **Feature-Leakage**: Wenn ein Feature den Target verrät. Beispiel: „Konto wurde geschlossen" als Feature für „Default" — das passiert oft erst nach dem Default. **Klassisch**: Feature beschreibt Folge, nicht Ursache.
4. **Preprocessing-Leakage**: `StandardScaler.fit()` auf den **gesamten** Daten, dann splitten — der Mean kommt mit aus dem Test-Set ins Modell. Lösung: in `Pipeline` wrappen, fit nur auf Train.
5. **Imbalanced-Resampling-Leakage**: SMOTE/Oversampling **vor** dem Splitten → synthetische Test-Samples leaken in Training. Lösung: nur auf Train resampeln, nie auf Test.

### Sklearn-Pipeline gegen Leakage

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("clf", LogisticRegression(max_iter=1000)),
])

pipe.fit(X_train, y_train)        # Scaler.fit() läuft NUR auf X_train
y_pred = pipe.predict(X_test)     # Scaler nutzt Train-Statistiken
```

**Vorteil**: das ist sowohl methodisch sauber als auch bei `cross_val_score` automatisch korrekt.

## Code-Walkthrough

```python
import numpy as np
from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.metrics import f1_score
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

# Synthetische unbalancierte Daten — 5 % Defaults
rng = np.random.default_rng(42)
n = 5000
X = rng.standard_normal((n, 10))
y = (rng.standard_normal(n) > 1.6).astype(int)  # ~5 % Positive

# Schritt 1: Train+Val vs. Test stratifiziert splitten
X_tv, X_test, y_tv, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# Schritt 2: K-Fold auf Train+Val
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
pipe = Pipeline([("sc", StandardScaler()), ("lr", LogisticRegression(max_iter=1000))])

f1_scores = []
for fold_idx, (train_idx, val_idx) in enumerate(skf.split(X_tv, y_tv)):
    pipe.fit(X_tv[train_idx], y_tv[train_idx])
    y_pred = pipe.predict(X_tv[val_idx])
    f1_scores.append(f1_score(y_tv[val_idx], y_pred))

print(f"K-Fold-F1: {np.mean(f1_scores):.3f} ± {np.std(f1_scores):.3f}")

# Schritt 3: EINMAL auf Test evaluieren
pipe.fit(X_tv, y_tv)
print(f"Test-F1 (Final): {f1_score(y_test, pipe.predict(X_test)):.3f}")
```

## Hands-on

→ [`code/01_kreditrisiko_klassifikator.py`](../code/01_kreditrisiko_klassifikator.py)

Marimo-Notebook: synthetisches Kreditrisiko-Dataset (10 Features, 5 % Default-Rate), zeigt drei Modell-Familien (Logistische Regression, Random Forest, Gradient Boosting), berichtet Stratified-K-Fold-F1, dann Test-F1, plus SHAP-Erklärung und Bias-Audit.

## Selbstcheck

- [ ] Du hast 10k Samples mit 3 % Positiv-Rate. Welche Splitting-Strategie?
- [ ] Du baust ein Aktien-Vorhersage-Modell und splittest zufällig. Was geht schief?
- [ ] Welcher Sklearn-Mechanismus verhindert Preprocessing-Leakage?
- [ ] Wann ist K-Fold-CV überlegener als ein einzelner Train/Val-Split?

## Compliance-Anker

- **AI-Act Art. 10** (Daten-Governance): Splitting-Strategie und Repräsentativität der Daten muss dokumentiert sein. Phase 20 zeigt das Template für die Tech-Doku.
- **AI-Act Art. 15** (Accuracy/Robustness): Ohne sauberes Test-Set ist keine Robustness-Aussage möglich.

→ [`compliance.md`](../compliance.md)

## Quellen

- Géron, A. (2022): „Hands-On Machine Learning with Scikit-Learn, Keras and TensorFlow", 3. Auflage, O'Reilly
- scikit-learn: Cross-Validation Guide — <https://scikit-learn.org/stable/modules/cross_validation.html>
- Kaufman et al. (2012): „Leakage in Data Mining: Formulation, Detection, and Avoidance" — <https://www.cs.umb.edu/~ding/history/470_670_fall_2011/papers/cs670_Tran_PreferredPaper_LeakingInDataMining.pdf>

## Weiterführend

- Lektion 02.02 (Modell-Auswahl)
- Phase 11 (Eval-Strategien für LLMs): viele dieser Patterns gelten auch dort
