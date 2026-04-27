---
id: 2
phase: 02-klassisches-ml
stand: 2026-04-27
anker:
  - hochrisiko-anhang-iii-5b
  - shap-erklaerbarkeit-pflicht
  - bias-test-pflicht
dsgvo_artikel:
  - art-22
  - art-35
ai_act_artikel:
  - art-13
  - art-15
---

# Compliance-Anker — Phase 02

## Kreditscoring = Hochrisiko (Anhang III Nr. 5b)

Wer ein Modell für Kreditwürdigkeitsprüfung baut — auch als Lernprojekt — sollte wissen: das ist Hochrisiko nach AI Act. Konsequenzen:

- **Risk-Management** (Art. 9), **Daten-Governance** (Art. 10), **Tech-Doku** (Art. 11), **Logging** (Art. 12), **Transparenz** (Art. 13), **Human Oversight** (Art. 14), **Accuracy/Robustness** (Art. 15)
- **Konformitätsbewertung + CE-Kennzeichnung** vor Inverkehrbringen
- **EU-Datenbank-Eintrag** (Anhang VIII)

Im Lernkontext nicht relevant — aber wer das Modell produktiv ausrollt, muss alle Pflichten erfüllen. Phase 20 vertieft.

## Automated Decision-Making (Art. 22 DSGVO)

Eine Kreditentscheidung allein durch Algorithmus = automatisierte Entscheidung. Betroffene haben Recht auf:

- Information über die Logik
- Menschliches Eingreifen
- Anfechtung

→ SHAP-Erklärung deckt einen Teil davon ab, ist aber nicht alleinige Lösung.

## DSFA-Pflicht (Art. 35)

Vor Inverkehrbringen eines Kreditscoring-Systems mit Personenbezug ist eine Datenschutz-Folgenabschätzung (DSFA) Pflicht. Template in [`docs/rechtliche-perspektive/dsgvo-checklisten.md`](../../docs/rechtliche-perspektive/dsgvo-checklisten.md).

## Bias-Test ist Pflicht

AI-Act Art. 10 fordert Repräsentativität der Trainingsdaten. Bei deutschen Kreditdaten: prüfe Bias gegen Postleitzahl, Geschlecht, Migrationshintergrund (Namens-Heuristik). AGG (Allgemeines Gleichbehandlungsgesetz) gilt parallel.

## Quellen

- [AI Act Anhang III](https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:32024R1689)
- [BaFin Fokusrisiken Digitalisierung 2026](https://www.bafin.de/DE/Aufsicht/Fokusrisiken/Fokusrisiken_2026/RIF_Trend_1_digitalisierung/RIF_Trend_1_digitalisierung_node.html)
- [Lundberg/Lee SHAP Paper](https://arxiv.org/abs/1705.07874)
