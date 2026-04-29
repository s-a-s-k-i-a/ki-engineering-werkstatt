---
id: 18.06
titel: Constitutional AI — Anthropic's Selbstkritik-Pattern
phase: 18-ethik-safety-alignment
dauer_minuten: 60
schwierigkeit: fortgeschritten
stand: 2026-04-29
voraussetzungen: [18.04]
lernziele:
  - Constitutional AI (CAI) konzeptuell verstehen
  - Wie Anthropic es bei Claude einsetzt
  - Vorteile gegenüber klassischem RLHF
  - Eigene Verfassungen für DACH-Use-Cases
compliance_anker:
  - explizite-werte-dokumentation
ai_act_artikel:
  - art-13
  - art-14
---

## Worum es geht

> Stop relying on annotators to encode your values. — Constitutional AI ist Anthropic's Pattern: das Modell **selbst-kritisiert** Outputs gegen explizite Verfassungs-Prinzipien. Skaliert besser als menschliche Annotation und macht Werte explizit.

## Voraussetzungen

- Lektion 18.04 (DPO als Vergleich)

## Konzept

### Das CAI-Prinzip

```mermaid
flowchart TB
    Init[Initial-Modell<br/>SFT-trainiert] --> Gen[Generiere<br/>Antworten]
    Gen --> Verfassung[Verfassungs-<br/>Prinzipien]
    Verfassung --> Krit[Modell kritisiert<br/>eigene Antwort]
    Krit --> Rev[Modell revidiert<br/>Antwort]
    Rev --> Train[Trainings-Pair:<br/>Original (rejected) vs.<br/>Revidiert (chosen)]
    Train --> RLAIF[RLAIF / DPO]
    RLAIF --> Final[Aligned Modell]

    classDef step fill:#FF6B3D,color:#0E1116
    class Init,Gen,Verfassung,Krit,Rev,Train,RLAIF,Final step
```

