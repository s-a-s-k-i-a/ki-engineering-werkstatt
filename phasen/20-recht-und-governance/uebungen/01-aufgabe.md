# Übung 20.01 — Klassifiziere DEIN System

> Schwierigkeit: leicht · Zeit: 60 Min · Voraussetzungen: Lektion 20.01.

## Ziel

Du wendest die AI-Act-Klassifizierung auf ein eigenes (oder Lehrgut-)KI-System an und erstellst die zugehörigen Compliance-Artefakte.

## Aufgabe

1. Wähle ein KI-System (eigenes Projekt oder eines aus Phase 19)
2. Erstelle eine `model-card.yaml` analog zu `vorlagen/model-card-tierheim-bot.yaml`
3. Lasse `ki-act-classifier --modell-karte deine-model-card.yaml` laufen
4. Notiere das Ergebnis (Risiko-Klasse + Pflichten)
5. Erstelle die zugehörigen Artefakte:
   - Bei **inakzeptabel**: dokumentiere die verbotenen Praktiken — System wird nicht gebaut
   - Bei **hochrisiko**: starte DSFA mit Vorlage `vorlagen/dsfa-template.md`
   - Bei **begrenzt**: ergänze Transparenz-Hinweise in der Anwendung
   - Bei **minimal**: dokumentiere AI-Literacy-Plan (Art. 4)

## Bonus

- Mappe deine Pflichten auf konkrete Tasks im Repo (Issues anlegen)
- Schreibe einen 200-Wort-Compliance-Plan
- Erstelle eine Audit-Logging-Konfig nach Lektion 20.05

## Abgabe

- `model-card.yaml` in deinem Projekt-Ordner
- Klassifizierungs-Output (JSON via `--als-json` redirected nach `klassifizierung.json`)
- DSFA / Compliance-Plan als `compliance.md`

## Wann gilt es als gelöst?

- `ki-act-classifier` exit-code 0 (oder 2 bei Inakzeptabel mit dokumentiertem „nicht gebaut"-Block)
- DSFA-Template ist konkret ausgefüllt (keine `<TODO>`-Platzhalter mehr)
- Alle Pflichten aus dem Klassifizierungs-Output sind als Issue oder im Compliance-Plan adressiert
