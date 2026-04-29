---
id: 04
titel: Computer Vision — VLMs, Image-Encoder, OCR, Edge-Vision
dauer_stunden: 10
schwierigkeit: mittel
stand: 2026-04-29
lernziele:
  - Open-Weights-VLM-Landschaft 2026 (Qwen3-VL, InternVL, LLaVA-OneVision, PaliGemma 2)
  - Image-Encoder + multilinguale Embeddings (SigLIP-2, DINOv3, jina-clip-v2)
  - OCR + Document-Understanding (LightOnOCR-2-1B, Tesseract, VLM-OCR)
  - Edge-VLM (MiniCPM-o, SmolVLM2) für Mobile + Browser
  - VLM-Inference-Stacks (vLLM, SGLang, Transformers)
  - End-to-End DSGVO-konforme Rechnungs-OCR-Pipeline
---

# Phase 04 · Computer Vision

> **Stop sending every image to the cloud.** — 2026 ist Edge-VLM (MiniCPM-o, SmolVLM2) auf GPT-4o-Niveau. Cloud-VLM (Qwen3-VL-235B Apache 2.0) für komplexe Tasks, OCR-spezialisiert (LightOnOCR-2-1B) für Document-Understanding.

**Status**: ✅ vollständig ausgearbeitet · **Dauer**: ~ 10 h · **Schwierigkeit**: mittel

## 🎯 Was du in diesem Modul lernst

- **VLM-Landschaft**: vier Open-Weights-Familien + ihre Use-Cases
- **Image-Encoder**: SigLIP-2 (Google), DINOv3 (Meta), jina-clip-v2 (Berlin) für Multi-modale RAG
- **OCR-Pfade**: LightOnOCR-2-1B als 2026-Default, VLM-OCR, Tesseract als Ergänzung
- **Edge-VLM**: MiniCPM-o auf iPhone, SmolVLM2 im Browser
- **Inference-Stacks**: vLLM mit Qwen3-VL (FP8 + YaRN)
- **End-to-End-Hands-on**: DSGVO-konforme Rechnungs-OCR-Pipeline mit PII-Filter

## 📚 Inhalts-Übersicht

| Lektion | Titel | Datei |
|---|---|---|
| 04.01 | VLM-Landschaft 2026 | [`lektionen/01-vlm-landschaft.md`](lektionen/01-vlm-landschaft.md) ✅ |
| 04.02 | Image-Encoder + Multilinguale Embeddings | [`lektionen/02-image-encoder-embeddings.md`](lektionen/02-image-encoder-embeddings.md) ✅ |
| 04.03 | OCR + Document-Understanding | [`lektionen/03-ocr-document-understanding.md`](lektionen/03-ocr-document-understanding.md) ✅ |
| 04.04 | Edge-VLM (MiniCPM-o, SmolVLM2) | [`lektionen/04-edge-vlm.md`](lektionen/04-edge-vlm.md) ✅ |
| 04.05 | VLM-Inference-Stacks (vLLM, SGLang, Transformers) | [`lektionen/05-vlm-inference-stacks.md`](lektionen/05-vlm-inference-stacks.md) ✅ |
| 04.06 | **Hands-on**: DSGVO-konforme Rechnungs-OCR | [`lektionen/06-hands-on-rechnungs-ocr.md`](lektionen/06-hands-on-rechnungs-ocr.md) ✅ |

## 💻 Hands-on-Projekt

**VLM-Selektor**: Marimo-Notebook, das je nach Hardware (Smartphone / RTX 4090 / H100), Use-Case (OCR / Allgemein / Edge / Multi-Modal) und Compliance-Tier das passende VLM empfiehlt. Stand 29.04.2026.

```bash
uv run marimo edit phasen/04-computer-vision/code/01_vlm_selektor.py
```

## 🧱 VLM-Wahl 2026 (Faustregel)

| Use-Case | Empfehlung |
|---|---|
| **Mobile / Edge (8 GB RAM)** | MiniCPM-o 2.6 oder SmolVLM2-2.2B |
| **RTX 4090 lokal** | Qwen3-VL-32B Q4_K_M oder InternVL3.5-8B |
| **OCR-spezialisiert** | LightOnOCR-2-1B (Pixtral + Qwen3-Decoder) |
| **Server-Production** | Qwen3-VL-235B-A22B-MoE auf H100/H200 |
| **Multi-modale RAG (DACH)** | jina-clip-v2 (Berlin) für DE-Image-Embedding |
| **Browser** | SmolVLM2-256M via Transformers.js + WebGPU |

## ⚖️ DACH-Compliance-Anker

→ [`compliance.md`](compliance.md): AI-Act Art. 5 (Verbote für Face-Use-Cases), DSGVO Art. 9 (biometrische Daten = besondere Kategorie), DSGVO Art. 25 (on-device-Edge-VLM für PII-haltige Bilder).

## 🔄 Wartung

Stand: 29.04.2026 · Reviewer: Saskia Teichmann ([@s-a-s-k-i-a](https://github.com/s-a-s-k-i-a)) · Nächster Review: 07/2026 (Qwen3-VL-Updates, MiniCPM-Roadmap, AI-Act-02.08.2026-Status).