**Quelle**: Bai et al. 2022, [arxiv.org/abs/2212.08073](https://arxiv.org/abs/2212.08073).

Statt menschlicher Annotation:

1. Initiales SFT-Modell generiert Antwort
2. Modell **kritisiert** eigene Antwort gegen explizite Verfassungs-Prinzipien
3. Modell **revidiert** Antwort
4. (Original, Revidiert) als Trainings-Pair für RLAIF/DPO
5. Resultat: Modell internalisiert Prinzipien

### Anthropic's Verfassungs-Prinzipien

Auszug aus [Anthropic's „Claude's Constitution"](https://www.anthropic.com/news/claudes-constitution):

- "Vermeide Antworten, die toxisch, rassistisch, sexistisch oder anderweitig diskriminierend sind"
- "Bevorzuge Antworten, die hilfreich, harmlos und ehrlich sind"
- "Vermeide übermäßig vorsichtige oder ausweichende Antworten zu Lasten der Nützlichkeit"
- "Berücksichtige verschiedene Perspektiven, ohne unangemessen einseitig zu sein"
- "Erkenne Menschenwürde an und respektiere Autonomie"
- "Konsultiere relevante Quellen für sachliche Genauigkeit"
- (~ 60 Prinzipien insgesamt)

### CAI-Algorithmus im Detail

```python
async def cai_korrigiere(prompt: str, prinzipien: list[str]) -> dict:
    # 1. Initiale Antwort
    initial = await modell.run(prompt)

    # 2. Selbst-Kritik gegen jedes Prinzip
    kritik_prompt = f"""
    Initial-Antwort: {initial.output}

    Verfassungs-Prinzipien:
    {chr(10).join(f'- {p}' for p in prinzipien)}

    Welche Prinzipien werden verletzt? Begründe jedes:
    """
    kritik = await modell.run(kritik_prompt)

    # 3. Revision
    revision_prompt = f"""
    Initial-Antwort: {initial.output}
    Kritik: {kritik.output}

    Schreibe die Antwort neu, sodass sie alle Prinzipien einhält:
    """
    revidiert = await modell.run(revision_prompt)

    return {
        "original_prompt": prompt,
        "rejected": initial.output,
        "chosen": revidiert.output,
        "kritik": kritik.output,
    }
```

Diese Funktion produziert **automatisch** DPO-Pairs.

### Vorteile gegenüber RLHF

| Aspekt | RLHF | CAI |
|---|---|---|
| Skalierung | Annotator-limitiert | unbegrenzt |
| Werte-Konsistenz | Annotator-Streuung | explizit + dokumentiert |
| Reproducibility | unklar | Verfassung ist Text |
| WEIRD-Bias | hoch | von Verfassung abhängig |
| Cost | $$$ Annotator | nur Compute |
| Audit-Trail | Annotator-Pool-Doku | Verfassung im Repo |

### Wann CAI sinnvoll ist

- **Skaliertes Alignment** (> 10k Pairs gewünscht)
- **Explizite Werte-Dokumentation** (AI-Act Art. 13)
- **Compliance-spezifische Use-Cases** (Recht, Ethik)
- **Multi-Sprach-Setups** (Verfassung wird übersetzt)

### DACH-Verfassung — eigenes Beispiel

```yaml
verfassungs_prinzipien:
  - "Verwende konsistent Du oder Sie — niemals Mix in einer Antwort."
  - "Berücksichtige DSGVO-Konformität bei jeder Empfehlung — wenn nicht möglich, das transparent machen."
  - "Vermeide Stereotype zu Bayern, Sachsen, Ost-/Westdeutschland."
  - "Frauen, Männer und non-binäre Personen werden gleich kompetent dargestellt."
  - "Migrationshintergrund ist kein Indikator für Sprachkompetenz oder Bildung."
  - "Bei Rechtsfragen IMMER Disclaimer 'Kein Rechtsrat — bitte Anwalt konsultieren'."
  - "Bei medizinischen Fragen IMMER Disclaimer 'Kein medizinischer Rat — bitte Arzt konsultieren'."
  - "Boomer und Gen-Z werden gleich respektvoll behandelt — keine generationen-spezifischen Klischees."
  - "Religionen werden neutral dargestellt — kein Säkularismus-Bias gegenüber muslimischen / jüdischen Gruppen."
  - "Bei Steuerthemen Stand der Steuergesetzgebung 2026 referenzieren, niemals raten."
```

### CAI-Pipeline für DACH

```python
DACH_VERFASSUNG = [
    "Verwende konsistent Du oder Sie...",
    # ... 10-30 Prinzipien
]

# 1.000 Trainings-Prompts (vielfältig)
prompts = load_prompts("datasets/de-prompts-vielfaeltig.jsonl")

# CAI-Pairs generieren
cai_pairs = []
for p in prompts:
    pair = await cai_korrigiere(p, DACH_VERFASSUNG)
    cai_pairs.append({
        "prompt": p,
        "chosen": pair["chosen"],
        "rejected": pair["rejected"],
    })

# DPO-Training mit diesen Pairs (Lektion 18.04)
trainer = DPOTrainer(
    model="Qwen/Qwen3-7B-Instruct",
    train_dataset=Dataset.from_list(cai_pairs),
    args=DPOConfig(num_train_epochs=1, learning_rate=5e-6, beta=0.1),
)
trainer.train()
```

### CAI-Limitationen

1. **Modell-Bias bleibt**: wenn das Initial-Modell biased ist, wird die Kritik auch biased sein
2. **Verfassungs-Lücken**: was nicht in der Verfassung steht, wird nicht korrigiert
3. **Prinzipien-Konflikte**: „hilfreich" vs. „harmlos" — Modell muss balancieren
4. **Compute-Hunger**: 3× Inferenz pro Trainings-Pair (Init + Kritik + Revision)

### Open-Source-Implementierungen

Stand 04/2026:

- **HF TRL `RLAIFTrainer`** — Stand prüfen
- **`safe-rlhf`** (PKU) — <https://github.com/PKU-Alignment/safe-rlhf>
- **OpenAssistant** — <https://github.com/LAION-AI/Open-Assistant> (Reste, weniger aktiv)
- **`Anthropic-evals`** — <https://github.com/anthropics/evals>

> Hinweis: 04/2026 ist die produktive CAI-Tooling-Landschaft **dünner** als bei DPO/GRPO. Anthropic nutzt es intern, aber Open-Source-Implementierungen sind weniger ausgereift.

### Compliance-Wert

CAI hat einen **starken Audit-Vorteil**: die Verfassung ist explizit im Repo. AI-Act Art. 13 (Transparency) wird besser erfüllt als bei „intransparent annotated":

- Verfassungs-Datei `verfassung-v1.0.yaml` committed
- Pre/Post-Audit dokumentiert
- Reproducibility: jeder kann mit gleicher Verfassung + gleichem Modell die Pipeline nachbauen

## Hands-on

1. Schreib eine 10-Prinzipien-Verfassung für deinen DACH-Use-Case
2. Implementiere `cai_korrigiere` mit Pydantic AI
3. Generiere 100 CAI-Pairs aus 100 Prompts
4. DPO-Run mit diesen Pairs
5. Eval: ist Modell näher an deinen Werten?

## Selbstcheck

- [ ] Du erklärst CAI als Selbstkritik-Pattern.
- [ ] Du nennst Vorteile gegenüber RLHF (Skalierung, Reproducibility).
- [ ] Du schreibst DACH-spezifische Verfassungs-Prinzipien.
- [ ] Du implementierst CAI-Pipeline + DPO.
- [ ] Du dokumentierst Verfassung im Repo (AI-Act Art. 13).

## Compliance-Anker

- **AI-Act Art. 13 (Transparency)**: Verfassung als explizite Werte-Dokumentation
- **AI-Act Art. 14 (Human Oversight)**: Verfassung wird **menschlich** geschrieben — Mensch im Loop bei Werte-Definition
- **DSGVO**: Verfassung kann DSGVO-Disclaimer-Pflichten kodifizieren

## Quellen

- Constitutional AI Paper (Bai et al. 2022) — <https://arxiv.org/abs/2212.08073>
- Anthropic's Claude Constitution — <https://www.anthropic.com/news/claudes-constitution>
- safe-rlhf (PKU) — <https://github.com/PKU-Alignment/safe-rlhf>
- Anthropic-evals — <https://github.com/anthropics/evals>

## Weiterführend

→ Lektion **18.07** (Red-Teaming gegen die trainierten Werte)
→ Lektion **18.09** (Llama Guard 4 als zusätzlicher Output-Filter)
→ Phase **20.01** (AI-Act-Risiko-Klassifizierung)
