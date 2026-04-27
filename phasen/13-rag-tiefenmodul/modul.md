---
id: 13
titel: RAG-Tiefenmodul — Vanilla bis Agentic mit deutschen Daten und EU-LLMs
dauer_stunden: 14
schwierigkeit: mittel
stand: 2026-04-27
lernziele:
  - Das gesamte RAG-Spektrum 2026 souverän einsetzen
  - Vanilla-RAG, Hybrid-Retrieval, ColBERT, Re-Ranking, GraphRAG, LazyGraphRAG, Agentic RAG abgrenzen
  - RAG-Architektur nach Use-Case wählen, nicht nach Hype
  - Ragas-Metriken (faithfulness, answer-relevancy, context-precision) interpretieren
  - Quellen-Attribution nach AI-Act Art. 50.4 sauber implementieren
---

# RAG-Tiefenmodul

> Stop pasting whole documents into prompts. — RAG ist 2026 das Standard-Pattern für Wissens-Anwendungen.

Showcase-Modul der KI-Engineering-Werkstatt. Im Original (rohitg00) hat RAG nur eine kurze Sektion — hier ein vollständiges Vertiefungsmodul mit deutschen Datenbasen.

## Was du danach kannst

- Du baust 7 RAG-Varianten (Vanilla, Hybrid, ColBERT/Late-Interaction, Re-Ranking, GraphRAG, LazyGraphRAG, Agentic) auf demselben deutschen Korpus
- Du misst RAG-Qualität mit Ragas — und weißt, was die Werte konkret bedeuten
- Du wählst die richtige Variante: Vanilla für FAQ, Hybrid für Code-Doku, ColBERT für Recht, GraphRAG/LazyGraphRAG für komplexe Wissensbasen
- Du implementierst Quellen-Attribution AI-Act-konform

## Inhalts-Übersicht

| Lektion | Titel | Dauer |
|---|---|---|
| 13.01 | Vanilla RAG: Chunk → Embed → Retrieve → Generate | 60 min |
| 13.02 | Hybrid Retrieval: BM25 + Dense + Reciprocal Rank Fusion | 60 min |
| 13.03 | ColBERT/Late-Interaction (jina-colbert-v2 mehrsprachig) | 60 min |
| 13.04 | Re-Ranking mit bge-reranker-v2-m3 | 45 min |
| 13.05 | GraphRAG (Microsoft 2024) | 90 min |
| 13.06 | LazyGraphRAG (Microsoft 2025) — 700× günstiger | 60 min |
| 13.07 | Agentic RAG: Self-RAG, Corrective RAG | 90 min |
| 13.08 | Eval mit Ragas: faithfulness, answer-relevancy, context-precision | 60 min |
| 13.09 | Quellen-Attribution AI-Act-konform | 30 min |

## Hands-on (Pflicht)

Vier RAG-Varianten auf demselben deutschen Wikipedia-Subset (Themen: Recht, Tierwelt, Geschichte) mit Ragas-Score + Latenz + EUR-Kosten-Vergleich. Pharia-1 vs. Mistral-Large als Generator.

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/s-a-s-k-i-a/ki-engineering-werkstatt/blob/main/dist-notebooks/phasen/13-rag-tiefenmodul/code/01_vanilla_rag.ipynb)

## Voraussetzungen

- Phase 00 (Werkstatt einrichten)
- Phase 05 (Tokenizer + Embeddings für Deutsch)
- Phase 11 (LLM-Engineering Grundlagen)

## Status

✅ Showcase-Modul — Vanilla RAG voll ausgearbeitet, weitere Varianten als Skelett.
