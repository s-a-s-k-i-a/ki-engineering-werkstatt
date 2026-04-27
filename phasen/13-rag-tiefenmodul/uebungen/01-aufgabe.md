# Übung 13.01 — Vanilla RAG mit echten deutschen Artikeln

> Schwierigkeit: leicht-mittel · Zeit: 90 Min · Voraussetzungen: Lektion 13.01.

## Ziel

Du baust die TF-IDF-Pipeline aus dem Notebook auf einen echten Embedding-Stack um und evaluierst die Qualität.

## Aufgabe

1. Lade 50 deutsche Wikipedia-Artikel über `datasets`:

   ```python
   from datasets import load_dataset
   ds = load_dataset("Cohere/wikipedia-22-12-de-embeddings", split="train[:50]")
   ```

2. Ersetze TF-IDF durch ein echtes multilinguales Embedding-Modell:

   ```python
   from sentence_transformers import SentenceTransformer
   model = SentenceTransformer("intfloat/multilingual-e5-large-instruct")
   ```

3. Implementiere **Chunking** mit `langchain_text_splitters.RecursiveCharacterTextSplitter`:

   ```python
   from langchain_text_splitters import RecursiveCharacterTextSplitter
   splitter = RecursiveCharacterTextSplitter(
       chunk_size=400,
       chunk_overlap=50,
       separators=["\n\n", "\n", ". ", " "],
   )
   ```

4. Schreibe **5 deutsche Fragen** zu deinem Korpus.

5. Evaluiere mit Ragas:

   ```python
   from ragas import evaluate
   from ragas.metrics import faithfulness, answer_relevancy, context_precision
   ```

6. Teste **drei Chunking-Größen** (200, 400, 800 Tokens) und plotte Ragas-Score gegen Größe.

## Bonus

- Tausche `multilingual-e5-large-instruct` gegen `BAAI/bge-m3` und `Aleph-Alpha/Luminous-base-control` aus
- Vergleiche Latenz und Qualität in einem Boxplot
- Schreibe eine Compliance-Notiz: für jeden getesteten Provider, was bedeutet AVV-Lage und Datenresidenz?

## Abgabe

- Marimo-Notebook in `loesungen/01_loesung.py`
- Ragas-Score-Tabelle als `loesungen/01_metriken.csv`
- 200-Wort-Fazit am Ende: welche Konfiguration für welchen Use-Case?

## Wann gilt es als gelöst?

- `just smoke` läuft durch
- Mind. 3 Embedding-Modelle wurden verglichen
- Ragas-Metriken sind plausibel (faithfulness ≥ 0.7 für gute Konfigurationen)
- Quellen-Attribution ist AI-Act Art. 50.4 konform
