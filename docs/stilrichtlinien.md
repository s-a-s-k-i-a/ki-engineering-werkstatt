# Stilrichtlinien

> Was in dieses Repo passt, was nicht.

## Sprache

- **Deutsch primär** (Inhalte, Erklärungen, Hands-on-Anleitungen)
- **Englisch in Code-Identifiern** (Industrie-Standard, internationale Lesbarkeit)
- **Du-Form** (kein Sie, nicht im Lehr-Kontext)
- **Deutsche Rechtschreibung nach Duden**
- **Kein Marketing-Sprech**: keine „revolutionary", „game-changing", „leveragen"
- **Geschlechtergerecht**: Doppelpunkt-Form `Entwickler:in` (oder Substantivierung wo passend) — keine Sterne, kein Binnen-I, keine generische maskuline Form

## Tone-of-Voice

- **Knapp, direkt, präzise** — Saskia-Stil
- **Hooks**: „Stop X from Y." als wiederkehrende Reibungs-Fläche
- **Real-World**: Beispiele aus deutsche Tierschutz-Organisation, deutschen KMU, isla, citelayer-Ökosystem
- **Selbstironisch, nicht zynisch** — Lernende sollen sich willkommen fühlen
- **Kein Hype**, nichts hochjubeln
- **Mermaid-Diagramme** statt Adjektivlawinen
- **Tabellen** statt Listen, wenn vergleichend
- **Code-Blöcke** sind copy-paste-tauglich

## Markdown

- **ATX-Header** (`#`, `##`, `###`)
- **Fenced Code Blocks** mit Sprach-Tag (```` ```python ````)
- **Inline-Code** mit Backticks
- **Links**: `[Text](url)` — keine Bare-URLs
- **Block-Quotes** für Hooks und Disclaimer
- **Mermaid** wo strukturell sinnvoll, nicht für Deko
- **Frontmatter** (YAML) für Metadaten in Lektionen + Modulen + Compliance

## Code

- **Marimo** als Notebook-Default (`.py`, source-of-truth)
- **Python 3.13** ausschließlich
- **uv** für Dependency-Management
- **Type Hints** auf öffentlichen Funktionen
- **Ruff + Ty** müssen grün sein
- **Keine `print()`-Debug-Statements** in Lehr-Notebooks (`rich.console` für hübsche Ausgabe, oder gar nichts)
- **Kommentare**: NUR wenn das *Warum* nicht aus dem Code ersichtlich ist
- **Docstrings**: einzeilig, prägnant. Keine multi-paragraphigen Erklärungen — die gehören in die Lektion.

## Lektionen-Struktur

1. **YAML-Frontmatter** (id, titel, dauer, schwierigkeit, stand, voraussetzungen, lernziele, compliance_anker, colab_badge)
2. **Optionaler Colab-Badge-Block** (auto-injiziert)
3. **Worum es geht** (Hook, 1 Satz)
4. **Voraussetzungen**
5. **Konzept** (Theorie, knapp)
6. **Code-Walkthrough** (Verweis auf `code/...py` + Schlüsselstellen inline)
7. **Hands-on** (Verweis auf `uebungen/...md`)
8. **Selbstcheck** (Checklisten-Punkte)
9. **Compliance-Anker**
10. **Quellen** (mit Datum)
11. **Weiterführend**

## Compliance-Anker-Frontmatter

```yaml
compliance_anker:
  - quellen-attribution-art-50  # kebab-case
ai_act_artikel:
  - art-50-abs-4
dsgvo_artikel:
  - art-5-abs-1-lit-b
```

Validiert per `werkzeuge/compliance_lint.py`.

## Quellen

- **Pflicht**: jede Lektion mit mindestens 3 Primärquellen + Datum (Zugriff oder Veröffentlichung)
- **Ankerverweise** in `docs/quellen.md` (z. B. `[B.1]`)
- **Inline-Links** mit URL und Datum
- **Stand-Datum** in Frontmatter — Update bei jedem inhaltlichen Refresh

## Was hier nicht hingehört

- Affiliate-Links
- Discord-/Newsletter-/Webinar-CTAs
- Marketing-Banner
- Auto-generierter Text ohne menschliche Redaktion
- Zynismus oder Geringschätzung anderer Frameworks
- Behauptungen ohne Quelle
