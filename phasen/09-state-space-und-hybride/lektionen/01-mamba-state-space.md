---
id: 09.01
titel: State-Space-Modelle — Mamba, Mamba-2 als Transformer-Alternative
phase: 09-state-space-und-hybride
dauer_minuten: 60
schwierigkeit: fortgeschritten
stand: 2026-04-29
voraussetzungen: [11.05]
lernziele:
  - SSM-Mechanik (Selective State-Space) verstehen
  - Mamba + Mamba-2 als linear-time-Alternativen zu Transformers
  - Wann Mamba statt Transformer
compliance_anker:
  - lizenz-disziplin-ssm
ai_act_artikel:
  - art-15
---

<!-- colab-badge:begin -->
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/s-a-s-k-i-a/ki-engineering-werkstatt/blob/main/dist-notebooks/phasen/09-state-space-und-hybride/code/01_long_context_kalkulator.ipynb)
<!-- colab-badge:end -->

## Worum es geht

> Stop assuming Transformers are the only game in town. — State-Space-Modelle (SSMs) sind 2026 die Linear-Time-Alternative für **Long-Context** (1M+ Tokens) bei **konstantem Memory**. Mamba (Gu & Dao 2023) + Mamba-2 (2024) waren die Wegbereiter. 2026 dominieren **Hybride** (siehe Lektion 09.02).

## Voraussetzungen

- Phase 11.05 (Anbieter-Vergleich)

## Konzept

### Warum überhaupt SSMs?

Transformers haben **quadratische** Komplexität in der Sequenz-Länge: O(N²) für N Tokens. Bei 1M Tokens: extrem teuer.

State-Space-Modelle (SSMs) sind **linear** in N: O(N). Bei 1M Tokens: massiv günstiger.

### Selective State-Space (Mamba)

URL: <https://arxiv.org/abs/2312.00752> (Gu & Dao, Dez 2023)

```text
h_t = A_t × h_{t-1} + B_t × x_t       # State-Update
y_t = C_t × h_t + D × x_t              # Output
```

Wo:

- `h_t` ∈ ℝ^N — versteckter Zustand (Memory)
- `A_t, B_t, C_t` werden **selektiv** für jeden Schritt berechnet (das ist der Mamba-Trick)
- `D` — Skip-Connection

**Warum das Magic ist**: durch selective parameters kann das Modell entscheiden, was es behält und was es vergisst — ähnlich wie LSTM, aber mit Hardware-Friendly-Implementation.

### Mamba-2 (Tri Dao et al., 05.2024)

URL: <https://arxiv.org/abs/2405.21060>

- **Structured State Space Duality (SSD)** — Verbindung zu Multi-Head-Attention
- 2–8× schneller als Mamba-1
- Skaliert bis ~ 7B Params produktiv

### Mamba vs. Transformer — wann was?

| Faktor | Transformer | Mamba (SSM) |
|---|---|---|
| Komplexität | O(N²) | **O(N) linear** |
| Memory bei N=1M | extrem hoch (quadratisch) | **konstant** |
| Recall genaue Tokens | sehr gut | mittel — kann „vergessen" |
| Expressivity | sehr hoch | gut, aber begrenzt |
| Training-Stabilität | bewährt | wird besser, aber weniger ausgereift |
| In-Context-Learning | sehr gut | mittel |
| Inference-Speed | schneller bei kurzen Seqs | schneller bei langen Seqs (> 8k) |

> **Faustregel 2026**: pure SSM nur bei **Long-Context-Tasks** (> 100k Tokens). Bei normalen LLM-Tasks: Transformer oder Hybride (siehe 09.02) sind besser.

### Pure-Mamba-Modelle (selten)

Stand 04/2026: pure-Mamba-Modelle sind **nicht** produktiver Standard. Die meisten Anwendungen nutzen **Hybride**:

- **Falcon Mamba 7B** (TII, Falcon-Familie, 08.2024) — pure-Mamba, gute aber nicht spitzige Performance
- Forschungs-Demos mit Mamba-Layern

Pure SSMs werden **selten** in Production deployed. Hybride dominieren (Phase 09.02).

### Implementations-Stand

URL: <https://github.com/state-spaces/mamba>

```python
from mamba_ssm import Mamba

# Mamba-Layer als drop-in-replacement für Attention
modell = Mamba(
    d_model=4096,
    d_state=16,
    d_conv=4,
    expand=2,
)

# Inference linear in N
output = modell(input_tokens)
```

Stand 04/2026: `mamba-ssm` Library aktiv, aber noch wenig in Mainstream-Frameworks (Transformers, vLLM) integriert.

### Wann SSM vs. Hybrid

| Use-Case | Empfehlung |
|---|---|
| Standard-LLM-Chat | Transformer (Phase 11) |
| Long-Context-Reasoning > 100k Tokens | Hybrid (Phase 09.02) — Jamba 1.5 |
| Audio (sehr lange Sequenzen) | Mamba-basiert |
| **Production-LLM 2026** | **Hybrid** schlägt pure SSM bei fast allen Tasks |
| Forschung | Mamba-2 für SSM-Verständnis |

### Compute-Effizienz

Bei 1M Tokens auf 1× H100:

| Modell-Typ | Memory | Inference-Zeit |
|---|---|---|
| Transformer 7B | OOM (typisch nur < 200k) | — |
| **Mamba 7B** | ~ 14 GB konstant | ~ 30 s |
| Hybrid Jamba 1.5 (Lektion 09.02) | ~ 24 GB | ~ 20 s |

> Pure-SSM-Stärke: konstantes Memory bei beliebiger Länge. Aber: Recall + In-Context-Learning hinken Transformern hinterher.

## Hands-on

1. Lies das Mamba-Paper-Abstract (Gu & Dao 2023)
2. `pip install mamba-ssm` + Mini-Mamba-7B-Demo
3. Vergleich: 100k-Token-Inferenz Mamba vs. Transformer (falls Hardware reicht)
4. Lese das Jamba-Paper (Lektion 09.02) als Bridge zu Hybriden

## Selbstcheck

- [ ] Du erklärst SSM-Mechanik (h_t = A_t h_{t-1} + B_t x_t).
- [ ] Du verstehst die O(N²) → O(N) Reduktion.
- [ ] Du wählst SSM nur bei Long-Context-Tasks > 100k.
- [ ] Du nutzt Hybride (Phase 09.02) für Production statt pure SSM.

## Compliance-Anker

- **AI-Act Art. 15**: SSMs haben weniger Eval-Reife als Transformer — Robustness-Tests pflicht
- **Lizenz**: Mamba-ssm-Library Apache 2.0; Falcon Mamba 7B siehe TII-Lizenz

## Quellen

- Mamba-Paper (Gu & Dao 2023) — <https://arxiv.org/abs/2312.00752>
- Mamba-2 / SSD (Dao et al. 2024) — <https://arxiv.org/abs/2405.21060>
- Mamba-ssm GitHub — <https://github.com/state-spaces/mamba>
- Falcon Mamba 7B — <https://huggingface.co/tiiuae/falcon-mamba-7b>

## Weiterführend

→ Lektion **09.02** (Hybrid-Modelle: Jamba 1.5, Hunyuan-TurboS)
→ Lektion **09.03** (Long-Context-Eval)
→ Phase **16** (Reasoning + Long-Context)
