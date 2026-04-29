---
id: 08.02
titel: Text-to-Video 2026 — Sora 2, Veo 3.1, Runway Gen-4.5, LTX-2.3 (Open)
phase: 08-generative-modelle
dauer_minuten: 60
schwierigkeit: mittel
stand: 2026-04-29
voraussetzungen: [08.01]
lernziele:
  - Vier T2V-Familien abgrenzen
  - Open-Weights-Spitze: LTX-2.3 (4K + Audio)
  - Pricing-Realität für API-Anbieter
compliance_anker:
  - lizenz-falle-eu-ausschluss
  - ai-act-50-2-video-watermark
ai_act_artikel:
  - art-50
---

## Worum es geht

> Stop assuming Sora is the only T2V option. — 2026 hat **LTX-2.3 (Lightricks, 22B)** den Open-Weights-Thron mit **4K + Audio + lokaler Inferenz**. Veo 3.1 Lite ist günstig, Runway Gen-4.5 ist Benchmark-Spitze, Sora 2 ist abo-pflichtig.

## Voraussetzungen

- Lektion 08.01 (T2I)

## Konzept

### Vier T2V-Familien

| Familie | Stand | Pricing | Lizenz / Tier |
|---|---|---|---|
| **Sora 2** (OpenAI) | 10.01.2026 | API: $ 0,10/s @720p | nur Plus ($ 20/Mo) + Pro ($ 200/Mo) |
| **Veo 3.1 Lite** (Google) | 31.03.2026 | API: $ 0,05–0,60/s | AI Pro $ 19,99/Mo, AI Ultra $ 249,99 |
| **Runway Gen-4.5** | seit 12/2025 | proprietär | aktuell #1 auf Artificial Analysis (Elo 1247) |
| **LTX-2.3** (Lightricks) | 05.03.2026 | — (Open Weights!) | **22B + 4K + Audio + lokal** |
| HunyuanVideo (Tencent) | weiter aktiv | Open Weights | ⚠️ EU-Region-Ausschluss bei einigen Hunyuan-3D-Modellen prüfen |
| Mochi-1 (Genmo) | Apache 2.0 | — | technisch überholt |

### LTX-2.3 — Open-Weights-Spitze 2026

URL: <https://github.com/Lightricks/LTX-Video>

- **22B Parameter**
- Native **4K @ 50fps** mit synchronem Audio
- Vollständig offen, lokal lauffähig (auf H100/H200)
- Plus Desktop-Editor

```python
# LTX-Video lokal (vereinfachtes Beispiel)
from ltx_video import LTXVideoPipeline

pipe = LTXVideoPipeline.from_pretrained(
    "Lightricks/LTX-Video-2.3",
    torch_dtype="bfloat16",
).to("cuda")

video = pipe(
    "Eine Drohne fliegt über ein verschneites Bergpanorama bei Sonnenaufgang",
    duration_s=10,
    resolution="3840x2160",  # 4K
    fps=50,
    audio=True,
).video
video.save("alps.mp4")
```

### Sora 2 (OpenAI)

URL: <https://openai.com/index/sora-2/>

- Seit 10.01.2026 nur noch via Subscription:
  - **Plus** ($ 20/Monat) — Standard-Generation
  - **Pro** ($ 200/Monat) — Premium-Features
- API: $ 0,10/s @ 720p, Pro $ 0,30–0,50/s
- US-Cloud — **DSGVO-strict-Use-Cases ausgeschlossen**

### Veo 3.1 + Veo 3.1 Lite (Google)

URL: <https://blog.google/innovation-and-ai/technology/ai/veo-3-1-lite/>

- **Veo 3.1 Lite seit 31.03.2026** — ~ 50 % günstiger als Veo 3.1
- Pricing: $ 0,05–0,60/s
- Subscription: AI Pro $ 19,99/Mo, AI Ultra $ 249,99/Mo

### Runway Gen-4.5

URL: <https://runwayml.com/research/introducing-runway-gen-4.5>

- Seit Dezember 2025 Flagship
- Aktuell **#1 auf Artificial Analysis Benchmark** (Elo 1247, vor Veo 3.1 + Kling 3.0)
- Proprietär, US-basiert

