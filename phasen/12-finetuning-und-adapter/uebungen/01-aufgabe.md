# Übung 12.01 — QLoRA-Finetune mit deutschem Domain-Datensatz + Eval

> Schwierigkeit: fortgeschritten · Zeit: 240–360 Min · Voraussetzungen: Lektionen 12.01–12.07

## Ziel

Du baust **end-to-end** ein QLoRA-Finetune für eine konkrete deutsche Domäne — mit Datenpipeline, Trainings-Manifest, vLLM-Deployment und Promptfoo-Eval gegen das Basis-Modell.

## Use-Case

Wähle **eines** der drei Profile (oder ein eigenes mit ≥ 200 dt. Beispielen):

### Profil A — Steuer-Beratungs-Stil (12 Steuerberater:innen, 800 Mandanten)

- Quelle: 500 anonymisierte Mandanten-Antworten (Du-Form, Steuer-Vokabular)
- Ziel: Modell lernt **fachlichen Tonfall** + StB-typische Formulierungen
- Modell: Qwen3-7B-Instruct (deutsch-stark, Apache 2.0)

### Profil B — Verwaltung-Bürger-Service (Stadtverwaltung)

- Quelle: 800 FAQ-Paare aus Bürger-Service (formales Sie, Behörden-Vokabular)
- Ziel: Modell beantwortet Behörden-Fragen mit korrektem Verweis auf Paragraphen
- Modell: Mistral-Nemo-12B-Instruct (Apache 2.0)

### Profil C — Charity-Adoptions-Bot (Tierschutz)

- Quelle: 500 Adoptions-Dialoge (siehe Lektion 12.08)
- Ziel: empathischer Tonfall, kein Verkaufston
- Modell: Qwen3-7B-Instruct

## Aufgabe

1. **Datenpipeline** aus Lektion 12.04 anwenden — Yield-Rate dokumentieren
2. **Trainings-Manifest** als YAML schreiben (siehe 12.02-Pattern), mit Hyperparametern + Daten-SHA-256
3. **QLoRA-Training** mit Unsloth oder axolotl (Wahl begründen)
4. **Adapter speichern** + manuell mit 5 Test-Prompts testen
5. **Mergen + AWQ-Quantization** (Lektion 12.06)
6. **vLLM-Deployment** (kann lokal sein) — Multi-LoRA-Setup mit Basis + Finetune parallel
7. **Promptfoo-Eval** mit ≥ 10 Test-Cases, vergleicht Basis vs. Finetune
8. **Modell-Card** schreiben (Lizenz, Datenherkunft, Eval-Scores, Bias-Audit)

## Bonus (für Schnelle)

- **DPO als zweite Stufe**: Sammle 100 „besser/schlechter"-Pairs, DPO mit TRL drüber
- **Multi-Adapter**: zweites Profil mit anderem Adapter, beide auf einem vLLM-Server
- **GerBBQ+ Bias-Audit**: vor und nach Training laufen lassen, Drift dokumentieren
- **Phoenix-Tracing**: Trainings-Loss + Eval-Scores in Phoenix loggen
- **HF-Hub-Upload** als privates Modell-Repo mit Tag v1.0
- **DoRA statt LoRA**: PEFT v0.19.1 `use_dora=True` — was passiert?

## Abgabe

- `daten/` mit `roh.jsonl` (gefiltert) + `clean.jsonl` (Pipeline-Output)
- `manifests/<modell>-v1.0.yaml` mit kompletter Reproduzierbarkeit
- `adapters/<modell>-v1.0/` mit Adapter-SafeTensors
- `merged/` (optional, falls AWQ-Variante deployed)
- `eval/promptfoo-results.json` mit ≥ 10 Test-Cases
- `BERICHT.md` (~ 2 Seiten) mit:
  - Profil-Wahl und Begründung
  - Datenpipeline-Yield-Rate
  - Trainings-Verlauf (Loss-Curve als Bild)
  - Eval-Vergleich Basis vs. Finetune (Tabelle)
  - Bias-Audit (Quote-Vergleich)
  - Reflexion: 3 Sätze, was hat überrascht / was wirst du beim nächsten Mal anders machen

## Wann gilt es als gelöst?

- Yield-Rate ≥ 60 % (sonst: Datenquelle überdenken)
- Trainings-Loss konvergiert (kein Overfitting nach 3 Epochen)
- Promptfoo-Score: Finetune **mindestens 10 % besser** als Basis auf Domänen-Tests
- Modell-Card vollständig (Lizenz, Datenherkunft, Hyperparameter, Eval-Scores, Bias-Audit)
- Kein PII im Training-Set (Pipeline-Audit-Log nachweisbar)

## Wenn du steckenbleibst

- [Unsloth Quickstart](https://docs.unsloth.ai/get-started/unsloth-notebooks)
- [axolotl YAML-Examples](https://github.com/axolotl-ai-cloud/axolotl/tree/main/examples)
- [TRL SFTTrainer-Doku](https://huggingface.co/docs/trl/sft_trainer)
- [Promptfoo Eval](https://www.promptfoo.dev/docs/intro/)
- [PEFT LoRA-Config](https://huggingface.co/docs/peft/conceptual_guides/lora)

## Compliance-Check (Pflicht-Pattern)

- [ ] Datensatz-Lizenz dokumentiert (eigene Daten brauchen Einwilligung — DSGVO Art. 6/7)
- [ ] PII-Filter in Pipeline mit Audit-Log
- [ ] Pseudonyme im Trainings-Set (kein Klartext-Name)
- [ ] Trainings-Manifest committet (Reproduzierbarkeit AI-Act Art. 12)
- [ ] Modell-Card mit Datenherkunft + Bias-Audit
- [ ] Lizenz des Basis-Modells im Repo angehängt
- [ ] GPU-Anbieter EU-Cloud (Scaleway / OVH) oder lokale Hardware
- [ ] Bei Mandanten-Daten: AVV mit Mandant über Daten-Nutzung (Phase 20.02)

## Reflexions-Fragen für `BERICHT.md`

- Hat sich der Aufwand gegenüber Few-Shot-Prompting (Phase 11.01) gelohnt?
- Welche LoRA-Hyperparameter (r, alpha, target_modules) hatten den größten Effekt?
- Wo siehst du Regression gegenüber Basis-Modell (z. B. allgemeine Mathe, Code)?
- Welche Compliance-Anforderung war im Detail am schwierigsten zu erfüllen?
