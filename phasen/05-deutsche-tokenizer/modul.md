---
id: 5
titel: Deutsche Tokenizer — Komposita, Umlaute, Token-Effizienz, EUR-Kosten
dauer_stunden: 6
schwierigkeit: mittel
stand: 2026-04-27
lernziele:
  - BPE/WordPiece/SentencePiece-Mechanik mit deutschem Korpus verstehen
  - Komposita-Problem auf Deutsch erklären können (warum `Donaudampfschifffahrtsgesellschaftskapitän` GPT-5 doppelt so viel kostet wie Pharia-1)
  - Token-Effizienz messen und in EUR-Kosten umrechnen
  - Tokenizer für deutsche Use-Cases nach Datenschutz, Effizienz, Kosten auswählen
  - Embedding-Provider mit deutscher Qualität bewerten
---

# Deutsche Tokenizer

> Stop wasting tokens on German compound words. — bei deutschem Text kannst du 30 % API-Kosten sparen, wenn du den richtigen Tokenizer wählst.

Ein Showcase-Modul der KI-Engineering-Werkstatt. Wer auch immer auf Deutsch produziert, sollte das gelesen haben.

## Was du danach kannst

- Du kennst die drei Tokenizer-Familien (BPE, WordPiece, SentencePiece) und ihre Annahmen
- Du verstehst, warum englisch-trainierte Tokenizer auf Deutsch ineffizient sind
- Du kannst denselben deutschen Text mit 6+ Tokenizern vergleichen und entscheiden, welcher für deinen Use-Case passt
- Du rechnest Token-Kosten in EUR um — nicht in „API-Calls" oder „Anfragen"

## Inhalts-Übersicht

| Lektion | Titel | Dauer |
|---|---|---|
| 05.01 | BPE/WordPiece/SentencePiece — wie funktioniert ein Tokenizer? | 60 min |
| 05.02 | Komposita & Umlaute — warum Deutsch teurer ist | 45 min |
| 05.03 | Token-Effizienz-Showdown (Hands-on Marimo-Notebook) | 90 min |
| 05.04 | Embeddings für deutsche Texte (e5, bge-m3, Pharia-Luminous) | 60 min |
| 05.05 | Tokenizer-Auswahl-Matrix für DACH-Use-Cases | 30 min |

## Hands-on (Pflicht)

Du tokenisierst denselben 10kGNAD-Artikel mit sechs Tokenizern (GPT-5 / Claude 4.7 / Llama 4 / Mistral Large / Pharia-1 / Teuken-7B), plottest Tokenanzahl + EUR-Kosten + semantische Granularität. Quintessenz: zwischen 0,05 € und 0,15 € für denselben Inhalt — bei Massen-Workloads schnell vierstellige Differenz pro Monat.

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/s-a-s-k-i-a/ki-engineering-werkstatt/blob/main/dist-notebooks/phasen/05-deutsche-tokenizer/code/01_tokenizer_showdown.ipynb)

## Voraussetzungen

- Phase 00 (Werkstatt einrichten)
- Optional: Phase 01 (Mathematik) für tiefe Embedding-Intuition

## Status

✅ Vollständig ausgearbeitet (Showcase-Modul Launch).
