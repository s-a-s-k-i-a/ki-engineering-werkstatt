---
id: 10.02
titel: Tokenizer-Training — SentencePiece, HF tokenizers, BPE für DE-Korpus
phase: 10-llm-von-null
dauer_minuten: 60
schwierigkeit: fortgeschritten
stand: 2026-04-29
voraussetzungen: [05.01, 10.01]
lernziele:
  - SentencePiece für BPE-Training mit DE-Korpus
  - HF tokenizers (Rust) für schnelles BPE
  - Komposita-Effizienz im eigenen Tokenizer prüfen
  - tiktoken als Vergleich (nur Inferenz)
compliance_anker:
  - tokenizer-reproducibility
ai_act_artikel:
  - art-10
---

## Worum es geht

> Stop using English BPE for German. — Phase 05 hat gezeigt: deutsche Komposita werden in englisch-trainierten Tokenizern bis zu 30 % ineffizienter kodiert. Diese Lektion zeigt, wie du **dein eigenes BPE** auf DACH-Korpus trainierst.

## Voraussetzungen

- Phase 05.01 (BPE + Deutsch — Komposita-Problem)
- Lektion 10.01 (Pretraining-Frameworks)

## Konzept

### Drei Tokenizer-Tools 2026

| Tool | Zweck | Lizenz | Wann |
|---|---|---|---|
| **SentencePiece** (Google) | BPE / Unigram-Training | Apache 2.0 | Standard für from-scratch |
| **HF tokenizers** (Rust-Backend) | schnelles BPE für große Korpora | Apache 2.0 | Production-Speed |
| **tiktoken** (OpenAI BPE) | Inferenz-only, kein Custom-Training | MIT | Vergleichs-Tokenizer |

### SentencePiece für DE-Korpus

URL: <https://github.com/google/sentencepiece>

```bash
# Train auf 1 GB DE-Text (Aleph-Alpha-GermanWeb-Subset)
spm_train \
    --input=de_corpus_1gb.txt \
    --model_prefix=tokenizer_de_v1 \
    --vocab_size=32000 \
    --model_type=bpe \
    --character_coverage=1.0 \
    --normalization_rule_name=nmt_nfkc \
    --num_threads=8
```

Wichtige Flags:

- `--character_coverage=1.0` für DE (kleiner Charset → 1.0; bei JP/CN: 0,9995)
- `--vocab_size=32000` Standard-Range; kleinere Modelle: 16k, größere: 64k
- `--normalization_rule_name=nmt_nfkc` für saubere Unicode-Normalisierung

### HF tokenizers (Rust-Backend)

URL: <https://huggingface.co/docs/tokenizers>

```python
from tokenizers import Tokenizer
from tokenizers.models import BPE
from tokenizers.trainers import BpeTrainer
from tokenizers.pre_tokenizers import Whitespace

tokenizer = Tokenizer(BPE(unk_token="[UNK]"))
tokenizer.pre_tokenizer = Whitespace()

trainer = BpeTrainer(
    vocab_size=32000,
    special_tokens=["[UNK]", "[CLS]", "[SEP]", "[PAD]", "[MASK]"],
    initial_alphabet=list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜäöüß"),
)

tokenizer.train(files=["de_corpus_1gb.txt"], trainer=trainer)
tokenizer.save("tokenizer-de-v1.json")
```

> Vorteil HF tokenizers: Rust-Backend = ~ 10× schneller als SentencePiece-Python-Binding. Nachteil: weniger Tokenizer-Familien (BPE, WordPiece, Unigram, ByteLevel).

### tiktoken als Vergleich

URL: <https://github.com/openai/tiktoken>

```python
import tiktoken

# OpenAI's o200k_base (GPT-4o + 5.x) für Vergleich
enc = tiktoken.get_encoding("o200k_base")
text = "Personenkraftwagenverkehrsbestimmungen"
tokens = enc.encode(text)
print(f"o200k_base: {len(tokens)} Tokens für 1 Wort")
# Output: ~ 9 Tokens (ineffizient bei dt. Komposita)
```

Gegen-Test mit eigenem DE-Tokenizer:

```python
mein_tokenizer = Tokenizer.from_file("tokenizer-de-v1.json")
de_tokens = mein_tokenizer.encode(text).tokens
print(f"DE-Tokenizer: {len(de_tokens)} Tokens")
# Output: ~ 4–5 Tokens (deutlich besser)
```

### Komposita-Effizienz-Check

```python
def komposita_test(tokenizer, samples=None):
    """Wie effizient kodiert der Tokenizer dt. Komposita?"""
    samples = samples or [
        "Donaudampfschifffahrtsgesellschaft",
        "Personenkraftwagenverkehrsbestimmungen",
        "Krankenhausverwaltungsorganisation",
        "Sozialversicherungsbeitragsberechnung",
        "Lebensversicherungsmathematik",
    ]
    avg_tokens = sum(len(tokenizer.encode(s).tokens) for s in samples) / len(samples)
    return avg_tokens


# Erwartung 2026:
# - tiktoken o200k_base: ~ 8–10 Tokens / Wort
# - DE-trainierter BPE 32k: ~ 3–5 Tokens / Wort
# - DE-trainierter BPE 64k (mehr Vocab für Komposita-Stems): ~ 2–4 Tokens
```

