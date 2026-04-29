---
id: 04.05
titel: VLM-Inference-Stacks — vLLM, SGLang, Transformers für Vision
phase: 04-computer-vision
dauer_minuten: 45
schwierigkeit: fortgeschritten
stand: 2026-04-29
voraussetzungen: [04.01, 17.02]
lernziele:
  - vLLM v0.20+ mit VLM-Support produktiv aufsetzen
  - SGLang für VLM-Latenz-Edge
  - Transformers-Pipelines als Forschungs-Stack
  - Helm-Deployment für VLM auf K8s
compliance_anker:
  - vlm-audit-trail
ai_act_artikel:
  - art-12
---

## Worum es geht

> Stop running VLM in pure Transformers when vLLM speed matters. — 2026 ist vLLM ≥ 0.20 für Qwen3-VL der Production-Standard. SGLang als Latenz-Edge. Transformers-Pipelines bleiben für Forschung.

## Voraussetzungen

- Lektion 04.01 (VLM-Landschaft)
- Phase 17.02 (vLLM Foundation)

## Konzept

### vLLM mit VLM-Support

URL: <https://docs.vllm.ai/projects/recipes/en/latest/Qwen/Qwen3-VL.html>

Stand vLLM v0.20.0 (siehe Phase 17.02): **Qwen3-VL voll unterstützt** mit FP8 + YaRN. Recipe-Doku verfügbar.

```bash
uv run python -m vllm.entrypoints.openai.api_server \
    --model Qwen/Qwen3-VL-32B-Instruct \
    --quantization fp8 \
    --max-model-len 32768 \
    --gpu-memory-utilization 0.92 \
    --port 8000 \
    --limit-mm-per-prompt image=4  # max 4 Bilder pro Prompt
```

OpenAI-kompatible Vision-API:

```bash
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Qwen/Qwen3-VL-32B-Instruct",
    "messages": [{
      "role": "user",
      "content": [
        {"type": "text", "text": "Was ist auf dem Bild?"},
        {"type": "image_url", "image_url": {"url": "https://..."}}
      ]
    }]
  }'
```

> ⚠️ **Llama-3.2-Vision-Support in offiziellem vLLM**: nicht eindeutig belegbar — vLLM-MLX-Fork nennt es, Mainline-Doku unklar. Vor Production-Einsatz Live-Check.

### SGLang für VLM

URL: <https://sgl-project.github.io/supported_models/text_generation/multimodal_language_models.html>

- **LLaVA-OneVision-Familie + Qwen-VL** unterstützt
- RadixAttention spart bei Multi-Image-Prompts (z. B. 4 Bilder mit selbem System-Prompt) deutlich Compute
- Wann: Latenz-kritische Pipelines mit Multi-Image-Pattern

### Transformers-Pipelines (Forschung)

URL: <https://huggingface.co/docs/transformers>

```python
from transformers import pipeline

# SigLIP-2 für Image-Klassifikation
classifier = pipeline(
    "zero-shot-image-classification",
    model="google/siglip2-so400m-patch14-384",
)
result = classifier(
    "katze.jpg",
    candidate_labels=["Katze", "Hund", "Vogel", "Auto"],
)
```

```python
# Qwen3-VL als Pipeline (langsamer als vLLM, aber simpler)
from transformers import Qwen3VLForConditionalGeneration, AutoProcessor

modell = Qwen3VLForConditionalGeneration.from_pretrained(
    "Qwen/Qwen3-VL-8B-Instruct",
    torch_dtype="bfloat16",
    device_map="auto",
)
processor = AutoProcessor.from_pretrained("Qwen/Qwen3-VL-8B-Instruct")
# Inferenz wie HF-Standard
```

**Wann Transformers**: Forschung, Schnell-Prototyping, neue Modelle ohne vLLM-Recipe.

### Helm-Deployment auf EU-Cloud-K8s

Stand 04/2026: vLLM-Production-Stack (siehe Phase 17.06) hat VLM-Templates.

