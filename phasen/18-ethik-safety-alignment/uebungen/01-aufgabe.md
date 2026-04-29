# Übung 18.01 — Bias-Audit + Self-Censorship-Audit + Safety-Stack

> Schwierigkeit: fortgeschritten · Zeit: 240–360 Min · Voraussetzungen: Lektionen 18.01–18.09

## Ziel

Du baust ein **vollständiges Audit-Paket** für ein konkretes DACH-Modell:

1. **Bias-Audit** auf 6 Dimensionen (Geschlecht, Migration, Region, Alter, Religion, Beruf)
2. **Self-Censorship-Audit** auf 50 dt. Geopolitik-Prompts (falls asiatisches Modell)
3. **Red-Team-Suite** mit DACH-Jailbreaks
4. **Safety-Stack** mit NeMo + Llama Guard 3
5. **Konformitätserklärung** als YAML (Anhang IV)

## Use-Case

Wähle eines der drei Profile:

### Profil A — Bürger-Service-Bot (Stadtverwaltung)

- Modell: **Pharia-1-LLM-7B** (Aleph Alpha) oder **Llama 3.3-8B-Instruct**
- Use-Case: Bürger fragt nach Behördengängen
- Compliance: DSGVO + AI-Act (begrenzt)

### Profil B — Internes QA-Tool (DACH-Mittelständler)

- Modell: **Qwen3-32B (lokal Ollama)** oder **R1-Distill-Qwen-32B**
- Use-Case: Mitarbeiter:innen fragen nach internen Prozessen
- Compliance: DSGVO + Self-Censorship-Disclaimer (asiatisches Modell)

### Profil C — News-Aggregator (Medienhaus)

- Modell: **Mistral Large 3** oder **Claude Sonnet 4.6**
- Use-Case: News-Zusammenfassung auf Deutsch
- Compliance: AI-Act (begrenzt) + redaktionelle Verantwortung

## Aufgabe

### Teil 1: Bias-Audit (Lektion 18.01 + 18.02)

1. **30 Probes** (5 pro Bias-Dimension) für DACH-Kontext
2. **20 Pairs** im BBQ-Style (Migrations-Hintergrund, Region, Alter)
3. **10 Open-End-Prompts** mit LLM-Judge
4. **Statistik**: DIR + Equalized Odds pro Dimension
5. **Report**: `audits/bias-<modell>-2026-04.json`

### Teil 2: Self-Censorship (Lektion 18.08, nur bei asiatischen Modellen)

1. **50 dt. Geopolitik-Prompts** (5 Kategorien × 10)
2. Pipeline mit LLM-Judge
3. Aggregat-Tabelle pro Kategorie
4. Disclaimer-Text generieren
5. Report: `audits/self-censorship-<modell>-2026-04.json`

### Teil 3: Red-Team (Lektion 18.07)

1. **30 dt. Jailbreak-Probes** (Rolle, Hypothese, Code-Switch, Du/Sie)
2. **20 Prompt-Injection-Probes** (direkt + indirekt)
3. **Garak** + **promptfoo** + eigenes DACH-Set
4. Refusal-Rate-Report
5. Report: `audits/redteam-<modell>-2026-04.json`

### Teil 4: Safety-Stack (Lektion 18.09)

1. **NeMo Guardrails** mit DACH-Custom-Policy (StGB § 86a/§ 130)
2. **Llama Guard 3** als Output-Filter
3. **Latenz-Test**: TTFT mit/ohne Safety-Layer
4. **False-Positive-Rate** auf 50 harmlosen Prompts
5. Config: `safety/nemo-config.yaml` + `safety/guard-policy.txt`

### Teil 5: Konformitätserklärung (Lektion 18.10)

1. YAML nach Anhang-IV-Template
2. Mappe 9 Pflicht-Inhalte zu deinen Audit-Reports
3. Konformitäts-Pfad wählen (Anhang VI Self-Assessment)
4. Lücken dokumentieren

## Bonus (für Schnelle)

- **Constitutional AI** (Lektion 18.06): eigene Verfassung schreiben + DPO-Run mit auto-generierten Pairs
- **Multi-Stage-Pipeline**: SFT → DPO (Bias-Korrektur) → GRPO (Multi-Reward) — Lektion 18.05
- **Bias-Drift-Monitoring**: Phoenix-Tracing mit Bias-Score als Custom-Metric
- **CI-Integration**: alle Audits als Pre-Production-Gate (`.github/workflows/safety.yml`)
- **OOD-Eval**: Test-Set außerhalb Trainings-Verteilung gegen Reward-Hacking

## Abgabe

- `audits/` mit 4 JSON-Reports (Bias, Self-Censorship optional, Red-Team, Safety-FP)
- `safety/` mit NeMo-Config + Llama Guard Policy
- `konformitaets-erklaerung-v1.0.yaml`
- `BERICHT.md` (~ 3 Seiten):
  - Profil-Wahl + Begründung
  - Audit-Ergebnisse pro Teil (Zusammenfassung)
  - Mitigation-Plan (welche DPO-Pairs / Guard-Rules)
  - Konformitäts-Lücken + Plan zur Schließung
  - Reflexion: 3 Sätze

## Wann gilt es als gelöst?

- Alle 4 Audit-Reports vorhanden + reproduzierbar
- Bias-DIR pro Dimension dokumentiert (idealerweise 0.8–1.25)
- Red-Team-Refusal-Rate ≥ 90 % auf kritischen Probes
- Safety-Stack reduziert False-Positive-Rate auf < 5 %
- Konformitätserklärung deckt alle 9 Anhang-IV-Punkte ab (oder Lücken-Plan)

## Wenn du steckenbleibst

- [Garak](https://github.com/leondz/garak)
- [PyRIT (Microsoft)](https://github.com/Azure/PyRIT)
- [promptfoo Red-Team](https://www.promptfoo.dev/docs/red-team/)
- [NeMo Guardrails](https://github.com/NVIDIA/NeMo-Guardrails)
- [Llama Guard 3](https://huggingface.co/meta-llama/Llama-Guard-3-8B)
- [BSI AIC4](https://www.bsi.bund.de/AIC4)

## Compliance-Check

- [ ] Modell-Lizenz dokumentiert
- [ ] AVV mit Modell-Provider (falls API)
- [ ] Audit-Reports nach AI-Act-Aufbewahrung (≥ 6 Monate)
- [ ] Self-Censorship-Disclaimer (falls asiatisches Modell) sichtbar im UI
- [ ] Bias-Audit pro Quartal eingeplant
- [ ] Red-Team-Audit pro Quartal eingeplant
- [ ] CI-Integration: PR-Block bei Bias-DIR < 0.8
- [ ] DACH-Custom-Policies (StGB § 86a/§ 130) im Safety-Stack

## Reflexions-Fragen für `BERICHT.md`

- Welche Bias-Dimension hat dich überrascht (positiv / negativ)?
- Hat das gewählte Modell die Anforderungen erfüllt? Mit welchen Auflagen?
- Welche Mitigations-Maßnahme hatte den größten Effekt (DPO / NeMo / Llama Guard)?
- Welche Compliance-Anforderung war im Detail am schwierigsten?
- Wenn du das Modell heute nicht nutzen würdest — welches stattdessen?
