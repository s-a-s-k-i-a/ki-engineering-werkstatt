---
id: 10
phase: 10-llm-von-null
stand: 2026-04-27
anker:
  - trainingsdaten-provenance
  - art-53-trainingsdaten-zusammenfassung
  - urhg-44b-tdm
dsgvo_artikel:
  - art-5-abs-1-lit-a
ai_act_artikel:
  - art-53
  - art-50-abs-2
---

# Compliance-Anker — Phase 10

## Trainingsdaten-Provenance

Wer einen LLM trainiert (auch 50M-Mini): Trainingsdaten-Quelle dokumentieren. Bei OSCAR-DE: Lizenz heterogen (Common-Crawl-Basis), bei Wikitext-DE klar (CC BY-SA).

## AI-Act Art. 53 — GPAI-Anbieter (auch für kleine Modelle?)

GPAI-Pflichten gelten ab "general-purpose"-Charakter. Ein 50M-Modell ist *funktional* nicht GPAI, aber wenn man es als foundation publiziert, greifen Art. 53 lit. c (Copyright-Policy) + lit. d (Trainingsdaten-Zusammenfassung). Template: AI-Office-Vorlage.

## § 44b UrhG — TDM-Schranke

Beim Training auf Web-Scraped-Daten (OSCAR, Common Crawl) gilt die TDM-Schranke nur, wenn:

1. der ursprüngliche Anbieter keinen maschinenlesbaren Vorbehalt gesetzt hat
2. die Trainingsdaten nach Verwendung gelöscht oder in Modellgewichten "verlustig" sind

**LG/OLG Hamburg LAION-Urteile** (09/2024, 12/2025): Forschungsdaten nach § 60d UrhG zulässig, kommerzieller TDM nach § 44b nur mit beachtetem Opt-out.

## Outputs

KI-generierte Texte sind in DE/EU **nicht** urheberrechtlich geschützt (Mensch-Schöpfer-Prinzip). Wer das Modell öffentlich macht, hilft dem Lernen — kein Schöpferrecht an Outputs.

## Quellen

- [LG Hamburg LAION-Urteil 27.09.2024](https://www.lto.de/recht/hintergruende/h/kuenstliche-intelligenz-ki-urheberrecht-text-data-mining-lg-hamburg-310o22723)
- [OLG Hamburg LAION 10.12.2025](https://www.elbkanzlei.com/ki-training-mit-fremden-fotos-was-das-olg-hamburg-jetzt-erlaubt-az-5-u-104-24-laion-kneschke/)
- [LLäMmlein Paper (Würzburg 2024)](https://arxiv.org/abs/2411.11171)