```yaml
# values.yaml für Qwen3-VL auf STACKIT SKE
servingEngineSpec:
  modelSpec:
    - name: "qwen3-vl-32b"
      model: "Qwen/Qwen3-VL-32B-Instruct"
      quantization: "fp8"
      replicaCount: 2
      resources:
        gpuCount: 1  # 1× H100 für 32B-FP8
      vllmConfig:
        maxModelLen: 32768
        gpuMemoryUtilization: 0.92
        limitMmPerPrompt:
          image: 4
```

### Performance-Realität (Stand 04/2026)

Bei Qwen3-VL-32B-FP8 auf 1× H100 (80 GB):

| Metrik | Wert |
|---|---|
| TTFT (First-Token) | ~ 800 ms |
| Throughput Single-Stream | ~ 25–35 Tokens/s |
| Concurrent (16 Streams) | ~ 600–900 Tokens/s aggregiert |
| Memory bei 32k Context | ~ 65 GB |

Bei MiniCPM-o 2.6 (8B) auf RTX 4090:

| Metrik | Wert |
|---|---|
| TTFT | ~ 600 ms |
| Throughput | ~ 30–45 Tokens/s |
| Memory Q4_K_M | ~ 5 GB |

### Multi-Image-Prompts

```python
# OpenAI-Format für mehrere Bilder
messages = [{
    "role": "user",
    "content": [
        {"type": "text", "text": "Vergleiche die zwei Rechnungen:"},
        {"type": "image_url", "image_url": {"url": "rechnung1.png"}},
        {"type": "image_url", "image_url": {"url": "rechnung2.png"}},
    ]
}]
```

> Stand 04/2026: bei Qwen3-VL und MiniCPM-o produktiv getestet bis 8 Bilder pro Request. Limit-Flag `--limit-mm-per-prompt image=N` beachten.

### Audit-Pattern für VLM-Calls

```python
def vlm_audit_log(user, image_hash, prompt, response):
    logger.info("vlm_call", extra={
        "user_pseudonym": user,
        "image_hash": image_hash,  # niemals raw image-bytes!
        "prompt_hash": hash(prompt),
        "response_tokens": len(response),
        "modell_version": "Qwen3-VL-32B-Instruct",
        "ts": datetime.now(UTC).isoformat(),
    })
```

> Pflicht für AI-Act Art. 12. Image-Hash statt Bytes — sonst werden Bilder im Log persistiert (DSGVO-Risiko).

## Hands-on

1. vLLM mit Qwen3-VL-8B starten (passt auf RTX 4090)
2. OpenAI-API mit 5 Test-Bildern füttern
3. Latenz + Throughput dokumentieren
4. Multi-Image-Prompt: 4 Bilder vergleichen
5. Helm-Deployment auf STACKIT SKE (falls Cluster verfügbar)

## Selbstcheck

- [ ] Du startest vLLM mit Qwen3-VL.
- [ ] Du nutzt OpenAI-Vision-API mit Multi-Image.
- [ ] Du wählst Transformers vs. vLLM vs. SGLang je nach Use-Case.
- [ ] Du loggst VLM-Calls audit-fähig (Image-Hash statt Bytes).

## Compliance-Anker

- **AI-Act Art. 12**: Audit-Log mit Image-Hashes
- **DSGVO Art. 25**: keine Bilder im Log persistieren

## Quellen

- vLLM Qwen3-VL Recipe — <https://docs.vllm.ai/projects/recipes/en/latest/Qwen/Qwen3-VL.html>
- SGLang Multimodal — <https://sgl-project.github.io/supported_models/text_generation/multimodal_language_models.html>
- Transformers VLM-Doku — <https://huggingface.co/docs/transformers/main/en/model_doc/qwen3_vl>
- vLLM Production Stack VLM — <https://github.com/vllm-project/production-stack>

## Weiterführend

→ Lektion **04.06** (Hands-on: Rechnungs-OCR-Pipeline)
→ Phase **17.02** (vLLM Foundation)
→ Phase **17.06** (Helm-Deployment)
