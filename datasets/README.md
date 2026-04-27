# Datasets

> Im Repo nur Mini-Samples (<1 MB). Echte Datasets via Manifest oder Hugging Face Hub.

## Struktur

```
datasets/
├── README.md            # diese Datei
├── samples/             # Mini-Auszüge für Soforttests, < 1 MB pro Datei
│   └── *.csv / *.json
├── manifests/           # YAML-Pointer auf HF / DVC
│   └── *.yaml
└── lizenzen/            # Pro Dataset: Lizenz-Snapshot mit Quelle und Datum
    └── *.md
```

## Bekannte deutsche Datasets

| Name | Lizenz | Verwendung |
|---|---|---|
| 10kGNAD | CC BY-NC-SA 4.0 | nicht-kommerziell |
| GermanQuAD | CC BY 4.0 | Pflicht-Attribution, kommerziell ok |
| GermEval (je Task) | varies | je Task prüfen |
| Common Voice DE | CC0 | frei |
| Wikitext-DE | CC BY-SA | Attribution + ShareAlike |
| OSCAR-DE | gemischt | Lizenz pro Quelle prüfen |
| Aleph-Alpha-GermanWeb | proprietär | nicht öffentlich |

## Wie Lade ich ein Dataset?

```python
from datasets import load_dataset

# Manifest-basiert
ds = load_dataset("Cohere/wikipedia-22-12-de-embeddings", split="train[:50]")
```

Lizenz-Snapshot in `lizenzen/<dataset>.md` aktuell halten.

## Compliance

- Kein Dataset mit Personenbezug ohne Einwilligungs-Doku
- Keine binären Modell-Gewichte commit (gigabyte-große Files via HF Hub)
- Bei eigenen Daten: synthetisch generieren oder anonymisieren
