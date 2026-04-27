---
id: 14
phase: 14-agenten-und-mcp
stand: 2026-04-27
anker:
  - human-oversight-art-14
  - tool-authorization
  - daten-minimierung-im-system-prompt
  - audit-tool-calls
dsgvo_artikel:
  - art-22
  - art-25
  - art-32
ai_act_artikel:
  - art-14
---

# Compliance-Anker — Phase 14

## Human Oversight (AI-Act Art. 14)

Hochrisiko-Agenten brauchen menschliche Aufsicht. Pattern:

- **Confidence-Threshold** für autonome Aktionen (z.B. Termin buchen nur bei >0.95)
- **Human-in-the-Loop**-Tool für Grenzfälle (LangGraph `interrupt_before`)
- **Approval-Queue** für Aktionen mit Außenwirkung (E-Mail, Zahlung)

## Tool-Whitelisting

Niemals dem Agent „alle Tools" geben — explizite Whitelist im Code. Audit jeden Tool-Call.

## Datenminimierung im System-Prompt (Art. 25)

System-Prompts werden oft an US-Cloud-LLM geschickt. Niemals echte Mandanten-/Patienten-/Kundendaten dort einbetten — pseudonymisierte Tokens nutzen, Auflösung lokal.

## Audit-Logging der Tool-Calls

Jeder Tool-Call: User-ID + Tool-Name + Argumente + Ergebnis + Zeitstempel — strukturiert, abrufbar bei Behörden-Anfrage. Beispiel in `phasen/20-recht-und-governance/code/05_audit_logging.py`.

## DSGVO Art. 22 — automatisierte Entscheidungen

Wenn Agent ohne Mensch zu rechtlich/wirtschaftlich relevanten Entscheidungen kommt: Betroffenen-Information, menschlicher Eingriffspfad, Anfechtung. Tierheim-Adoption ist Grenzfall — der finale Match wird vom Mitarbeiter freigegeben (Pattern!).

## Quellen

- [MCP Spezifikation](https://modelcontextprotocol.io)
- [Pydantic AI Docs](https://ai.pydantic.dev)
- [Anthropic Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)
