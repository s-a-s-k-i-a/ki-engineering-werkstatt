---
id: 11.08
titel: Eval mit Promptfoo (CI-tauglich)
phase: 11-llm-engineering
dauer_minuten: 60
schwierigkeit: mittel
stand: 2026-04-28
voraussetzungen: [11.05]
lernziele:
  - Promptfoo als Open-Source-Eval-Framework einsetzen
  - Eine `promptfooconfig.yaml` schreiben und ausführen
  - Eval-Suite in GitHub Actions als CI-Gate integrieren
  - Modell-Vergleiche und Prompt-Variationen automatisch testen
compliance_anker:
  - eval-pflicht-vor-deployment
  - kosten-monitoring
ai_act_artikel:
  - art-13
  - art-15
---

## Worum es geht

> Stop deploying LLM-Apps without tests. — Promptfoo macht „klickt sich gut auf meinem Rechner" zu „grünes CI-Gate".

**Promptfoo** (aktuelle Version v0.121.9, 27.04.2026) ist das De-facto-Standard-Tool für LLM-Eval und Red-Teaming. Open Source, CLI-first, CI-tauglich. Genutzt von OpenAI und Anthropic intern.

## Voraussetzungen

- Lektion 11.05 (Anbieter-Vergleich)
- Node.js (Promptfoo läuft auf Node)

## Konzept

### Was Promptfoo macht

Drei Achsen, die du gleichzeitig variierst:

| Achse | Beispiele |
|---|---|
| **Prompts** | „Antworte knapp." vs. „Antworte ausführlich." |
| **Provider** | Claude Sonnet 4.6 vs. GPT-5.4 vs. Mistral vs. Pharia lokal |
| **Test-Cases** | reale User-Fragen mit erwarteten Antworten |

Promptfoo führt **alle Kombinationen** aus, sammelt Outputs, vergleicht gegen Asserts, gibt eine Tabelle zurück.

### Installation

```bash
npm install -g promptfoo
# oder einmalig: npx promptfoo eval
```

### Minimal-Konfiguration

`promptfooconfig.yaml`:

```yaml
description: "Tierheim-FAQ-Bot Eval"

prompts:
  - "Du bist Assistenz im Tierheim. Antworte auf Deutsch knapp.\n\nFrage: {{frage}}"
  - "Du bist Assistenz im Tierheim. Antworte auf Deutsch ausführlich.\n\nFrage: {{frage}}"

providers:
  - id: anthropic:claude-sonnet-4-6
  - id: openai:gpt-5-4-mini
  - id: ollama:qwen3:8b
    config:
      apiHost: http://localhost:11434

tests:
  - vars:
      frage: "Wie kann ich einen Hund adoptieren?"
    assert:
      - type: contains
        value: "Termin"
      - type: llm-rubric
        value: "Antwort nennt mindestens drei konkrete Schritte."

  - vars:
      frage: "Was kostet eine Adoption?"
    assert:
      - type: regex
        value: "\\d+\\s?(€|EUR)"
      - type: not-contains
        value: "kostenlos"
```

### Ausführen

```bash
promptfoo eval
# → führt alle Kombis aus (2 Prompts × 3 Provider × 2 Tests = 12 Calls)
# → öffnet UI mit Tabelle: Pass/Fail je Zelle
```

```bash
# Headless für CI
promptfoo eval -o results.json --no-cache
```

### Wichtige Assert-Typen

| Type | Was es prüft |
|---|---|
| `contains` / `not-contains` | exakte Substring |
| `regex` | regulärer Ausdruck |
| `equals` / `is-json` | strukturell |
| `cost` | API-Kosten ≤ Wert |
| `latency` | Antwortzeit ≤ ms |
| `similar` | Cosine-Embedding-Ähnlichkeit zu Referenz |
| `llm-rubric` | „Bewerte mit LLM-Judge gegen diese Rubric" |
| `factuality` | „Stimmt die Antwort mit Referenz überein?" |
| `javascript` | beliebige JS-Logik |

### CI-Integration (GitHub Actions)

`.github/workflows/llm-eval.yml`:

```yaml
name: LLM Eval
on:
  pull_request:
    paths:
      - "phasen/14-agenten-und-mcp/**"
      - "promptfoo/**"

jobs:
  eval:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - name: Run Promptfoo Eval
        uses: promptfoo/promptfoo-action@v1
        with:
          openai-api-key: ${{ secrets.OPENAI_API_KEY }}
          anthropic-api-key: ${{ secrets.ANTHROPIC_API_KEY }}
        env:
          PROMPTFOO_FAIL_ON_ERROR: "true"
```

→ PR mit Veränderung am Prompt → CI führt Eval aus → bei Regression: Build rot.

### Beispiel-Output

```text
┌────────────────────────┬──────────────────┬────────────────┐
│ Prompt                 │ Sonnet 4.6       │ GPT-5.4-mini   │
├────────────────────────┼──────────────────┼────────────────┤
│ knapp                  │ ✅ 2/2 (1,2 €)   │ ✅ 2/2 (0,4 €) │
│ ausführlich            │ ✅ 2/2 (3,4 €)   │ ⚠️ 1/2 (1,1 €) │
└────────────────────────┴──────────────────┴────────────────┘
```

→ „GPT-5.4-mini mit ausführlichem Prompt" hat ein Test-Case nicht bestanden. Im UI siehst du **welcher** und **warum**.

## Hands-on (30 Min.)

```bash
mkdir /tmp/promptfoo-test && cd /tmp/promptfoo-test
npm init -y
npx promptfoo init  # interaktive Initialisierung

# .env.example als Vorlage
cat > .env <<EOF
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
EOF

# Eigene config schreiben (siehe oben)
nano promptfooconfig.yaml

# Eval starten
promptfoo eval
promptfoo view  # öffnet UI lokal
```

## Selbstcheck

- [ ] Du verstehst die drei Achsen (Prompts × Provider × Tests).
- [ ] Du schreibst eine eigene `promptfooconfig.yaml` für deinen Use-Case.
- [ ] Du kennst die wichtigsten Assert-Typen (contains, llm-rubric, regex).
- [ ] Du integrierst Promptfoo in CI als Pflicht-Gate vor Production-Deploy.

## Compliance-Anker

- **Eval-Pflicht (AI-Act Art. 15)**: Hochrisiko-Systeme verlangen genauigkeits-belegbare Ausgaben. Promptfoo ist die niedrigschwelligste Methode.
- **Kosten-Monitoring**: Eval läuft mit `cost`-Assert → CI bricht bei zu teuren Anfragen.
- **PII in Test-Daten**: keine echten Personennamen / Kontodaten in Test-Cases. Synthetische Daten generieren.

## Quellen

- Promptfoo Docs — <https://www.promptfoo.dev/docs/intro/> (Zugriff 2026-04-28)
- Promptfoo Releases — <https://github.com/promptfoo/promptfoo/releases> (aktuell v0.121.9)
- Promptfoo CI Integration — <https://www.promptfoo.dev/docs/integrations/ci-cd/>

## Weiterführend

→ Lektion **11.09** (Ragas — Eval für RAG-Pipelines)
→ Lektion **11.10** (Observability — Tracing in Production)
→ Phase **18** (Ethik / Bias-Audit — Promptfoo + Self-Censorship-Eval)
