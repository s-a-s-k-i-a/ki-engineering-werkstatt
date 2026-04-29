# Übung 15.01 — Autonomie-Klassifikation + 4-Schicht-Memory-Plan für drei DACH-Use-Cases

> Schwierigkeit: fortgeschritten · Zeit: 75–105 Min · Voraussetzungen: Lektionen 15.01–15.03

## Ziel

Du klassifizierst drei DACH-Use-Cases nach **Autonomie-Stufen L0-L5 / STOP** und entwirfst pro Case einen **4-Schicht-Memory-Plan** (Working / Episodic / Semantic / Procedural) mit DSGVO-Right-to-be-Forgotten-Endpoint und HITL-Eskalations-Pfaden. Schwerpunkt: **Architektur-Entscheidungen vor dem ersten Production-Deploy**.

## Use-Case

1. **Persönlicher Voice-Assistent** (Hannover-Solo-Founder, 6+-Wochen-Sessions): plant Termine, recherchiert, schreibt Drafts. Nutzer:in ist fortgeschritten, will hohe Autonomie. Cost-Cap-möglich, reversible Aktionen, hohe Konfidenz im LLM.
2. **Bürger-Service-Agent** (Stadt Hannover, gleiche Use-Case wie Phase 14.01): nimmt Bürger-Anfragen entgegen, entscheidet Routing zu Wissens-/Termin-/Formular-Sub-Agent. Behörden-Pflicht: Audit-Trail, HITL bei Entscheidungs-Vorgang.
3. **Bewerber-Vorauswahl-Bot** (HR-Abteilung, ~ 200 Bewerbungen/Woche): liest Lebensläufe, scored Kandidat:innen. **Stop-Signal**: AI-Act Anhang III Nr. 1a + DSGVO Art. 22 (automatisierte Entscheidung).

## Aufgabe

1. **Pydantic-Profil-Schema** mit `name`, `aktion_typ` (`info_only` / `reversibel` / `destruktiv` / `entscheidung`), `rechtsrelevant` (bool), `betroffene` (`person` / `behoerde` / `kommerziell`), `cost_cap_moeglich`, `konfidenz_hoch`
2. **Autonomie-Klassifikator-Funktion** `klassifiziere(profil) -> dict[stufe: L0|L1|L2|L3|L4|L5|STOP, begruendung, kontrollen]`
3. **Memory-Plan-Funktion**: pro Use-Case definiere die 4 Schichten — was wird in Working/Episodic/Semantic/Procedural gespeichert?
4. **RTBF-Endpoint-Plan**: `DELETE /api/user/{id}` muss alle 4 Memory-Schichten löschen — wie strukturierst du das?
5. **HITL-Eskalations-Pfade**: bei welchen Aktionen pflichtmäßig Mensch-im-Loop?
6. **Konfidenz-Threshold**: bei `< 0.85` Konfidenz → eskaliere; bei rechtlich-relevant immer Mensch
7. **AI-Act-Anhang-III-Check** + DSGVO Art. 22-Markierung
8. **Smoke-Test**: 5 Asserts (richtige Stufe pro Use-Case, Bewerber-Bot = STOP, RTBF in allen)

## Bonus (für Schnelle)

- **LangGraph-Postgres-Checkpointer**-Skizze für Voice-Assistent: Schema, `thread_id` als User-ID
- **Auto-Pruning-Strategie**: Episodic-Memory > 90 Tage → Auto-Lösch (DSGVO Art. 5)
- **Konfidenz-Eskalations-Demo**: bei < 0.7 → STOP, 0.7-0.85 → HITL, > 0.85 → autonom
- **Policy-Brake**: Rechts-/Steuer-/Med.-Themen erkennen + zwingend in HITL routen

## Abgabe

- Marimo-Notebook in `loesungen/01_loesung.py` (smoke-test-tauglich)
- Kurze `BERICHT.md`: warum HR-Bot **STOP** und nicht L1 mit allen Kontrollen?

## Wann gilt es als gelöst?

- Voice-Assistent → L3-L4 (reversibel + Cost-Cap)
- Bürger-Service → L2-L3 (Recht oft tangiert, HITL bei Entscheidung)
- Bewerber-Bot → STOP (DSGVO Art. 22 + AI-Act Anhang III Nr. 1a)
- Smoke-Test grün

## Wenn du steckenbleibst

- [LangGraph Postgres-Checkpointer](https://langchain-ai.github.io/langgraph/reference/checkpoints/#postgressaver)
- [DSGVO Art. 22 — Automatisierte Entscheidungen](https://eur-lex.europa.eu/eli/reg/2016/679/oj#d1e2746-1-1)
- [AI Act Anhang III](https://eur-lex.europa.eu/eli/reg/2024/1689/oj) — Hochrisiko-Use-Cases
- [Anthropic „Building Effective Agents"](https://www.anthropic.com/research/building-effective-agents)

## Compliance-Check

- [ ] AI-Act Art. 14 — HITL-Pflicht für Hochrisiko-Systeme
- [ ] DSGVO Art. 22 bei automatisierten Entscheidungen → Mensch + Anfechtung + Logik-Erklärung
- [ ] DSGVO Art. 17 (RTBF) — Lösch-Endpoint binnen 30 Tagen
- [ ] DSGVO Art. 5 (Datenminimierung) — Auto-Pruning
- [ ] DSGVO Art. 25 (Privacy by Design) — Memory-Pseudonymisierung
- [ ] AGG bei HR-Bewerber-Use-Cases — verboten ohne Mensch
- [ ] Audit-Trail für Sub-Agent-Calls (Phase 17.06)
