---
id: 08.03
titel: Audio + 3D-Generation — Stable Audio, MusicGen, TRELLIS.2 (NICHT Hunyuan3D in EU!)
phase: 08-generative-modelle
dauer_minuten: 60
schwierigkeit: mittel
stand: 2026-04-29
voraussetzungen: [08.01, 08.02]
lernziele:
  - Audio-Generation: Stable Audio Open Small, MusicGen, Suno v5, ElevenLabs
  - 3D-Generation: TRELLIS.2 als 2026-Spitze
  - **Hunyuan3D-2 EU-/UK-/SK-Ausschluss** — Pflicht-Hinweis
compliance_anker:
  - hunyuan3d-eu-ausschluss
  - audio-generation-lizenz
ai_act_artikel:
  - art-50
---

## Worum es geht

> Stop using Hunyuan3D in EU production. — Tencent Hunyuan3D Community License **schließt EU/UK/Südkorea explizit aus**. Stattdessen: **Microsoft TRELLIS.2** (4B, Open Source) für 3D. Plus Stable Audio Open Small + MusicGen für Audio.

## Voraussetzungen

- Lektion 08.01 + 08.02

## Konzept

### Audio-Generation

| Modell | Lizenz | Pricing | Wann |
|---|---|---|---|
| **Stable Audio Open Small** (05/2025) | Stability Community License | < 1 Mio. USD frei | smartphone-fähig, kurze Sound-Effects |
| **MusicGen** (Meta) | MIT | — (Open) | seit 2024 nicht aktualisiert, instrumental-only, OSS-Standard |
| **Suno v5 / v5.5** | proprietär | Free 50 Credits/Tag (non-commercial), Pro $ 10/Mo | Music-Generation, kommerziell |
| **ElevenLabs Music** | proprietär | Starter $ 5 — Pro $ 99 | integriert in alle Tarife |

> Empfehlung 2026: **MusicGen** für Open-Source-Music-Generation (kommerziell ok), **Suno Pro** für Music-as-a-Service. Stable Audio für kurze Sound-Effects.

```python
# MusicGen (Meta) — Open + kommerziell ok
from transformers import MusicgenForConditionalGeneration, AutoProcessor
import torchaudio

modell = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-large")
processor = AutoProcessor.from_pretrained("facebook/musicgen-large")

inputs = processor(
    text=["Entspannte Gitarren-Melodie für Bürger-Service-Wartemusik"],
    padding=True,
    return_tensors="pt",
)
audio = modell.generate(**inputs, max_new_tokens=512)
torchaudio.save("musik.wav", audio[0].cpu(), 32000)
```

> ⚠️ Stand 04/2026: **„Stable Audio 2.0 Open"** als 2026er-Release ist **nicht eindeutig belegbar**. Stable Audio Open Small (Mai 2025) ist die letzte verifizierte Open-Variante.

### 3D-Generation — 2026 produktiv geworden

| Modell | Lizenz | DACH-tauglich? | Wann |
|---|---|---|---|
| **TRELLIS.2** (Microsoft, 4B) | Open Source | ✅ ja | **Image-to-3D bis 1536³ mit PBR** — SOTA Open |
| Hunyuan3D-2 (Tencent) | Tencent Hunyuan 3D Community License | ❌ **EU/UK/SK explizit ausgeschlossen** | nicht für DACH-Production |
| „Stable 3D" | — | unklar | Stability hat 3D-Linie nicht weitergeführt |

### TRELLIS.2 — der DACH-3D-Default 2026

URL: <https://microsoft.github.io/TRELLIS.2/>

- **4B Params**
- Image-to-3D bis 1536³ mit PBR-Materialien
- Open Source auf HF/GitHub
- Aktuell SOTA Open-Weights für 3D

```python
# TRELLIS.2 (vereinfachtes Beispiel)
from trellis import Trellis

trellis = Trellis.from_pretrained("microsoft/TRELLIS-2-4B")

mesh = trellis.image_to_3d(
    "produktfoto-stuhl.png",
    resolution=1024,
    pbr=True,
)
mesh.export("stuhl.glb")
```

> Wann: 3D-Asset-Generation aus Produktfotos für E-Commerce, AR/VR-Anwendungen, technische Doku.

### Hunyuan3D-2 — die EU-Lizenz-Falle

URL: <https://github.com/Tencent-Hunyuan/Hunyuan3D-2/blob/main/LICENSE>

**Wichtig**: Tencent Hunyuan 3D Community License **explizit EU + UK + Südkorea ausgeschlossen**. Für DACH-Tutorial: **nicht produktiv einsetzbar** ohne Direktvertrag mit Tencent.

