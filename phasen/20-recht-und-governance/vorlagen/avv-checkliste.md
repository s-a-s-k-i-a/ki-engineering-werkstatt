# AVV-Checkliste für Cloud-LLM-Verträge (Art. 28 DSGVO)

> **Disclaimer**: Diese Checkliste ist keine Rechtsberatung. Nutze sie als Vorab-Prüfung, lass den finalen AVV von Datenschutzbeauftragte:n oder Kanzlei prüfen.

## Pflicht-Inhalte eines AVV nach Art. 28 Abs. 3

- [ ] **Gegenstand und Dauer** der Verarbeitung
- [ ] **Art und Zweck** der Verarbeitung
- [ ] **Art der personenbezogenen Daten**
- [ ] **Kategorien betroffener Personen**
- [ ] **Pflichten und Rechte** des Verantwortlichen
- [ ] **Weisungsgebundenheit** des Auftragsverarbeiters
- [ ] **Vertraulichkeitsverpflichtung** der Mitarbeitenden
- [ ] **Technisch-organisatorische Maßnahmen** (TOM) nach Art. 32
- [ ] **Subunternehmer-Regelung** (Vorabgenehmigung oder Liste)
- [ ] **Unterstützung des Verantwortlichen** bei Betroffenenrechten
- [ ] **Meldepflicht** bei Datenschutzverletzungen (≤ 72h)
- [ ] **Mitwirkung bei DSFA**
- [ ] **Löschung/Rückgabe** nach Vertragsende
- [ ] **Nachweis-/Audit-Recht** des Verantwortlichen

## Pro Anbieter

### Aleph Alpha

- AVV im Self-Service-Portal verfügbar
- TOM dokumentiert (BSI C5, ISO 27001)
- Server-Standort: Heidelberg, DE
- Subunternehmer: Hetzner (DE), AWS Frankfurt (für spezifische Workloads)

### Mistral AI

- DPA online signierbar
- Server: La Plateforme in Frankreich
- Empfohlen: Region `eu-west-3` explizit setzen

### OpenAI

- Enterprise/Team-Tier nötig (Free/Plus reichen NICHT für PII)
- Zero-Data-Retention setzen
- EU-Datazone (Q1 2026 erweitert)
- DPF + SCCs als Backup
- TIA aktuell halten

### Anthropic

- DPA via Account-Manager
- EU-Datazone (Q1 2026 angekündigt)
- DPF + SCCs als Backup
- Server: USA (mit EU-Routing optional)

### Google Cloud (Gemini)

- DPA online (Cloud-Konsole)
- Region: `europe-west` Family
- Customer-Managed Encryption Keys empfohlen

### IONOS AI Model Hub

- AVV im Cloud-Portal
- Server: Deutschland
- BSI C5 zertifiziert

### StackIT (Schwarz IT)

- AVV als Teil des Cloud-Vertrags
- Server: Deutschland
- BSI C5, ISO 27001

### OVH AI

- DPA-Anhang im Standard-Vertrag
- Region: `eu-west-2` (Paris) oder `eu-central-2` (Frankfurt)

### Hugging Face Inference Endpoints

- AVV per Enterprise-Plan
- Region wählbar (AWS / GCP / Azure-Backed)

### Drittanbieter (Together, Fireworks, DeepInfra, Scaleway, Nebius)

- AVV-Status individuell prüfen
- Bei US-Hostern: SCCs + TIA
- Bei EU-Hostern: Region erzwingen

## Wenn kein AVV verfügbar

- **Nicht produktiv nutzen** mit Personenbezug
- Für Lehre/Sandbox: synthetische Daten only
- Schatten-KI verhindern (siehe Bitkom 21.10.2025)

## Quellen

- [Art. 28 DSGVO (EUR-Lex)](https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:32016R0679)
- [BfDI Mustertexte](https://www.bfdi.bund.de/)
- [DSK Orientierungshilfe KI 06.05.2024](https://www.datenschutzkonferenz-online.de/media/oh/20240506_DSK_Orientierungshilfe_KI_und_Datenschutz.pdf)
