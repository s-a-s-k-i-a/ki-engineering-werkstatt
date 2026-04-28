---
id: 11.01
titel: Prompt-Patterns — Zero/Few-Shot, CoT, Self-Consistency
phase: 11-llm-engineering
dauer_minuten: 60
schwierigkeit: leicht
stand: 2026-04-28
voraussetzungen: [0.04]
lernziele:
  - Die vier wichtigsten Prompt-Patterns 2026 unterscheiden und einsetzen
  - Zero-Shot / Few-Shot / Chain-of-Thought / Self-Consistency entscheiden
  - System-Prompt vs. User-Prompt vs. Tool-Definition strukturieren
  - Prompt-Hygiene als Grundlage für Production-Apps
compliance_anker: []
colab_badge: false
---

## Worum es geht

> Stop hoping the model „understands" you. — gute Prompts sind Engineering, nicht Magie.

Bevor du Pydantic AI, Tool-Calling, MCP einführst, solltest du die **vier Prompt-Patterns** beherrschen, die 2026 Standard sind.

## Voraussetzungen

- Phase 00.04 (Ollama lokal — du kannst LLM-Calls absetzen)
- Optional: ein API-Key für einen EU-Cloud-Anbieter (Lektion 00.05)

## Konzept

### 1. Zero-Shot

Du gibst dem Modell **nur die Aufgabe**, keine Beispiele. Das funktioniert bei einfachen, klaren Tasks.

```text
System: Antworte auf Deutsch in einem Satz.
User: Was ist eine BPE-Tokenisierung?
```

**Wann**: Allgemeinwissen, einfache Fragen, gut trainierte Modelle.

**Wann nicht**: Domänenspezifische Konventionen, Format-Anforderungen, Ton.

### 2. Few-Shot

Du zeigst **2–5 Beispiele**, bevor die echte Frage kommt. Das Modell lernt Format und Stil aus den Beispielen.

```text
System: Klassifiziere Support-Anfragen in eine von drei Kategorien.
User:
Beispiele:
"Mein Login geht nicht"  → Login
"Rechnung falsch"         → Abrechnung
"Ich will kündigen"       → Kündigung

Klassifiziere:
"Passwort vergessen"      →
```

**Wann**: spezifische Klassifikation, Format-Konsistenz, Ton-Adaption, ohne Finetuning.

**Wichtig**: zu wenige Beispiele → unzuverlässig. Zu viele → teurer. Sweet Spot bei drei bis fünf.

### 3. Chain-of-Thought (CoT)

Du forderst das Modell auf, **schrittweise zu denken**. Bei Reasoning-Tasks (Mathematik, Logik, mehrteilige Probleme) verbessert das die Genauigkeit erheblich.

**Klassisches CoT**:

```text
User: Ein Newsletter mit 8.000 Empfängern wird einmal pro Woche
verschickt, jede Anfrage kostet 0,15 € pro 1M Tokens. Pro Newsletter
sind 1.200 Tokens. Wie hoch sind die Jahreskosten?

Denke Schritt für Schritt:
1. Tokens pro Versand
2. Versände pro Jahr
3. Gesamtkosten
```

**Zero-Shot-CoT** (Kojima et al. 2022): einfach „Lass uns Schritt für Schritt überlegen." am Ende anhängen — kostet keine Beispiele und verbessert oft schon.

**2026-Update**: viele moderne Modelle (Claude Sonnet 4.6+, GPT-5.x, Gemini 3) machen CoT bereits **intern**. Bei Reasoning-Modellen wie **OpenAI o3** oder **DeepSeek-R1** ist CoT **nicht nötig** — sie haben einen separaten Reasoning-Trace.

### 4. Self-Consistency

Du fragst das Modell **mehrmals dieselbe Frage** mit `temperature > 0`, sammelst die Antworten, nimmst die Mehrheit. Das hilft bei Reasoning-Aufgaben mit hohem Stochastik-Anteil.

```python
antworten = []
for _ in range(5):
    r = client.chat.completions.create(
        model="claude-sonnet-4-6",
        messages=[{"role":"user","content": frage}],
        temperature=0.7,
    )
    antworten.append(extract_answer(r.choices[0].message.content))

# Mehrheit gewinnt
final = Counter(antworten).most_common(1)[0][0]
```

