# Workshops aus dem Curriculum

> Drei Workshop-Formate, abgeleitet aus den 21 Phasen + 5 Capstones — direkt einsetzbar in Inhouse-Schulungen, KMU-Beratung oder Hochschul-Lehre. **MIT-Lizenz** wie das ganze Repo: Trainer:innen dürfen Folien, Übungen und Notebook-Auszüge frei adaptieren, **bitte mit Attribution** auf das Curriculum (`ki-engineering-werkstatt`).

## Format-Übersicht

| Format | Dauer | Zielgruppe | Output |
|---|---|---|---|
| [**4-h-Crashkurs**](4h-crashkurs.md) | 1 Halbtag | Entscheider:innen, Compliance-Officer, technisch interessierte Generalist:innen | „Ich kann meinen Use-Case AI-Act-Klassifizieren und Anbieter wählen" |
| [**8-h-Tagesworkshop**](8h-tagesworkshop.md) | 1 Tag | Backend-Entwickler:innen mit Python-Erfahrung | Lauffähige DSGVO-konforme RAG-App auf EU-Stack |
| [**16-h-Zweitagesworkshop**](16h-zweitagesworkshop.md) | 2 Tage | KI-Engineers, ML-Quereinsteiger:innen mit Backend-Hintergrund | Production-tauglicher Stack (RAG + Agent + Observability + Compliance-Doku) |

## Welches Format wann?

```mermaid
flowchart TD
    A[Wer ist die Zielgruppe?] --> B{Programmiert<br/>aktiv?}
    B -->|Nein| C[4h-Crashkurs]
    B -->|Ja| D{Production-Use-Case<br/>im Sinn?}
    D -->|Nein, „erst kennen­lernen"| E[8h-Tagesworkshop]
    D -->|Ja, will deployen| F[16h-Zweitagesworkshop]

    classDef option fill:#FF6B3D,color:#0E1116,stroke:#FF6B3D
    class C,E,F option
```

## Was alle drei Formate gemeinsam haben

- **Anti-Marketing-Block** zu Beginn — keine LLM-Hypes, sondern was 2026 in DACH wirklich funktioniert
- **EU-First-Stack**: Pharia, Mistral, Aleph Alpha, IONOS, OVH, Scaleway, STACKIT als Default
- **Compliance-First**: AI-Act-Risiko-Klassifizierung + DSGVO-Pflichten in jedem Format
- **Hands-on**: kein Slide-only — alle Formate haben mindestens ein Marimo-Notebook im Live-Demo
- **DACH-Kontext**: Maschinenbau, Finanz-/Versicherungs-, öffentliche Hand, Mittelstand-Beispiele
- **Quellen mit Datum**: jede Aussage über Markt / Anbieter / Pricing belegbar

## Was sie nicht sind

- **Nicht** „Chat-GPT für Anfänger" — wer nur Prompts in einem Browser tippen will, ist hier falsch
- **Nicht** „LLM-Foundations from Scratch" — selbst der 16-h-Workshop nutzt Pre-trained-Modelle; Phase 10 (LLM von Null) ist Curriculum-Material, kein Workshop-Format
- **Nicht** ohne Vorbereitung lieferbar — Trainer:innen brauchen Hands-on-Vorlauf mit dem Curriculum

## Trainer:innen-Vorbereitung (alle Formate)

1. **Mindestens 1× durchgespielt**: Notebooks lokal ausgeführt, Smoke-Tests grün
2. **EU-API-Keys parat**: Mistral, Aleph Alpha, optional Anthropic / OpenAI mit AVV
3. **Backup-Plan**: bei API-Ausfall Ollama-Local-Fallback (Phase 00)
4. **Compliance-Templates**: AVV-Muster, DSFA-Light, ai.txt-Generator-Output für Beispiel-Kunde
5. **Mit Saskia abgestimmt**: bei kommerzieller Nutzung als „offizieller `ki-engineering-werkstatt`-Trainer:in" gerne kurz Bescheid geben — dann kann das Repo auch als Referenz auf den Workshop verlinken (siehe [`CONTRIBUTING.md`](../../CONTRIBUTING.md))

## Teilnehmenden-Setup (vor dem Workshop)

| Format | Setup | Hardware |
|---|---|---|
| 4-h-Crashkurs | Browser reicht (Live-Demo durch Trainer:in) | Laptop, Internet |
| 8-h-Tagesworkshop | Repo geklont, `just setup` durchgelaufen, EU-API-Key | 16+ GB RAM, idealerweise Apple Silicon oder NVIDIA-GPU |
| 16-h-Zweitagesworkshop | wie 8 h **plus** Docker / OrbStack lauffähig, ggf. STACKIT/IONOS-Demo-Account | wie 8 h |

## Lizenz + Adaption

- **Workshop-Material**: MIT (wie das Repo). Adaptieren erlaubt — Attribution erbeten.
- **Bilder, Folien-Templates**: Lizenz pro Asset prüfen (`docs/assets/`)
- **Trainings-Daten / Beispiele**: nur Datasets aus `datasets/lizenzen/` ohne Re-Verifikation nutzen — andere immer mit Lizenz-Check

## Stand

29.04.2026 · Reviewer: Saskia Teichmann ([@s-a-s-k-i-a](https://github.com/s-a-s-k-i-a)) · Nächster Review nach erstem realen Workshop-Lauf.