> **Anti-Pattern 2026**: Hunyuan3D-2 in DACH-Production nutzen. Lizenzverstoß führt zu rechtlichen Konsequenzen.

### Audio + 3D Compliance

#### Audio-Generation

- **AI-Act Art. 50.2** ab 02.08.2026: KI-erstellte Audio-Outputs müssen markiert sein (siehe Lektion 06.05 + AudioSeal)
- Bei Music-Generation mit Stimme: KUG Art. 22 + Persönlichkeitsrecht beachten

#### 3D-Generation

- **AI-Act Art. 50.2**: KI-erstellte 3D-Modelle ebenfalls markiert (C2PA für GLTF/GLB-Format in Entwicklung)
- **Urheberrecht**: bei „inspiriert von Marken-Design" — Markenrecht prüfen (kein KI-Freibrief)

### Inferenz-Stacks für Generation

URLs: <https://github.com/Comfy-Org/ComfyUI/releases> · <https://huggingface.co/blog/modular-diffusers> · <https://github.com/invoke-ai/InvokeAI>

| Stack | Status 04/2026 |
|---|---|
| **ComfyUI 0.19.3** (17.04.2026) | LTX-Templates, Hunyuan3D-Nodes, integrierter Manager. 30 Mio. USD Funding bei 500 Mio. USD Bewertung (Craft Ventures) |
| **Diffusers 0.37 (HF)** | Modular Diffusers, neue Pipelines für LTX-2, Helios (14B Video), Z-Image, Kandinsky 5 |
| **InvokeAI** | kommerzielle Hosted-Plattform am 31.10.2025 abgeschaltet (Adobe-Acquihire). Open-Source-Projekt läuft community-gepflegt weiter, unterstützt FLUX.2 Klein, Z-Image Turbo |
| vLLM für Vision-Generation | **nicht Standard** — vLLM ist primär LLM-Serving |

### Pricing-Realität 2026

EU-GPU-Cloud-Hardware-Preise stiegen Q1 2026 um ~ 30 % wegen DRAM-Knappheit. Stand 04/2026:

- **Scaleway H100**: ~ $ 3,80/h (vorher € 2,73/h)
- **Scaleway A100**: ~ $ 2,70/h
- **OVHcloud H100**: ähnlich, vergleichbarer Range

> Bei der Generation-Pipeline: ~ 1 Min Inferenz-Zeit auf H100 = ~ $ 0,06 pro Bild. Bei großen Mengen: Caching + Quantisierung pflichtbewusst.

## Hands-on

1. MusicGen-large für 1-Min-Wartemusik (Bürger-Service-Bot-Background)
2. TRELLIS.2 auf H100 — Produktfoto → GLB-Export
3. Stable Audio Open Small — kurze Sound-Effects (Klick, Erfolg, Error)
4. C2PA-Manifest in Audio-Output einbetten
5. **Anti-Pattern üben**: Hunyuan3D-2-License lesen — warum NICHT in DACH

## Selbstcheck

- [ ] Du nutzt MusicGen für Open-Weights-Music-Generation.
- [ ] Du wählst TRELLIS.2 als 3D-Default für DACH.
- [ ] Du **vermeidest Hunyuan3D-2 in EU-Production** (License-Falle).
- [ ] Du planst AI-Act-Watermark für Audio + 3D.

## Compliance-Anker

- **AI-Act Art. 50.2**: Watermark-Pflicht für KI-erstellte Audio + 3D
- **Hunyuan3D-2 EU-Ausschluss**: Lizenzverstoß bei Production-Einsatz in DACH
- **KUG Art. 22**: Persönlichkeitsrecht bei Voice-Music-Generation

## Quellen

- TRELLIS.2 — <https://microsoft.github.io/TRELLIS.2/>
- Hunyuan3D-2 LICENSE — <https://github.com/Tencent-Hunyuan/Hunyuan3D-2/blob/main/LICENSE>
- Stable Audio Open Small — <https://stability.ai/news>
- MusicGen — <https://huggingface.co/facebook/musicgen-large>
- Suno Pricing — <https://suno.com/pricing>
- ElevenLabs Music — <https://help.elevenlabs.io/hc/en-us/articles/37821528996497-How-much-does-Eleven-Music-cost>
- ComfyUI Releases — <https://github.com/Comfy-Org/ComfyUI/releases>
- Diffusers 0.37 — <https://huggingface.co/blog/modular-diffusers>

## Weiterführend

→ Lektion **08.04** (Inference-Stacks: ComfyUI + Diffusers im Detail)
→ Lektion **08.05** (Recht: UrhG + AI-Act)
