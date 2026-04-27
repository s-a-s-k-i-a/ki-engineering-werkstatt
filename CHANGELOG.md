# Changelog

Alle nennenswerten Änderungen an diesem Repo werden hier dokumentiert.
Format orientiert sich an [Keep a Changelog](https://keepachangelog.com/de/1.1.0/),
Versionierung folgt einer angepassten [Semantic Versioning](https://semver.org/lang/de/):

- **MAJOR**: Curriculum-Restrukturierung, breaking changes an Phasen/IDs
- **MINOR**: neues Modul fertig, neue Phase, neues Werkzeug
- **PATCH**: einzelne Lektion ergänzt, Compliance-Update, Quellen-Refresh, Bugfix

## [Unreleased]

## [0.1.0] - 2026-04-27

### Hinzugefügt

- Repo-Skelett mit allen 21 Phasen (00-werkzeugkasten bis 20-recht-und-governance)
- Drei voll ausgearbeitete Showcase-Module:
  - **Phase 05 — Deutsche Tokenizer**: Token-Effizienz-Showdown auf 10kGNAD
    mit GPT-5, Claude 4.7, Llama 4, Mistral Large, Pharia-1, Teuken-7B
  - **Phase 13 — RAG-Tiefenmodul**: Vanilla → Hybrid → ColBERT → GraphRAG →
    LazyGraphRAG → Agentic RAG mit Qdrant + dt. Wikipedia
  - **Phase 20 — Recht & Governance**: AI-Act-Risk-Klassifizierung-CLI,
    AVV-Mustertemplate, DSFA-Workflow, ai.txt-Generator, Audit-Logging-Skelett
- Compliance-Layer (`docs/rechtliche-perspektive/`):
  - AI-Act-Tracker mit Stand 2026-04-27
  - DSGVO-Checklisten für KI-Systeme
  - AVV-Musterklauseln-Verweise (BfDI/EDPB)
  - Urheberrecht & TDM-Opt-out (§ 44b UrhG)
  - Disclaimer "Kein Rechtsrat"
- EU-Modelle Setup (`infrastruktur/eu-modelle/`): Aleph Alpha Pharia, Mistral EU,
  IONOS AI Foundation, Ollama lokal, vLLM on-prem
- Quellenbibliothek `docs/quellen.md` mit kuratierten Primärquellen,
  kategorisiert in 13 Bereiche inkl. DACH-Marktstudien und asiatischen LLMs
- Vier Persona-Lernpfade (WP-Entwickler:in, Data Scientist, Compliance-Officer,
  Quereinsteiger:in)
- CI/CD: lint, typecheck, notebooks-build, notebooks-smoke, link-check,
  secrets-scan, compliance-check, release-please
- Tooling: uv 0.10, Python 3.13, Marimo, Ruff, Ty, pre-commit, gitleaks
- TDM-Opt-out via `ai.txt` und `robots.txt` für 18 KI-Crawler

### Compliance-Updates

- AI-Act-Tracker initial mit Stand der Inkrafttretens-Stufen Q2/2026
- Hinweis auf Digital-Omnibus-AI-Vorschlag (Verschiebung Hochrisiko evtl. → 12/2027)
- DSGVO/EDPB Opinion 28/2024 zu LLMs/Trainingsdaten verlinkt
- LG/OLG-Hamburg-LAION-Urteile (TDM-Schranke) referenziert
- BSI Grundschutz++ KI-Bausteine (operativ ab 04/2026) erwähnt

### Bekannte Lücken

- 17 von 20 Phasen sind als Skelett vorhanden, voll ausgearbeitet folgen
  iterativ (siehe ROADMAP.md)
- Eigene EN-Übersetzung steht aus (Schwesterrepo geplant)
- Capstone-Implementierungen sind als Skelett angelegt, vollständige
  Codebases folgen
