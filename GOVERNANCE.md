# Governance

## Maintainer

| Rolle | Person | Kontakt |
|---|---|---|
| Lead Maintainer | Saskia Teichmann ([@s-a-s-k-i-a](https://github.com/s-a-s-k-i-a)) | via GitHub |
| Compliance-Reviewer | n/a (offen) | — |
| Reviewer Asien-LLMs | n/a (offen) | — |

Solange das Repo klein ist (BDFL-Phase): Saskia entscheidet final, freut sich
aber über Beitragende, die Reviewer-Rollen übernehmen wollen.

## Entscheidungsprozesse

| Art der Entscheidung | Wie | Wer |
|---|---|---|
| Tippfehler, Quellen-Refresh, kleine Code-Fixes | Squash-Merge nach 1× Approve | Lead Maintainer |
| Neue Lektion, neue Übung | PR + 1 Reviewer | Lead Maintainer |
| Neue Phase, strukturelle Änderung | Discussion → RFC in `docs/architektur-entscheidungen/` → PR | Lead Maintainer + min. 1 weiterer Maintainer |
| Compliance-Update | PR + Verweis auf Primärquelle (BfDI/EDPB/EUR-Lex) | Lead Maintainer (oder Compliance-Reviewer) |
| Lizenzwechsel | Großer RFC, alle Mitwirkenden mit > 5 Commits werden konsultiert | Lead Maintainer |

## RFC-Prozess (Architektur-Entscheidungen)

Größere Änderungen werden als ADR ([Architecture Decision Record](https://adr.github.io/)
im MADR-Format) in `docs/architektur-entscheidungen/` dokumentiert. Beispiele:

- "Wir wechseln von Marimo zu Quarto"
- "Wir ergänzen ein Schwesterrepo auf Englisch"
- "Wir ersetzen Qdrant als Default-Vektor-DB"

ADR-Workflow:

1. Discussion eröffnen: Problem, Optionen, Trade-offs
2. Innerhalb von 14 Tagen: Entscheidung als ADR (Status: `proposed`)
3. PR mit ADR + ggf. Migrations-Plan
4. Merge → Status `accepted`

Verworfene ADRs bleiben mit Status `rejected` im Repo (Lerngut).

## Rolle der Community

- **Discussions** sind der primäre Ort für Ideen, Lektions-Wünsche,
  Quellen-Hinweise.
- **Issues** ausschließlich für reproduzierbare Probleme.
- **Wiki / Projects** sind aus.
- **Discord/Slack/Newsletter**: nicht geplant. Wir respektieren Aufmerksamkeit.

## Wartungsversprechen

| Bereich | Frequenz |
|---|---|
| AI-Act-Tracker | monatlich |
| Quellen-Bibliothek | quartalsweise |
| Curriculum-Module | wöchentliche PRs (soweit Zeit) |
| Hotfix-Issues bei AI-Act-Updates | binnen 7 Tagen |
| Security-Reports | Antwort binnen 7 Tagen |

## Bei Konflikten

Wenn Maintainer und Beitragende sich nicht einigen:

1. Discussion eröffnen, beide Standpunkte sachlich darstellen
2. Wenn keine Einigung: Lead Maintainer entscheidet, Begründung im Thread
3. Bei Verstößen gegen den Verhaltenskodex → CODE_OF_CONDUCT.md greift

## Wenn ich (Saskia) ausfalle

- Repo bleibt unter MIT-Lizenz public verfügbar.
- Falls 6 Monate keine Aktivität: Forks sind ausdrücklich willkommen, mit
  Hinweis auf Original.
- `CODEOWNERS` wird gepflegt — wenn ich Co-Maintainer ernenne, stehen sie
  dort.
