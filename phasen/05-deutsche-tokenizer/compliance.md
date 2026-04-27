---
id: 5
phase: 05-deutsche-tokenizer
stand: 2026-04-27
anker:
  - datenresidenz-embedding-provider
  - bafa-zertifizierung-aleph-alpha
  - dataset-lizenz-10kgnad
dsgvo_artikel:
  - art-28
  - art-44
ai_act_artikel:
  - art-13
---

# Compliance-Anker — Phase 05

## Datenresidenz Embedding-Provider

Embeddings sind nicht „nur Zahlen" — wer Texte bei einem Cloud-Provider zum Embedden hochlädt, transferiert die Original-Strings inklusive eventuellem Personenbezug. Tabelle:

| Provider | Server-Standort | AVV | Empfehlung |
|---|---|---|---|
| Aleph Alpha Luminous Embeddings | Heidelberg | ✓ | sehr empfohlen für DE |
| Mistral Embed | Frankreich | ✓ | empfohlen für mehrsprachig |
| OpenAI text-embedding-3 | USA (EU-Routing optional) | DPA | nur mit EU-Routing + Zero-Retention |
| Cohere Embed v3 | USA + EU-Region | DPA | EU-Region wählen |
| HF Inference (Sentence-Transformers) | je nach Endpoint | varies | bei Self-Hosting unkritisch |
| Lokal (e5-mistral, bge-m3, GBERT) | lokal | n/a | maximale Datenhoheit |

## Aleph Alpha — BAFA-/BSI-Zertifizierungen

Aleph Alpha (Heidelberg) führt BSI C5 + ISO 27001 + BAFA-Aufstellung als „IT-Sicherheits-Vertrauensdienst". Wer im öffentlichen Sektor oder regulierten Branchen arbeitet, sollte das im Vergabe-Prozess erwähnen.

## 10kGNAD-Lizenz (Dataset im Hands-on)

`10kGNAD` ist **CC BY-NC-SA 4.0** — ausdrücklich nicht-kommerziell. Im Lehrkontext ok, für kommerzielle Folgeprojekte:

- Wikitext-DE (CC BY-SA 4.0)
- Common Crawl Multilingual (heterogen)
- OpenLegalData (für legal-Domain)
- Eigene anonymisierte Daten

Lizenz-Snapshots in [`datasets/lizenzen/`](../../datasets/lizenzen/).

## Embedding-Sicherheit (oft übersehen)

Embeddings können **invertierbar** sein. Beispiel: HF-Modell `vec2text` rekonstruiert Texte aus Embeddings mit ~92 % Wort-Treffer. Heißt:

- Embedding-Vektoren bekommen denselben Schutz wie der Originaltext
- Niemals roh in öffentlichen Vektor-DBs (öffentliches Qdrant Demo)
- Bei Auslagerung an Dienstleister: AVV greift

## AI-Act Art. 13 — Transparenz

Wer Embedding-Modelle in einem Hochrisiko-System nutzt: Modell-ID, Version, Provider, Updates dokumentieren.

## Quellen

- [Aleph Alpha Compliance-Whitepaper](https://aleph-alpha.com/security)
- [Morris et al. vec2text Paper](https://arxiv.org/abs/2310.06816)
- [10kGNAD Dataset Card](https://huggingface.co/datasets/10kGNAD)
- [Sennrich et al. BPE Paper](https://arxiv.org/abs/1508.07909)
