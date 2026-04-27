---
id: 5.01
titel: BPE, WordPiece, SentencePiece — und warum Deutsch teurer ist
phase: 05-deutsche-tokenizer
dauer_minuten: 60
schwierigkeit: mittel
stand: 2026-04-27
voraussetzungen: [0.01, 0.02]
lernziele:
  - Unterscheiden, was BPE, WordPiece und SentencePiece tun
  - Erklären, warum dieselbe deutsche Aussage in unterschiedlich vielen Tokens kodiert wird
  - Erkennen, wo der Komposita-Bias herkommt
compliance_anker:
  - datenresidenz-embedding-provider
colab_badge: false
---
<!-- colab-badge:begin -->
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/s-a-s-k-i-a/ki-engineering-werkstatt/blob/main/dist-notebooks/phasen/05-deutsche-tokenizer/code/01_tokenizer_showdown.ipynb)
<!-- colab-badge:end -->

## Worum es geht

> Stop assuming tokens are words. — sie sind Subwort-Einheiten, deren Größe vom Trainings-Korpus abhängt.

Zwei Tokenizer können denselben Satz in **vier vs. zwölf** Tokens kodieren. Bei deutschem Text passiert das ständig, weil die meisten verbreiteten Tokenizer auf englischlastigen Korpora trainiert wurden. Diese Lektion zeigt, warum.

## Voraussetzungen

- Du hast `uv sync` einmal ausgeführt (Phase 00)
- Du kennst Python-Listen und Strings

## Konzept

### 1. BPE (Byte-Pair Encoding)

Sennrich et al. (2016) — der Klassiker: starte mit einzelnen Bytes, fusioniere die häufigsten Paare iterativ. Das Vokabular wächst, bis die gewünschte Größe (z. B. 50.000 Tokens) erreicht ist.

GPT-Familien (1 bis 5), Mistral, Llama 3 nutzen BPE-Varianten.

### 2. WordPiece

Schuster & Nakajima (2012), bei BERT eingesetzt: ähnlich BPE, aber wählt das Paar mit der höchsten Wahrscheinlichkeitssteigerung statt der höchsten Frequenz.

GBERT, distil-bert-german nutzen WordPiece.

### 3. SentencePiece

Kudo & Richardson (2018): arbeitet auf Roh-Bytes (kein Pre-Tokenization), kann Whitespace mit-tokenisieren. Zwei Modi:

- **BPE-Mode** (wie GPT)
- **Unigram-Mode** (wahrscheinlichkeitsbasiert)

T5, mT5, Qwen, Pharia-1, Teuken-7B nutzen SentencePiece.

### 4. Warum Deutsch oft mehr Tokens braucht

Drei Effekte:

**(a) Komposita.** „Donau­dampf­schiff­fahrts­gesellschafts­kapitän" ist ein Wort. Englisch-trainierte BPEs sehen das nie und müssen es in 8–12 Subwörter zerlegen. Deutsch-trainierte Tokenizer (Pharia, Teuken) haben Komposita-Stamm-Tokens und schaffen das in 3–4.

**(b) Umlaute.** `ä`, `ö`, `ü`, `ß` sind in UTF-8 Multi-Byte. Wenn der Tokenizer keine deutschen Bytes als Atom hat, splittet er auf 2 Tokens pro Umlaut.

**(c) Wortlängen-Verteilung.** Deutsche Texte haben durchschnittlich 6,4 Buchstaben/Wort, englische 5,1. Die Tokenizer-Effizienz korreliert mit der mittleren Wortlänge.

## Code-Walkthrough

Im Marimo-Notebook [`code/01_tokenizer_showdown.py`](../code/01_tokenizer_showdown.py) sind die wichtigsten Schritte:

1. Laden eines Standard-Beispieltexts (~700 Wörter aus 10kGNAD).
2. Tokenisierung mit `tiktoken` (GPT-4o/5-Approximation), `transformers` (Llama 3, Mistral, GBERT) und `sentencepiece` (Pharia/Teuken-Stand-in).
3. Token-Anzahl, ggf. Token-Decoding pro Tokenizer ausgeben.
4. EUR-Kosten anhand der Provider-Preisliste (Stand April 2026).
5. Vergleichsdiagramm in `matplotlib`.

## Hands-on

Bearbeite `uebungen/01-aufgabe.md`. Du implementierst:

1. Tokenisierung von 5 selbstgewählten deutschen Texten (Sport, Recht, Technik, Belletristik, Werbung)
2. Erstellung einer Tabelle mit `pandas`
3. Eigenes Diagramm und kurze Auswertung („welcher Tokenizer für welchen Use-Case?")

## Selbstcheck

- [ ] Du kannst erklären, warum `tiktoken cl100k` für deutschen Text suboptimal ist.
- [ ] Du kannst zeigen, wie viele Tokens das Wort `Donaudampfschifffahrtsgesellschaftskapitän` in mindestens drei Tokenizern braucht.
- [ ] Du hast eine eigene Empfehlung pro Use-Case (Coding-Assistent vs. Behörden-Bot vs. Marketing-Texter).

## Compliance-Anker

- Wenn du Embedding-Provider nutzt, **Server-Standort** prüfen — siehe [`compliance.md`](../compliance.md).
- 10kGNAD ist CC BY-NC-SA — keine kommerzielle Wiederverwendung.
- Bei der Wahl deines Tokenizers: dokumentiere die Entscheidung in deiner Modell-Karte (AI-Act Art. 13).

## Quellen

- Sennrich et al. (2016): „Neural Machine Translation of Rare Words with Subword Units" — <https://arxiv.org/abs/1508.07909> (Zugriff 27.04.2026)
- Kudo & Richardson (2018): „SentencePiece" — <https://arxiv.org/abs/1808.06226>
- Aleph Alpha (2024): „Pharia-1 Technical Report" — <https://aleph-alpha.com/introducing-pharia-1-llm-transparent-and-compliant/>
- LLäMmlein (Schmidt et al., Würzburg, 2024) — <https://arxiv.org/abs/2411.11171>

## Weiterführend

→ Lektion 05.02 (Komposita-Tiefen­tauch­gang) und 05.03 (Showdown im Notebook).
