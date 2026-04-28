# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "marimo",
#   "numpy>=2.0",
# ]
# ///

"""Vanilla RAG — minimaler, smoke-test-tauglicher Prototyp ohne externe APIs.

Statt eines echten Embedding-Modells nutzen wir TF-IDF als Embedding-Stub.
Damit läuft das Notebook offline, in CI und ohne API-Keys. In der Vollversion
ersetzt du die TF-IDF-Vektoren durch sentence-transformers oder Aleph-Alpha-Embeddings.
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
        # Vanilla RAG auf deutschem Mini-Korpus

        Vier Schritte: **Chunken → Embedden → Retrieven → Generieren**.

        Wir nutzen TF-IDF als Embedding-Stub (offline & in CI lauffähig).
        Für echte Antwort-Qualität ersetzt du das durch:

        - `sentence-transformers/multilingual-e5-large-instruct` (lokal)
        - `aleph_alpha_client` mit `Luminous-base-control` (Heidelberg)
        - `mistralai` mit `mistral-embed` (Frankreich)
        """
    )
    return


@app.cell
def _():
    """Mini-Korpus mit 8 deutschen Wikipedia-Auszügen (paraphrasiert).

    In der Vollversion: lade 50+ echte Artikel via `datasets` aus
    `Cohere/wikipedia-22-12-de-embeddings` oder eigenem Wiki-Snapshot.
    """
    korpus = [
        {
            "id": 1,
            "titel": "Datenschutz-Grundverordnung (DSGVO)",
            "thema": "Recht",
            "text": (
                "Die Datenschutz-Grundverordnung ist eine Verordnung der Europäischen Union, "
                "mit der die Regeln zur Verarbeitung personenbezogener Daten durch private "
                "Unternehmen und öffentliche Stellen EU-weit vereinheitlicht werden. Sie ist "
                "seit dem 25. Mai 2018 anwendbar."
            ),
            "quelle": "Wikipedia DE — DSGVO",
            "lizenz": "CC BY-SA 4.0",
        },
        {
            "id": 2,
            "titel": "Verordnung über künstliche Intelligenz (KI-VO)",
            "thema": "Recht",
            "text": (
                "Die Verordnung (EU) 2024/1689, kurz KI-Verordnung oder AI Act, ist eine "
                "EU-Verordnung zur Regulierung von Systemen der künstlichen Intelligenz. "
                "Sie trat am 1. August 2024 in Kraft und gilt gestaffelt: Verbote ab 2025, "
                "GPAI-Pflichten ab August 2025, Hochrisiko-Pflichten ab August 2026."
            ),
            "quelle": "Wikipedia DE — KI-Verordnung",
            "lizenz": "CC BY-SA 4.0",
        },
        {
            "id": 3,
            "titel": "Hund (Haustier)",
            "thema": "Tierwelt",
            "text": (
                "Der Haushund ist ein Haustier und wird als Unterart des Wolfes eingeordnet. "
                "Hunde leben seit Jahrtausenden mit dem Menschen zusammen und werden in "
                "Deutschland in Tierschutz-Organisationen, bei privaten Haltern und in Zuchten gehalten. "
                "Die Adoption aus einer Tierschutz-Organisation ist ein verbreiteter Weg."
            ),
            "quelle": "Wikipedia DE — Hund",
            "lizenz": "CC BY-SA 4.0",
        },
        {
            "id": 4,
            "titel": "Tierschutzgesetz (Deutschland)",
            "thema": "Recht",
            "text": (
                "Das deutsche Tierschutzgesetz regelt den Schutz des Lebens und Wohlbefindens "
                "der Tiere. Niemand darf einem Tier ohne vernünftigen Grund Schmerzen, Leiden "
                "oder Schäden zufügen. Tierschutz-Organisationen unterliegen den "
                "Anforderungen des § 11 TierSchG."
            ),
            "quelle": "Wikipedia DE — Tierschutzgesetz",
            "lizenz": "CC BY-SA 4.0",
        },
        {
            "id": 5,
            "titel": "Hannover",
            "thema": "Geschichte",
            "text": (
                "Hannover ist die Hauptstadt des Landes Niedersachsen und neunte größte Stadt "
                "Deutschlands. Sitz des Tierschutzvereins Hannover und Umgebung e. V., der das "
                "größte Tierschutz-Organisation der Region betreibt. Die Stadt wurde im Zweiten "
                "Weltkrieg stark zerstört und nach 1945 wieder aufgebaut."
            ),
            "quelle": "Wikipedia DE — Hannover",
            "lizenz": "CC BY-SA 4.0",
        },
        {
            "id": 6,
            "titel": "Berliner Mauer",
            "thema": "Geschichte",
            "text": (
                "Die Berliner Mauer war eine Grenzbefestigung der DDR, die zwischen 1961 und "
                "1989 die DDR von West-Berlin abriegelte. Mit dem Mauerfall am 9. November "
                "1989 begann der Prozess der deutschen Wiedervereinigung."
            ),
            "quelle": "Wikipedia DE — Berliner Mauer",
            "lizenz": "CC BY-SA 4.0",
        },
        {
            "id": 7,
            "titel": "Wolf",
            "thema": "Tierwelt",
            "text": (
                "Der Wolf ist ein Raubtier aus der Familie der Hunde und Stammvater des "
                "Haushundes. In Deutschland war er bis Ende des 19. Jahrhunderts ausgerottet, "
                "kehrt aber seit der Jahrtausendwende über Polen wieder ein. Der Wolfsbestand "
                "wird vom Bundesamt für Naturschutz dokumentiert."
            ),
            "quelle": "Wikipedia DE — Wolf",
            "lizenz": "CC BY-SA 4.0",
        },
        {
            "id": 8,
            "titel": "Bundesverfassungsgericht",
            "thema": "Recht",
            "text": (
                "Das Bundesverfassungsgericht in Karlsruhe ist das höchste deutsche Gericht "
                "für Verfassungsfragen. Es wurde 1951 errichtet und entscheidet über "
                "Grundrechtsfragen, Organstreitigkeiten und die Vereinbarkeit von Gesetzen "
                "mit dem Grundgesetz."
            ),
            "quelle": "Wikipedia DE — Bundesverfassungsgericht",
            "lizenz": "CC BY-SA 4.0",
        },
    ]
    return (korpus,)


