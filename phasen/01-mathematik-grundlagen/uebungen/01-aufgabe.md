# Übung 01.01 — Eigenes Mini-Embedding + Perplexitäts-Eval

> Schwierigkeit: leicht · Zeit: 60–90 Min · Voraussetzungen: Lektionen 01.01–01.03

## Ziel

Du baust ein **Mini-Embedding-Modell** auf einem deutschen Mini-Korpus und evaluierst zwei LLM-Verteilungen mit **Cross-Entropy + Perplexität**. Ohne Deep-Learning-Frameworks — nur NumPy. Ziel: das Embedding-/Loss-Trio so weit verstanden zu haben, dass du es jeder Kollegin in 5 Min. erklären kannst.

## Use-Case

Ein DACH-KMU sammelt Customer-Support-Tickets in Deutsch und will die Tickets nach Themen-Cluster gruppieren — als Vorstufe für eine RAG-Pipeline (Phase 13). Bevor man Sentence-Transformers anwirft: erstmal verstehen, wie Embedding-Ähnlichkeit überhaupt funktioniert.

## Aufgabe

1. **Mini-Korpus** mit 25 deutschen Wörtern aus 5 Themen-Clustern (Tier / Fahrzeug / Möbel / Recht / Werkstatt)
2. **Embedding-Funktion** mit handgebauten Cluster-Richtungen (8-dimensional, L2-normalisiert)
3. **Kosinus-Ähnlichkeit-Funktion** (Skalarprodukt, da L2-normalisiert)
4. **Top-3-Nachbarn-Funktion** für ein gegebenes Wort
5. **Cross-Entropy-Funktion** über Wahrscheinlichkeitsverteilung
6. **Perplexitäts-Funktion** (`exp(CE)`)
7. **Eval auf 3 LLM-Verteilungen**: sehr-sicher-richtig, unsicher-richtig, sehr-sicher-falsch — die Perplexitäts-Reihenfolge muss passen
8. **5 Test-Asserts**: Cluster-Nachbarn intra-cluster > inter-cluster, Perplexitäts-Monotonie

## Bonus (für Schnelle)

- **PCA** (NumPy `np.linalg.eigh` auf Kovarianzmatrix) auf den 8D-Embeddings → 2D-Projektion plotten
- **KL-Divergenz** zwischen zwei Modell-Verteilungen berechnen + zeigen, dass `KL(p||q) ≠ KL(q||p)`
- **Gradient Descent** auf `f(w) = (w₀ - 3)² + (w₁ + 1)²` mit drei Lernraten (0.1 / 0.5 / 1.05) — divergent vs. konvergent
- **Echte Embeddings** mit `BAAI/bge-m3` (Vollversion mit `sentence-transformers`) — Kosinus-Ähnlichkeiten vergleichen

## Abgabe

- Marimo-Notebook in `loesungen/01_loesung.py` (smoke-test-tauglich)
- Kurze `BERICHT.md` (1 Absatz pro Test-Assert): was hast du beobachtet?

## Wann gilt es als gelöst?

- Top-3-Nachbarn von „Hund" sind alle Tier-Cluster-Wörter
- Top-3-Nachbarn von „Auto" enthalten kein Tier-Wort
- Perplexität steigt monoton: sehr-sicher-richtig < unsicher-richtig < sehr-sicher-falsch
- Mini-Korpus hat exakt 25 Wörter, 5 Cluster, je 5 Wörter
- Smoke-Test grün: alle 5 Asserts laufen ohne Exception

## Wenn du steckenbleibst

- [Mikolov et al. (2013) word2vec](https://arxiv.org/abs/1301.3781) — Original-Paper zu „König – Mann + Frau ≈ Königin"
- [Stanford CS224N: Word Vectors](https://web.stanford.edu/class/cs224n/) — Vorlesung mit Visualisierungen
- [bge-m3 Model Card](https://huggingface.co/BAAI/bge-m3) — moderne deutsche Sentence-Embeddings
- Wenn `np.log(0)` → benutze Epsilon `1e-12`

## Compliance-Check

Vor produktivem Einsatz auf realen Customer-Support-Tickets:

- [ ] Trainings-Korpus dokumentiert (Phase 02 Art. 10 AI-Act)
- [ ] Personenbezogene Daten in Tickets pseudonymisiert (DSGVO Art. 25)
- [ ] Bei kommerziellem Einsatz: Korpus-Lizenz prüfen (10kGNAD = CC BY-NC-SA → Wikitext-DE als Alternative)
- [ ] Drittland-Transfer prüfen, falls Embeddings via OpenAI/Cohere generiert werden (DSGVO Art. 44)
