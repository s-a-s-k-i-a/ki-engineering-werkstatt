---
id: 11
phase: 11-llm-engineering
stand: 2026-04-27
anker:
  - avv-pflicht-jeder-cloud-call
  - prompt-injection-owasp
  - audit-logging-art-12
  - drittland-transfer-tia
dsgvo_artikel:
  - art-28
  - art-32
  - art-44
  - art-46
ai_act_artikel:
  - art-12
  - art-13
  - art-15
---

# Compliance-Anker — Phase 11

## AVV-Pflicht bei jedem Cloud-Aufruf (Art. 28 DSGVO)

Jeder Aufruf an OpenAI/Anthropic/Mistral/etc. mit potenziellem Personenbezug: AVV nötig. Standard-Templates:

- **Aleph Alpha**: AVV im Self-Service-Portal
- **Mistral**: DPA online signierbar
- **OpenAI Enterprise/Team**: DPA inkludiert + Zero-Data-Retention
- **Anthropic Enterprise**: DPA + EU-Datazone (Q1/2026)
- **IONOS / StackIT**: AVV im Cloud-Portal

→ Vor jeder Lektion in Phase 11: prüfe, dass dein Account das hat.

## Prompt Injection (OWASP LLM Top 10 #1)

Lektionen 11.03 (Function Calling) und 11.04 (MCP) zeigen Tool-Use. **Sicherheits-Pflicht**:

- Tool-Whitelisting (nur erlaubte Tools im Schema)
- Input-Sanitization (PII-Filter via Presidio o.ä.)
- Output-Validation (Pydantic-Validierung verhindert SQL-Injection-Strings)
- Rate Limiting

## Audit-Logging (AI-Act Art. 12)

Hochrisiko-Systeme müssen Aktivitäten loggen. Mindest-Felder:

- Zeitstempel (ISO 8601 UTC)
- User-ID (pseudonymisiert)
- Modell-Identifier + Version
- Prompt-Hash (SHA-256, nicht Plaintext!)
- Output-Hash
- Tool-Calls (welche, mit welchen Argumenten)
- Latenz, Token-Anzahl, Kosten

Beispiel-Implementation in `phasen/20-recht-und-governance/code/05_audit_logging.py`.

## Drittland-Transfer (Art. 44, 46 DSGVO)

US-LLM mit Personenbezug → DPF (Adequacy Decision EU-US) reicht **allein nicht**. Best Practice:

- DPF + SCCs als Backup
- Aktuelles TIA (Transfer Impact Assessment)
- Bei sensiblen Daten: EU-Region erzwingen oder lokale Modelle nutzen

## Self-Censorship-Audit für asiatische Modelle

Wer DeepSeek/Qwen für Use-Cases mit historisch-/politisch-/geographischem Bezug einsetzt: Audit auf Tiananmen, Taiwan, Xinjiang, Xi Jinping pflicht (siehe Phase 18 Hands-on).

## Quellen

- [OWASP LLM Top 10 (2025)](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)
- [EDPB Opinion 28/2024](https://www.edpb.europa.eu/system/files/2024-12/edpb_opinion_202428_ai-models_en.pdf)
- [DSK Orientierungshilfe KI 06.05.2024](https://www.datenschutzkonferenz-online.de/media/oh/20240506_DSK_Orientierungshilfe_KI_und_Datenschutz.pdf)
