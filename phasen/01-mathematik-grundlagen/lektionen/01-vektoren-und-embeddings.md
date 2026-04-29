---
id: 01.01
titel: Vektoren als Bedeutungs-Richtungen — Embeddings und Kosinus-Ähnlichkeit
phase: 01-mathematik-grundlagen
dauer_minuten: 90
schwierigkeit: leicht
stand: 2026-04-29
voraussetzungen: []
lernziele:
  - Vektoren als Richtungen im Bedeutungs-Raum interpretieren
  - Kosinus-Ähnlichkeit von Hand berechnen und intuitiv verstehen
  - Den Unterschied Skalarprodukt vs. Kosinus kennen — und warum RAG-Systeme Kosinus nutzen
compliance_anker:
  - dataset-lizenz-10kgnad-cc-bync
ai_act_artikel:
  - art-10
---

<!-- colab-badge:begin -->
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/s-a-s-k-i-a/ki-engineering-werkstatt/blob/main/dist-notebooks/phasen/01-mathematik-grundlagen/code/01_embedding_explorer.ipynb)
<!-- colab-badge:end -->

## Worum es geht

> Stop fearing math. — Vektoren sind keine abstrakten Pfeile, sondern **Richtungen im Bedeutungs-Raum**. Wer Embeddings versteht, versteht 80 % von RAG, semantischer Suche und LLM-Internals.

Diese Lektion macht Embeddings konkret: deutsche Wörter werden zu Vektoren, Vektoren werden zu Ähnlichkeiten, Ähnlichkeiten werden zu Suchergebnissen. Alle Beispiele auf deutschen Wörtern (10kGNAD-Vokabular).

## Voraussetzungen

Keine. Schul-Mathematik (Vektoraddition, Wurzel ziehen) reicht.

## Konzept

### Was ist ein Vektor?

Ein **Vektor** ist eine Liste von Zahlen. Bei modernen Embeddings: 384, 768, 1024, 1536 oder 4096 Zahlen pro Wort.

```text
"Hund"  → [0.21, -0.45, 0.83, ..., 0.12]   # 768 Dimensionen
"Katze" → [0.18, -0.52, 0.79, ..., 0.15]
"Auto"  → [-0.61, 0.33, -0.21, ..., 0.88]
```

Die Magie: **semantisch ähnliche Wörter haben ähnliche Zahlen**. „Hund" und „Katze" sind sich näher als „Hund" und „Auto", weil das Embedding-Modell beim Training auf Millionen deutschen Sätzen gelernt hat: Hunde und Katzen tauchen in ähnlichen Kontexten auf.

### Kosinus-Ähnlichkeit — die Standard-Metrik für Embeddings

Die Frage „wie ähnlich sind zwei Vektoren?" beantwortet man 2026 fast immer mit **Kosinus-Ähnlichkeit**:

```text
cos(a, b) = (a · b) / (||a|| × ||b||)
```

Wo:

- `a · b` — Skalarprodukt (komponentenweises Produkt, dann Summe)
- `||a||` — Länge (L2-Norm) des Vektors a

**Wertebereich**: -1 bis +1.

- **+1** = identische Richtung (synonym)
- **0** = senkrecht (semantisch unabhängig)
- **-1** = entgegengesetzte Richtung (Antonym, theoretisch)

In Praxis (deutsche Embeddings): Werte zwischen 0.3 und 0.9 sind typisch. Alles über 0.85 wird in RAG meist als „starker Hit" gewertet.

### Warum nicht einfach Skalarprodukt?

Skalarprodukt `a · b` allein berücksichtigt **Länge** und **Richtung**. Bei Embeddings interessiert uns nur die **Richtung** — die Länge ist meist Modell-Artefakt (z.B. Häufigkeit eines Worts im Korpus).

**Beispiel**: Wenn der Vektor für „Hund" einfach 10× länger wäre als der für „Katze", würde Skalarprodukt mit „Hundeleine" einen höheren Wert geben — nicht weil „Hund" bedeutungsähnlicher ist, sondern weil der Vektor länger ist. Kosinus normalisiert das weg.

> **Praxis-Hinweis**: Viele moderne Embedding-Modelle (OpenAI text-embedding-3, Cohere embed-multilingual-v3, Mistral mistral-embed, Aleph Alpha luminous-embedding) liefern bereits **L2-normalisierte** Vektoren. Dann ist Kosinus = Skalarprodukt — und du kannst günstig Skalarprodukt rechnen.

