---
id: 06.03
titel: Voice-Cloning + DACH-Datasets — KUG, DSGVO Art. 9, deutsche Speech-Korpora
phase: 06-sprache-und-audio
dauer_minuten: 45
schwierigkeit: mittel
stand: 2026-04-29
voraussetzungen: [06.02]
lernziele:
  - KUG-Persönlichkeitsrecht bei Voice-Cloning
  - Einwilligungs-Pattern für Voice-Production
  - DACH-Speech-Datasets für Forschung + Finetuning
compliance_anker:
  - kug-22-einwilligung
  - speech-dataset-lizenzen
ai_act_artikel:
  - art-50
dsgvo_artikel:
  - art-7
  - art-9
---

## Worum es geht

> Stop cloning voices without consent. — Voice-Cloning ist 2026 trivial (5 s Audio reichen). Damit wird **Einwilligung** + **Lizenz-Disziplin** das eigentliche Problem. KUG Art. 22 + DSGVO Art. 9 sind hart.

## Voraussetzungen

- Lektion 06.02 (TTS-Landschaft)

## Konzept

### Persönlichkeitsrecht: KUG Art. 22

KUG (Kunsturhebergesetz) Art. 22:

> „Bildnisse dürfen nur mit Einwilligung des Abgebildeten verbreitet oder öffentlich zur Schau gestellt werden."

**Stand 04/2026** wird das **analog auf die Stimme** angewendet (BGH-Rechtsprechung weiter im Fluss, aber konservativer Default ist: Voice = persönlichkeitsrechtlich geschützt). Plus: DSGVO Art. 9 als zusätzliche Schicht.

Die Pflicht-Schritte für DACH-Voice-Cloning:

1. **Schriftliche Einwilligung** des Reference-Speakers (Art. 9 Abs. 2 lit. a DSGVO)
2. **Klarer Zweck** (was wird mit dem Voice-Clone gemacht?)
3. **Befristung** (z. B. 1 Jahr, dann erneuern)
4. **Widerrufsrecht** klar dokumentiert
5. **Versions-Kontrolle** der Voice-Modell-Datei (Lösch-Workflow)

### Einwilligungs-Template (Pflicht-Pattern)

```yaml
# einwilligung-voice-clone.yaml
person:
  pseudonym: "speaker-001"  # KEIN Klarname im Audit-Log
  echtname_hash: "sha256:abc..."  # separate verschlüsselte Mapping-DB

einwilligung:
  datum: "2026-04-29"
  zweck: "Synthese von Bürger-Service-Bot-Antworten in Du-Form"
  befristung_bis: "2027-04-29"
  technische_zwecke:
    - "TTS-Voice-Clone für Charity-Adoptions-Bot v1.x"
  ausgeschlossen:
    - "Werbung, Marketing"
    - "Politische Aussagen"
    - "Pornografie / sexuelle Inhalte"
    - "Hassrede / verfassungsfeindliche Inhalte"
  widerrufsrecht: "jederzeit, formlos per E-Mail an datenschutz@..."

reference_audio:
  pfad: "private/refs/speaker-001-2026-04-29.wav"
  laenge_sekunden: 12.5
  qualitaet: "studio-monaural"

unterschriften:
  speaker: "..."  # digital signiert
  verantwortlicher: "..."
```

### Voice-Cloning-Pipeline mit Audit

```python
import asyncio
from datetime import datetime, UTC
import yaml
from pathlib import Path


async def voice_clone_with_audit(
    text: str, voice_id: str, einwilligung_pfad: Path
) -> bytes:
    # 1. Einwilligung lesen + validieren
    einwilligung = yaml.safe_load(einwilligung_pfad.read_text())
    if datetime.fromisoformat(einwilligung["einwilligung"]["befristung_bis"]) < datetime.now(UTC):
        raise PermissionError("Einwilligung abgelaufen.")

    # 2. Zweck-Check (text gegen ausgeschlossene_zwecke filtern)
    if any(zweck in text.lower() for zweck in einwilligung["einwilligung"]["ausgeschlossen"]):
        raise PermissionError("Text widerspricht ausgeschlossenen Zwecken.")

    # 3. TTS-Inferenz
    audio = await tts_clone(text, voice_id=voice_id)

    # 4. Watermark + Audit-Log
    audio_marked = add_audio_watermark(audio)
    log_audit({
        "voice_id": voice_id,
        "einwilligung_hash": hash(einwilligung_pfad.read_bytes()),
        "text_hash": hash(text),
        "ts": datetime.now(UTC).isoformat(),
    })

    return audio_marked
```

### DACH-Speech-Datasets

