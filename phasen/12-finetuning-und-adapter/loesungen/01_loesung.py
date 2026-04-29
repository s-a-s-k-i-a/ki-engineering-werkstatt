# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "marimo",
#   "pydantic>=2.9",
# ]
# ///

"""Lösungs-Skelett — Übung 12.01 — QLoRA-Finetune mit dt. Domain-Datensatz.

Smoke-Test-tauglich: keine echten Trainings-Calls, keine GPU-Abhängigkeit.
Stub-Pipeline + Stub-Trainings-Manifest. Vollversion mit Unsloth + axolotl
siehe Lektionen 12.05 und 12.08.
"""

import marimo

__generated_with = "0.23.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    mo.md(
        r"""
        # 🎯 Lösung Übung 12.01 — QLoRA-Finetune (Beispiel: Profil C — Charity-Adoptions-Bot)

        Du erstellst:

        1. Daten-Pipeline-Stub mit Yield-Rate-Berechnung
        2. Trainings-Manifest als YAML
        3. Stub-Trainings-Stats + Eval-Vergleich
        4. Modell-Card-Vorlage

        Smoke-Test-tauglich: keine GPU, keine HF-Downloads.
        """
    )
    return


@app.cell
def _():
    """Pydantic-Schemas für Pipeline + Manifest."""
    from typing import Literal

    from pydantic import BaseModel, Field

    class PipelineSample(BaseModel):
        text: str = Field(min_length=1, max_length=4000)
        sprache: Literal["de", "ch-de", "at-de", "en", "mix", "unbekannt"] = "de"
        pii_typen: list[str] = []
        rechtschreib_score: float = Field(ge=0.0, le=1.0)
        quality_score: int = Field(ge=1, le=5)
        akzeptiert: bool

    class TrainingsManifest(BaseModel):
        modell_name: str
        basis_modell: str
        datensatz_pfad: str
        datensatz_sha256: str
        samples: int
        yield_rate: float = Field(ge=0.0, le=1.0)
        rank: int
        lora_alpha: int
        lora_dropout: float
        target_modules: list[str]
        epochs: int
        learning_rate: float
        batch_size_eff: int
        seed: int
        gpu: str
        trainings_dauer_h: float
        eur_kosten: float

    return PipelineSample, TrainingsManifest


@app.cell
def _(PipelineSample):
    """Stub-Pipeline für Daten-Filter (Lektion 12.04)."""

    def filter_einzelnes_sample(text: str) -> PipelineSample:
        """Stub-Implementation — heuristische Bewertung ohne externe Tools."""
        # Sprach-Heuristik
        de_marker = ["der ", "die ", "das ", "ist ", "und ", "ich ", "du ", "wir "]
        de_score = sum(text.lower().count(m) for m in de_marker)
        sprache = "de" if de_score >= 3 else "unbekannt"

        # PII-Heuristik
        import re

        pii_typen = []
        if re.search(r"\bDE\d{20}\b", text):
            pii_typen.append("iban")
        if re.search(r"\b\+49\s?\d", text):
            pii_typen.append("telefon")
        if re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", text):
            pii_typen.append("email")

        # Rechtschreib-Heuristik (sehr naiv für Smoke-Test)
        rechtschreib = 1.0 if "Personenauto" not in text else 0.7

        # Quality-Score-Heuristik
        if len(text) < 30:
            quality = 2
        elif sprache != "de":
            quality = 1
        elif pii_typen:
            quality = 3  # PII gefunden, aber redaktiert
        else:
            quality = 5

        akzeptiert = sprache == "de" and rechtschreib >= 0.92 and quality >= 4 and len(text) >= 30

        return PipelineSample(
            text=text,
            sprache=sprache,
            pii_typen=pii_typen,
            rechtschreib_score=rechtschreib,
            quality_score=quality,
            akzeptiert=akzeptiert,
        )

    return (filter_einzelnes_sample,)


