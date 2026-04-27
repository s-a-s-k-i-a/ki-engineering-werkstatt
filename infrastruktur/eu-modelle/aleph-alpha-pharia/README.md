# Aleph Alpha — Pharia-1

> Heidelberg, BSI C5 + ISO 27001, BAFA-zertifiziert. Deutsch-zentrierte Trainingsdaten. Default für regulierte DACH-Use-Cases.

## Setup

```bash
# uv-managed
uv add aleph-alpha-client

# .env
ALEPH_ALPHA_API_KEY=...
ALEPH_ALPHA_API_BASE=https://api.aleph-alpha.com  # oder eigene Instanz
```

## Beispiel-Aufruf (Python)

```python
import os
from aleph_alpha_client import Client, CompletionRequest, Prompt

client = Client(token=os.environ["ALEPH_ALPHA_API_KEY"])
request = CompletionRequest(
    prompt=Prompt.from_text("Erkläre BPE-Tokenizer in zwei Sätzen."),
    maximum_tokens=128,
)
response = client.complete(request, model="Pharia-1-LLM-7B-control")
print(response.completions[0].completion)
```

## Wann einsetzen

- **Behörden / öffentlicher Sektor**: BAFA-Zertifizierung trägt
- **Pharma / Medizin**: deutsche Domain-Sprachverarbeitung stark
- **DSGVO-First**: Server in Heidelberg, keine US-Subunternehmer
- **Energie / Versorger**: kritische Infrastruktur, BSI C5 wichtig

## Wann nicht

- Wenn du Apache-2.0-Open-Weights brauchst (Pharia ist proprietär)
- Wenn dein Use-Case Coding-Performance über alles braucht — DeepSeek/Qwen sind dort 2026 vorn (mit DACH-Disclaimer)

## Compliance

- AVV im Self-Service-Portal nach Vertragsabschluss
- Server: Heidelberg, optional eigene OnPrem-Instanz
- ISO 27001 / BSI C5 / BAFA Vertrauensdienst

## Quellen

- [Aleph Alpha Pharia-1 Tech Report](https://aleph-alpha.com/introducing-pharia-1-llm-transparent-and-compliant/)
- [Hugging Face Pharia-1 Model Card](https://huggingface.co/Aleph-Alpha/Pharia-1-LLM-7B-control)
- [Aleph Alpha Compliance & Security](https://aleph-alpha.com/security)
