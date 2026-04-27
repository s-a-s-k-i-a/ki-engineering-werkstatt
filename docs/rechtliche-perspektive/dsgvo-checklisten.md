# DSGVO-Checklisten für KI-Systeme

> Praktische Checklisten — kein Rechtsrat. Bei konkreten Fragen: Datenschutzbeauftragte:n einbinden.

## 1. Vor Projektstart

- [ ] Verfahrensbeschreibung in das **Verzeichnis von Verarbeitungstätigkeiten** (VVT, Art. 30) eingetragen
- [ ] **Rechtsgrundlage** geklärt (Art. 6 Abs. 1 lit. a–f)
- [ ] **Besondere Kategorien** (Art. 9) geprüft — wenn ja, explizite Einwilligung oder Ausnahme
- [ ] **Einwilligungs-Templates** vorbereitet (Art. 7 — informiert, freiwillig, widerrufbar)
- [ ] **DSFA** (Art. 35) geprüft — Pflicht bei hohem Risiko
- [ ] **AVV** (Art. 28) mit allen Auftragsverarbeitern signiert (LLM, Vector-DB, Hosting, Tracing)
- [ ] **Drittland-Transfer** (Art. 44–46) geklärt — DPF, SCCs, BCR, TIA
- [ ] **Datenschutzbeauftragte:r** informiert

## 2. Beim Bauen

### Datenminimierung (Art. 5 Abs. 1 lit. c)

- [ ] Im System-Prompt **keine** Personenbezugsfelder hardcoden
- [ ] Vor dem LLM-Call: PII-Filter (Presidio, regex IBAN/E-Mail/Telefon)
- [ ] Embeddings: vor dem Embedden überprüfen, was im Text steht
- [ ] Logs: Hashes statt Plaintext (siehe Audit-Logging-Skelett)

### Zweckbindung (Art. 5 Abs. 1 lit. b)

- [ ] LLM-Aufrufe nur für deklarierten Zweck
- [ ] Keine „secondary use" Daten-Sammlung („für später vielleicht nützlich")

### Speicherbegrenzung (Art. 5 Abs. 1 lit. e)

- [ ] Aufbewahrungsfristen pro Datenklasse dokumentiert
- [ ] Auto-Delete-Jobs in Vector-DB und Logs
- [ ] Recht auf Löschung (Art. 17): Workflow definiert

### Integrität & Vertraulichkeit (Art. 5 Abs. 1 lit. f, Art. 32)

- [ ] TLS 1.3 für alle externen Calls
- [ ] At-rest-Verschlüsselung (AES-256)
- [ ] Zugriffskontrollen + Logging
- [ ] Schlüssel niemals im Code (siehe `.env.example`)

### Automatisierte Entscheidung (Art. 22)

- [ ] Bei Entscheidungen mit Rechtswirkung: Information + menschliches Eingreifen + Anfechtung
- [ ] Logik der Entscheidung kommunizieren (SHAP, Reasoning-Trace, Quellen)

## 3. Beim Betreiben

- [ ] **Audit-Logs** rotiert und gesichert (siehe Phase 20.05)
- [ ] **Vorfälle** binnen 72h melden (Art. 33)
- [ ] **Betroffenen-Rechte** (Art. 15–22) als API/Workflow umgesetzt
- [ ] Regelmäßige **Re-DSFA** bei wesentlichen Änderungen
- [ ] AVV-Subunternehmer-Liste aktuell halten

## 4. Bei Drittland-Transfer

- [ ] **DPF**-Status des Anbieters prüfen ([Liste der EU-Kommission](https://www.dataprivacyframework.gov/list))
- [ ] **SCCs** (Standardvertragsklauseln) zusätzlich abschließen
- [ ] **TIA** (Transfer Impact Assessment) erstellen — quartalsweise reviewen
- [ ] **EU-Datazone** (OpenAI, Anthropic, Google) wo möglich aktivieren
- [ ] Bei sensiblen Daten: **lokale Inferenz** (Ollama, Pharia) prüfen

## 5. Bei Trainingsdaten

- [ ] **Lizenz** der Trainingsdaten dokumentiert
- [ ] **TDM-Vorbehalte** (§ 44b UrhG) respektiert
- [ ] **Kein Scraping** von ai.txt-Disallow-Quellen
- [ ] **Bias-Test** auf Geschlecht, Alter, Region, Migrationshintergrund
- [ ] **Datasheet for Datasets** (Gebru et al.) erstellt

## 6. Quellen

- [DSGVO konsolidiert (EUR-Lex)](https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:32016R0679)
- [DSK Orientierungshilfe KI 06.05.2024](https://www.datenschutzkonferenz-online.de/media/oh/20240506_DSK_Orientierungshilfe_KI_und_Datenschutz.pdf)
- [BfDI Mustertexte](https://www.bfdi.bund.de/)
- [EDPB Opinion 28/2024](https://www.edpb.europa.eu/system/files/2024-12/edpb_opinion_202428_ai-models_en.pdf)
- [Bitkom Leitfaden KI & Datenschutz 2.0 (08/2025)](https://www.bitkom.org/sites/main/files/2025-08/bitkom-leitfaden-kuenstliche-intelligenz-und-datenschutz-auflage-2.pdf)
