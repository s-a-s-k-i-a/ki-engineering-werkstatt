# IONOS AI Model Hub

> Karlsruhe / Berlin. Deutsche Cloud, BSI C5, EU-Cloud-Code-of-Conduct.

## Setup

IONOS bietet OpenAI-kompatible APIs für gehostete Llama-4-Maverick, Mistral, Aleph-Alpha-Modelle.

```bash
# OpenAI-kompatibel
uv add openai

# .env
IONOS_AI_API_KEY=...
IONOS_AI_BASE_URL=https://openai.inference.de-txl.ionos.com/v1
```

## Beispiel-Aufruf

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["IONOS_AI_API_KEY"],
    base_url=os.environ["IONOS_AI_BASE_URL"],
)
response = client.chat.completions.create(
    model="meta-llama/Llama-4-Maverick-17B-128E-Instruct",
    messages=[{"role": "user", "content": "Worum geht es im AI Act?"}],
)
print(response.choices[0].message.content)
```

## Wann einsetzen

- DACH-KMU mit IONOS-Hosting bereits
- Wenn du günstige Llama-4 / Mistral-Hosting in DE brauchst
- AVV mit Server-Standort Deutschland erforderlich

## Compliance

- AVV im Cloud-Portal
- Server: Deutschland (Karlsruhe / Berlin / Frankfurt)
- BSI C5
- EU-Cloud-Code-of-Conduct
- ISO 27001 + ISO 27018

## Quellen

- [IONOS AI Model Hub](https://docs.ionos.com/cloud/ai/ai-model-hub)
