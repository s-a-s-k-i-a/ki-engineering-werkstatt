---
id: 18
phase: 18-ethik-safety-alignment
stand: 2026-04-27
anker:
  - agg-diskriminierungsverbot
  - bias-test-anhang-iv
  - red-teaming-pflicht-gpai
  - self-censorship-eval
dsgvo_artikel:
  - art-22
  - art-25
ai_act_artikel:
  - art-10
  - art-15
  - art-55
---

# Compliance-Anker — Phase 18

## AGG (Allgemeines Gleichbehandlungsgesetz) DE

KI-Systeme in HR (Personalauswahl, Performance-Review) sind Hochrisiko (AI-Act Anhang III Nr. 4) **und** AGG-relevant. Diskriminierungsverbot nach AGG umfasst Geschlecht, Alter, Religion, Behinderung, ethnische Herkunft, sexuelle Identität.

→ Bias-Test-Pipeline ist nicht optional.

## Konformitätsbewertung Anhang IV (Art. 43)

Hochrisiko-Systeme: vor Inverkehrbringen Konformitätsbewertung. Anhang IV verlangt:

- Risikomanagement-Bericht
- Datensatz-Beschreibung mit Bias-Analyse
- Trainingsmethoden-Doku
- Validierungs- und Testberichte
- Cybersecurity-Maßnahmen

## Red-Teaming-Pflicht für GPAI mit systemischem Risiko (Art. 55)

Modelle ≥10²⁵ FLOPs Trainings-Compute brauchen:

- Adversarial Testing
- State-of-the-Art-Eval auf Sicherheitsrisiken
- Schwerwiegende Vorfälle ans AI-Office melden

## Self-Censorship-Audit

> Pflicht-Eval für asiatische Modelle vor produktivem Einsatz. Kategorien:
>
> 1. Geopolitik (Tiananmen, Taiwan, Xinjiang)
> 2. Personen (Xi Jinping, Mao)
> 3. Geschichte (Hongkong-Proteste, Tibet)
> 4. Religion (Falun Gong, Uyguren-Islam)
> 5. Wirtschaft (CCP-kritische Aussagen)

Ergebnis dokumentieren — gehört zur Modell-Karte.

## Quellen

- [AGG Bundesgesetz](https://www.gesetze-im-internet.de/agg/)
- [Bai et al. Constitutional AI](https://arxiv.org/abs/2212.08073)
- [Rafailov et al. DPO](https://arxiv.org/abs/2305.18290)
- [Enkrypt AI Bias Studie zu DeepSeek](https://www.enkryptai.com/blog/deepseek-r1-redteaming)
