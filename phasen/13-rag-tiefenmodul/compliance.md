---
id: 13
phase: 13-rag-tiefenmodul
stand: 2026-04-27
anker:
  - quellen-attribution-art-50
  - wikipedia-cc-by-sa-shareAlike
  - personenbezug-im-vektorstore
  - eu-vektorstore-bevorzugen
dsgvo_artikel:
  - art-5-abs-1-lit-b
  - art-17
  - art-28
ai_act_artikel:
  - art-13
  - art-50-abs-4
---

# Compliance-Anker — Phase 13

## Quellen-Attribution (AI-Act Art. 50)

Wer KI-Outputs an Endnutzer:innen ausgibt, muss bei generierten Inhalten Transparenz herstellen — RAG ist das natürlichste Mittel:

- **Quellen explizit nennen** (Titel, URL, ggf. Seite/Abschnitt)
- **Differenz** zwischen LLM-Wissen und Retrieval-Kontext kenntlich machen
- Bei Quellen mit Lizenz: Lizenz-Hinweis übernehmen

Beispiel-Pattern:

> Antwort: ... [Quelle 1, Wikipedia-DE „Datenschutz", Stand 2026-04-15, CC BY-SA 4.0]

## Wikipedia-Lizenz (CC BY-SA 4.0 / GFDL)

Wer Wikipedia als RAG-Korpus nutzt:

- **Attribution** ist Pflicht (Quellen-URL + Autoren-Verweis ausreichend)
- **ShareAlike**: KI-Outputs, die direkt aus Wikipedia-Inhalten stammen, dürften unter CC BY-SA 4.0 stehen — Rechtslage bei Mensch-Schöpfer-Prinzip nicht final geklärt
- Sicherer Weg: Quellen-Attribution + eigenständige Antwort-Formulierung

## Personenbezug im Vektorstore

Vektoren sind invertierbar (siehe Phase 05). Wenn dein Korpus Namen, E-Mails, Adressen enthält, ist der Vektorstore selbst eine Verarbeitung im Sinne der DSGVO:

- AVV mit Vektorstore-Provider (Qdrant Cloud, Pinecone, Weaviate Cloud)
- Auskunfts-/Löschrechte (Art. 17): wie löscht man einen Embedding-Eintrag?
- Zweckbindung: nur was du dem User auch zeigen darfst

## Vektorstore-Wahl

| Anbieter | Standort | AVV | Empfehlung |
|---|---|---|---|
| **Qdrant Cloud** | EU + US | ✓ | EU-Region wählen |
| **Qdrant self-hosted** | wo du willst | n/a | Default für DACH |
| **pgvector** | wo deine PG liegt | n/a | wenn schon Postgres |
| **Weaviate Cloud** | EU + US | ✓ | EU-Region |
| **Pinecone** | US-zentriert | DPA | nur mit SCC + TIA |
| **LanceDB embedded** | lokal | n/a | für Edge-Cases |

## Right to be Forgotten (Art. 17)

Wer löscht einen Eintrag aus deinem Vektor-Index? Dokumentiere den Workflow:

1. User-Request bei `dsgvo@deine-firma.de`
2. Such im Vektor-Index per Metadaten
3. Lösche Vektoren + zugehöriges Dokument
4. Bestätige Löschung in 30 Tagen

## Quellen

- [AI Act Art. 50](https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:32024R1689)
- [Wikipedia CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/deed.de)
- [Microsoft GraphRAG Paper](https://arxiv.org/abs/2404.16130)
- [Microsoft LazyGraphRAG Blog](https://www.microsoft.com/en-us/research/blog/lazygraphrag-setting-a-new-standard-for-quality-and-cost/)
- [Asai et al. Self-RAG](https://arxiv.org/abs/2310.11511)
