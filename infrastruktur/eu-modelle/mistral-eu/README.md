# Mistral AI — EU-Modelle

> Paris. Frankreichs LLM-Champion. Open-Weights für viele Modelle, EU-Hosting.

## Setup

```bash
uv add mistralai

# .env
MISTRAL_API_KEY=...
```

## Beispiel-Aufruf

```python
import os
from mistralai import Mistral

client = Mistral(api_key=os.environ["MISTRAL_API_KEY"])
response = client.chat.complete(
    model="mistral-large-2411",
    messages=[{"role": "user", "content": "Was ist DPO?"}],
)
print(response.choices[0].message.content)
```

## Selbst-Hosting (Open-Weights)

```bash
# Mistral Small / Mixtral via Ollama
ollama pull mistral-small
ollama pull mixtral

# Mistral via vLLM
docker run --gpus all -p 8000:8000 \
  -v ~/models:/models \
  vllm/vllm-openai:latest \
  --model mistralai/Mistral-Small-Instruct-2409
```

## Wann einsetzen

- Mehrsprachige Use-Cases (FR, DE, EN, IT, ES)
- RAG mit gutem Tool-Use
- Production wenn EU-AVV + Open-Weights gleichzeitig nötig

## Compliance

- DPA online signierbar
- Server: Frankreich (La Plateforme)
- Empfohlen: Region `eu-west-3` explizit setzen
- Open-Weights-Modelle (Mistral 7B, Mixtral, Mistral Small) frei selbst hostbar

## Quellen

- [Mistral La Plateforme](https://docs.mistral.ai/)
- [Mistral Hugging Face](https://huggingface.co/mistralai)