@app.cell
def _(korpus, mo):
    """Schritt 1+2: Chunking und Embedding (TF-IDF als Stub).

    Hier ist jeder Korpus-Eintrag bereits ein Chunk. Bei längeren Texten:
    `langchain_text_splitters.RecursiveCharacterTextSplitter` einsetzen.
    """
    import re
    from collections import Counter

    import numpy as np

    def tokenize_de(text: str) -> list[str]:
        text = text.lower()
        text = re.sub(r"[^a-zäöüß0-9 ]+", " ", text)
        return [w for w in text.split() if len(w) >= 2]

    # Vokabular bauen
    all_tokens: list[str] = []
    chunk_token_lists: list[list[str]] = []
    for c in korpus:
        toks = tokenize_de(c["text"])
        chunk_token_lists.append(toks)
        all_tokens.extend(toks)

    vocab = sorted(set(all_tokens))
    vocab_index = {w: i for i, w in enumerate(vocab)}

    # Document Frequency
    df = Counter()
    for toks in chunk_token_lists:
        for w in set(toks):
            df[w] += 1

    n_chunks = len(korpus)

    def tfidf_vector(tokens: list[str]) -> np.ndarray:
        tf = Counter(tokens)
        vec = np.zeros(len(vocab), dtype=np.float32)
        for w, count in tf.items():
            if w not in vocab_index:
                continue
            idf = np.log((1 + n_chunks) / (1 + df[w])) + 1
            vec[vocab_index[w]] = count * idf
        norm = np.linalg.norm(vec)
        if norm > 0:
            vec /= norm
        return vec

    chunk_vectors = np.stack([tfidf_vector(toks) for toks in chunk_token_lists])
    mo.md(
        f"### Embeddings\n"
        f"- {n_chunks} Chunks\n"
        f"- {len(vocab)}-dim TF-IDF-Vektoren\n"
        f"- L2-normiert (Cosine = Skalarprodukt)\n"
    )
    return chunk_vectors, np, tfidf_vector, tokenize_de


