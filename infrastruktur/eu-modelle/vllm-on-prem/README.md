# vLLM on-prem — High-Throughput-Inference auf eigener Hardware

> Production-grade. Continuous Batching + PagedAttention. Deine GPU, deine Daten.

## Setup

```bash
# Docker (empfohlen)
docker pull vllm/vllm-openai:latest

# Oder pip via uv (mit CUDA)
uv add vllm
```

## Server starten

```bash
docker run --gpus all -p 8000:8000 \
  -v $HOME/models:/root/.cache/huggingface \
  vllm/vllm-openai:latest \
  --model Qwen/Qwen3-8B \
  --tensor-parallel-size 1 \
  --max-num-seqs 32 \
  --enable-prefix-caching
```

## OpenAI-kompatibel

```python
from openai import OpenAI

client = OpenAI(api_key="dummy", base_url="http://localhost:8000/v1")
response = client.chat.completions.create(
    model="Qwen/Qwen3-8B",
    messages=[{"role": "user", "content": "Hi"}],
)
```

## Wann einsetzen

- Hoher QPS-Bedarf, lokale Hardware verfügbar
- Maximale Datenhoheit, kein Cloud-Vertrauen
- KRITIS-Sektoren mit eigenständiger IT

## Compliance

- Keine Daten verlassen das Rechenzentrum
- Audit-Logging-Layer trivial nachzurüsten (siehe Phase 20.05)
- Empfohlen mit Reverse-Proxy + LiteLLM für Multi-Modell-Setup

## Quellen

- [vLLM Docs](https://docs.vllm.ai/)
- [vLLM Speculative Decoding](https://docs.vllm.ai/en/latest/features/spec_decode/)
- [vLLM Quantization](https://docs.vllm.ai/en/latest/features/quantization/)
