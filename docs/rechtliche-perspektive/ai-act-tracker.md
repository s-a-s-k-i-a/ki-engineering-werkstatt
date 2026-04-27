# AI-Act-Tracker

> Lebende Tabelle: Welcher AI-Act-Artikel gilt ab wann, welche Module dieses Repos sind betroffen?

**Stand: 2026-04-27.** Letzte Verifikation: heute. Volatil — siehe Hinweise am Ende.

## Inkrafttretens-Stufen

| Datum | Was greift | Betroffene Module |
|---|---|---|
| **01.08.2024** | AI Act tritt in Kraft (Inkrafttreten ≠ Anwendung) | alle |
| **02.02.2025** | **Verbote** (Art. 5) anwendbar | 04, 18, 20 |
| **02.02.2025** | **AI Literacy** (Art. 4) Pflicht für Bereitsteller | alle (insbesondere 20) |
| **02.08.2025** | **GPAI-Modell-Pflichten** (Art. 53) anwendbar | 10, 11, 16, 18 |
| **02.08.2025** | EU-Bußgeldbefugnis startet | alle |
| **02.08.2026** | **Hochrisiko**-Pflichten (Art. 6 + 9–15 + Anhang III) anwendbar | 02, 04, 06, 12, 14, 18, 19, 20 |
| **02.08.2026** | **Transparenz** (Art. 50) anwendbar | 06, 08, 11, 13, 14 |
| **02.08.2027** | Hochrisiko-Pflichten für Anhang-I-Bereiche (z. B. Medizinprodukt) | 19 (Capstone Medizin) |
| **02.08.2027** | Bestandsmodelle: Übergangsende für vor Aug 2025 in Verkehr gebrachte GPAI | 10, 11 |
| **31.12.2030** | Übergangsfrist für KI in IT-Großsystemen der Union (Anhang X) | 19 |

## Volatilität (was sich kurzfristig ändern kann)

- **Digital Omnibus on AI** (Kommissionsvorschlag 19.11.2025): Hochrisiko-Stichtag könnte von 02.08.2026 → **02.12.2027** verschoben werden. Trilog läuft, Einigung bis Mai 2026 angestrebt.
- **CEN-CENELEC harmonisierte Normen**: erste Q3 2026 erwartet — schaffen Konformitätsvermutung.
- **DPF (EU-US Data Privacy Framework)**: gültig bis EuGH-Urteil im Latombe-Verfahren (Q4 2026 erwartet).
- **KI-MIG (Deutsches Durchführungsgesetz)**: Verabschiedung Q2/Q3 2026.
- **Schweizer KI-Gesetz**: Vernehmlassung Ende 2026, Inkrafttreten frühestens 2028.

## Behörden DACH