@app.cell
def _(chunk_vectors, korpus, mo, np, tfidf_vector, tokenize_de):
    """Schritt 3: Retrieval per Cosine-Similarity."""

    def retrieve(frage: str, top_k: int = 3) -> list[dict]:
        q_vec = tfidf_vector(tokenize_de(frage))
        sims = chunk_vectors @ q_vec
        top_idx = np.argsort(-sims)[:top_k]
        return [{**korpus[i], "score": float(sims[i])} for i in top_idx if sims[i] > 0]

    frage = "Wie kann ich einen Hund aus einem Tierschutz-Organisation in Deutschland adoptieren?"
    treffer = retrieve(frage, top_k=3)
    out = "\n\n".join(
        f"**[{t['id']}] {t['titel']}** (score={t['score']:.3f}, {t['thema']})\n  {t['text']}\n  *Quelle: {t['quelle']} ({t['lizenz']})*"
        for t in treffer
    )
    mo.md(f"### Retrieval\nFrage: *{frage}*\n\n{out}")
    return frage, retrieve, treffer


@app.cell
def _(frage, mo, treffer):
    """Schritt 4: Prompt-Bau und Stub-Antwort.

    In der Vollversion ersetzt du `stub_antwort` durch einen echten LLM-Aufruf:

    ```python
    from pydantic_ai import Agent
    agent = Agent(model="aleph-alpha:Pharia-1-LLM-7B-control")
    antwort = agent.run_sync(prompt).output
    ```
    """
    quellen_block = "\n".join(f"[{t['id']}] {t['titel']}: {t['text']}" for t in treffer)
    prompt = f"""Du bist eine hilfreiche Assistenz. Beantworte die Frage NUR auf Basis der folgenden Quellen.
Wenn die Quellen nicht reichen, sag das ausdrücklich.

Quellen:
{quellen_block}

Frage: {frage}

Antworte auf Deutsch und nenne die verwendeten Quellen-Nummern."""

    # Stub-Antwort für Smoke-Test (kein API-Call)
    stub_antwort = (
        "Aus den Quellen lässt sich entnehmen, dass es eine deutsche Tierschutz-Organisation "
        "vom Tierschutzverein Hannover und Umgebung e. V. in Burgwedel gibt [5]. "
        "Adoptionen aus Tierschutz-Organisationen sind nach § 11 Tierschutzgesetz reguliert [4]. "
        "Hunde sind als Haustiere ausdrücklich für die Adoption geeignet [3]. "
        "Für konkrete Schritte: Tierschutz-Organisation direkt kontaktieren — die Quellen liefern "
        "keine Detail-Anweisungen."
    )
    mo.md(
        f"### Prompt (gekürzt)\n```\n{prompt[:300]}...\n```\n\n"
        f"### Stub-Antwort (Vollversion: echtes LLM)\n{stub_antwort}\n\n"
        f"### Quellen-Attribution (AI-Act Art. 50.4 konform)\n"
        + "\n".join(f"- [{t['id']}] {t['quelle']} ({t['lizenz']})" for t in treffer)
    )
    return prompt, stub_antwort


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Was du in der Vollversion machst

        - Korpus auf 50+ Wikipedia-Artikel erweitern (`datasets.load_dataset("Cohere/wikipedia-22-12-de-embeddings")`)
        - TF-IDF durch echtes Multilingual-Embedding ersetzen (`sentence-transformers`)
        - Vektorstore: Qdrant lokal via Docker-Compose (siehe `infrastruktur/vektorstores/qdrant-compose.yml`)
        - LLM: Pharia-1 (Aleph Alpha) oder Mistral-Large (Mistral) — beide mit AVV
        - Eval mit Ragas (`faithfulness`, `answer-relevancy`, `context-precision`)
        - Quellen-Attribution mit Inline-Links und Datum

        ### Quellen

        - [Karpukhin et al. 2020 — Dense Passage Retrieval](https://arxiv.org/abs/2004.04906)
        - [Lewis et al. 2020 — RAG](https://arxiv.org/abs/2005.11401)
        - [Microsoft GraphRAG Paper 2024](https://arxiv.org/abs/2404.16130)
        - [LangChain Text Splitters Docs](https://python.langchain.com/docs/modules/data_connection/document_transformers/)
        """
    )
    return


if __name__ == "__main__":
    app.run()