### HunyuanVideo + EU-Lizenz-Falle

URL: <https://github.com/Tencent-Hunyuan/HunyuanVideo>

- **13B Parameter**, Tencent Hunyuan Community License
- Kommerziell ok, aber bei > 100 Mio. MAU gesondert lizenzieren
- ⚠️ **EU-Region-Ausschluss bei Hunyuan3D — bei Video-Variante License-Text prüfen**! (siehe Lektion 08.05)

### Mochi-1 (Genmo)

URL: <https://huggingface.co/genmo/mochi-1-preview>

- Apache 2.0
- 480p, 5,4 s
- Stand 04/2026: technisch überholt, Marktinteresse stark gefallen

### Wann welches Modell

| Use-Case | Empfehlung |
|---|---|
| **Open-Weights, 4K, lokal** | **LTX-2.3** |
| **Beste Quality (Cloud)** | Runway Gen-4.5 |
| **Preisbewusst** | Veo 3.1 Lite |
| **OpenAI-Stack-Affinität** | Sora 2 (Plus für Standard) |
| **Kommerziell + Forschung** | LTX-2.3 oder HunyuanVideo (Lizenz-Detail prüfen) |
| **DSGVO-strict** | nur LTX-2.3 self-hosted (alle anderen US/CN) |

### Compute-Realität für T2V (Open-Weights)

LTX-2.3 für 10 s @ 4K auf 1× H200:

- Inference-Zeit: ~ 4–8 Min
- VRAM: ~ 80 GB (FP8)
- Cost auf Scaleway: ~ € 0,30–0,50 pro Video

> Für 1080p reicht 1× H100. Für 4K + Audio: H200 (141 GB VRAM) empfohlen.

### AI-Act Art. 50.2 — Video-Watermark

Stand 04/2026 (voll wirksam ab 02.08.2026):

- **KI-erstellte Videos müssen markiert sein** (Standard: C2PA-Manifest)
- Plus unsichtbares Watermark in Frames
- Plus optional Audio-Watermark (siehe Lektion 06.05)

```python
# C2PA-Manifest in MP4 einbetten (mit c2patool)
import subprocess

subprocess.run([
    "c2patool", "video.mp4",
    "--manifest", "manifest.json",
    "--output", "video_signed.mp4",
])
```

## Hands-on

1. LTX-2.3 auf H100/H200 (Scaleway oder STACKIT) testen
2. 3 dt. Test-Prompts (Bürger-Service-Pikto, Hannover-Drone, Steuer-Office)
3. Cost + Latenz pro Video dokumentieren
4. C2PA-Manifest in einen Output einbetten
5. Vergleich gegen Sora 2 / Veo 3.1 Lite (falls API-Account)

## Selbstcheck

- [ ] Du nennst die vier T2V-Familien + ihre Stärken.
- [ ] Du wählst LTX-2.3 als Open-Weights-Default.
- [ ] Du kennst HunyuanVideo + die EU-Lizenz-Fallen.
- [ ] Du planst C2PA-Watermark in Production-Outputs.

## Compliance-Anker

- **AI-Act Art. 50.2**: Video-Watermark-Pflicht ab 02.08.2026
- **Lizenz-Disziplin**: HunyuanVideo bei großem Use-Case extra prüfen
- **§ 201b StGB-Entwurf**: Deepfake-Pattern bei Person-im-Video

## Quellen

- LTX-2.3 GitHub — <https://github.com/Lightricks/LTX-Video>
- Sora 2 — <https://openai.com/index/sora-2/>
- Veo 3.1 Lite — <https://blog.google/innovation-and-ai/technology/ai/veo-3-1-lite/>
- Runway Gen-4.5 — <https://runwayml.com/research/introducing-runway-gen-4.5>
- HunyuanVideo — <https://github.com/Tencent-Hunyuan/HunyuanVideo>
- Mochi-1 — <https://huggingface.co/genmo/mochi-1-preview>

## Weiterführend

→ Lektion **08.03** (Image-to-Video / Animation — LivePortrait)
→ Lektion **08.05** (3D-Generation + Hunyuan-EU-Ausschluss)
→ Lektion **08.07** (UrhG + Watermark-Pflicht)
