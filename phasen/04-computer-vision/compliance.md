---
id: 4
phase: 04-computer-vision
stand: 2026-04-27
anker:
  - biometrie-verbot-art-5
  - vlm-china-disclaimer
  - synthetische-bilder-art-50
dsgvo_artikel:
  - art-9
  - art-22
ai_act_artikel:
  - art-5-abs-1-lit-e
  - art-5-abs-1-lit-h
  - art-50-abs-2
---

# Compliance-Anker — Phase 04

## Biometrie-Verbote (Art. 5)

- **Art. 5 Abs. 1 lit. e**: Aufbau von Gesichtserkennungs-Datenbanken aus Internet-/CCTV-Scraping = **inakzeptables Risiko, verboten** (auch für Lernprojekte!).
- **Art. 5 Abs. 1 lit. h**: Echtzeit-Gesichtserkennung in öffentlich zugänglichen Räumen für Strafverfolgung = grundsätzlich verboten (eng definierte Ausnahmen).
- Im Lernprojekt: nutze **Tier**-Bilder (deutsche Tierschutz-Organisation) statt menschliche Gesichter.

## DSGVO Art. 9 — biometrische Daten als besondere Kategorie

Selbst „nur" zu Demo-Zwecken: biometrische Daten (Gesichts-Embeddings) brauchen ausdrückliche Einwilligung oder andere enge Rechtsgrundlage.

## Asiatische VLMs — DACH-Disclaimer

Qwen3-VL und MiniCPM-o sind exzellent (Apache 2.0!) und werden in dieser Phase eingesetzt. Aber:

> **⚠️ Lokale Inferenz auf eigener/EU-Hardware = DSGVO-konform.** Modell-Weights sind Mathematik, kein Datentransfer.
> **Offizielle CN-API (dashscope.aliyun.com) = problematisch** — kein EU-Vertreter, AVV unklar.
> **Self-Censorship-Bedenken**: weniger relevant für Bild-Klassifikation, sehr relevant für Bild-Beschreibung mit politischem Kontext (Tiananmen-Foto, Taiwan-Karte etc.).

Volle Hinweise in `docs/rechtliche-perspektive/asiatische-llms.md`.

## Synthetische Bilder (Art. 50 Abs. 2)

Wenn deine Pipeline Bilder generiert (Phase 08): Pflicht zur **maschinenlesbaren Markierung** (C2PA). Ab 02.08.2026 voll wirksam.

## Quellen

- [AI Act Art. 5](https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:32024R1689)
- [SAM 2 Paper](https://ai.meta.com/research/publications/sam-2-segment-anything-in-images-and-videos/)
- [Qwen3-VL GitHub](https://github.com/QwenLM/Qwen3-VL)