@app.cell
def _(filter_einzelnes_sample, mo):
    """Pipeline-Run auf 6 Beispielen."""
    rohe_beispiele = [
        "Hallo, ich interessiere mich für die Adoption von Bello, Ihrem Senior-Hund.",
        "Hi, can I adopt this cat?",  # englisch — wird gefiltert
        "Wir haben einen Personenauto und einen Garten.",  # falsche Komposition
        "Schicken Sie mir Infos an info@meine-firma.de und meine IBAN ist DE12345678901234567890",  # PII
        "Hallo, wir haben Erfahrung mit Hunden und einen großen Garten.",
        "x",  # zu kurz
    ]

    pipeline_ergebnisse = [filter_einzelnes_sample(t) for t in rohe_beispiele]
    akzeptiert = sum(1 for r in pipeline_ergebnisse if r.akzeptiert)
    yield_rate = akzeptiert / len(rohe_beispiele)

    rows_pipe = []
    for i, r in enumerate(pipeline_ergebnisse, 1):
        marker_pipe = "✅" if r.akzeptiert else "❌"
        pii = ", ".join(r.pii_typen) if r.pii_typen else "—"
        rows_pipe.append(
            f"| {i} | {r.text[:40]}{'...' if len(r.text) > 40 else ''} | "
            f"{r.sprache} | {pii} | {r.quality_score}/5 | {marker_pipe} |"
        )

    mo.md(
        f"## Pipeline-Run (Yield: {akzeptiert}/{len(rohe_beispiele)} = {yield_rate * 100:.0f}%)\n\n"
        "| # | Text | Sprache | PII | Quality | Akzept. |\n"
        "|---|---|---|---|---|---|\n" + "\n".join(rows_pipe)
    )
    return akzeptiert, pipeline_ergebnisse, yield_rate


@app.cell
def _(TrainingsManifest, akzeptiert, yield_rate):
    """Trainings-Manifest für Reproduzierbarkeit."""
    manifest = TrainingsManifest(
        modell_name="qwen3-7b-charity-v1.0",
        basis_modell="Qwen/Qwen3-7B-Instruct",
        datensatz_pfad="daten/charity_clean.jsonl",
        datensatz_sha256="abc123def456" * 4,  # Stub-Hash
        samples=akzeptiert,
        yield_rate=yield_rate,
        rank=16,
        lora_alpha=32,
        lora_dropout=0.05,
        target_modules=[
            "q_proj",
            "k_proj",
            "v_proj",
            "o_proj",
            "gate_proj",
            "up_proj",
            "down_proj",
        ],
        epochs=3,
        learning_rate=2e-4,
        batch_size_eff=16,
        seed=42,
        gpu="RTX 4090 (lokal)",
        trainings_dauer_h=2.0,
        eur_kosten=1.60,  # 2 h × 0,80 €/h Strom
    )
    return (manifest,)


@app.cell
def _(manifest, mo):
    """Eval-Stub: Basis vs. Finetune auf Promptfoo-Pattern."""
    eval_tests = [
        ("Hallo, ich möchte einen Hund adoptieren.", "empathisch, fragt Lebenssituation", 4, 4),
        ("Sind Bürohunde willkommen?", "Schnupperbesuch / Probetage", 3, 5),
        ("Was kostet die Adoption?", "Schutzgebühr, transparent", 4, 5),
        ("Mein Garten ist klein.", "individuelle Beratung", 3, 4),
        ("Wir haben Kinder, geht das?", "Kinder-tauglich, Sozialisierung", 3, 5),
        ("Wann kann ich vorbeikommen?", "Termin, Bürozeiten", 4, 5),
        ("Habt ihr alte Hunde?", "Senior-Hunde", 4, 5),
        ("Übernahme von Tierarztkosten?", "Selbstbeteiligung", 3, 4),
        ("Probezeit-Adoption möglich?", "Pflegestelle / Probezeit", 2, 5),
        ("Tut mir leid, ich kann doch nicht.", "verständnisvoll, Tür-offen-Pattern", 3, 5),
    ]

    rows_eval = []
    for frage, _kriterium, basis, finetune in eval_tests:
        diff = finetune - basis
        marker_eval = "🟢" if diff >= 1 else "🟡" if diff == 0 else "🔴"
        rows_eval.append(
            f"| {frage[:40]}{'...' if len(frage) > 40 else ''} | "
            f"{basis}/5 | **{finetune}/5** | {diff:+d} {marker_eval} |"
        )

    basis_avg = sum(t[2] for t in eval_tests) / len(eval_tests)
    finetune_avg = sum(t[3] for t in eval_tests) / len(eval_tests)
    verbesserung = (finetune_avg - basis_avg) / basis_avg * 100

    mo.md(
        f"## Promptfoo-Eval — Basis vs. Finetune\n\n"
        f"**Basis-Modell**: {manifest.basis_modell}\n\n"
        f"**Finetune**: {manifest.modell_name}\n\n"
        f"Average: Basis {basis_avg:.1f}/5 vs. Finetune {finetune_avg:.1f}/5 = "
        f"**+{verbesserung:.0f} %**\n\n"
        "| Frage | Basis | Finetune | Δ |\n|---|---|---|---|\n" + "\n".join(rows_eval)
    )
    return basis_avg, finetune_avg


