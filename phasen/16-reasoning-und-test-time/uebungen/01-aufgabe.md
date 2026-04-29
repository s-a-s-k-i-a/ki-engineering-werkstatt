# Übung 16.01 — Self-Consistency vs. Reasoning-Modell vs. GRPO-Mini auf dt. Mathe

> Schwierigkeit: fortgeschritten · Zeit: 240–360 Min · Voraussetzungen: Lektionen 16.01–16.06

## Ziel

Du vergleichst **drei TTC-Strategien** auf einem konkreten dt. Mathe-Set:

1. **Self-Consistency** (N=8) auf einem Standard-Modell
2. **Eingebautes Reasoning** (GPT-5.5 effort=high oder Opus 4.7 adaptive)
3. **Eigenes GRPO-Modell** (Qwen2.5-Math-1.5B mit 200 Aufgaben trainiert)

Output: Accuracy + Cost + Latenz-Vergleich.

## Use-Case

200 deutsche Mathe-Aufgaben mit Endlösung:

- 50 aus MMLU-DE-Math
- 50 aus GSM8K-DE-Übersetzung
- 100 selbst kuratierte (Steuer-Berechnungen, Prozent, Bruchrechnung)

Validation-Set: 50 Aufgaben (separate)
Test-Set: 50 Aufgaben (separate)
Trainings-Set: 100 Aufgaben

## Aufgabe

1. **Aufgaben kuratieren** + in JSONL-Format speichern (`frage`, `loesung`, `schwierigkeit`)
2. **Verifier-Funktion** schreiben (Final-Answer-Match mit Tolerance ≤ 0.001)
3. **Strategie 1 — Self-Consistency**: Qwen2.5-Math-7B-Instruct mit N=8, Majority-Vote
4. **Strategie 2 — Reasoning-Modell**: GPT-5.5 mit `effort=medium` (oder Opus 4.7 adaptive)
5. **Strategie 3 — GRPO-Mini**: Qwen2.5-Math-1.5B mit 100 Trainings-Aufgaben + GRPOTrainer
6. **Eval auf 50 Test-Aufgaben** für alle drei Strategien
7. **Cost-Tabelle**: € pro 50 Aufgaben + Total-Cost für Trainings-Run
8. **Latenz-Vergleich**: p50 + p95 pro Strategie

## Bonus (für Schnelle)

- **R1-Distill-Qwen-32B lokal** als 4. Strategie hinzufügen
- **Multi-Reward**: Format + Length-Penalty in GRPO einbauen
- **Reward-Hacking-Test**: prüfe, ob das GRPO-Modell auf einer **OOD-Distribution** (z. B. AIME-DE) genauso gut ist
- **Phoenix-Tracing**: alle Calls in Phoenix loggen, Reasoning-Tokens als separates Feld
- **Self-Consistency mit GPT-5.5**: triplet — eingebautes + N=4 Vote — bringt es noch was?

## Abgabe

- `daten/` mit `train.jsonl`, `val.jsonl`, `test.jsonl`
- `code/`:
  - `01_self_consistency.py` (Strategie 1)
  - `02_reasoning_modell.py` (Strategie 2)
  - `03_grpo_training.py` (Strategie 3)
  - `04_eval.py` (alle drei auf Test-Set)
- `manifests/grpo-v1.0.yaml` mit Hyperparametern
- `eval/results.json` mit Accuracy + Cost + Latenz pro Strategie
- `BERICHT.md` (~ 2 Seiten):
  - Welche Aufgaben-Typen profitieren am meisten von TTC?
  - Wann lohnt sich Self-Consistency (Cost-Faktor 8)?
  - Wann GRPO selber trainieren?
  - Reflexion: 3 Sätze

## Wann gilt es als gelöst?

- Verifier funktioniert (Tolerance, sinnvolle Match-Rate auf Validation)
- Alle drei Strategien produzieren Eval-Output
- Cost-Tabelle pro 50 Aufgaben transparent
- GRPO-Training konvergiert (Loss + Reward-Curve dokumentiert)
- Mindestens **eine** Strategie schlägt das Basis-Modell ohne TTC um ≥ 10 pp

## Wenn du steckenbleibst

- [TRL GRPOTrainer](https://huggingface.co/docs/trl/grpo_trainer)
- [Self-Consistency Paper](https://arxiv.org/abs/2203.11171)
- [DeepSeek-Math GRPO](https://arxiv.org/abs/2402.03300)
- [Anthropic Extended Thinking](https://platform.claude.com/docs/en/build-with-claude/extended-thinking)
- [GPT-5.5 reasoning-effort](https://developers.openai.com/api/docs/models/gpt-5.5)

## Compliance-Check (Pflicht)

- [ ] Trainings-Daten + Test-Daten dokumentiert + lizenzkonform
- [ ] Verifier ist deterministisch + reproduzierbar
- [ ] Reasoning-Tokens werden für Cost-Audit geloggt (Lektion 16.02)
- [ ] Bei Self-Consistency: Token-Budget pro Run aktiv (Cost-Cap)
- [ ] AVV mit Reasoning-Modell-Provider (Anthropic Enterprise / OpenAI Enterprise)
- [ ] GRPO-Manifest committet (Reproduzierbarkeit AI-Act Art. 12)

## Reflexions-Fragen für `BERICHT.md`

- Welche Strategie hatte das beste Cost/Accuracy-Verhältnis?
- War Self-Consistency seine 8× Cost wert? Oder hat eingebautes Reasoning gewonnen?
- Wo siehst du Grenzen für GRPO-Mini (Compute, Daten, Domain-Transfer)?
- Welche Compliance-Anforderung war im Detail am schwierigsten zu erfüllen?
- Wenn du nur einen Stack für DACH-Mittelstand 2026 wählen müsstest — welcher?
