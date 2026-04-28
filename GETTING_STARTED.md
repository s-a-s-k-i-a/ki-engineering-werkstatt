# Wie du dieses Repo bedienst

> Stop scrolling, start learning. — eine Lektion in unter 10 Minuten von „git clone" bis „erste Antwort".

Diese Datei zeigt dir Schritt für Schritt, **wie du eine Lektion absolvierst** und das Curriculum produktiv nutzt. Wenn du nur die Übersicht willst: zurück zur [README](README.md).

## In 30 Sekunden: das Mentalmodell

```text
21 Phasen-Module        → grobe Themen (Tokenizer, RAG, Recht & Governance, ...)
└─ Lektionen            → einzelne Theorie-Häppchen (`lektionen/01-...md`)
   └─ Code-Notebook     → ausführbare Demo (`code/01-...py` als Marimo-.py)
   └─ Übung             → eigene Aufgabe (`uebungen/01-...md`)
   └─ Lösung            → Referenz-Implementierung (`loesungen/01-...py`)
   └─ Compliance-Anker  → DACH-/EU-Rechtshinweise (`compliance.md`)
```

Du arbeitest immer in **diesem Loop**: Lektion lesen → Notebook ausführen → Übung machen → Lösung vergleichen → Selbstcheck → nächste Lektion.

## Schritt 1 — einmaliges Setup (5 Min.)

```bash
# Falls du sie nicht hast: uv und just installieren
brew install uv just                 # macOS
# oder: curl -LsSf https://astral.sh/uv/install.sh | sh   # Linux
# Windows: siehe https://docs.astral.sh/uv/getting-started/installation/

# Repo holen
gh repo clone s-a-s-k-i-a/ki-engineering-werkstatt
cd ki-engineering-werkstatt

# Dependencies + pre-commit installieren
just setup

# Smoke-Test — alles grün?
just smoke
```