**Wann**: hohe Genauigkeits-Anforderung, kritisch.
**Nachteil**: 5x Kosten. Spar dir das, bis es nötig ist.

## Prompt-Struktur in Production

Was du **immer** trennst:

| Block | Inhalt | Beispiel |
|---|---|---|
| **System-Prompt** | Rolle, Stil, Sprache, Boundaries | „Du bist Assistenz im Tierheim Hannover. Antworte auf Deutsch." |
| **Tool-Definitionen** | strukturierte Werkzeug-Schemata (Pydantic) | siehe Lektion 11.02 |
| **Few-Shot-Beispiele** | falls Format-Konsistenz nötig | als `messages=[{"role":"user", ...}, {"role":"assistant", ...}, ...]` |
| **User-Prompt** | die eigentliche Frage | „Wie kann ich einen Hund adoptieren?" |
| **Output-Schema** | falls strukturierte Antwort | Pydantic-Modell |

```python
# Pseudo-Code
client.chat.completions.create(
    model="anthropic:claude-sonnet-4-6",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        # Few-Shot:
        {"role": "user", "content": "Beispiel-Frage 1"},
        {"role": "assistant", "content": "Beispiel-Antwort 1"},
        # Echte Frage:
        {"role": "user", "content": user_input},
    ],
    tools=[...],
    response_format={"type": "json_schema", "json_schema": ...},
)
```

## Hands-on

Probiere dieselbe Frage mit allen vier Patterns in deinem Ollama-REPL aus:

```bash
ollama run qwen3:8b
```

```text
# Zero-Shot
>>> Berechne: ein Newsletter mit 8000 Empfängern, einmal pro Woche, 1200 Tokens, 0,15 €/1M Tokens. Jahreskosten?

# Zero-Shot-CoT
>>> Berechne ... Lass uns Schritt für Schritt überlegen.

# Few-Shot
>>> Beispiel: Newsletter mit 1000 Empfängern, einmal pro Woche, 1000 Tokens, 0,15 €/1M = 0,156 € pro Versand × 52 = 8,12 € pro Jahr.
>>> Berechne nun: 8000 Empfänger, 1200 Tokens.

# Self-Consistency: 5x ausführen mit temperature=0.7, Mehrheit nehmen
```

Vergleiche: welches Pattern gibt die beste Antwort? Wie viel kostet 5x-Self-Consistency mehr?

## Selbstcheck

- [ ] Du nennst die vier Patterns ohne nachzuschauen.
- [ ] Du erklärst, warum Few-Shot bei Klassifikations-Tasks oft Zero-Shot schlägt.
- [ ] Du weißt, dass moderne Reasoning-Modelle (o3, DeepSeek-R1) kein explizites CoT brauchen.
- [ ] Du erkennst Self-Consistency als 5x-Kostenfresser — und nutzt es nur, wenn nötig.

## Compliance-Anker

- **System-Prompts mit Personenbezug**: niemals echte Namen / Adressen / Mandanten-Daten direkt einbetten. Nutze Tokens (`{{user_id}}`), die dein Code lokal auflöst.
- **Logging**: Plaintext-Prompts speichern = DSGVO-Verarbeitung. Hashes statt Plaintext (siehe Phase 20.05).

## Quellen

- Brown et al. (2020) „GPT-3 / In-context Learning" — <https://arxiv.org/abs/2005.14165>
- Kojima et al. (2022) „Zero-Shot CoT" — <https://arxiv.org/abs/2205.11916>
- Wei et al. (2022) „Chain-of-Thought Prompting" — <https://arxiv.org/abs/2201.11903>
- Wang et al. (2022) „Self-Consistency" — <https://arxiv.org/abs/2203.11171>
- Anthropic, „Effective Prompt Engineering" — <https://docs.claude.com/en/docs/build-with-claude/prompt-engineering> (Zugriff 2026-04-28)

## Weiterführend

→ Lektion **11.02** (Structured Outputs mit Pydantic AI)
→ Lektion **11.05** (Anbieter-Vergleich mit echten Token-Kosten)
→ Phase **16** (Reasoning-Modelle — wenn CoT überflüssig wird)