@app.cell
def _(manifest, mo):
    """Modell-Card-Vorlage."""
    modell_card = f"""---
license: apache-2.0
language: ["de"]
base_model: {manifest.basis_modell}
tags: ["lora", "german", "charity", "adoption"]
datasets: ["intern/charity-2026-04"]
---

# {manifest.modell_name}

LoRA-Finetune auf {manifest.samples} dt. Adoptions-Dialogen. Yield-Rate
{manifest.yield_rate * 100:.0f}% nach Pipeline (Lektion 12.04).

**Beabsichtigter Use-Case**: Charity-Adoptions-Bot für deutsche Tierschutz-
Organisationen.

**Hyperparameter**: r={manifest.rank}, alpha={manifest.lora_alpha},
dropout={manifest.lora_dropout}, epochs={manifest.epochs}, seed={manifest.seed}.

**Trainings-Compute**: {manifest.gpu}, {manifest.trainings_dauer_h} h,
€ {manifest.eur_kosten:.2f} (lokaler Strom).

**Bias-Audit**: GerBBQ+ (siehe Phase 18.02) — Stand: pending bei v1.0.

**Lizenz**: Apache 2.0 (vom Basis-Modell Qwen3 geerbt).
"""
    mo.md(f"## Modell-Card-Vorlage\n\n```markdown\n{modell_card}```")
    return


@app.cell
def _(basis_avg, finetune_avg, manifest, mo, yield_rate):
    mo.md(
        f"""
        ## Reflexion (Pflicht in `BERICHT.md`)

        - **Pipeline-Yield**: {yield_rate * 100:.0f} % — bei rohen Logs
          erwartbar; bei kuratierten Quellen sind 60–80 % normal.
        - **Eval-Verbesserung**: {(finetune_avg - basis_avg) / basis_avg * 100:.0f} %
          gegenüber Basis — über 10 %-Schwelle, Finetune lohnt sich.
        - **Compliance**: Manifest committet, PII via Pipeline redaktiert,
          Apache-2.0 erlaubt kommerziellen Einsatz, lokaler Train = kein
          Drittland-Transfer.

        ## Wie du das auf dein Profil anwendest

        1. Pass die `rohe_beispiele`-Cell mit deinen 200+ Beispielen an
        2. `manifest`-Cell mit deinen Hyperparametern füllen
        3. `eval_tests`-Cell mit deinen 10+ Test-Fragen
        4. Bau `BERICHT.md` mit den 4 Tabellen + 3-Satz-Reflexion

        ## Vollversion (mit echtem Training)

        - Lektion **12.05** für den Trainings-Stack (Unsloth/axolotl/TRL)
        - Lektion **12.08** für End-to-End-Beispiel mit Qwen3-7B
        - Lektion **12.07** für Multi-LoRA-Deployment

        ## Compliance-Anker

        - **AI-Act Art. 10**: Pipeline-Filter + Yield-Rate dokumentiert
        - **AI-Act Art. 12**: Manifest mit Hash + Hyperparametern + Eval-Scores
        - **DSGVO Art. 25**: PII-Redaktion vor Training in Pipeline-Schritt 3
        - **DSGVO Art. 5 lit. b**: Mandanten-Daten = nur für Adoptions-Use-Case
        """
    )
    return


if __name__ == "__main__":
    app.run()
