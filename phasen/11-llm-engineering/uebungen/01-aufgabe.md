# Übung 11.01 — Production-LLM-App mit Pydantic AI + Eval

> Schwierigkeit: mittel · Zeit: 90–120 Min · Voraussetzungen: Lektionen 11.01 bis 11.05 + 11.08

## Ziel

Du baust eine **klein, aber vollständige** LLM-App mit:

1. Strukturiertem Output (Pydantic AI)
2. Tool-Calling
3. Anbieter-Vergleich (mind. 2 Provider)
4. Promptfoo-Eval als CI-Gate

## Use-Case

Ein **Support-Klassifikator**: bekommt eine Kunden-E-Mail, gibt zurück:

- `kategorie`: Login | Abrechnung | Kündigung | Sonstiges
- `dringlichkeit`: 1 (niedrig) … 5 (kritisch)
- `naechster_schritt`: kurze Empfehlung
- `tool_call`: optional, wenn ein Tool besser passt (z. B. „kontostand_pruefen")

## Aufgabe

1. **Pydantic AI Agent** mit Output-Schema (`SupportKlassifikation`)
2. **Tool**: `kontostand_pruefen(kunden_id: str) -> dict` als Mock
3. Test mit **mind. 5 echten Beispiel-E-Mails** (eigene oder paraphrasiert)
4. **Provider-Vergleich**: derselbe Code gegen `claude-sonnet-4-6` UND `gpt-5-4-mini` (oder Ollama lokal, falls keine Keys)
5. **`promptfooconfig.yaml`** mit:
   - 2 Prompt-Varianten („knapp" vs. „mit Begründung")
   - 2 Provider
   - 5 Test-Cases mit Asserts (`contains`, `regex`, `llm-rubric`)
6. **CI-Workflow** (oder lokaler `npx promptfoo eval`-Lauf), dokumentiert in der Lösung
7. **Cost-Vergleich** für die 5 Test-Cases × 2 Provider — wer ist günstiger, was kostet das?

## Bonus (für Schnelle)

- Ollama-Modell als drittes Provider hinzufügen
- Caching aktivieren (Anthropic Prompt Cache mit `cache_control`)
- Phoenix-Tracing aktivieren (Lektion 11.10)
- Self-Censorship-Test: chinesisches Modell (DeepSeek-R1 oder Qwen3) im Vergleich

## Abgabe

- Marimo-Notebook in `loesungen/01_loesung.py`
- `promptfooconfig.yaml` in `loesungen/`
- Eval-Output (JSON oder Screenshot) in `ressourcen/eval-output.md`

## Wann gilt es als gelöst?

- Pydantic-AI-Agent läuft mit beiden Providern ohne Code-Änderung
- Promptfoo-Eval grün (oder dokumentierte Regressionen)
- Cost-Vergleich zeigt mind. Faktor 2 zwischen Provider
- Lösung passt in ~ 100 Zeilen Code

## Wenn du steckenbleibst

- [Pydantic AI Docs](https://pydantic.dev/docs/ai/overview/)
- [Promptfoo Quickstart](https://www.promptfoo.dev/docs/quickstart/)
- GitHub Discussion eröffnen mit dem konkreten Stack-Trace

## Compliance-Check

Vor produktivem Einsatz:

- [ ] AVV mit Provider:innen signiert (Lektion 11.05)
- [ ] PII-Filter vor LLM-Call (Lektion 11.03)
- [ ] Audit-Logging mit Tool-Call-Trail (Lektion 11.10 + Phase 20.05)
- [ ] Eval-Suite als CI-Gate (Lektion 11.08)
- [ ] Wenn chinesisches Modell: Self-Censorship-Audit (Lektion 11.06)
