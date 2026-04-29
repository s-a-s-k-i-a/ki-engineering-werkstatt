# 4-h-Crashkurs „Erste KI-Anwendung DSGVO-konform"

> Halbtägiger Crashkurs für Entscheider:innen, Compliance-Officer und technisch interessierte Generalist:innen. **Kein Coding-Workshop** — sondern ein orientierungs- und entscheidungsfähig-machendes Format. Teilnehmende verlassen den Workshop mit einem **konkreten AI-Act-Klassifizierungsergebnis** für ihren eigenen Use-Case + einer **EU-Anbieter-Auswahl**.

## Zielgruppe

- KMU-Geschäftsführer:innen, die KI strategisch einführen wollen
- Compliance- / Datenschutz-Beauftragte vor erster KI-Beschaffung
- Produktmanager:innen, die einen LLM-Anbieter auswählen müssen
- IT-Leiter:innen ohne tiefes ML-Vorwissen

## Voraussetzungen

- Mindestens **eine konkrete Geschäftsidee oder Use-Case-Vermutung** mitbringen (nicht „wir wollen irgendwas mit KI")
- Browser, Internet
- Optional: 1 PDF / Dokument-Beispiel des eigenen Use-Cases (Tipp: Anonymisiert!)

## Lernergebnisse

Nach dem Crashkurs können Teilnehmende:

- Den **Markt-Stand 2026 in DACH** einschätzen (Bitkom, KfW, VDMA-Zahlen)
- LLM-Anbieter (OpenAI / Anthropic / Mistral / Aleph Alpha / DeepSeek / Qwen) **mit Compliance-Brille** vergleichen
- Den eigenen Use-Case nach **AI-Act-Risikoklasse** einordnen
- **EU-Hosting-Optionen** (STACKIT, IONOS, OVH, Scaleway) benennen und Trade-offs verstehen
- Eine **erste DSFA-Skizze** (Datenschutz-Folgenabschätzung) für ihren Use-Case erstellen
- Erkennen, wann **klassisches ML** ausreicht und kein LLM nötig ist

## Agenda (4 × 45 min + Pausen)

### 0:00–0:30 · Markt-Realität DACH (Welcome + Phase 00.07)

- Anti-Marketing-Block: was 2026 in DACH wirklich passiert
- Bitkom 41 % Adoption vs. KfW ~ 20 % (KMU) — der Realitäts-Spread
- Top-3-Hindernisse: Recht 53 % / Know-how 53 % / Datenschutz 48 %
- **Lernziel**: realistische Erwartungshaltung statt Hype

> **Material**: [`phasen/00-werkzeugkasten/markt-und-realitaet.md`](../../phasen/00-werkzeugkasten/markt-und-realitaet.md), [Bitkom-Studie](https://www.bitkom.org/Presse/Presseinformation/Durchbruch-Kuenstliche-Intelligenz)

### 0:30–1:00 · Welcher Anbieter — und warum?

- Anbieter-Vergleich (Phase 11.05): Pricing pro 1M Token, Datenresidenz, AVV-Verfügbarkeit
- EU-First-Stack: Mistral / Aleph Alpha / Pharia / IONOS / Scaleway
- US-Anbieter mit DSGVO: AVV + SCC + TIA, Anthropic-Münchner-Office als pragmatischer Anker
- Asiatische Open-Weights: lokal okay, API problematisch (DeepSeek, Qwen, GLM)
- **Hands-on (Live-Demo)**: Anbieter-Showdown-Notebook (nur Trainer:in spielt vor)

> **Material**: [`phasen/11-llm-engineering/lektionen/05-anbieter-vergleich.md`](../../phasen/11-llm-engineering/lektionen/05-anbieter-vergleich.md), [`phasen/11-llm-engineering/code/01_anbieter_showdown.py`](../../phasen/11-llm-engineering/code/01_anbieter_showdown.py)

### 1:00–1:15 · Pause

### 1:15–2:00 · LLM oder klassisches ML? (Phase 02 + 11)

- Wann LLM: unstrukturierter Text / Generierung / Multi-Turn-Dialog
- Wann klassisches ML: tabular Data, < 1M Samples, gemischte Features → Boosting (XGBoost / LightGBM)
- Kostenvergleich: LLM-Inferenz vs. Random-Forest-Inferenz (Faktor 100-1000×)
- AI-Act-Konsequenzen: SHAP für Erklärbarkeit (Phase 02.03), DSGVO Art. 22

> **Material**: [`phasen/02-klassisches-ml/lektionen/02-modellauswahl-baseline-bis-boosting.md`](../../phasen/02-klassisches-ml/lektionen/02-modellauswahl-baseline-bis-boosting.md)

### 2:00–3:00 · AI-Act-Klassifikator: dein Use-Case (Phase 20)

- AI-Act-Risikoklassen (verboten / Hochrisiko / GPAI / niedrig) anhand Phase 20.01
- **Hands-on (alle)**: jede:r Teilnehmer:in füllt für den eigenen Use-Case eine Klassifikations-Karte aus (Template wird verteilt)
- **Live-Demo**: `ki-act-classifier` CLI mit Beispiel-Modell-Karte
- Anhang III-Use-Cases (Recruiting, Kredit, Bildung, Justiz, biometrische Daten) als Stop-Signal

> **Material**: [`phasen/20-recht-und-governance/lektionen/01-ai-act-risk.md`](../../phasen/20-recht-und-governance/lektionen/01-ai-act-risk.md), [`werkzeuge/ai_act_classifier.py`](../../werkzeuge/ai_act_classifier.py)

### 3:00–3:15 · Pause

### 3:15–4:00 · DSFA-Light + EU-Hosting + nächste Schritte

- DSFA-Light-Template (Phase 20): Schwellwerte, wann DSFA-pflicht
- EU-Hosting-Übersicht (Phase 17.04): STACKIT (BSI C5 Type 2), IONOS, OVH, Scaleway
- Pharia-1 als DACH-Default für nicht-frontier-Anwendungen
- **Wrap-up**: jede:r formuliert 3 nächste Schritte für ihren Use-Case
- Verweis auf Curriculum für vertiefende Selbststudien

> **Material**: [`phasen/17-production-und-eu-hosting/lektionen/04-eu-cloud-stack.md`](../../phasen/17-production-und-eu-hosting/lektionen/04-eu-cloud-stack.md), [`docs/rechtliche-perspektive/dsgvo-checklisten.md`](../rechtliche-perspektive/dsgvo-checklisten.md)

## Material-Pakete

### Was Trainer:innen mitbringen

- Folien-Set (50–80 Slides, ~ 60 % Inhalt + 40 % Diskussion)
- Anbieter-Vergleichs-Notebook (Phase 11) **vorab live-getestet**
- 5–7 vorgefertigte AI-Act-Klassifizierungs-Beispiele aus DACH-Branchen (Maschinenbau, Steuerberatung, Recht, Gesundheit, HR, Bildung, öffentliche Hand)
- DSFA-Light-Template als ausfüllbares PDF
- Backup: gedrucktes „Spickzettel-Heft" mit Quellen-URLs

### Was Teilnehmende mitnehmen

- DSFA-Light-Template (eigener Use-Case)
- Anbieter-Vergleichs-Tabelle (eigene Auswahl)
- AI-Act-Klassifizierungs-Karte (eigener Use-Case mit Risikoklasse)
- Lese-Liste: `docs/lernpfade/compliance-officer.md` und `docs/lernpfade/quereinsteigerin.md`
- Optional: kostenfreies Folge-Q&A nach 4–6 Wochen

## Trainer:innen-Checkliste (Vorbereitung)

- [ ] Curriculum mindestens 1× selbst durchgespielt (Phasen 00, 02, 11, 17, 20)
- [ ] Anbieter-Showdown-Notebook lokal lauffähig
- [ ] Aktuelle Markt-Zahlen geprüft (Bitkom, KfW — Stand-Datum < 6 Monate)
- [ ] AI-Act-Stand geprüft (Inkrafttreten / Anhang IV / GPAI Code of Practice)
- [ ] Branchen-spezifische DACH-Beispiele für die Zielgruppe vorbereitet
- [ ] EU-API-Keys für Live-Demo (mind. Mistral + Aleph Alpha)
- [ ] Backup-Internet (Hotspot) bei externem Workshop

## Anti-Patterns

- **Nicht** stundenlang über Transformer-Mathematik dozieren — die Zielgruppe braucht Geschäftsentscheidungen, keine Linear-Algebra
- **Nicht** ChatGPT-Demo als Hauptelement — alle haben das schon, das spart keine Zeit
- **Nicht** ein einziges US-Anbieter-Beispiel ohne EU-Alternative
- **Nicht** Compliance als „Bremsklotz" framen — es ist Pflicht-Pattern, nicht Hindernis

## Erfolgs-Metrik

Eine Workshop-Sitzung war erfolgreich, wenn am Ende:

- Mindestens 80 % der Teilnehmenden eine konkrete AI-Act-Risikoklasse für ihren Use-Case nennen können
- Mindestens 60 % einen konkreten EU-Anbieter mit Begründung wählen
- Mindestens 50 % wissen, ob sie eine DSFA brauchen (und warum)

## Stand

29.04.2026 · 4-h-Format basiert auf Phasen 00 / 02 / 11 / 17 / 20 · Format-Reviewer: Saskia Teichmann.
