---
id: 6
phase: 06-sprache-und-audio
stand: 2026-04-27
anker:
  - stimm-biometrie-art-5
  - einwilligung-aufnahme
  - dialekt-fairness
dsgvo_artikel:
  - art-9
  - art-7
ai_act_artikel:
  - art-5-abs-1-lit-h
  - art-50-abs-3
---

# Compliance-Anker — Phase 06

## Stimm-Biometrie

Wer Stimmen identifizieren will (nicht: erkennen, was gesagt wurde): biometrische Daten nach DSGVO Art. 9 → Einwilligung Art. 7 nötig. Bei öffentlichen Räumen: AI-Act Art. 5 Abs. 1 lit. h.

## Einwilligung bei Aufnahmen

Aufnahme von Personen ohne deren Wissen (auch zu „Trainingszwecken") ist DSGVO-Verstoß und je nach Kontext **§ 201 StGB** (Verletzung der Vertraulichkeit des Wortes).

→ Im Lehrkontext: nur Common Voice DE oder eigene, eingewilligte Aufnahmen.

## Dialekt-Fairness

ASR-Modelle haben oft schlechtere WER auf Dialekten. Wenn dein Voice-Agent in einer Behörde eingesetzt wird (öffentliche Stelle = AGG-relevant): dokumentiere Dialekt-WER, baue Eskalationspfad.

## Synthetische Stimme (Art. 50 Abs. 3)

TTS-Output, der eine reale Person imitiert: muss als KI-generiert kenntlich gemacht werden. Voice-Cloning ohne Einwilligung = Persönlichkeitsrechts-Verletzung.

## Quellen

- [Common Voice DE Dataset Card](https://commonvoice.mozilla.org/de/datasets)
- [Sesame CSM-1 Tech Report](https://www.sesame.com/research/crossing_the_uncanny_valley_of_voice)
- [Whisper-v3 Paper](https://cdn.openai.com/papers/whisper.pdf)
