# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "marimo",
#   "numpy>=2.0",
# ]
# ///

"""Lösung 13.01 (Skelett) — wird mit echten Embeddings + 50 Artikeln befüllt.

Dieses Lösungs-Skelett ist intentional minimal: es zeigt das *Pattern* einer
echten Lösung (Imports, Funktions-Stubs, TODO-Markierungen) und ist
smoke-test-tauglich, weil keine externen Modelle geladen werden.

Wer die Übung wirklich macht, ersetzt die Stubs durch echte Calls — die
Lösung liegt dann im jeweiligen Fork des Lernenden.
"""

import marimo

__generated_with = "0.10.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    mo.md(
        r"""
        # Lösungs-Skelett — Übung 13.01

        Dies ist ein **Skelett**. Im Smoke-Test läuft es ohne externe Modelle durch.
        Für die echte Lösung ersetze die TODO-Stubs durch:

        - `datasets.load_dataset("Cohere/wikipedia-22-12-de-embeddings")`
        - `SentenceTransformer("intfloat/multilingual-e5-large-instruct")`
        - Ragas-Metriken via `from ragas import evaluate`

        Siehe Übungs-Hinweise in [`uebungen/01-aufgabe.md`](../uebungen/01-aufgabe.md).
        """
    )
    return


@app.cell
def _():
    """TODO 1: Lade 50 dt. Wikipedia-Artikel via `datasets`."""
    # from datasets import load_dataset
    # ds = load_dataset("Cohere/wikipedia-22-12-de-embeddings", split="train[:50]")
    n_articles_target = 50
    return (n_articles_target,)


@app.cell
def _():
    """TODO 2: Lade Embedding-Modell."""
    # from sentence_transformers import SentenceTransformer
    # model = SentenceTransformer("intfloat/multilingual-e5-large-instruct")
    embedding_model = None
    return (embedding_model,)


@app.cell
def _():
    """TODO 3: Implementiere Chunking."""
    # from langchain_text_splitters import RecursiveCharacterTextSplitter
    # splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=50)
    chunk_size = 400
    chunk_overlap = 50
    return chunk_overlap, chunk_size


@app.cell
def _(mo):
    """Liste der 5 Test-Fragen — diese darfst du jetzt füllen."""
    fragen = [
        "Was regelt die DSGVO seit Mai 2018?",
        "Welche Stufen hat das Inkrafttreten der KI-Verordnung?",
        "Wie groß ist das Tierschutz-Organisation in Deutschland?",
        "Wann wurde die Berliner Mauer gebaut?",
        "Welche Rolle hat das Bundesverfassungsgericht?",
    ]
    mo.md("### 5 Test-Fragen\n" + "\n".join(f"{i + 1}. {f}" for i, f in enumerate(fragen)))
    return (fragen,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ### TODO 4–6 (für deinen Fork)

        - Implementiere Embed → Retrieve → Generate-Loop
        - Variiere Chunk-Größe ∈ {200, 400, 800}
        - Berechne Ragas-Score (faithfulness + answer-relevancy + context-precision)
        - Plotte Score gegen Chunk-Größe als Linien-Diagramm
        - Schreibe Compliance-Notiz pro getesteten Provider

        Wenn du fertig bist: `just smoke` und PR.
        """
    )
    return


if __name__ == "__main__":
    app.run()
