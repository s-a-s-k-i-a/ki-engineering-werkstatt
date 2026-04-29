---
id: 04.02
titel: Image-Encoder + Embeddings — SigLIP-2, DINOv3, jina-clip-v2
phase: 04-computer-vision
dauer_minuten: 45
schwierigkeit: mittel
stand: 2026-04-29
voraussetzungen: [04.01, 13.02]
lernziele:
  - Drei Image-Encoder-Familien abgrenzen (CLIP/SigLIP, DINO, Jina)
  - Multi-modale Embeddings für Image-Search
  - DACH-Daten: deutsche Texte + Bilder
compliance_anker:
  - bild-embedding-lizenz
ai_act_artikel:
  - art-15
---

## Worum es geht

> Stop using OpenAI CLIP from 2021. — 2026 sind SigLIP-2 (Google), DINOv3 (Meta) und jina-clip-v2 (Jina AI, DE-Standort) die produktiven Image-Encoder. Diese Lektion zeigt, wann welcher.

## Voraussetzungen

- Lektion 04.01 (VLM-Landschaft)
- Phase 13.02 (Embedding-Modelle)

## Konzept

### Drei Encoder-Familien

| Familie | Stärke | Lizenz | Stand 04/2026 |
|---|---|---|---|
| **SigLIP-2** | Multi-modal (Image+Text), multilingual | Apache 2.0 | ViT-B/L/So400m/g |
| **DINOv3** | Self-Supervised, kein Text-Pair nötig | kommerziell, Meta-Lizenz | 7B-Backbone |
| **jina-clip-v2** | DE-stark, EU-hosted (Berlin) | Apache 2.0 | 89 Sprachen |

### SigLIP-2 (Google, 20.02.2025)

URL: <https://huggingface.co/blog/siglip2>

- Verbessertes CLIP-Training mit Sigmoid-Loss
- Multilingual von Anfang an
- ViT-B / L / So400m (400M-Param) / g
- **NaFlex-Varianten**: native Auflösung statt Crop

> Der Default-Encoder vieler 2026-VLMs (Qwen3-VL, MiniCPM-o nutzen SigLIP-2-Linie).

### DINOv3 (Meta, 14.08.2025)

URL: <https://ai.meta.com/blog/dinov3-self-supervised-vision-model/>

- 7B-Backbone, 1.7 Mrd. Trainings-Bilder
- Pure self-supervised — kein Text-Paar nötig
- ConvNeXt-Varianten verfügbar
- Kommerzielle Lizenz (Meta) — Restrictions prüfen

**Wann DINOv3**: bei reinen Bild-Aufgaben (Klassifikation, Detection, Segmentierung) ohne Text-Anker. CLIP-Style fällt weg.

### jina-clip-v2 (Jina AI, Berlin)

URL: <https://jina.ai/models/jina-clip-v2/>

- 89 Sprachen inkl. DE
- Image+Text-Embedding für Multi-modale RAG
- **EU-hosted (Berlin)** — DSGVO-Bonus
- Apache 2.0
- Vorgänger jina-embeddings-v3 ist text-only

> Empfehlung 2026 für DACH-Multi-modale-RAG: **jina-clip-v2** wegen DE-Performance + EU-Standort.

### MobileCLIP2 (Apple, 08.2025)

URL: <https://github.com/apple/ml-mobileclip>

- Edge-CLIP für Smartphones
- In OpenCLIP integriert
- TMLR-veröffentlicht

Wann: Edge-Geräte, < 100M Params, kompakte Bild-Suche.

### Konkret nutzen — Multi-modale RAG

```python
from sentence_transformers import SentenceTransformer
from PIL import Image

# jina-clip-v2 für DE-Multi-modale RAG
modell = SentenceTransformer("jinaai/jina-clip-v2", trust_remote_code=True)

# Image-Embedding
bild = Image.open("foto.jpg")
bild_emb = modell.encode([bild])  # 1024-dim

# Text-Embedding (gleiche Vector-Space)
text_emb = modell.encode(["Eine Katze sitzt auf einem Stuhl"])

# Cosine-Similarity
import torch
sim = torch.nn.functional.cosine_similarity(
    torch.from_numpy(bild_emb), torch.from_numpy(text_emb)
)
print(f"Match-Score: {sim.item():.3f}")
```

### Vector-Stores für Bild-Embeddings

Wie bei Text-RAG (Phase 13):

| Store | EU-Standort | Multi-modal | Stand 04/2026 |
|---|---|---|---|
| **Qdrant Cloud** | Berlin / Frankfurt | ja | Standard für DACH |
| **Weaviate** | EU-Region verfügbar | ja | Vergleichbar |
| **pgvector** | self-hosted | ja | bei Postgres-zentriert |
| **Milvus / Zilliz** | self-hosted / US | ja | weniger verbreitet in DACH |

Empfehlung 2026: **Qdrant Cloud Berlin** + jina-clip-v2 für Bild-RAG.

### DACH-Multi-modale-Datasets

| Dataset | Größe | Lizenz | URL |
|---|---|---|---|
| **LAION-Multilingual** | sehr groß | CC-BY 4.0 | <https://laion.ai/projects/> |
| MS-COCO-DE (Übersetzung) | ~ 120k | community | <https://huggingface.co/datasets?search=coco-de> |
| Multi30k (DE-Captions) | 30k | community | <https://github.com/multi30k/dataset> |
| **OCR-D** (historische DE-Drucke, DFG) | groß | offen | <https://ocr-d.de/daten/> |
| German-OCR-3 (HF, Apache 2.0) | 200+ DE-Rechnungen | Apache 2.0 | <https://huggingface.co/Keyven/german-ocr-3> |

> **Warnung**: viele MS-COCO-DE-Übersetzungen sind community-übersetzt — Qualität schwankt. Für Production eigene Annotation oder LAION-Multilingual.

## Hands-on

1. jina-clip-v2 lokal laden (CPU reicht für 1024-dim)
2. 20 Bilder + DE-Captions embedden
3. Cosine-Similarity-Matrix → wer matcht wem?
4. Qdrant-Collection mit Multi-modalen Embeddings befüllen
5. Image-zu-Text und Text-zu-Image Suche testen

## Selbstcheck

- [ ] Du nennst SigLIP-2, DINOv3, jina-clip-v2 + ihre Stärken.
- [ ] Du nutzt jina-clip-v2 für DE-Multi-modale-RAG.
- [ ] Du legst Qdrant-Collection mit Bild-Embeddings an.
- [ ] Du kennst LAION-Multilingual als DACH-Daten-Quelle.

## Compliance-Anker

- **Lizenz**: Apache 2.0 für SigLIP-2 + jina-clip-v2 — frei kommerziell. DINOv3 mit Meta-Lizenz prüfen.
- **DSGVO**: jina-clip-v2 als EU-Anbieter bevorzugt.

## Quellen

- SigLIP-2 Blog — <https://huggingface.co/blog/siglip2>
- SigLIP-2 Paper — <https://arxiv.org/abs/2502.14786>
- DINOv3 — <https://ai.meta.com/blog/dinov3-self-supervised-vision-model/>
- jina-clip-v2 — <https://jina.ai/models/jina-clip-v2/>
- MobileCLIP2 — <https://github.com/apple/ml-mobileclip>

## Weiterführend

→ Lektion **04.03** (OCR mit LightOnOCR + Qwen3-VL)
→ Phase **13** (RAG-Tiefenmodul für Multi-modale Pipelines)
