<!-- Danke fürs Beitragen! Bitte das Folgende kurz beantworten. -->

## Was ändert sich?

<!-- 1-3 Sätze, was diese PR macht -->

## Warum?

<!-- Welches Problem löst das? Verlinke Issue/Discussion falls vorhanden. -->

## Art der Änderung

- [ ] Tippfehler / Sprachkorrektur
- [ ] Quellen-Update (`docs/quellen.md` oder Lektion)
- [ ] Code-Fix (Bug, nicht-lauffähiges Notebook)
- [ ] Neue Lektion / neue Übung
- [ ] Compliance-Update (AI Act, BfDI, DSK, EDPB)
- [ ] Werkzeug / CI-Workflow
- [ ] Strukturelle Änderung (RFC nötig — verlinke ADR)

## Lokale Tests grün?

```bash
just smoke
# ✓ alles grün?
```

- [ ] `just lint` grün
- [ ] `just typecheck` grün
- [ ] `just smoke` grün
- [ ] (falls Notebook geändert) `marimo edit ...` läuft durch
- [ ] (falls Lektion geändert) Quellen sind erreichbar (`lychee` lokal)

## Quellen

<!-- Pflicht für Lektionen + Compliance: mind. 3 Primärquellen mit Datum -->

- [Quelle 1](url) (Stand: YYYY-MM-DD)

## DCO

<!-- Bestätige, dass du den Verhaltens­kodex und DCO gelesen hast -->

- [ ] Mein Commit enthält `Signed-off-by:` (`git commit -s`)
- [ ] Ich respektiere `CODE_OF_CONDUCT.md` und die Stilrichtlinien
- [ ] Bei AI-generiertem Text: Ich habe ihn redigiert, geprüft und nehme die Verantwortung