> Faustregel: pro Verdopplung des Vocab-Size sinkt die Token-Anzahl pro Wort um ~ 30 % bei DE-Komposita. Aber: größeres Vocab = größere Embeddings = mehr Memory.

### Vocab-Size-Trade-off

| Vocab-Size | Embedding-Memory (1B-Modell) | DE-Komposita-Effizienz |
|---|---|---|
| 16k | ~ 32 MB | mittel |
| **32k** | ~ 64 MB | gut (Standard) |
| 64k | ~ 128 MB | sehr gut |
| 128k | ~ 256 MB | optimal — aber kostet Memory |
| 200k+ | ~ 400 MB+ | nur Sinn bei Multilingual |

### Korpus-Vorbereitung

Pflicht-Schritte vor Tokenizer-Training:

```python
# 1. Sprach-Filter (siehe Phase 12.04)
texts = [t for t in texts if ist_deutsch(t)]

# 2. Umlaut-Normalisierung
import unicodedata
texts = [unicodedata.normalize("NFKC", t) for t in texts]

# 3. Quotes vereinheitlichen („..." → "...")
texts = [t.replace("„", '"').replace("“", '"') for t in texts]

# 4. Min-Length-Filter
texts = [t for t in texts if len(t) >= 50]

# 5. Dedupe
texts = list(set(texts))

# 6. Speichern als 1-Zeile-pro-Sample
Path("de_corpus_1gb.txt").write_text("\n".join(texts))
```

### Reproduzierbarkeits-Manifest

Pflicht für AI-Act Art. 10:

```yaml
# tokenizer-manifest.yaml
tokenizer_name: "ki-werkstatt-de-v1"
algorithmus: "BPE"
vocab_size: 32000

trainings_korpus:
  pfad: "datasets/de_corpus_2026-04.txt"
  sha256: "abc123..."
  groesse_gb: 1.0
  quellen:
    - "Aleph-Alpha-GermanWeb (Subset 5%)"
    - "OSCAR-2301 DE-Subkorpus"
    - "FineWeb-2 DE"

filter_pipeline:
  - "fasttext DE >= 0.85"
  - "NFKC-Normalisierung"
  - "Quote-Unification"
  - "Min-Length 50 chars"
  - "Dedupe via Set"

hyperparameter:
  character_coverage: 1.0
  normalization_rule_name: "nmt_nfkc"

eval:
  komposita_test_avg_tokens: 4.2
  vergleich_tiktoken_o200k: 8.7
  effizienz_gewinn: "52 %"

zeitstempel: "2026-04-29T12:00:00Z"
```

### Tokenizer-zu-Modell-Pipeline

Der Tokenizer wird **vor** dem Pretraining trainiert. Im nanochat-Workflow:

```bash
# Schritt 1: Tokenizer trainieren (~ 10 Min auf RTX 4090)
python scripts/train_tokenizer.py \
    --corpus datasets/de_corpus_2026-04.txt \
    --vocab-size 32000 \
    --output tokenizer-de-v1.json

# Schritt 2: Korpus tokenisieren (~ 30 Min für 50B Tokens)
python scripts/tokenize_corpus.py \
    --tokenizer tokenizer-de-v1.json \
    --corpus datasets/de_corpus_2026-04.txt \
    --output datasets/tokens-de-v1.bin

# Schritt 3: Pretraining starten (mit nanochat / litgpt)
python scripts/pretrain.py \
    --tokens datasets/tokens-de-v1.bin \
    --tokenizer tokenizer-de-v1.json \
    --model-config nanochat-1.5b
```

## Hands-on

1. SentencePiece auf 100 MB DE-Sample (z. B. Wikipedia-DE-Subset)
2. HF tokenizers parallel — Speed-Vergleich
3. Komposita-Test gegen tiktoken o200k_base — Effizienz-Differenz
4. Vocab-Size-Variation: 16k vs. 32k vs. 64k — wo der Sweet-Spot?
5. Manifest committen für AI-Act-Reproduzierbarkeit

## Selbstcheck

- [ ] Du trainierst SentencePiece-BPE auf DE-Korpus.
- [ ] Du nutzt HF tokenizers für Production-Speed.
- [ ] Du misst Komposita-Effizienz gegen tiktoken.
- [ ] Du wählst Vocab-Size je nach Modell-Größe.
- [ ] Du dokumentierst Tokenizer-Manifest für Reproduzierbarkeit.

## Compliance-Anker

- **AI-Act Art. 10**: Trainings-Korpus dokumentiert + lizenziert
- **Reproduzierbarkeit**: Tokenizer + Korpus + Hyperparameter im Manifest

## Quellen

- SentencePiece — <https://github.com/google/sentencepiece>
- HF tokenizers — <https://huggingface.co/docs/tokenizers>
- tiktoken — <https://github.com/openai/tiktoken>
- HF Tokenizer Summary — <https://huggingface.co/docs/transformers/tokenizer_summary>
- Aleph-Alpha-GermanWeb — <https://huggingface.co/datasets/Aleph-Alpha/Aleph-Alpha-GermanWeb>

## Weiterführend

→ Lektion **10.03** (DE-Pretraining-Daten in Detail)
→ Phase **05.01** (BPE + Deutsch — Theorie)
→ Lektion **10.01** (Pretraining-Frameworks)
