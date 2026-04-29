---
id: 15.01
titel: Autonom vs. Supervisor — wann welches Pattern
phase: 15-autonome-systeme
dauer_minuten: 60
schwierigkeit: fortgeschritten
stand: 2026-04-29
voraussetzungen: [14.07, 14.08]
lernziele:
  - Autonomie-Stufen abgrenzen (HITL → semi-autonom → vollständig autonom)
  - AI-Act Art. 14 — Human Oversight als Pflicht-Pattern
  - DSGVO Art. 22 — automatisierte Entscheidungen
  - Wann **NICHT** autonom (Recht, Medizin, Finanzen)
compliance_anker:
  - autonomie-stufen
  - human-oversight-art-14
ai_act_artikel:
  - art-14
  - art-22
dsgvo_artikel:
  - art-22
---

<!-- colab-badge:begin -->
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/s-a-s-k-i-a/ki-engineering-werkstatt/blob/main/dist-notebooks/phasen/15-autonome-systeme/code/01_autonomie_klassifikator.ipynb)
<!-- colab-badge:end -->

## Worum es geht

> Stop calling everything an "autonomous agent". — die meisten „autonomen Agenten" sind tatsächlich **Supervisor-Worker mit HITL**. Echte Autonomie hat hohe Compliance-Hürden (AI-Act Art. 14, DSGVO Art. 22).

## Voraussetzungen

- Phase 14.07 (Multi-Agent-Patterns)
- Phase 14.08 (Sicherheit + OWASP LLM Top 10)

## Konzept

### Autonomie-Stufen

```mermaid
flowchart LR
    L0[Level 0<br/>Mensch macht alles] --> L1[Level 1<br/>Tools assistieren]
    L1 --> L2[Level 2<br/>Agent schlägt vor<br/>Mensch entscheidet]
    L2 --> L3[Level 3<br/>Agent macht<br/>HITL bei kritisch]
    L3 --> L4[Level 4<br/>Agent vollständig<br/>autonom in Domäne]
    L4 --> L5[Level 5<br/>vollständig autonom<br/>überall]

    classDef hitl fill:#FF6B3D,color:#0E1116
    classDef auto fill:#3D8BFF,color:#FFF
    class L0,L1,L2,L3 hitl
    class L4,L5 auto
```

### Wo „autonome" Systeme 2026 wirklich sind

| Use-Case | Reale Stufe |
|---|---|
| **„autonomer" Email-Assistent** | meist L2 (Vorschläge mit User-Bestätigung) |
| **Customer-Service-Bot** | L2-L3 (HITL bei Eskalation) |
| **Code-Agent** (Cursor, Claude Code) | L3 (Human reviewt Code) |
| **Trading-Bot** | L4 in Domäne, mit Cost-Caps |
| **Selbstfahrende Autos** | L3-L4 (mit Driver-Override) |
| **„AGI"** | nicht existent 2026 |

> **Pattern 2026**: 95 % der „autonomen" Production-Systeme sind tatsächlich L2-L3 mit klarer HITL-Stelle.

### AI-Act Art. 14 — Human Oversight Pflicht

URL: <https://artificialintelligenceact.eu/article/14/>

Hochrisiko-KI-Systeme **müssen** so gestaltet sein, dass:

1. **Mensch kann eingreifen** während Operation
2. **Mensch kann ablehnen / abbrechen** (Stop-Button-Pflicht)
3. **Mensch versteht** was das System macht (Explainability)
4. **Konfidenzwerte sichtbar** (Modell-Unsicherheit kommuniziert)
5. **Kritische Entscheidungen** explizit Mensch-bestätigt

### DSGVO Art. 22 — automatisierte Entscheidungen

> „Die betroffene Person hat das Recht, **nicht** einer ausschließlich auf einer automatisierten Verarbeitung — einschließlich Profiling — beruhenden Entscheidung unterworfen zu werden, die ihr gegenüber rechtliche Wirkung entfaltet oder sie in ähnlicher Weise erheblich beeinträchtigt."

**Praxis-Pattern**: bei Entscheidungen über Personen (Bewerbung, Kredit, Versicherung, Bürger-Service) **Mensch-im-Loop pflicht** — entweder:

- Vorab-Mensch-Review oder
- Nachträgliche Anfechtungs-Möglichkeit

### Wann NICHT autonom

```mermaid
flowchart TB
    Frage[Soll dieser Agent<br/>autonom handeln?] --> Q1{Rechtlich/<br/>medizinisch/<br/>finanziell relevant?}
    Q1 -->|ja| Stop1[STOP — HITL pflicht<br/>Art. 22 DSGVO]
    Q1 -->|nein| Q2{Hochrisiko nach<br/>AI-Act Anhang III?}
    Q2 -->|ja| Stop2[STOP — Art. 14<br/>Human Oversight Pflicht]
    Q2 -->|nein| Q3{Reversible Aktion<br/>oder destruktiv?}
    Q3 -->|destruktiv| HITL[HITL bei kritisch<br/>L3]
    Q3 -->|reversibel| Q4{Cost-Cap<br/>möglich?}
    Q4 -->|ja| OK[OK für L4]
    Q4 -->|nein| Stop3[STOP — Cost-DoS-Risiko]

    classDef stop fill:#A8B0BA,color:#0E1116
    classDef hitl fill:#FF6B3D,color:#0E1116
    classDef ok fill:#3D8BFF,color:#FFF
    class Stop1,Stop2,Stop3 stop
    class HITL hitl
    class OK ok
```

