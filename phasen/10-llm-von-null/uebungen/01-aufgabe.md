# Übung 10.01 — Pretrain-Compute-Kalkulator für drei DACH-Foundation-Modelle

> Schwierigkeit: fortgeschritten · Zeit: 75–105 Min · Voraussetzungen: Lektionen 10.01–10.04

## Ziel

Du baust einen **Compute- + Daten-Kalkulator** für drei realistische DACH-Foundation-Modell-Vorhaben (Klein / Mittel / Groß). Pro Modell: Chinchilla-optimale Token-Anzahl, GPU-Stunden, Strom-Verbrauch (kWh + EUR), Korpus-Empfehlung mit Lizenz-Check.

## Use-Case

1. **Klein (1B-Param-Modell)**: Forschungs-Prototyp einer Hochschule, Apache-2.0-Open-Source-Release, 24-GB-GPU verfügbar
2. **Mittel (7B-Param-Modell)**: Mittelstands-Stiftung, deutsches Domain-LLM (Recht / Steuern / Medizin), 8× H100 verfügbar
3. **Groß (70B-Param-Modell)**: BMWK-gefördertes Sovereign-AI-Projekt (Konsortium aus Aleph Alpha post-Cohere + Hochschule + Forschungsinstitut), 256× H200 in EU-Cloud (STACKIT / OVH / Scaleway)

## Aufgabe

1. **Pydantic-Profil-Schema** mit `name`, `parameter_n_b`, `gpu_typ` (`h100` / `h200` / `b200`), `n_gpus`, `tflops_pro_gpu_bf16` (theoretisch), `mfu_real` (Realitäts-Faktor, ~ 40-50 %)
2. **Chinchilla-Token-Funktion**: optimale Token-Anzahl ≈ 20× Parameter-Anzahl (z.B. 20B Tokens für 1B-Modell)
3. **FLOPs-Berechnung**: ≈ 6 × N × D (N=Parameter, D=Token), in PFLOP-days
4. **Wall-Clock-Funktion**: GPU-Tage × Anzahl-GPUs ÷ MFU-Real-Faktor
5. **Strom-Verbrauch**: 700 W pro H100, 1.000 W pro H200, 1.200 W pro B200; kWh-Preis 0,30 € (Industrie-Tarif DE)
6. **Korpus-Empfehlung**: Aleph-Alpha-GermanWeb (Apache 2.0 für Forschung — kommerziell prüfen), Common Crawl (CC-BY-Variante), Wikitext-DE (CC-BY-SA), Curlicat (Politik DE-AT)
7. **Lizenz-Pflicht-Check**: Korpus muss zur Modell-Release-Lizenz passen (Apache 2.0 → freie Korpora; Custom-Lizenz → Trainings-Daten-Pflichten dokumentiert)
8. **Smoke-Test**: 5 Asserts (Chinchilla-Verhältnis, FLOPs-Größenordnung, Wall-Clock-Plausibilität)

## Bonus (für Schnelle)

- **Karpathy-nanochat-Plan**: konkretes Setup für 1B-Forschungs-Modell — wie viele GPU-Tage realistisch?
- **TorchTitan vs. DeepSpeed**: für 7B-Modell — welcher Stack, warum?
- **Datacenter-PUE-Faktor**: kWh × PUE 1,3 für realistische Strom-Schätzung
- **Mixed-Precision-Plan**: bf16 + fp8 (FlashAttention-3 auf H100, oder FlashAttention-4 auf B200)

## Abgabe

- Marimo-Notebook in `loesungen/01_loesung.py` (smoke-test-tauglich)
- Kurze `BERICHT.md`: für 70B-Sovereign-Projekt — wie strukturierst du den Strom-Verbrauchs-Audit für AI-Act Annex IV?

## Wann gilt es als gelöst?

- 1B-Modell: ~ 20B Tokens, ~ 1-3 PFLOP-days, ~ Tage auf 24-GB-GPU
- 7B-Modell: ~ 140B Tokens, ~ 250-500 PFLOP-days, ~ Wochen auf 8 H100
- 70B-Modell: ~ 1.4T Tokens, ~ 6.000-12.000 PFLOP-days, ~ Monate auf 256 H200
- Smoke-Test grün

## Wenn du steckenbleibst

- [Chinchilla-Paper (Hoffmann et al. 2022)](https://arxiv.org/abs/2203.15556)
- [Karpathy nanochat](https://github.com/karpathy/nanochat)
- [TorchTitan Paper](https://arxiv.org/abs/2410.06511)
- [Aleph-Alpha-GermanWeb](https://huggingface.co/datasets/Aleph-Alpha/GermanWeb)
- [llm.c GitHub](https://github.com/karpathy/llm.c) — minimal Pretraining-Stack

## Compliance-Check

- [ ] Trainings-Korpus-Lizenz dokumentiert (Apache 2.0 / CC-BY-SA / CC-BY-NC)
- [ ] AI-Act Art. 53 (GPAI-Pflichten) bei > 10²⁵ FLOPs (≈ Llama 3 70B-Bereich)
- [ ] GPAI Code of Practice (10.07.2025 finalisiert) — Trainings-Daten-Zusammenfassung Pflicht
- [ ] Strom-/CO₂-Bilanz dokumentiert (AI-Act Anhang IV)
- [ ] UrhG § 44b TDM-Opt-out-Check für jedes Korpus-Item
- [ ] Aleph-Alpha-GermanWeb-Lizenz für kommerzielle Nutzung prüfen
