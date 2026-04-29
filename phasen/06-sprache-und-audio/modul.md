---
id: 06
titel: Sprache & Audio — Whisper, Voxtral, F5-TTS, LiveKit, EU-Hosting
dauer_stunden: 10
schwierigkeit: mittel
stand: 2026-04-29
lernziele:
  - ASR-Landschaft 2026 (Whisper-large-v3, Voxtral-STT, Faster-Whisper)
  - TTS-Landschaft mit Lizenz-Disziplin (Voxtral-TTS, F5-TTS, XTTS, Cartesia)
  - Voice-Cloning mit KUG / DSGVO Art. 9 Compliance
  - LiveKit Agents v1.4 für Realtime-Voice
  - EU-Hosting + AI-Act-Watermark-Pflicht
---

# Phase 06 · Sprache & Audio

> **Stop using F5-TTS for commercial work.** — F5-TTS ist CC-BY-NC. Voxtral-TTS (Mistral, Apache 2.0, DE nativ) ist 2026 der DACH-Standard. Plus: Whisper-v4 existiert NICHT — nur large-v3 + large-v3-Turbo.

**Status**: ✅ vollständig ausgearbeitet · **Dauer**: ~ 10 h · **Schwierigkeit**: mittel

## 🎯 Was du in diesem Modul lernst

- **ASR-Landschaft**: Whisper-large-v3 + Turbo, Faster-Whisper als Production-Default, Voxtral-STT als Alternative
- **TTS-Landschaft**: Voxtral-TTS, F5-TTS (Forschung-only!), XTTS-Idiap-Fork, Sesame ≠ Anthropic
- **Voice-Cloning + Compliance**: KUG Art. 22 + DSGVO Art. 9 + Einwilligungs-Pflicht-Pattern
- **Realtime-Voice**: LiveKit Agents v1.4, OpenAI gpt-realtime, Deepgram Nova-3
- **EU-Hosting**: Self-Hosted Stack auf Scaleway / OVH / STACKIT
- **AI-Act Art. 50.2**: Watermark-Pflicht für KI-Audio ab 02.08.2026

## 📚 Inhalts-Übersicht

| Lektion | Titel | Datei |
|---|---|---|
| 06.01 | ASR-Landschaft 2026 | [`lektionen/01-asr-landschaft.md`](lektionen/01-asr-landschaft.md) ✅ |
| 06.02 | TTS-Landschaft 2026 (mit Lizenz-Disziplin) | [`lektionen/02-tts-landschaft.md`](lektionen/02-tts-landschaft.md) ✅ |
| 06.03 | Voice-Cloning + DACH-Speech-Datasets | [`lektionen/03-voice-cloning-datasets.md`](lektionen/03-voice-cloning-datasets.md) ✅ |
| 06.04 | Realtime-Voice + LiveKit Agents | [`lektionen/04-realtime-voice-livekit.md`](lektionen/04-realtime-voice-livekit.md) ✅ |
| 06.05 | EU-Hosting für Audio + AI-Act-Watermark | [`lektionen/05-eu-hosting-audio.md`](lektionen/05-eu-hosting-audio.md) ✅ |

## 💻 Hands-on-Projekt

**Audio-Stack-Selektor**: Marimo-Notebook, das ASR + TTS basierend auf Use-Case + Compliance + Lizenz-Anforderung empfiehlt.

```bash
uv run marimo edit phasen/06-sprache-und-audio/code/01_audio_stack_selektor.py
```

## 🧱 Audio-Wahl 2026 (Faustregel)

| Use-Case | ASR | TTS |
|---|---|---|
| **DACH-Mittelstand-Voice-Agent** | Faster-Whisper-Turbo | **Voxtral-TTS 4B** |
| **Realtime mit Voice-Cloning** | Faster-Whisper | XTTS-v2 Idiap-Fork |
| **Latenz-kritisch (proprietär ok)** | Deepgram Nova-3 | Cartesia Sonic 2 |
| **Forschung (CC-BY-NC ok)** | Whisper | F5-TTS-DE |
| **Q&A direkt aus Audio** | **Voxtral-STT 3B** | — |

## ⚖️ DACH-Compliance-Anker

→ [`compliance.md`](compliance.md): DSGVO Art. 9 (Voice = biometrisch), KUG Art. 22 (Persönlichkeitsrecht an Stimme), DSGVO Art. 25 (on-device wenn möglich), AI-Act Art. 50.2 (Watermark ab 02.08.2026).

## 🔄 Wartung

Stand: 29.04.2026 · Reviewer: Saskia Teichmann ([@s-a-s-k-i-a](https://github.com/s-a-s-k-i-a)) · Nächster Review: 07/2026 (Voxtral-Updates, AI-Act-Watermark-C2PA-Finalisierung Juni 2026).