| Dataset | Größe | Lizenz | URL |
|---|---|---|---|
| **Common Voice DE** | ~ 1.000 h, viele Sprecher | CC0 | <https://commonvoice.mozilla.org/de> |
| **Tatoeba** (Sätze + Audios) | gemischt | CC-BY 2.0 | <https://tatoeba.org/de> |
| **Multilingual LibriSpeech (MLS)** DE | ~ 2.000 h | CC-BY 4.0 | <https://www.openslr.org/94/> |
| **VoxLingua107** DE | ~ 50 h | community | <http://bark.phon.ioc.ee/voxlingua107/> |
| **Thorsten Müller TTS-Dataset** (DE-Voice) | ~ 23 h, 1 Sprecher (mit Einwilligung) | CC-BY-SA-4.0 | <https://github.com/thorstenMueller/Thorsten-Voice> |

> **Wichtig**: Common Voice ist CC0 = volle Freiheit. Thorsten-Voice ist CC-BY-SA-4.0 = Attribution + ShareAlike pflicht. Für kommerzielles Voice-Cloning: Common Voice + eigene Reference-Speaker mit Einwilligung.

### Whisper-Finetune auf DACH-Audio

Falls die WER deines DE-Use-Case (Dialekt, Fachsprache) nicht reicht:

```python
# Phase 12.05-Pattern für Whisper-Finetune
from transformers import WhisperForConditionalGeneration, WhisperProcessor
from peft import LoraConfig, get_peft_model

modell_basis = WhisperForConditionalGeneration.from_pretrained("openai/whisper-large-v3-turbo")
processor = WhisperProcessor.from_pretrained("openai/whisper-large-v3-turbo")

# LoRA für ASR
lora_config = LoraConfig(
    r=16, lora_alpha=32, lora_dropout=0.05,
    target_modules=["q_proj", "v_proj"],
    bias="none",
    task_type="SPEECH_RECOGNITION",
)
modell = get_peft_model(modell_basis, lora_config)

# Trainings-Dataset: Common Voice DE + eigene Domäne
# ... Standard HF-Training-Loop ...
```

> Pattern: 100–500 h DE-Audio + LoRA-Finetune kann WER von 5 % auf 2,5 % senken. Phase 12.05 hat Details.

### TTS-Finetune (Voxtral-TTS oder XTTS)

XTTS-v2 hat ein offizielles Finetune-Setup:

```python
from TTS.tts.utils.managers import save_file
from TTS.tts.configs.xtts_config import XttsConfig

config = XttsConfig.from_json_file("xtts_config.json")
# Trainings-Daten: Speaker-eingewilligte 1-2 h Audio
# Output: Custom-Voice-Modell für genau diesen Speaker
```

> Realität: 1-2 h Reference-Audio + Training auf RTX 4090 (~ 8 h) ergeben einen sauberen Voice-Clone. Pflicht: Einwilligung + Audit-Log + Auto-Lösch-Pipeline.

## Hands-on

1. Common Voice DE herunterladen + 10 Samples transkribieren
2. Einwilligungs-Template ausfüllen (für eigenen Voice-Clone)
3. XTTS-v2-Voice-Clone aus eigener Reference (10 s)
4. Audit-Log-Pattern testen — wird Zweck-Check ausgelöst?
5. Optional: Whisper-Turbo + LoRA-Finetune-Pattern skizzieren

## Selbstcheck

- [ ] Du kennst KUG Art. 22 + DSGVO Art. 9 für Voice-Cloning.
- [ ] Du nutzt das Einwilligungs-Template als Pflicht-Pattern.
- [ ] Du wählst Common Voice / Thorsten-Voice je nach Lizenz-Bedarf.
- [ ] Du implementierst Voice-Audit-Log mit Zweck-Check.
- [ ] Du planst Auto-Lösch-Pipeline für Reference-Audio.

## Compliance-Anker

- **KUG Art. 22**: Persönlichkeitsrecht an Stimme
- **DSGVO Art. 9**: Voice = besondere Kategorie
- **DSGVO Art. 7**: Einwilligungs-Anforderungen
- **AI-Act Art. 50.2**: KI-Audio-Watermark pflicht ab 02.08.2026

## Quellen

- Common Voice DE — <https://commonvoice.mozilla.org/de>
- Thorsten-Voice — <https://github.com/thorstenMueller/Thorsten-Voice>
- MLS — <https://www.openslr.org/94/>
- KUG Art. 22 — <https://www.gesetze-im-internet.de/kunsturhg/__22.html>
- DSGVO Art. 9 — <https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:32016R0679>

## Weiterführend

→ Lektion **06.04** (Realtime-Voice + LiveKit)
→ Phase **12.05** (Whisper-Finetune mit LoRA)
→ Capstone **19.C** + **19.E** (Voice-Use-Cases)
