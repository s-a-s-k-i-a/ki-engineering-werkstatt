---
id: 12
phase: 12-finetuning-und-adapter
stand: 2026-04-27
anker:
  - trainingsdaten-einwilligung
  - modell-karte-pflicht
  - ueber-fitting-bias
dsgvo_artikel:
  - art-7
  - art-9
  - art-25
ai_act_artikel:
  - art-10
  - art-13
---

# Compliance-Anker — Phase 12

## Trainingsdaten-Einwilligung

Wer eigene Daten zum Finetuning nutzt (Charity-Dialoge, Kundengespräche, E-Mails):

- **Einwilligung** (Art. 7) oder **berechtigtes Interesse** (Art. 6 lit. f) als Rechtsgrundlage
- Bei besonderen Kategorien (Gesundheit, Religion): explizite Einwilligung Art. 9
- **Datenminimierung**: nur was wirklich nötig
- **Zweckbindung**: Training für genau den deklarierten Zweck

## Modell-Karte (AI-Act Art. 13)

Pro Finetune: Model Card mit:

- Trainingsdaten-Beschreibung (Quelle, Größe, Lizenz, Bias-Test)
- Use Case (intended) + Out-of-Scope
- Performance auf Held-out-Test-Set
- Bekannte Limitationen
- Energieverbrauch des Trainings

Template in `phasen/20-recht-und-governance/vorlagen/model-card.yaml`.

## Bias durch Finetuning

Adapter "verstärken" oft Bias der Originaldaten. Pflicht-Test:

- Geschlechter-Bias (deutsche Berufsbezeichnungen)
- Migrations-Bias (Namens-Heuristik)
- Alters-Bias

Phase 18 vertieft.

## Quellen

- [Hu et al. LoRA Paper](https://arxiv.org/abs/2106.09685)
- [Dettmers et al. QLoRA](https://arxiv.org/abs/2305.14314)
- [Unsloth Docs](https://unsloth.ai/docs)
