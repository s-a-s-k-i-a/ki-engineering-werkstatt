# Übung 02.01 — KMU-Churn-Klassifikator-Selektor + Bias-Audit-Plan

> Schwierigkeit: leicht-mittel · Zeit: 60–90 Min · Voraussetzungen: Lektionen 02.01–02.03

## Ziel

Du erstellst für **drei reale KMU-Use-Cases** einen begründeten Modell-Auswahl-Selektor und einen Bias-Audit-Plan. Ohne Modell-Training — der Schwerpunkt liegt auf der **Methodik vor dem ersten `fit()`**: Splitting, Modell-Familie, Eval-Metrik, AGG-Bias-Risiko.

## Use-Case

Ein DACH-Mittelstands-Berater sammelt drei Fälle:

1. **Maschinenbau-Predictive-Maintenance**: 850.000 Sensor-Snapshots, 0.8 % Defekt-Rate, < 50 ms Latenz-Anforderung
2. **Steuerberatung-Mandanten-Churn**: 12.000 Kunden mit 8 % Churn-Rate, demografische Merkmale + Vertragsdauer + Mandatshöhe enthalten
3. **Bildungs-Drop-out-Vorhersage**: 4.500 Auszubildende, 18 % Drop-out, mit Geschlecht / Alter / Migrationshintergrund-Proxy

## Aufgabe

1. **Profil-Pydantic-Schema** mit Feldern: `name`, `n_samples`, `feature_typ`, `latenz_ms`, `unbalanciert`, `ai_act_hochrisiko`, `agg_geschuetztes_merkmal`
2. **Modell-Auswahl-Funktion** `empfehle_modell(profil) -> dict` mit Begründung (`grund: str`)
3. **Eval-Strategie-Funktion** `empfehle_eval(profil) -> dict` (Stratified-Split vs. K-Fold-CV vs. Time-Split)
4. **Bias-Audit-Plan** `bias_audit_pflichten(profil) -> list[str]` mit Demographic-Parity / Equalized-Odds / Proxy-Bias-Test
5. **AI-Act-Risiko-Klassifikation** integriert (Anhang III Nr. 5b für Kreditwürdigkeit, andere Anhänge prüfen)
6. **Tabelle** mit allen drei Use-Cases: Modell + Eval + Compliance-Pflichten
7. **Smoke-Test**: 4 Asserts (richtige Modell-Familie pro Use-Case)

## Bonus (für Schnelle)

- **SHAP-Setup**-Skizze als Pseudo-Code für die Bildung-Auszubildenden-Daten — welche `shap.TreeExplainer`-Konfiguration?
- **Time-Split** für Maschinenbau-Sensoren: wie viel Test-Window, wie viel Embargo?
- **Pipeline mit StandardScaler + LogisticRegression** als Pflicht-Baseline pro Use-Case (Pseudo-Code reicht)
- **Ergänzung Recht**: AGG-Klauseln mappen — welcher AGG-Paragraph greift bei „Migrationshintergrund-Proxy"?

## Abgabe

- Marimo-Notebook in `loesungen/01_loesung.py` (smoke-test-tauglich, keine sklearn-Calls)
- Kurze `BERICHT.md`: für Use-Case 3 (Bildungs-Drop-out) — würdest du das überhaupt deployen? Begründung.

## Wann gilt es als gelöst?

- Maschinenbau-Profil → Modell ist LightGBM oder XGBoost (Latenz + Datenmenge)
- Mandanten-Churn → Bias-Audit ist Pflicht (AGG-Merkmale enthalten)
- Bildungs-Drop-out → AI-Act-Hochrisiko-Markierung + DSFA-Pflicht im Output
- Smoke-Test grün: 4 Asserts laufen

## Wenn du steckenbleibst

- [Grinsztajn et al. 2022 — Tree-based vs. DL on Tabular](https://arxiv.org/abs/2207.08815)
- [Hardt et al. 2016 — Equality of Opportunity (EOpp)](https://arxiv.org/abs/1610.02413)
- [Microsoft Fairlearn Docs](https://fairlearn.org/)
- [BaFin Fokusrisiken Digitalisierung 2026](https://www.bafin.de/DE/Aufsicht/Fokusrisiken/Fokusrisiken_2026/RIF_Trend_1_digitalisierung/RIF_Trend_1_digitalisierung_node.html)

## Compliance-Check

Bevor irgendein KMU-Modell live geht:

- [ ] AI-Act-Klassifizierung dokumentiert (Phase 20.01)
- [ ] DSFA bei AGG-Merkmalen pflicht (DSGVO Art. 35)
- [ ] AVV mit Sklearn-/XGBoost-Hosting (oft eigene Server, dann nur intern)
- [ ] Bias-Audit-Schwellen vor dem Live-Schalten festgelegt (DP < 5 %, EOpp < 10 %)
- [ ] Reproduzierbarer Trainings-Run mit MLflow-3-Logging (Phase 03.03)
