---
id: 15
phase: 15-autonome-systeme
stand: 2026-04-27
anker:
  - robots-txt-respekt
  - urhg-44b-bei-scrapen
  - persoenlichkeitsrechte-personenbezug
  - cost-cap-pflicht
dsgvo_artikel:
  - art-5-abs-1-lit-c
  - art-25
ai_act_artikel:
  - art-14
---

# Compliance-Anker — Phase 15

## robots.txt + ai.txt respektieren

Wer Browser-Agenten baut, die fremde Webseiten lesen: respektiere `robots.txt` und `ai.txt` der Zielseite. Verstoß = Hausfriedensbruch im virtuellen Raum + ggf. UWG (Wettbewerbsverzerrung).

## § 44b UrhG bei Web-Scraping

Auch Agent-basiertes Lesen ist TDM. Wenn die Webseite einen TDM-Vorbehalt hat (`ai.txt` Disallow), darf der Agent **nicht** für KI-Training oder dauerhafte Speicherung scrapen.

## Persönlichkeitsrechte / DSGVO-Art. 5

Webseiten enthalten oft Personennamen, Bilder, E-Mails. Agent-Output mit Personenbezug → DSGVO greift voll. Pseudonymisieren, nur wenn Zweck es deckt.

## Cost-Caps (Art. 14 — Human Oversight Edge-Case)

Long-Running-Agent ohne Budget-Limit = Risk. Pflicht-Pattern:

- Pro-Run-Token-Limit
- Pro-Tool-Call-Limit
- Wall-Clock-Timeout
- Eskalation bei Überschreitung

## Quellen

- [BfDI zu Web-Scraping](https://www.bfdi.bund.de/)
- [Anthropic Computer Use Policy](https://docs.anthropic.com/en/docs/build-with-claude/computer-use)
- [E2B Docs](https://e2b.dev/docs)