### Klassisches Embedding-Spiel: König – Mann + Frau ≈ Königin

Das berühmteste Embedding-Beispiel (Mikolov et al., 2013, mit word2vec):

```text
v(König) - v(Mann) + v(Frau) ≈ v(Königin)
```

Auf Englisch funktioniert das mit word2vec robust. Auf **Deutsch** funktioniert es mit modernen Sentence-Transformern (BAAI/bge-m3, jina-embeddings-v3, mistral-embed) deutlich besser, weil sie Komposita und Umlaute besser handhaben.

**Achtung**: Dieser „Vector-Arithmetik"-Trick ist 2026 mehr Marketing als Praxis. Moderne Sentence-Embeddings sind nicht zwingend so linear-strukturiert. **Was zählt**: Kosinus-Ähnlichkeit für Retrieval funktioniert und ist die Basis von RAG.

## Code-Walkthrough

```python
import numpy as np

# Beispiel-Vektoren (vereinfacht, 4-dimensional)
hund = np.array([0.8, 0.6, 0.1, 0.0])
katze = np.array([0.7, 0.7, 0.1, 0.1])
auto = np.array([0.1, -0.3, 0.9, 0.4])

def kosinus(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

print(f"Hund ↔ Katze : {kosinus(hund, katze):.3f}")   # ~0.985
print(f"Hund ↔ Auto  : {kosinus(hund, auto):.3f}")    # ~-0.05
```

Mit echten Embeddings (deutsche Sentence-Transformer-Modelle):

```python
from sentence_transformers import SentenceTransformer

# bge-m3 ist 2026 Standard für DE/EN-mehrsprachige Embeddings (Apache 2.0)
modell = SentenceTransformer("BAAI/bge-m3")
saetze = ["Der Hund jagt die Katze.", "Die Katze flieht vor dem Hund.", "Das Auto fährt zur Werkstatt."]
emb = modell.encode(saetze, normalize_embeddings=True)  # L2-normalisiert!

# Mit normalisierten Vektoren ist Kosinus = Skalarprodukt
print(f"Satz 1 ↔ Satz 2 : {emb[0] @ emb[1]:.3f}")   # hoch
print(f"Satz 1 ↔ Satz 3 : {emb[0] @ emb[2]:.3f}")   # niedrig
```

## Hands-on

→ [`code/01_embedding_explorer.py`](../code/01_embedding_explorer.py)

Marimo-Notebook: gib eigene deutsche Wörter ein, bekomme Top-5 Nachbarn aus 10kGNAD-Vokabular zurück, plus Kosinus-Score-Tabelle. Smoke-test-tauglich (offline, kein HuggingFace-Download nötig).

## Selbstcheck

- [ ] Kannst du in einem Satz erklären, warum Kosinus statt Skalarprodukt?
- [ ] Berechne von Hand: Kosinus von `[1, 0]` und `[1, 1]`. (Lösung: `1/√2 ≈ 0.707`)
- [ ] Welche Embedding-Modelle sind 2026 für **deutsche** Texte stark? (Antwort: bge-m3, jina-embeddings-v3, multilingual-e5-large, mistral-embed)

## Compliance-Anker

- **AI-Act Art. 10** (Daten-Governance): Trainings-Korpus für Embeddings muss dokumentiert sein. 10kGNAD ist **CC BY-NC-SA 4.0** — nicht-kommerziell. Für Produktion: Wikitext-DE (CC BY-SA), GermEval (frei) oder eigene pseudonymisierte Korpora.
- **Datenresidenz**: OpenAI-Embeddings → US-Transfer (SCC + TIA). Aleph Alpha luminous-embedding (Heidelberg/post-Cohere) und mistral-embed (Paris) sind EU-konform. Lokal mit `bge-m3` ist die DSGVO-sicherste Variante.

→ [`compliance.md`](../compliance.md)

## Quellen

- Mikolov et al. (2013): „Efficient Estimation of Word Representations in Vector Space" — <https://arxiv.org/abs/1301.3781>
- BAAI (2024): bge-m3 Multilingual Embeddings — <https://huggingface.co/BAAI/bge-m3>
- Reimers & Gurevych (2019): Sentence-BERT — <https://arxiv.org/abs/1908.10084>
- 10kGNAD Dataset Card — <https://huggingface.co/datasets/10kGNAD>

## Weiterführend

- Phase 05 (Tokenizer): warum deutsche Wörter mehr Tokens brauchen
- Phase 13 (RAG): wie Kosinus zur Suche wird
