---
id: 1
phase: 01-mathematik-grundlagen
stand: 2026-04-27
anker:
  - dataset-lizenzen-verstehen
dsgvo_artikel:
  - art-5-abs-1-lit-c
ai_act_artikel:
  - art-10
---

# Compliance-Anker — Phase 01

## Lizenz-Hinweis 10kGNAD

Die in dieser Phase verwendeten deutschen Wort-Vektoren basieren auf dem 10kGNAD-Korpus, lizenziert unter **CC BY-NC-SA 4.0** — also ausdrücklich **nicht-kommerziell**.

→ Für kommerzielle Folgeprojekte: anderes Korpus wählen (Wikitext-DE = CC BY-SA, GermEval = teilweise frei). Siehe `datasets/lizenzen/`.

## Datenminimierung (Art. 5 Abs. 1 lit. c DSGVO)

Embeddings können personenbezogene Daten enthalten, wenn der Trainingstext Namen/Adressen enthielt. Bei eigenen Embeddings: pseudonymisierte Trainingsdaten verwenden.

## Daten-Governance (AI-Act Art. 10)

Hochrisiko-Systeme müssen Trainings-, Validierungs- und Testdaten dokumentieren. Wer eigene Embeddings als Teil eines Hochrisiko-Systems nutzt, dokumentiert die Quelle ab Phase 01.

## Quellen

- [10kGNAD Dataset Card](https://huggingface.co/datasets/10kGNAD)
- [GermEval Tasks](https://germeval.github.io/)
- [AI Act Art. 10](https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:32024R1689)
