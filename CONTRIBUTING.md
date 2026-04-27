# Mitwirken an der KI-Engineering-Werkstatt

Du willst beitragen — schön. Damit der Aufwand für alle gering bleibt, hier
das Wichtigste auf einer Seite.

## Für welche Beiträge ich offen bin

✅ **Sehr willkommen:**

- Tippfehler, falsche Übersetzungen, schiefe Formulierungen
- Aktualisierte Quellen-URLs (besonders bei `docs/quellen.md`)
- Compliance-Updates (AI Act, BSI, BfDI, DSK, EDPB)
- Neue Lektionen oder Übungen mit deutschem Kontext (Datasets, Use-Cases)
- Korrekturen in Code-Beispielen, die nicht mehr lauffähig sind
- Persona-Pfade für Lernende, die ich übersehen habe
- Übersetzungsfehler bei Fachbegriffen (DE↔EN)

🤔 **Bitte zuerst Discussions:**

- Neue Phasen oder strukturelle Änderungen
- Größere Refactorings
- Neue Tooling-Wahl (Marimo durch X ersetzen, etc.)
- Ergänzungen zum Compliance-Layer

❌ **Bitte nicht:**

- Marketing-Pull-Requests („Add affiliate link to course X")
- AI-generierte Texte ohne menschliche Überarbeitung — fallen meist auf
  und werden nicht akzeptiert
- LinkedIn-/Discord-/Newsletter-Buttons in der README

## Bevor du anfängst

1. Suche bestehende Issues und Discussions
2. Bei größeren Änderungen: erst Discussion eröffnen
3. Lies `docs/stilrichtlinien.md` für Tone-of-Voice und Tabellen-/Mermaid-Stil

## Workflow

```bash
# 1. Fork auf GitHub anlegen, dann lokal:
gh repo clone DEIN-USER/ki-engineering-werkstatt
cd ki-engineering-werkstatt

# 2. Branch erstellen
git checkout -b lektion/13-04-colbert

# 3. Setup
just setup

# 4. Arbeiten — und dabei eines der Marimo-Notebooks editieren
just edit 13-rag-tiefenmodul

# 5. Vor dem Commit: lokal grün bekommen
just smoke

# 6. Conventional Commit + DCO
git commit -s -m "feat(phase-13): add ColBERT late-interaction lesson"

# 7. Push, PR auf upstream main
git push origin lektion/13-04-colbert
gh pr create
```

## Commit-Konvention

Wir folgen [Conventional Commits](https://www.conventionalcommits.org/):

```text
<type>(<scope>): <kurze Aussage>

<längere Beschreibung optional>

Signed-off-by: Vorname Nachname <mail@example.com>
```

**Types**: `feat`, `fix`, `docs`, `refactor`, `test`, `compliance`, `chore`

**Scopes**: `phase-NN`, `compliance`, `werkzeuge`, `docs`, `ci`, `infra`

Beispiele:

- `feat(phase-13): add LazyGraphRAG vergleichs-notebook`
- `compliance(docs): update AI-Act-Tracker after Digital-Omnibus`
- `fix(werkzeuge/ai_act_classifier): handle empty model-card.yaml`

## DCO statt CLA

Wir nutzen den [Developer Certificate of Origin](https://developercertificate.org/)
statt eines CLA. Heißt: jeder Commit muss `Signed-off-by:` enthalten —
`git commit -s` macht das automatisch.

## Stilrichtlinien

### Sprache

- **Du-Form**, deutsche Rechtschreibung nach Duden, klare Sätze
- **Englische Code-Identifier** sind okay (Industrie-Standard)
- **Keine Emojis im Fließtext**, max. 1 in Section-Headern
- **Keine Marketing-Floskeln** („revolutionary", „game-changing", „leveragen")
- **Mermaid-Diagramme bevorzugt** statt Adjektivlawinen
- **Quellen-Pflicht**: jede Lektion mind. 3 Primärquellen mit Datum

### Code

- **Marimo `.py`** als source-of-truth (kein `.ipynb` committen)
- **uv** statt pip/poetry — Dependencies in `pyproject.toml`
- **Python 3.13**, kein älterer Stack
- **Ruff + Ty** müssen grün sein
- **Type Hints** für öffentliche Funktionen
- **Keine `print()`-Debug-Statements** — `rich.console` oder strukturierte Logs

### Lektionen

Jede neue Lektion folgt diesem Schema:

```markdown
---
id: 13.04
titel: ColBERT Late-Interaction
phase: 13-rag-tiefenmodul
dauer_minuten: 60
schwierigkeit: mittel
stand: 2026-04-27
voraussetzungen: [13.01, 13.02]
lernziele: [...]
compliance_anker: [...]
colab_badge: true
---

## Worum es geht
> Hook in einem Satz.

## Voraussetzungen
## Konzept
## Code-Walkthrough
## Hands-on
## Selbstcheck
## Compliance-Anker
## Quellen
## Weiterführend
```

### Compliance-Updates

Wenn das EU-AI-Act-Datum sich verschiebt oder eine BfDI-Stellungnahme neu
erscheint:

1. `docs/rechtliche-perspektive/ai-act-tracker.md` updaten (mit Stand-Datum)
2. CHANGELOG-Eintrag unter „Compliance-Updates"
3. Betroffene `compliance.md` der Phasen prüfen

## Akzeptanztests

Vor dem Merge müssen lokal grün sein:

```bash
just smoke   # Lint + Typecheck + Pytest + Linkcheck (offline) + Gitleaks
```

In der CI laufen zusätzlich:

- `notebooks-smoke.yml`: jedes Notebook headless ausführen
- `link-check.yml`: lychee online (ohne Cache)
- `compliance-check.yml`: Schema je `compliance.md`
- `secrets-scan.yml`: gitleaks + trufflehog full-history

## Diskussion und Kontakt

- **GitHub Discussions**: für Ideen, Lektions-Vorschläge, Architektur-Fragen
- **GitHub Issues**: für konkrete Bugs/Tippfehler
- **conduct [at] wp-studio.dev**: für Verstöße gegen den Verhaltenskodex
- **security [at] wp-studio.dev**: für Sicherheitslücken

Kein Discord, kein Slack, kein Newsletter. Bitte respektieren.

## Danke

Jeder ernsthafte Beitrag macht das Curriculum besser. Versprochen, ich
schaue regelmäßig in die Issues — auch wenn die Antwort manchmal ein paar
Tage braucht.