### Selbst-Reflexion + ReAct

URL: <https://arxiv.org/abs/2210.03629>

Zentrales Pattern für autonome Agenten: **ReAct** (Reasoning + Action):

```text
Thought: Was soll ich als Nächstes tun?
Action: Tool-X mit Argument-Y aufrufen
Observation: Tool-Output
Thought: Macht das Sinn? Brauch ich noch was?
Action: ...
```

Plus **Reflexion** (Shinn et al. 2023): Agent kritisiert eigene Outputs:

```python
# Pattern aus Phase 14.07
class AgentLoop:
    def step(self, state):
        thought = await self.reflect(state)
        if thought.confidence < 0.5:
            return await self.escalate_to_human(state, thought)
        action = await self.act(thought)
        observation = await self.execute(action)
        return self.update_state(observation)
```

### Cost-Caps für Autonomie

Pflicht für L4-Autonomie:

| Cap-Typ | Pflicht-Wert (Default) |
|---|---|
| **Tool-Calls pro Run** | max. 20 |
| **Tokens pro Run** | max. 50.000 |
| **Recursion-Limit (LangGraph)** | 25 |
| **Time-Budget** | 5–10 Minuten |
| **Cost-Cap Tokens/User/Tag** | 100k Tokens |
| **HITL-Trigger** | bei Konfidenz < 0,7 oder destruktiver Aktion |

Phase 14.08 hat Detail.

### Memory-Architekturen für Long-Running-Agenten

```mermaid
flowchart LR
    Agent --> WM[Working Memory<br/>aktuelle Konversation]
    Agent --> EM[Episodic Memory<br/>vergangene Sessions]
    Agent --> SM[Semantic Memory<br/>Wissen / Facts]
    Agent --> PM[Procedural Memory<br/>gelernte Patterns]

    WM --> Buffer[(In-Memory<br/>Conv-Buffer)]
    EM --> Vec[(Vector-DB<br/>Qdrant)]
    SM --> Vec
    PM --> Adapter[(LoRA-Adapter<br/>Phase 12)]

    classDef mem fill:#FF6B3D,color:#0E1116
    classDef store fill:#3D8BFF,color:#FFF
    class WM,EM,SM,PM mem
    class Buffer,Vec,Adapter store
```

**LangGraph Postgres-Checkpointer** (Phase 14.05) deckt Working + Episodic Memory ab. Semantic Memory via RAG (Phase 13). Procedural Memory via LoRA-Finetune (Phase 12).

### Wann Long-Running-Agenten?

| Use-Case | Pattern |
|---|---|
| **Customer-Support-Bot** mit Multi-Session | Working + Episodic Memory |
| **Personal-Assistent** | + Semantic Memory (User-Profil) |
| **Lern-Agent** | + Procedural Memory (LoRA-Update) |
| **Autonome Pipeline** | alle 4 Memory-Typen |

> **Realität 2026**: vollständig autonome L4-Agenten sind in Production **selten**. Customer-Support-Bots, Code-Assistants und ähnliche bleiben L2-L3 mit klaren HITL-Stellen.

## Hands-on

1. Klassifiziere 5 deiner Agent-Use-Cases nach Autonomie-Stufe
2. Identifiziere für jeden HITL-Pflicht-Stellen
3. Lies AI-Act Art. 14 + DSGVO Art. 22
4. Bau ein Cost-Cap-Pattern für einen LangGraph-Agent

## Selbstcheck

- [ ] Du nennst die fünf Autonomie-Stufen.
- [ ] Du erkennst, dass 95 % der „autonomen" Systeme tatsächlich L2-L3 sind.
- [ ] Du kennst AI-Act Art. 14 + DSGVO Art. 22 als HITL-Pflicht.
- [ ] Du wählst Use-Cases, wo NICHT autonom (Recht, Medizin, Finanzen).
- [ ] Du planst 4-Schicht-Memory für Long-Running-Agenten.

## Compliance-Anker

- **AI-Act Art. 14**: Human Oversight für Hochrisiko-Systeme
- **DSGVO Art. 22**: Mensch bei automatisierten Entscheidungen
- **Cost-Caps**: Pflicht für L4-Autonomie

## Quellen

- AI-Act Art. 14 — <https://artificialintelligenceact.eu/article/14/>
- DSGVO Art. 22 — <https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:32016R0679>
- ReAct (Yao et al. 2022) — <https://arxiv.org/abs/2210.03629>
- Reflexion (Shinn et al. 2023) — <https://arxiv.org/abs/2303.11366>

## Weiterführend

→ Lektion **15.02** (Long-Running-Agenten in Production)
→ Phase **14.05** (LangGraph + Postgres-Checkpointer)
→ Phase **18.07** (Red-Teaming für Autonomie-Risiken)
