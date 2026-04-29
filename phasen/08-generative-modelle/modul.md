---
id: 08
titel: Generative Modelle — FLUX.2, LTX-2.3, TRELLIS.2, Watermark-Pflicht
dauer_stunden: 10
schwierigkeit: mittel
stand: 2026-04-29
lernziele:
  - Text-to-Image-Landschaft 2026 (FLUX.2 Apache 2.0 BFL Freiburg, SD 3.5, Midjourney)
  - Text-to-Video (LTX-2.3 als Open-Weights-Spitze, Sora 2, Veo 3.1)
  - Audio + 3D-Generation (MusicGen, Stable Audio, TRELLIS.2 vs. Hunyuan3D-EU-Falle)
  - UrhG § 44b TDM + AI-Act Art. 50.2 Watermark-Pflicht (ab 02.08.2026)
  - Mehrschicht-Watermark-Pipeline (C2PA + unsichtbar + Fingerprint)
---

# Phase 08 · Generative Modelle

> **Stop using Hunyuan3D in EU production.** — die Tencent-Lizenz schließt EU/UK/SK explizit aus. Stattdessen: **FLUX.2 [klein] (Apache 2.0, BFL Freiburg)** für Bilder, **LTX-2.3 (Lightricks)** für Video, **TRELLIS.2 (Microsoft)** für 3D. AI-Act Art. 50.2-Watermark-Pflicht ab 02.08.2026.

**Status**: ✅ vollständig ausgearbeitet · **Dauer**: ~ 10 h · **Schwierigkeit**: mittel

## 🎯 Was du in diesem Modul lernst

- **Text-to-Image**: FLUX.2 (BFL Freiburg, Apache 2.0!) als DACH-Default, SD 3.5 Community License, DALL-E EOL 12.05.2026
- **Text-to-Video**: LTX-2.3 als Open-Weights-Spitze (4K + Audio), Sora 2 / Veo 3.1 / Runway Gen-4.5
- **Audio + 3D**: MusicGen, Stable Audio Open, TRELLIS.2 (NICHT Hunyuan3D in EU!)
- **Recht**: UrhG § 44b TDM-Schranke + Opt-out (ai.txt, robots.txt, W3C-TDM-Rep)
- **AI-Act Art. 50.2** (ab 02.08.2026): Watermark-Pflicht (C2PA + unsichtbar + Fingerprint)
- **Hands-on**: Mehrschicht-Watermark-Pipeline für FLUX.2-Bilder

## 📚 Inhalts-Übersicht

| Lektion | Titel | Datei |
|---|---|---|
| 08.01 | Text-to-Image 2026 (FLUX.2, SD 3.5, Midjourney V8α) | [`lektionen/01-text-to-image.md`](lektionen/01-text-to-image.md) ✅ |
| 08.02 | Text-to-Video (Sora 2, Veo 3.1, Runway Gen-4.5, LTX-2.3) | [`lektionen/02-text-to-video.md`](lektionen/02-text-to-video.md) ✅ |
| 08.03 | Audio + 3D-Generation (Hunyuan3D-EU-Falle!) | [`lektionen/03-audio-3d-generation.md`](lektionen/03-audio-3d-generation.md) ✅ |
| 08.04 | **Recht**: UrhG § 44b + AI-Act Art. 50.2 + § 201b StGB | [`lektionen/04-recht-urheberrecht-watermark.md`](lektionen/04-recht-urheberrecht-watermark.md) ✅ |
| 08.05 | **Hands-on**: Multi-Layer-Watermark-Pipeline | [`lektionen/05-hands-on-watermark-pipeline.md`](lektionen/05-hands-on-watermark-pipeline.md) ✅ |

## 💻 Hands-on-Projekt

**Generative-Modell-Selektor**: Marimo-Notebook, das je Modalität (Image / Video / Audio / 3D) + Lizenz-Anforderung das passende Modell empfiehlt — inkl. Hunyuan3D-EU-Ausschluss-Warnung.

```bash
uv run marimo edit phasen/08-generative-modelle/code/01_generative_selektor.py
```

## 🧱 Generative-Wahl 2026 (Faustregel)

| Modalität | DACH-Default 2026 | Bemerkung |
|---|---|---|
| **Image** | **FLUX.2 [klein]** (Apache 2.0, BFL Freiburg) | Volle kommerzielle Freiheit |
| **Video** | **LTX-2.3** (Open-Weights, 4K + Audio) | DSGVO-strict-tauglich |
| **Audio (Music)** | **MusicGen large** (Meta, MIT) | OSS-Standard |
| **Audio (Effects)** | **Stable Audio Open Small** | Community License |
| **3D** | **TRELLIS.2** (Microsoft, 4B) | Hunyuan3D = ❌ in EU |
| Speed-Image | Z-Image Turbo, SDXL Lightning | 4–8 Steps |
| Premium-Image | FLUX.2 [pro] / Midjourney V8 | Subscription |

## ⚖️ DACH-Compliance-Anker

→ [`compliance.md`](compliance.md): UrhG § 44b TDM-Schranke + Opt-out, AI-Act Art. 50.2 (Watermark-Pflicht), § 201b StGB-Entwurf (Deepfake-Strafbarkeit), Hunyuan3D-EU-Ausschluss.

## 🔄 Wartung

Stand: 29.04.2026 · Reviewer: Saskia Teichmann ([@s-a-s-k-i-a](https://github.com/s-a-s-k-i-a)) · Nächster Review: 07/2026 (FLUX.2-Updates, EU-AI-Office-Code-of-Practice-Finalisierung Juni 2026, § 201b StGB-Verabschiedung).
