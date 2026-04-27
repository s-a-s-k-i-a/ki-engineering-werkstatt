# Übung 05.01 — Eigener Tokenizer-Showdown

> Schwierigkeit: mittel · Zeit: 60–90 Min · Voraussetzung: Lektion 05.01 + Showdown-Notebook gelaufen.

## Ziel

Du wendest den Showdown auf **deine eigenen Texte** an und triffst eine fundierte Tokenizer-Entscheidung für einen konkreten Use-Case.

## Aufgabe

1. **Sammle 5 deutsche Texte** aus unterschiedlichen Domänen, jeweils ca. 200–500 Wörter:
   - Sport-Bericht (z. B. NDR.de, kicker.de)
   - Rechtstext (z. B. ein Auszug aus § 44b UrhG, BGH-Urteil)
   - Technik (Heise, Golem, Github-README auf DE)
   - Belletristik (Goethe, Kafka — gemeinfrei!)
   - Werbung/Marketing (Newsletter, Online-Shop-Beschreibung)

2. **Tokenisiere** jeden Text mit mindestens vier dieser Tokenizer:
   - `tiktoken` `cl100k_base` (GPT-4)
   - `tiktoken` `o200k_base` (GPT-5/o3)
   - `transformers` `mistralai/Mistral-Large-Instruct-2411`
   - `transformers` `meta-llama/Llama-3-8B`
   - `transformers` `Aleph-Alpha/Pharia-1-LLM-7B-control`
   - `transformers` `openGPT-X/Teuken-7B-instruct-research-v0.4`

3. **Erstelle eine Vergleichs-Tabelle** mit Pandas:

   | Tokenizer | Sport | Recht | Technik | Belletristik | Werbung | Summe | EUR pro 1.000× |
   |---|---|---|---|---|---|---|---|

4. **Plotte zwei Diagramme**:
   - Bar-Chart der Token-Anzahl pro Tokenizer × Domäne
   - Boxplot der Token-pro-Wort-Verhältnisse

5. **Schreibe eine Empfehlung** (max. 200 Wörter): Welcher Tokenizer für welchen Use-Case in deinem Unternehmen / Projekt? Begründe Effizienz, Kosten und DSGVO-Einordnung.

## Bonus (für Schnelle)

- Vergleiche Token-Anzahl mit DeepSeek-V3 (`deepseek-ai/DeepSeek-V3-Base`) und Qwen3 (`Qwen/Qwen3-8B`). Übernimm den DACH-Compliance-Disclaimer aus `docs/rechtliche-perspektive/asiatische-llms.md`.
- Berechne, wie viele Tokens dein durchschnittlicher Newsletter pro Versand spart, wenn du von GPT-5 auf Pharia oder Teuken wechselst — und multipliziere mit deiner Versandfrequenz.

## Abgabe

- Marimo-Notebook in `loesungen/01_loesung.py` committet
- Pandas-Tabelle als CSV in `loesungen/01_tabelle.csv`
- Empfehlungstext als Markdown-Block am Ende des Notebooks

## Wann gilt es als gelöst?

- `just smoke` läuft ohne Fehler durch
- Mindestens 4 Tokenizer wurden verglichen
- Empfehlung enthält konkrete EUR-Beträge, nicht nur Token-Zahlen
- Compliance-Hinweise mit verlinkten Quellen
