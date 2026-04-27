---
id: 8
phase: 08-generative-modelle
stand: 2026-04-27
anker:
  - synthetische-inhalte-art-50
  - c2pa-pflicht
  - persoenlichkeitsrechte
  - deepfake-verbot
dsgvo_artikel:
  - art-22
ai_act_artikel:
  - art-50-abs-2
  - art-50-abs-4
---

# Compliance-Anker — Phase 08

## Synthetische Inhalte (Art. 50 Abs. 2)

Ab 02.08.2026: jedes KI-generierte Bild/Audio/Video muss **maschinenlesbar markiert** werden. Pflicht-Standards:

- **C2PA** (Content Authenticity Initiative) — von Adobe, Microsoft, BBC etc.
- Alternative: SynthID (Google), aber nicht harmonisiert
- Im Repo: C2PA-CLI-Beispiele in `code/06_c2pa.py`

## Deepfakes (Art. 50 Abs. 4)

Eine reale Person darstellende KI-Inhalte: zusätzlich **deutlich sichtbar** kennzeichnen ("Dieses Video ist KI-generiert").

## FLUX.1 — EU-Provenance-Bonus

Black Forest Labs (Freiburg) hat FLUX als Open Weights veröffentlicht. Vorteil: dokumentierte EU-Trainingsdaten, kein US-/CN-Hosting nötig. **Nutze FLUX als Default für DACH-Use-Cases.**

## Persönlichkeitsrechte

Bilder, die reale Personen erkennbar zeigen, brauchen Einwilligung (KUG § 22, in DACH analog). LoRA-Finetuning auf 30 Mitarbeiterfotos = Einwilligung jeder Person + DSFA.

## Quellen

- [C2PA Spezifikation](https://c2pa.org/specifications/)
- [FLUX.1 Hugging Face](https://huggingface.co/black-forest-labs/FLUX.1-dev)
- [Lipman et al. Flow Matching Paper](https://arxiv.org/abs/2210.02747)