Wenn `just smoke` grün ist, bist du startklar. Wenn nicht: siehe [„Troubleshooting"](#troubleshooting) unten.

## Schritt 2 — wähle deinen Lernpfad

Vier Personas, vier vorbereitete Routen:

| Profil | Lernpfad | Zeit |
|---|---|---|
| 🛠️ WordPress-Entwickler:in | [docs/lernpfade/wp-entwicklerin.md](docs/lernpfade/wp-entwicklerin.md) | ~ 50 h |
| 📊 Data Scientist | [docs/lernpfade/data-scientist.md](docs/lernpfade/data-scientist.md) | ~ 100 h |
| ⚖️ Compliance-Officer | [docs/lernpfade/compliance-officer.md](docs/lernpfade/compliance-officer.md) | ~ 30 h |
| 🌱 Quereinsteiger:in | [docs/lernpfade/quereinsteigerin.md](docs/lernpfade/quereinsteigerin.md) | ~ 60 h |

Wenn du keinen Pfad wählen willst: starte einfach mit **Phase 05 (Deutsche Tokenizer)** — sie ist eines der drei voll ausgearbeiteten Showcase-Module und in 30–60 Minuten machbar.

## Schritt 3 — eine Lektion absolvieren (Beispiel: 05.01)

### 3.1 Modul-README anschauen

```bash
# Im Browser ansehen oder im Editor öffnen:
open phasen/05-deutsche-tokenizer/modul.md
```

Du findest dort:

- Lernziele
- Voraussetzungen (welche anderen Phasen du davor brauchst)
- Inhaltsübersicht (welche Lektionen es gibt)
- Verweis auf das Hands-on-Notebook
- Status (✅ fertig · 🚧 in Arbeit · ⏳ geplant)

### 3.2 Lektion lesen

```bash
open phasen/05-deutsche-tokenizer/lektionen/01-bpe-und-deutsch.md
```

Jede Lektion folgt dem gleichen Schema:

1. **Worum es geht** — Hook in einem Satz
2. **Voraussetzungen** — was du davor wissen solltest
3. **Konzept** — die Theorie, knapp
4. **Code-Walkthrough** — Verweis auf das Marimo-Notebook
5. **Hands-on** — Verweis auf die Übung
6. **Selbstcheck** — Checkliste, ob du's verstanden hast
7. **Compliance-Anker** — DACH-/EU-Rechtsbezug
8. **Quellen** — Primärquellen mit Datum
9. **Weiterführend** — was als Nächstes lohnt

### 3.3 Notebook ausführen

```bash
just edit 05-deutsche-tokenizer
# öffnet Marimo im Browser unter http://localhost:2718
```

**Was ist Marimo?** Ein modernes Notebook-Format. Statt `.ipynb` nutzt es `.py`-Dateien — das macht Git-Diffs lesbar und das Notebook deterministisch reproduzierbar. Du klickst „Run all" und siehst die Ergebnisse.

**Wenn du lieber Jupyter / Colab willst**: in CI werden `.ipynb`-Versionen automatisch aus den `.py`-Notebooks gebaut. Im README siehst du den Colab-Badge pro Lektion — ein Klick öffnet sie in Google Colab.

### 3.4 Übung machen

```bash
open phasen/05-deutsche-tokenizer/uebungen/01-aufgabe.md
```

Du bekommst eine konkrete Aufgabe (typisch 60–90 Min.). Schreibe dein eigenes Marimo-Notebook im selben Stil.

### 3.5 Lösung vergleichen

```bash
open phasen/05-deutsche-tokenizer/loesungen/01_loesung.py
```

Eine Referenz-Lösung. **Wichtig**: erst nach eigenen Versuch ansehen — sonst bringt das Lernen nichts.

### 3.6 Selbstcheck

Am Ende jeder Lektion ist eine Checkliste:

> - [ ] Du kannst erklären, warum `tiktoken cl100k` für deutschen Text suboptimal ist.
> - [ ] Du kannst zeigen, wie viele Tokens das Wort „Donaudampfschifffahrtsgesellschaftskapitän" in mindestens drei Tokenizern braucht.
> - [ ] Du hast eine eigene Empfehlung pro Use-Case.

Wenn du alle Punkte abhaken kannst → nächste Lektion.

## Schritt 4 — Quellen kennen lernen

Jede Lektion zitiert Primärquellen. Die zentrale Bibliothek liegt in [`docs/quellen.md`](docs/quellen.md), kategorisiert in 13 Bereiche:

- **A** Bücher
- **B** Foundational Papers
- **C** 2024–2026 State-of-the-Art
- **D** Deutsche / DACH-spezifisch
- **E** Recht & Compliance
- **F** Tooling-Docs
- **G** Datasets (mit Lizenz)
- **H** Blogs & Newsletter
- **I** Video-Kurse
- **K** Markt-Studien DACH-Mittelstand
- **L** Asiatische LLMs
- **M** China-Compliance
- **N** Sonstiges Tooling

Lektionen verweisen mit Anker-Codes (`[B.1]`, `[D.4]`, `[K.2]`) auf Einträge in dieser Datei. Lass dich nicht von der Menge erschlagen — du brauchst nicht alles auf einmal.

## Schritt 5 — Compliance verstehen

Jede Phase hat ein **`compliance.md`** mit den DACH-/EU-Rechtshinweisen, die für dieses Modul zentral sind. Beispiel: in Phase 13 (RAG) findest du Hinweise zu Quellen-Attribution nach AI-Act Art. 50.4 und Wikipedia-Lizenz (CC BY-SA 4.0).

Der **zentrale Compliance-Layer** liegt in [`docs/rechtliche-perspektive/`](docs/rechtliche-perspektive/):

- `ai-act-tracker.md` — welcher AI-Act-Artikel gilt ab wann?
- `dsgvo-checklisten.md` — vor / während / nach Projekt
- `avv-musterklauseln.md` — pro Cloud-Anbieter
- `urheberrecht-trainingsdaten.md` — TDM-Schranke § 44b UrhG
- `asiatische-llms.md` — Self-Censorship + Lizenz-Fallstricke
- `disclaimer.md` — kein Rechtsrat

Phase 20 ist das vollwertige **„Recht & Governance"-Modul** und liefert dir Werkzeuge:

```bash
# AI-Act-Klassifizierung deines KI-Systems
ki-act-classifier --modell-karte deine-model-card.yaml

# ai.txt + robots.txt für deine Domain (TDM-Opt-out)
ki-ai-txt --domain example.de -o ./output/

# Compliance-Schema validieren
ki-compliance-lint phasen/
```

## Schritt 6 — eigenes Capstone bauen (Phase 19)

Nach mehreren Phasen kannst du dein Wissen in einem Capstone bündeln. Vorgegebene Vorschläge:

- **19.A** WP-Plugin-Helfer-RAG
- **19.B** DSGVO-Compliance-Checker (KMU-Webseiten-Scanner)
- **19.C** Adoptions-Bot für eine Tierschutz-Organisation
- **19.D** Aktiengesetz-Rechtsfrage-Beantworter
- **19.E** Mehrsprachiger Voice-Agent

Du kannst auch **dein eigenes** Capstone bauen — wichtig ist, dass du dabei `ki-act-classifier` durchläufst und eine DSFA-Light schreibst.

## Schritt 7 — Mitwirken

Wenn du Tippfehler siehst, eine Quelle veraltet ist, oder du eine Lektion ergänzen willst:

```bash
# Branch erstellen
git checkout -b lektion/13-04-mein-vorschlag

# Arbeiten...
# Vor dem Commit: lokal grün?
just smoke

# Sign-off-Commit (DCO)
git commit -s -m "feat(phase-13): add ColBERT lesson"

# PR erstellen
git push origin lektion/13-04-mein-vorschlag
gh pr create
```

Details: [`CONTRIBUTING.md`](CONTRIBUTING.md) und [`docs/stilrichtlinien.md`](docs/stilrichtlinien.md).

## Troubleshooting

### `uv` oder `just` nicht gefunden

```bash
# uv
brew install uv      # macOS
curl -LsSf https://astral.sh/uv/install.sh | sh    # Linux

# just
brew install just    # macOS
cargo install just   # Linux/anywhere
```

### `just smoke` schlägt mit Permission-Fehlern fehl

```bash
chmod +x werkzeuge/*.py
just setup   # nochmal
```

### Marimo-Notebook öffnet, aber keine Outputs

Wahrscheinlich fehlt eine optionale Dependency. Pro Phase gibt es Extras:

```bash
uv sync --extra tokenizer      # für Phase 05
uv sync --extra rag            # für Phase 13
uv sync --extra agents         # für Phase 14
uv sync --extra production     # für Phase 17
```

### „No module named X"

Häufigster Grund: du hast `uv sync` ohne `--extra` für die Phase ausgeführt. Schau in die Phase-`modul.md`, welches Extra du brauchst.

### `docker compose up` für RAG-Stack

```bash
cd infrastruktur/docker
docker compose -f compose-fullstack.yml up -d
# Phoenix: http://localhost:6006
# Qdrant:  http://localhost:6333/dashboard
```

### Es läuft trotzdem nicht

[GitHub Discussion](https://github.com/s-a-s-k-i-a/ki-engineering-werkstatt/discussions) eröffnen — bitte mit:

- OS + Python-Version (`uv python list`)
- Output von `just smoke`
- Welche Phase / Lektion

## Was dieses Repo nicht ersetzt

- **Studium / Berufsausbildung**: dieses Curriculum ist Praxis-orientiert, ergänzt aber keine Vorlesung in Mathematik oder Informatik.
- **Rechtsberatung**: wir operationalisieren AI Act und DSGVO, aber bei konkreten Fällen → Datenschutzbeauftragte:r oder Kanzlei.
- **Sicherheits-Audit**: dieses Repo macht dich nicht zum Penetration Tester. OWASP LLM Top 10 wird in Phase 14 erklärt, aber tiefe Security braucht Spezialisten.

## Tempo

Realistische Erwartung:

- **Showcase-Module (05, 13, 20)**: 1–2 Wochen bei 4 h/Woche
- **Persona-Lernpfad WP**: ~ 12 Wochen
- **Persona-Lernpfad DS**: ~ 6 Monate
- **Voll-Curriculum mit allen 21 Phasen**: 1+ Jahr

Wenn du ein KI-Engineer in 30 Tagen werden willst: dieses Repo ist nicht für dich.

## Zurück zur README

Die Module-Tabelle, Mermaid-Curriculum-Übersicht und Markt-Realität findest du in der Haupt-[README](README.md).
