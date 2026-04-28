---
id: 0.04
titel: Ollama lokal — dein erster lokaler LLM-Aufruf
phase: 00-werkzeugkasten
dauer_minuten: 30
schwierigkeit: einsteiger
stand: 2026-04-28
voraussetzungen: [0.01, 0.02]
lernziele:
  - Ollama auf Mac / Linux / Windows installieren
  - Modelle ziehen, ausführen und beenden
  - Die OpenAI-kompatible API gegen `localhost:11434` nutzen
  - Ein passendes Modell zur eigenen Hardware-Klasse wählen
compliance_anker:
  - lokale-inferenz-dsgvo-bonus
colab_badge: false
---

## Worum es geht

> Stop sending your test prompts to OpenAI. — lokale Modelle sind 2026 gut genug für 80 % der Lehr-Use-Cases. Und sie verlassen deinen Rechner nie.

**Ollama** (aktuelle Version v0.22.0, 28.04.2026) ist die einfachste Methode, LLMs lokal zu betreiben. Open-Source, native für Mac / Linux / Windows. Im Hintergrund läuft `llama.cpp` (oder MLX auf Apple Silicon).

## Voraussetzungen

- Phase 00.01 (Hardware-Klasse bestimmt)
- Phase 00.02 (uv installiert)
- Mind. 8 GB RAM (für 1–4B-Modelle); für 7B-Modelle 16 GB; siehe Lektion 00.01

## Konzept

### Was Ollama ist (und was nicht)

| | Ollama | OpenAI-API | Hugging Face Transformers |
|---|---|---|---|
| Modelle | quantisierte GGUF-Modelle | proprietär in der Cloud | jedes HF-Modell |
| Setup-Zeit | ~ 5 Min. | ~ 2 Min. (Account) | ~ 30 Min. (Python) |
| Datenfluss | bleibt lokal | nach USA / EU | bleibt lokal |
| Wartung | Auto-Updates | n/a | manuell |
| Kosten | nur Strom | $/M Tokens | nur Strom |
| Lehr-Eignung | 🟢 sehr gut | 🟡 produktiv, kostet | 🟡 für Tieftraining |

Ollama eignet sich für: **Lehr-Demos, Lokal-Test, Datenschutz-sensitive Use-Cases, Offline-Arbeit**.

Nicht ideal für: **Production mit hohem QPS** (vLLM oder Cloud-API ist da besser, siehe Phase 17).

### Installation

**macOS**:

```bash
brew install ollama
# oder Download .dmg von https://ollama.com/download
```

**Linux**:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Windows**: Native Installer von <https://ollama.com/download> (kein WSL nötig seit 2024).

Verifizieren:

```bash
ollama --version
# → ollama version is 0.22.0
```

### Wichtige Befehle

```bash
# Modell ziehen
ollama pull qwen3:8b
# → lädt ~ 4,8 GB nach ~/.ollama/

# Modell ausführen (REPL)
ollama run qwen3:8b
# → ">>> hallo, wer bist du?"

# Service starten (Daemon-Mode)
ollama serve
# → läuft im Hintergrund, OpenAI-API auf Port 11434

# Was läuft gerade?
ollama list
ollama ps

# Modell löschen
ollama rm qwen3:8b
```

### Modell-Empfehlungen für deutsche Texte (April 2026)

| Modell | Größe | RAM | Eignung Deutsch | Eignung Code | Lizenz |
|---|---|---|---|---|---|
| `qwen3:4b` | 4B | 8 GB | 🟢 sehr gut, 119 Sprachen | 🟡 ok | Apache 2.0 |
| `qwen3:8b` | 8B | 16 GB | 🟢 sehr gut | 🟢 gut | Apache 2.0 |
| `gemma3:12b` | 12B | 24 GB | 🟢 gut, EU-Provenance | 🟢 gut | Apache 2.0 |
| `mistral` | 7B | 16 GB | 🟢 gut (FR-Anbieter) | 🟢 gut | Apache 2.0 |
| `llama3.3:70b` | 70B | 64 GB | 🟢 sehr gut | 🟢 sehr gut | Llama-Lizenz |
| `deepseek-r1:8b` | 8B | 16 GB | 🟡 mit Self-Censorship | 🟢 sehr gut (Reasoning!) | MIT |

