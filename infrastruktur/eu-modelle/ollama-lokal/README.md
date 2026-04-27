# Ollama lokal — keine Daten verlassen deine Maschine

> Default für Lehre, Entwicklung und maximale Datenhoheit. Mac/Linux/Windows.

## Installation

```bash
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.com/install.sh | sh

# Windows
# Installer von ollama.com herunterladen
```

## Erste Schritte

```bash
# Service starten
ollama serve  # läuft als Daemon

# Modell laden
ollama pull qwen3:8b           # Apache 2.0, multilingual
ollama pull mistral-small      # Apache 2.0, Frankreich
ollama pull deepseek-r1:8b     # MIT, Reasoning
ollama pull gemma3:12b         # Apache 2.0, Google

# Chatten
ollama run qwen3:8b
```

## Aus Python

```bash
uv add ollama
```

```python
import ollama

response = ollama.chat(
    model="qwen3:8b",
    messages=[{"role": "user", "content": "Erkläre RAG in 3 Sätzen."}],
)
print(response["message"]["content"])
```

## Hardware-Empfehlung

| Modell | RAM (CPU) | VRAM (GPU) | Bemerkung |
|---|---|---|---|
| Llama-3.2-1B | 4 GB | 2 GB | nur für Tests |
| Llama-3.2-3B / Qwen3-3B | 8 GB | 4 GB | OK für Demos |
| Mistral 7B / Qwen3-8B | 16 GB | 8 GB | gute Allrounder |
| Llama-3.3-70B (q4) | 64 GB | 24 GB | gute Antwort-Qualität |
| DeepSeek-R1-70B (q4) | 64 GB | 24 GB | Reasoning |

## Compliance

- Keine Daten verlassen den Host → kein AVV nötig
- DSGVO-konform für jede Datenkategorie
- Achtung: bei Self-Censorship-Modellen (DeepSeek, Qwen) trotzdem Self-Censorship-Audit machen — siehe `docs/rechtliche-perspektive/asiatische-llms.md`

## Quellen

- [Ollama Docs](https://docs.ollama.com/)
- [Ollama Library](https://ollama.com/library)
