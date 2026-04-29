# Übung 09.01 — Long-Context vs. RAG vs. Mamba für drei DACH-Use-Cases

> Schwierigkeit: mittel · Zeit: 60–90 Min · Voraussetzungen: Lektionen 09.01–09.03

## Ziel

Du baust einen **Architektur-Entscheidungs-Selektor** für drei Long-Context-Use-Cases. Pro Use-Case: Long-Context-Transformer vs. RAG vs. Hybrid (Jamba/Hunyuan-TurboS), Kosten-Schätzung pro Monat, Eval-Pflicht (RULER bei effektiver vs. behaupteter Context-Länge).

## Use-Case

1. **Bundestag-Protokoll-Analyse** (Forschungsinstitut): Single-Shot-Analyse von 500.000-Tokens-Protokollen, einmaliger Job, weniger Kosten- als Genauigkeits-sensitiv
2. **Vertrags-DB-Q&A** (Anwaltskanzlei): 200 Verträge à 60.000 Tokens, häufig abgefragt (50 Queries/Tag), DSGVO-pflicht
3. **Echtzeit-Code-Repo-Assistent** (Software-Team): 3M-Token-Codebasis, jeder Dev macht 30 Queries/Tag, Latenz < 3 sec TTFB

## Aufgabe

1. **Pydantic-Profil-Schema** mit `name`, `tokens_pro_call`, `calls_pro_tag`, `wiederkehrend` (bool), `latenz_budget_ms`, `dsgvo_sensibel`
2. **Architektur-Entscheidungs-Funktion**: < 32k Tokens → Standard-LLM; 32k-200k wiederkehrend → RAG; > 200k einmalig → Long-Context-Modell; sehr lang + häufig → Hybrid (Jamba)
3. **Kosten-Funktion**: pro Monat in EUR — Standard-LLM (~ 1 €/1M), Long-Context-Modell (per Modell-Pricing), RAG (~ 0,05 €/Query nur Top-5-Retrieval)
4. **Eval-Pflicht**: bei `tokens_pro_call > 32_000` → RULER-Eval Pflicht (echte vs. behauptete Context-Länge)
5. **Modell-Empfehlung pro Szenario**: Mistral Large 3, Claude Opus 4.7, Jamba 1.5, Hunyuan-TurboS, DeepSeek-V4 (mit DSGVO-Caveat)
6. **DSGVO-Pflicht-Check**: bei `dsgvo_sensibel=True` und CN-API → SCC + TIA + DPIA, alternative auf Open-Weights-Self-Hosted
7. **Smoke-Test**: 5 Asserts (richtige Architektur pro Szenario, RULER-Pflicht, DSGVO-Markierung)

## Bonus (für Schnelle)

- **Hybrid-Mamba-Tiefe**: bei welchem Token-Volumen lohnt Jamba 1.5 vs. Mistral Large mit RAG?
- **GraphRAG-Light**: für Vertrags-DB — wann lohnt LazyGraphRAG (kostenoptimiert) vs. Standard?
- **KV-Cache-Reduktions-Plan**: bei Mistral Large 3 (GQA, 8 KV-Heads) — wie viel VRAM auf 200k Tokens?
- **Sliding-Window-Attention**: für 3M-Code-Repo — wie StreamingLLM die ersten 4 Tokens (Attention-Sinks) behält

## Abgabe

- Marimo-Notebook in `loesungen/01_loesung.py` (smoke-test-tauglich)
- Kurze `BERICHT.md`: für Vertrags-DB — Hybrid (Jamba) vs. RAG-mit-Pharia? Wieso?

## Wann gilt es als gelöst?

- Bundestag-Analyse → Long-Context-Modell (Opus 4.7 oder Jamba 1.5)
- Vertrags-DB → RAG (50 Queries × 200 Verträge — RAG günstiger)
- Code-Repo → Hybrid oder RAG mit Code-spezifischem Splitting
- Smoke-Test grün

## Wenn du steckenbleibst

- [Mamba Paper (Gu & Dao 2023)](https://arxiv.org/abs/2312.00752)
- [Jamba 1.5 Tech Report (AI21)](https://www.ai21.com/jamba) — 256k Hybrid
- [RULER Long-Context-Benchmark](https://github.com/NVIDIA/RULER)
- [Hunyuan-TurboS (Tencent)](https://github.com/Tencent-Hunyuan)

## Compliance-Check

- [ ] AI-Act Art. 15 — Robustness-Eval bei Long-Context (RULER)
- [ ] DSGVO Art. 44 bei DeepSeek-V4-API (CN) → SCC + TIA + DPIA
- [ ] Selbst-Hosting-Alternative für sensible Daten (Pharia, Mistral Large 3, Jamba 1.5)
- [ ] Kosten-Cap dokumentiert in DSFA (Phase 20.03)
- [ ] AVV mit EU-Cloud-Anbieter (Scaleway, IONOS, OVH, STACKIT)
