# Übung 03.01 — DL-Architektur + Tracking-Selektor für drei DACH-Vorhaben

> Schwierigkeit: mittel · Zeit: 60–90 Min · Voraussetzungen: Lektionen 03.01–03.03

## Ziel

Du baust einen **Architektur- + Hardware- + Tracking-Selektor** für drei reale DACH-DL-Vorhaben. Pro Vorhaben: Architektur-Empfehlung, Optimizer-Setup (AdamW + Cosine + Warmup), Tracking-Stack (MLflow vs. Comet vs. W&B mit AVV), VRAM-Budget. Schwerpunkt: **Entscheidung vor dem ersten `torch.compile()`**.

## Use-Case

1. **Industrie-Defekt-Klassifikator** (Maschinenbau, Hannover): 8.000 Bilder à 224×224 px, 4 Defekt-Klassen, On-Prem-Hosting, 24-GB-GPU verfügbar
2. **Hochschul-Chatbot** (Universität, EU-Cloud-Hosting bevorzugt): 50.000 Q&A-Paare aus deutschen Vorlesungs-Skripten, Dialog-Format, sensible Studi-Daten
3. **Krankenhaus-Bildgebung-Diagnose** (Universitätsklinikum): 320.000 anonymisierte CT-Scans à 512×512×64, 80-GB-A100 verfügbar, **AI-Act Anhang III Nr. 5a**

## Aufgabe

1. **Pydantic-Profil-Schema** mit `name`, `daten_typ` (`bild_klein` / `bild_gross` / `sequenz` / `text`), `n_samples`, `gpu_vram_gb`, `hosting` (`dach_on_prem` / `hybrid_eu` / `cloud_us`), `sensible_daten`, `ai_act_hochrisiko`
2. **Architektur-Empfehlungs-Funktion**: tabular → kein DL (Phase 02 zurück), Bild < 50k → Pre-trained ResNet50, Bild > 100k → ConvNeXt / ViT, etc.
3. **Optimizer-Setup-Funktion**: AdamW + Cosine-Schedule mit Warmup-Steps + bf16 + Gradient-Accumulation falls VRAM klein
4. **Tracking-Selektor**: DACH-On-Prem → MLflow 3.11; EU-Cloud → Comet (EU-Region); US-Cloud nur mit AVV+SCC+TIA → W&B
5. **VRAM-Budget-Schätzung**: `(modell_gb + kv_cache_gb + aktivierungen_gb) × 1.2` — passt das auf die gegebene GPU?
6. **AI-Act-Pflichten** falls Hochrisiko: Reproduzierbarkeit, Tech-Doku, Logging
7. **Smoke-Test**: 5 Asserts (richtige Architektur + Tracking + AI-Act-Markierung)

## Bonus (für Schnelle)

- **Distributed-Training-Plan** für CT-Scans-Vorhaben: DDP vs. FSDP, wie viele GPUs, wie viel Tokens/sec geschätzt?
- **Mixed-Precision-Strategie**: wann bf16, wann fp16, wann fp32 — und warum
- **Lightning-vs-Vanilla-PyTorch-Vergleich** für jeden Use-Case (Argumente pro/contra)
- **DSFA-Skizze** für Kliniken-Vorhaben: Schwellwerte für „besonders schützenswert" nach DSGVO Art. 9

## Abgabe

- Marimo-Notebook in `loesungen/01_loesung.py` (smoke-test-tauglich, kein PyTorch-Import)
- Kurze `BERICHT.md`: für CT-Scans-Vorhaben — würdest du W&B Cloud nutzen oder hartes On-Prem? Begründung.

## Wann gilt es als gelöst?

- Defekt-Klassifikator → ResNet50 mit Pre-trained Backbone (Bilder < 50k)
- Hochschul-Chatbot → Decoder-only-Transformer (sensible Daten → MLflow lokal)
- CT-Scans → AI-Act-Hochrisiko-Markierung + DSFA-Pflicht im Output
- Smoke-Test grün

## Wenn du steckenbleibst

- [PyTorch 2.7 Release Notes](https://pytorch.org/blog/pytorch-2-7/)
- [TorchTitan Paper](https://arxiv.org/abs/2410.06511) — Production-LLM-Pretraining
- [MLflow 3.11 Releases](https://mlflow.org/releases/)
- [Loshchilov & Hutter SGDR (Cosine-Schedule)](https://arxiv.org/abs/1608.03983)

## Compliance-Check

- [ ] Random-Seeds dokumentiert (AI-Act Art. 11)
- [ ] Trainings-Hyperparameter committed (Reproducibility-Disziplin)
- [ ] Modell- + Daten-Hashes archiviert (Tech-Doku-Pflicht)
- [ ] DSGVO Art. 44 bei W&B-Hosting → SCC + TIA + DPIA
- [ ] DSGVO Art. 9 bei CT-Scans → DSFA-Pflicht (Phase 20.03)
- [ ] AI-Act-Hochrisiko bei Bildgebungs-Diagnose → CE-Kennzeichnung (Phase 18.10)