| Land | Behörde | Rolle | Kontakt |
|---|---|---|---|
| DE | **BNetzA** (vorgesehen, ab KI-MIG) | zentrale Marktaufsicht | [bundesnetzagentur.de](https://www.bundesnetzagentur.de/) |
| DE | **BSI** | Cybersecurity, AIC4 | [bsi.bund.de](https://www.bsi.bund.de/) |
| DE | **BfDI** | Datenschutz (Bund) | [bfdi.bund.de](https://www.bfdi.bund.de/) |
| DE | **DSK** | Datenschutzkonferenz Bund/Länder | [datenschutzkonferenz-online.de](https://www.datenschutzkonferenz-online.de/) |
| DE | **BaFin** | Finance-Sektor | [bafin.de](https://www.bafin.de/) |
| AT | **RTR KI-Servicestelle** | KI-Auskunft & Beratung (kein Bußgeld) | [rtr.at/ki](https://www.rtr.at/rtr/service/ki-servicestelle/) |
| CH | **EDÖB** + sektorale Behörden | Datenschutz, KI-Konvention-Ratifikation | [edoeb.admin.ch](https://www.edoeb.admin.ch/) |
| EU | **AI Office** (DG CNECT) | GPAI mit systemischem Risiko | [digital-strategy.ec.europa.eu](https://digital-strategy.ec.europa.eu/) |

## Pro Artikel

### Art. 4 — AI Literacy

- **Wer**: Bereitsteller (Betreiber von KI-Systemen)
- **Was**: ausreichendes Maß an KI-Kompetenz
- **Modul**: 20 (siehe `vorlagen/ai-literacy-onboarding.md`)
- **Ab**: 02.02.2025
- **Sanktionsfähig**: ab 02.08.2026

### Art. 5 — Verbote

- **Wer**: alle
- **Was**: 8 verbotene Praktiken (Social Scoring, kognitive Manipulation, ...)
- **Modul**: 04, 18, 20
- **Ab**: 02.02.2025

### Art. 6 + Anhang III — Hochrisiko

- **Wer**: Anbieter, Bereitsteller
- **Was**: Konformitätsbewertung, Tech-Doku, Logging, Human Oversight
- **Module**: 02, 04, 06, 12, 14, 18, 19, 20
- **Ab**: 02.08.2026

### Art. 9–15 — Hochrisiko-Pflichten

- Risk Management, Data-Governance, Tech-Doku, Logging, Transparenz, Human Oversight, Accuracy/Robustness/Cybersecurity
- **Modul**: 20

### Art. 50 — Transparenz

- **Wer**: Anbieter und Bereitsteller von Chatbots, GenAI, Deepfakes, Emotionserkennung
- **Was**: Hinweise + maschinenlesbare Markierung
- **Module**: 06, 08, 11, 13, 14
- **Ab**: 02.08.2026

### Art. 53 — GPAI-Anbieter

- **Wer**: Provider von General-Purpose-AI-Modellen
- **Was**: Tech-Doku, Information an Bereitsteller, Copyright-Policy, Trainingsdaten-Zusammenfassung
- **Modul**: 10, 11
- **Ab**: 02.08.2025

### Art. 51, 55 — GPAI mit systemischem Risiko

- **Schwelle**: ≥10²⁵ FLOPs Trainings-Compute
- **Was**: zusätzlich Eval, Cybersecurity, Incident-Reporting, Energie-Doku
- **Modul**: 10, 11, 16, 18
- **Ab**: 02.08.2025

## Sanktionsrahmen

| Verstoß-Typ | Bußgeld-Obergrenze |
|---|---|
| Verbote (Art. 5) | bis 35 Mio. € oder 7 % Jahresumsatz (höher) |
| Hochrisiko-Pflichten | bis 15 Mio. € oder 3 % Jahresumsatz |
| Falsche/irreführende Angaben | bis 7,5 Mio. € oder 1 % Jahresumsatz |
| GPAI-Pflichten | bis 15 Mio. € oder 3 % weltweiter Umsatz |

KMU/Startups: günstigste Variante (3-Optionen-Regel).

## Quellen

- [VO 2024/1689 EUR-Lex (DE)](https://eur-lex.europa.eu/legal-content/DE/ALL/?uri=CELEX:32024R1689)
- [TÜV Consulting Digital Omnibus 2026](https://consulting.tuv.com/aktuelles/ki-im-fokus/eu-ai-act-2026-zwischenstand)
- [GPAI Provider Guidelines](https://digital-strategy.ec.europa.eu/en/policies/guidelines-gpai-providers)
- [BfDI AI-Act-Kurzpapier](https://www.bfdi.bund.de/SharedDocs/Kurzmeldungen/DE/2024/AI-Act.html)
- [Bundestag KI-MIG 1. Lesung 20.03.2026](https://www.bundestag.de/dokumente/textarchiv/2026/kw12-de-kuenstliche-intelligenz-1151800)
- [RTR KI-Servicestelle Zeitplan](https://www.rtr.at/rtr/service/ki-servicestelle/ai-act/Zeitplan.de.html)
- [Bundesrat CH 12.02.2025](https://www.news.admin.ch/de/nsb?id=104110)
