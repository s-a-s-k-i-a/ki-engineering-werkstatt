---
id: 19
phase: 19-abschlussprojekte
stand: 2026-04-27
anker:
  - capstone-pflicht-dsfa
  - capstone-pflicht-modell-karte
  - capstone-pflicht-ai-act-klassifikation
dsgvo_artikel:
  - art-35
ai_act_artikel:
  - art-43
---

# Compliance-Anker — Phase 19

## Pflicht-Bestandteile jedes Capstone

Jeder Abschluss gilt erst als „done", wenn:

1. **AI-Act-Klassifikation** mit `werkzeuge/ai_act_classifier.py` — Output committet
2. **Modell-Karte** im Projekt-Verzeichnis (Template in Phase 20)
3. **DSFA-Light** in `compliance.md` des Capstones
4. **AVV-Liste** aller genutzten Cloud-Anbieter
5. **Quellen-Liste** (Datasets, Modelle, Code)
6. **Bias-Test-Bericht** (mind. Geschlecht und Region für deutsche Use-Cases)
7. **Self-Censorship-Audit**, falls asiatisches Modell genutzt

## Konformitätsbewertung (Art. 43)

Capstones, die **nicht** für reale Inverkehrbringung gedacht sind, brauchen keine Vollständige Konformitätsbewertung — aber die Doku-Struktur soll geübt werden.

## Verstoß-Fall

Wenn dein Capstone DSGVO-Verstöße enthält (z.B. realdaten ohne Einwilligung in HF-Dataset hochgeladen), wird der PR nicht gemerged. Lieber synthetische Test-Daten generieren.
