---
id: 04.04
titel: Edge-VLM — MiniCPM-o, SmolVLM2 für Smartphone + IoT
phase: 04-computer-vision
dauer_minuten: 45
schwierigkeit: mittel
stand: 2026-04-29
voraussetzungen: [04.01]
lernziele:
  - Edge-VLM-Familien abgrenzen (MiniCPM, SmolVLM, MobileCLIP)
  - On-Device-Inferenz auf iOS / Android
  - Wann Cloud-VLM, wann Edge
compliance_anker:
  - on-device-keine-cloud-uebertragung
ai_act_artikel:
  - art-50
dsgvo_artikel:
  - art-25
---

## Worum es geht

> Stop sending every image to the cloud. — Edge-VLMs (MiniCPM-o, SmolVLM2) laufen auf Smartphones mit GPT-4o-Niveau. Für DSGVO-strict-Use-Cases (Behörden, medizinische Bilder) ist on-device-Inferenz das einzig saubere Pattern.

## Voraussetzungen

- Lektion 04.01 (VLM-Landschaft)

## Konzept

### Drei Edge-Familien

| Familie | Größe | Plattform | Lizenz | Stand 04/2026 |
|---|---|---|---|---|
| **MiniCPM-o 2.6** | 8B | iPad / iPhone Pro / Edge-GPU | Apache 2.0 | GA |
| **MiniCPM-V 4.0** | 4,1B | iPhone 16 Pro Max | Apache 2.0 | < 2 s First-Token |
| **SmolVLM2** | 256M / 500M / 2,2B | Browser / Mobile | Apache 2.0 | Video-Verständnis |
| **MobileCLIP2** | < 100M | Smartphone-CPU | Apache 2.0 | nur Embedding |

### MiniCPM-o 2.6 — der Edge-Champion

URL: <https://github.com/OpenBMB/MiniCPM-o> · HF: <https://huggingface.co/openbmb/MiniCPM-o-2_6>

- **8B Params**, GPT-4o-Niveau bei Single-Image
- **Speech-to-Speech + Live-Streaming** auf iPad
- Apache 2.0
- Multilingual (inkl. DE)

```python
from transformers import AutoModel, AutoTokenizer
from PIL import Image

modell = AutoModel.from_pretrained(
    "openbmb/MiniCPM-o-2_6",
    trust_remote_code=True,
    torch_dtype="bfloat16",
)
tokenizer = AutoTokenizer.from_pretrained("openbmb/MiniCPM-o-2_6", trust_remote_code=True)

bild = Image.open("dokument.png")
msgs = [{"role": "user", "content": [bild, "Beschreibe das Bild auf Deutsch."]}]
res = modell.chat(image=None, msgs=msgs, tokenizer=tokenizer)
print(res)
```

### MiniCPM-V 4.0 — Speed-Edge

URL: <https://huggingface.co/openbmb/MiniCPM-V-4>

- **4,1B Params** (SigLIP-2 + MiniCPM4-3B)
- **< 2 s First-Token + 17 tok/s** auf iPhone 16 Pro Max
- Beste Latenz / Qualität-Balance für Mobile

### SmolVLM2 (HuggingFace, 02.2025)

URL: <https://huggingface.co/blog/smolvlm2>

- Drei Größen: **256M / 500M / 2,2B**
- **Video-Verständnis** out-of-the-box
- Apache 2.0
- Browser-tauglich (WebGPU)

```python
# 256M-Variante läuft im Browser via Transformers.js
# 2,2B-Variante auf RTX 3060 / iPhone 15 Pro
```

#### Smol2Operator (09.2025)

Nachfolger: SmolVLM2-2.2B als **agentischer GUI-Coder**. Macht Klick-Pfade auf Screenshots → für Test-Automation oder Behörden-Bot mit Webseiten-Interaktion.

### Wann Cloud, wann Edge?

| Faktor | Cloud-VLM (Qwen3-VL-32B) | Edge-VLM (MiniCPM-o) |
|---|---|---|
| Qualität | besser bei komplexen Tasks | gut bei Standard-Tasks |
| Latenz | 2–5 s p50 | 1–2 s on-device |
| Kosten | API-Cost ($) | Hardware-CapEx (Edge-Device) |
| **DSGVO** | mit AVV | **kein Datentransfer** |
| **Skalierung** | horizontal | pro Gerät |
| **Privacy** | Cloud-Leck-Risiko | absolut sauber |
| Wann | komplexe Doku-Analyse | medizinisch / Behörde / Mandanten |

