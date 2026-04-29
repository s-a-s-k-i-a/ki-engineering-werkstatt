# Übung 06.01 — Audio-Stack + DSGVO-Plan für drei Sprach-Use-Cases

> Schwierigkeit: mittel · Zeit: 75–105 Min · Voraussetzungen: Lektionen 06.01–06.05

## Ziel

Du baust einen **STT- + TTS- + Voice-Agent-Selektor** für drei DACH-Audio-Use-Cases. Pro Use-Case: Modell-Familie (Whisper / Voxtral / F5-TTS / XTTS), Diarization-Strategie, DSGVO-Auto-Lösch-Pipeline, EU-Hosting-Plan.

## Use-Case

1. **Anwaltskanzlei-Diktiergerät**: Anwält:innen diktieren Schriftsätze → Transkript → DSGVO Art. 9 sensibel (Mandantendaten). On-Prem-Hosting Pflicht.
2. **Notdienst-Voice-Bot** (Tierheim Hannover, 19.E-bezug): mehrsprachig DE/EN/TR, Realtime < 800 ms TTFB, mit Whisper + F5-TTS oder XTTS-Fork
3. **Customer-Support-Hotline** (KMU 50 Mitarbeitende): aufgenommene Anrufe transkribieren + Sprecher-Diarization für Compliance-Stichproben (mind. 6 Monate Aufbewahrung)

## Aufgabe

1. **Pydantic-Profil-Schema** mit `name`, `modus` (`stt` / `tts` / `voice_agent`), `realtime`, `sprachen`, `pii_sensitivity` (`niedrig` / `mittel` / `hoch`), `hosting`, `aufbewahrungsdauer_tage`
2. **STT-Empfehlung**: Whisper-large-v3 (nicht v4!) für hohe Accuracy, Voxtral-STT für Speed-Cluster, Distil-Whisper für Edge
3. **TTS-Empfehlung**: F5-TTS (CC-BY-NC! → kommerziell sperrt), XTTS-Idiap-Fork, Voxtral-TTS, Polly EU-Region als Fallback
4. **Voice-Agent-Stack**: LiveKit Agents v1.4 + Whisper + Pharia/Mistral + F5/XTTS für Realtime
5. **Diarization-Plan**: pyannote.audio v3 vs. NVIDIA NeMo, Modell-Größe + Hardware
6. **DSGVO-Auto-Lösch-Pipeline**: bei `pii_sensitivity=hoch` → Audio + Transkript nach `aufbewahrungsdauer_tage` automatisch löschen, signiertes Lösch-Log
7. **EU-Hosting-Plan**: AVV-Liste, BSI-C5-/HDS-Mapping
8. **Smoke-Test**: 5 Asserts (richtiges STT/TTS, F5-TTS-NC-Disclaimer, Auto-Lösch-Pflicht, DSGVO-Art-9-Markierung)

## Bonus (für Schnelle)

- **§ 201 StGB-Hinweis**: bei nicht-öffentlichen Gesprächen ist Aufnahme **strafbar** ohne Einwilligung — wie testest du das in der Pipeline?
- **§ 201b StGB-Entwurf** (Deepfakes): bei TTS auf realer Stimme → Watermarking-Pflicht
- **Stimm-Klon-Schutz**: F5-TTS Voice-Cloning mit nur 3 sec Material — wie verhinderst du Missbrauch?
- **Realtime-Optimierung**: für LiveKit-Bot — Whisper-Streaming-Modus, Chunked-Decode, KV-Cache pre-warm

## Abgabe

- Marimo-Notebook in `loesungen/01_loesung.py` (smoke-test-tauglich, kein Audio-Inference)
- Kurze `BERICHT.md`: für Customer-Support-Hotline — wie strukturierst du das Audio-Lösch-Log nach 6 Monaten? (TPS, Hash-Chain, Audit-Anker)

## Wann gilt es als gelöst?

- Anwaltskanzlei → On-Prem-Hosting + Whisper-large-v3 + DSGVO Art. 9 markiert
- Notdienst-Bot → LiveKit + 3-Sprachen-Setup mit XTTS oder Voxtral-TTS (nicht F5 wegen NC!)
- Hotline → Auto-Lösch-Pipeline nach 180 Tagen + Diarization-Plan
- Smoke-Test grün

## Wenn du steckenbleibst

- [Whisper-large-v3 Model Card](https://huggingface.co/openai/whisper-large-v3)
- [F5-TTS GitHub](https://github.com/SWivid/F5-TTS) — **CC-BY-NC** beachten!
- [LiveKit Agents Docs](https://docs.livekit.io/agents/) — Realtime-Voice-Stack
- [pyannote.audio v3](https://github.com/pyannote/pyannote-audio) — Diarization
- [§ 201 StGB](https://www.gesetze-im-internet.de/stgb/__201.html) + [§ 201b StGB-Entwurf](https://www.bmj.de/SharedDocs/Gesetzgebungsverfahren/DE/Persoenlichkeitsschutz_Deepfake.html)

## Compliance-Check

- [ ] § 201 StGB — Einwilligung bei nicht-öffentlichen Gesprächen (Phase 06.06)
- [ ] DSGVO Art. 9 bei Stimm-Aufnahmen mit besonders sensiblen Daten
- [ ] DSGVO Art. 17 (RTBF) — Lösch-Pipeline binnen 30 Tagen
- [ ] AVV mit Cloud-Anbieter falls nicht On-Prem
- [ ] F5-TTS = **CC BY-NC** → kommerzielle Nutzung gesperrt, alternative TTS-Modelle wählen
- [ ] § 201b StGB-Entwurf bei Stimm-Klonen → Watermark-Pflicht (Phase 08.04)
