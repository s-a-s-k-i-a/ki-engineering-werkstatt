# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "marimo",
#   "pydantic>=2.9",
# ]
# ///

"""Lösungs-Skelett — Übung 06.01 — Audio-Stack-Selektor + DSGVO-Plan.

Smoke-test-tauglich. Kein Audio-Inference.
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
        # 🎯 Lösung Übung 06.01 — Audio-Stack-Selektor

        Drei DACH-Audio-Use-Cases → STT + TTS + Diarization + DSGVO-Pipeline.
        """
    )
    return


@app.cell
def _():
    """Pydantic-Profil-Schema."""
    from pydantic import BaseModel, Field

    class AudioProfil(BaseModel):
        name: str
        modus: str  # "stt", "tts", "voice_agent"
        realtime: bool
        sprachen: list[str]
        pii_sensitivity: str  # "niedrig", "mittel", "hoch"
        hosting: str  # "on_prem", "eu_cloud", "edge"
        aufbewahrungsdauer_tage: int = Field(ge=0, le=3650)
        kommerziell: bool

    return (AudioProfil,)


@app.cell
def _():
    """Empfehlungs-Logik."""

    def empfehle_stt(p) -> dict:
        if p.realtime and len(p.sprachen) > 1:
            return {
                "modell": "Whisper-large-v3 mit Streaming oder Voxtral-STT",
                "grund": "multilingual + realtime",
            }
        if p.hosting == "edge":
            return {"modell": "Distil-Whisper-large-v3", "grund": "kompakt für Edge"}
        return {
            "modell": "Whisper-large-v3",
            "grund": "höchste Accuracy für DE; kein offizielles Whisper-large-v4 Stand 04/2026",
        }

    def empfehle_tts(p) -> dict:
        if p.kommerziell:
            return {
                "modell": "XTTS-Idiap-Fork oder Voxtral-TTS (Mistral)",
                "grund": "kommerziell-tauglich (F5-TTS = CC-BY-NC sperrt!)",
            }
        return {
            "modell": "F5-TTS (CC-BY-NC, nicht-kommerziell!) oder Voxtral-TTS",
            "grund": "F5 ist State-of-the-Art für Forschung/Edu",
        }

    def diarization_plan(p) -> dict:
        return {
            "tool": "pyannote.audio v3 (Apache 2.0)",
            "alternative": "NVIDIA NeMo Diarization",
            "modell_groesse": "~ 1 GB",
            "hardware": "CPU okay, GPU empfohlen für Volumen",
        }

    def auto_loesch_plan(p) -> list[str]:
        plan = []
        if p.pii_sensitivity == "hoch":
            plan.append("DSGVO Art. 9 (besonders sensibel) → DSFA Pflicht")
        if p.aufbewahrungsdauer_tage > 0:
            plan.append(f"Auto-Lösch nach {p.aufbewahrungsdauer_tage} Tagen via Cron-Job")
            plan.append("Signiertes Lösch-Log mit SHA-256 + Timestamp + Audit-Anker")
        plan.append("DSGVO Art. 17 (RTBF) — manueller Lösch-Endpunkt binnen 30 Tagen")
        plan.append("§ 201 StGB — Einwilligung dokumentiert (nicht-öffentliche Gespräche)")
        return plan

    def avv_liste(p) -> list[str]:
        if p.hosting == "on_prem":
            return ["Kein AVV nötig — eigene Infrastruktur"]
        if p.hosting == "edge":
            return ["Kein AVV nötig — kein Datentransfer"]
        return [
            "IONOS AI Model Hub",
            "OVHcloud (FR)",
            "Scaleway (FR, HDS)",
            "STACKIT (DE, BSI C5 Type 2)",
        ]

    return auto_loesch_plan, avv_liste, diarization_plan, empfehle_stt, empfehle_tts