> **Pattern 2026**: Edge-VLM für **PII-haltige** Bilder (Mandanten-Dokumente, medizinisch, Bewerbungen). Cloud-VLM für allgemeine Doku-Verarbeitung mit AVV.

### iOS-/Android-Deployment

#### iOS (mit Apple Intelligence-Stack)

```swift
// MLX-Swift für Apple Silicon
import MLX
import MLXNN

let modell = try MLXModel.loadVLM("MiniCPM-V-4-MLX-4bit")
let result = await modell.generate(prompt: "...", image: uiImage)
```

> Stand 04/2026: **MLX-Swift + MLX-VLM** sind produktiv für iPhone 15 Pro+ und iPad M-Series.

#### Android (mit Google AICore + MediaPipe)

```kotlin
// MediaPipe LLM Inference
val options = LlmInferenceOptions.builder()
    .setModelPath("/path/to/minicpm-v-4-android.tflite")
    .build()
val llm = LlmInference.createFromOptions(context, options)
```

### Browser-Deployment (WebGPU)

```javascript
// Transformers.js mit SmolVLM2-256M
import { pipeline } from '@huggingface/transformers';

const vlm = await pipeline(
    'image-to-text',
    'HuggingFaceTB/SmolVLM2-256M-Video-Instruct',
    { device: 'webgpu' }
);
const result = await vlm(imageURL);
```

> Vorteil: 100 % Browser-lokal, kein Server, kein Datentransfer.

### DSGVO-Pattern für Edge-VLM

```python
# Edge-Pipeline mit Audit-Logging (auch lokal)
def edge_vlm_call(image, user_pseudonym):
    # 1. On-Device-Inferenz
    response = minicpm_local.generate(image)

    # 2. Audit-Log lokal (kein Cloud-Call!)
    local_log({
        "ts": now(),
        "user_hash": sha256(user_pseudonym),
        "image_hash": sha256(image.tobytes()),
        "tokens": len(response),
        "modell": "minicpm-v-4-on-device",
    })

    # 3. Optional: Aggregat-Telemetrie an EU-Cloud
    if user_consent_telemetry:
        send_aggregate_only(...)  # keine Inhalte!

    return response
```

## Hands-on

1. MiniCPM-o 2.6 lokal auf RTX 4090 laden (Q4_K_M, ~ 5 GB VRAM)
2. 10 deutsche Bilder beschreiben — Latenz pro Bild messen
3. SmolVLM2-256M im Browser via Transformers.js testen
4. Vergleich gegen Cloud-Qwen3-VL-32B (Lektion 04.01) — Qualitäts-Differenz?
5. iPhone-/iPad-Deployment-Test (falls Apple-Hardware verfügbar)

## Selbstcheck

- [ ] Du wählst Cloud vs. Edge je Use-Case.
- [ ] Du deployest MiniCPM-o oder SmolVLM2 lokal.
- [ ] Du kennst die DSGVO-Vorteile von on-device.
- [ ] Du nutzt MLX-Swift / MediaPipe für iOS / Android.

## Compliance-Anker

- **DSGVO Art. 25**: on-device = Privacy by Design
- **AI-Act Art. 50**: bei generativen Edge-Outputs Disclaimer „KI-erstellt"

## Quellen

- MiniCPM-o GitHub — <https://github.com/OpenBMB/MiniCPM-o>
- MiniCPM-V 4 HF — <https://huggingface.co/openbmb/MiniCPM-V-4>
- SmolVLM2 — <https://huggingface.co/blog/smolvlm2>
- Smol2Operator — <https://huggingface.co/blog/smolagents>
- MobileCLIP2 — <https://github.com/apple/ml-mobileclip>
- MLX Swift — <https://github.com/ml-explore/mlx-swift>
- MediaPipe LLM — <https://developers.google.com/mediapipe/solutions/genai/llm_inference>

## Weiterführend

→ Lektion **04.05** (DACH-Datasets + Eigene Daten-Pipeline)
→ Phase **06** (Audio + Edge-Integration)