> ⚠️ **DeepSeek R1**: lokal ausgeführt = DSGVO-konform. Aber zensiert ~ 88 % geopolitischer CN-Fragen — siehe `docs/rechtliche-perspektive/asiatische-llms.md`.

**Empfehlung für deinen ersten Aufruf**: `qwen3:8b` (wenn ≥ 16 GB RAM). Apache 2.0, sehr gut auf Deutsch, kein Self-Censorship-Drama für normale Use-Cases.

### OpenAI-kompatible API

Ollama spricht das OpenAI-API-Protokoll auf `http://localhost:11434/v1`:

```python
from openai import OpenAI

client = OpenAI(
    api_key="ollama",  # Dummy, wird ignoriert
    base_url="http://localhost:11434/v1",
)

response = client.chat.completions.create(
    model="qwen3:8b",
    messages=[
        {"role": "system", "content": "Antworte auf Deutsch."},
        {"role": "user", "content": "Was ist eine BPE-Tokenisierung in zwei Sätzen?"},
    ],
)
print(response.choices[0].message.content)
```

**Konsequenz**: Code, der gegen Ollama läuft, läuft auch gegen OpenAI / Anthropic / IONOS / StackIT / OVH — du musst nur `base_url` und ggf. `api_key` ändern. Das ist der Standard-Pattern für „lokal entwickeln, in EU-Cloud deployen".

## Hands-on (15 Min.)

```bash
# 1. Ollama installieren (siehe oben)
ollama --version

# 2. Empfohlenes Modell ziehen (passt zu deiner Hardware aus 00.01)
ollama pull qwen3:8b
# bei < 16 GB RAM: ollama pull qwen3:4b
# bei ≥ 32 GB RAM/Apple-Silicon: ollama pull gemma3:12b

# 3. Direkt im Terminal testen
ollama run qwen3:8b "Erkläre den AI Act in zwei Sätzen auf Deutsch."

# 4. Service im Hintergrund starten (Daemon-Modus)
ollama serve &

# 5. OpenAI-API testen (im Werkstatt-Repo)
cd /pfad/zur/ki-engineering-werkstatt
uv run python -c "
from openai import OpenAI
c = OpenAI(api_key='ollama', base_url='http://localhost:11434/v1')
r = c.chat.completions.create(
    model='qwen3:8b',
    messages=[{'role':'user','content':'Hallo, Werkstatt — antworte auf Deutsch.'}]
)
print(r.choices[0].message.content)
"
```

## Selbstcheck

- [ ] `ollama --version` zeigt 0.22.0+ (oder neuer).
- [ ] Du hast mindestens ein Modell gezogen (`ollama list` zeigt es).
- [ ] Du kannst direkt mit `ollama run` chatten.
- [ ] Du verstehst, dass die OpenAI-kompatible API bei `localhost:11434/v1` lebt.
- [ ] Du hast ein passendes Modell für deine Hardware gewählt (Tabelle oben).

## Compliance-Anker

- **Lokale Inferenz = DSGVO-konform**: Modell-Gewichte sind Mathematik. Keine Daten verlassen deinen Host. Kein AVV nötig.
- **Asiatische Modelle (Qwen, DeepSeek)**: lokal OK, Self-Censorship-Audit pflicht für Use-Cases mit Politik / Geschichte / Tagesnachrichten. → `docs/rechtliche-perspektive/asiatische-llms.md`
- **Logging**: Selbst lokal kannst du Prompts / Outputs speichern wollen (Audit nach AI-Act Art. 12). Phase 20 zeigt Pattern.

## Quellen

- Ollama Docs — <https://docs.ollama.com/> (Zugriff 2026-04-28)
- Ollama Library — <https://ollama.com/library>
- Ollama OpenAI-Kompatibilität — <https://docs.ollama.com/api/openai-compatibility>
- Ollama Releases — <https://github.com/ollama/ollama/releases> (aktuell v0.22.0)
- Qwen3 Model Card — <https://huggingface.co/Qwen/Qwen3-8B>

## Weiterführend

→ Lektion **00.05** (EU-Cloud-Stack) — wenn du mehr Throughput / größere Modelle brauchst
→ Phase **05** (Deutsche Tokenizer) — du nutzt Ollama-Modelle für den Token-Showdown
→ Phase **17** (Production EU-Hosting) — vLLM und Ollama im Vergleich