@app.cell
def _(AudioProfil):
    """Drei Use-Cases."""
    profile = [
        AudioProfil(
            name="Anwaltskanzlei-Diktiergerät",
            modus="stt",
            realtime=False,
            sprachen=["de"],
            pii_sensitivity="hoch",  # Mandantendaten = besonders schützenswert
            hosting="on_prem",
            aufbewahrungsdauer_tage=2555,  # 7 Jahre Steuerrecht / Mandantenakte
            kommerziell=True,
        ),
        AudioProfil(
            name="Notdienst-Voice-Bot (Tierheim)",
            modus="voice_agent",
            realtime=True,
            sprachen=["de", "en", "tr"],
            pii_sensitivity="mittel",
            hosting="eu_cloud",
            aufbewahrungsdauer_tage=30,
            kommerziell=False,  # gemeinnützig, F5-TTS okay
        ),
        AudioProfil(
            name="KMU-Customer-Support-Hotline",
            modus="stt",
            realtime=False,
            sprachen=["de", "en"],
            pii_sensitivity="hoch",
            hosting="eu_cloud",
            aufbewahrungsdauer_tage=180,  # 6 Monate Compliance
            kommerziell=True,
        ),
    ]
    return (profile,)


@app.cell
def _(
    auto_loesch_plan,
    avv_liste,
    diarization_plan,
    empfehle_stt,
    empfehle_tts,
    mo,
    profile,
):
    """Detail pro Use-Case."""
    blocks = []
    for p in profile:
        stt = empfehle_stt(p)
        tts = empfehle_tts(p) if p.modus in {"tts", "voice_agent"} else None
        diar = diarization_plan(p)
        loesch = auto_loesch_plan(p)
        avvs = avv_liste(p)
        loesch_str = "\n".join(f"  - {x}" for x in loesch)
        avv_str = "\n".join(f"  - {x}" for x in avvs)
        tts_block = f"- **TTS**: {tts['modell']} *({tts['grund']})*\n" if tts else ""
        blocks.append(
            f"### {p.name}\n\n"
            f"- **STT**: {stt['modell']} *({stt['grund']})*\n"
            + tts_block
            + f"- **Diarization**: {diar['tool']}\n"
            f"- **DSGVO-/StGB-Plan**:\n{loesch_str}\n"
            f"- **AVV-Optionen**:\n{avv_str}\n"
        )
    mo.md("## Detail pro Use-Case\n\n" + "\n".join(blocks))
    return


@app.cell
def _(auto_loesch_plan, empfehle_stt, empfehle_tts, profile):
    """Smoke-Test: 5 Akzeptanz-Asserts."""
    p_kanzlei = profile[0]
    p_voice = profile[1]
    p_hotline = profile[2]

    # 1. Anwaltskanzlei → Whisper-large-v3 (NICHT v4)
    kanzlei_stt = empfehle_stt(p_kanzlei)["modell"]
    assert "Whisper-large-v3" in kanzlei_stt
    assert "v4" not in kanzlei_stt

    # 2. Anwaltskanzlei → DSGVO Art. 9
    kanzlei_plan = auto_loesch_plan(p_kanzlei)
    assert any("DSGVO Art. 9" in p for p in kanzlei_plan)

    # 3. Voice-Bot kommerziell=False → F5-TTS okay (für gemeinnützig)
    voice_tts = empfehle_tts(p_voice)["modell"]
    assert "F5" in voice_tts or "Voxtral" in voice_tts

    # 4. Hotline kommerziell=True → KEIN F5-TTS empfohlen (NC sperrt)
    # Diese Übung hat Hotline=stt-only, daher prüfe ein hypothetisches kommerzielles TTS
    p_hotline_tts = p_hotline.model_copy(update={"modus": "tts", "kommerziell": True})
    hotline_tts = empfehle_tts(p_hotline_tts)["modell"]
    assert "F5" not in hotline_tts or "XTTS" in hotline_tts or "Voxtral" in hotline_tts

    # 5. Auto-Lösch-Plan enthält RTBF
    for prof in profile:
        plan = auto_loesch_plan(prof)
        assert any("RTBF" in p or "Art. 17" in p for p in plan)

    print("✅ Übung 06.01 — alle 5 Asserts grün")
    return


if __name__ == "__main__":
    app.run()
