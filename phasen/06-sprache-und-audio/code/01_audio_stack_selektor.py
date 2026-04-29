# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "marimo",
#   "pydantic>=2.9",
# ]
# ///

"""Audio-Stack-Selektor — wählt ASR + TTS basierend auf Use-Case + Compliance.

Smoke-Test-tauglich: keine externen Calls. Modell-Daten Stand 29.04.2026.
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
        # 🎙️ Audio-Stack-Selektor · Phase 06

        Wählt ASR + TTS basierend auf:

        - Use-Case (Realtime / Batch / Voice-Cloning)
        - Compliance (DSGVO-strict / Standard)
        - Lizenz-Anforderung (kommerziell ok / Forschung ok)

        Stand: 29.04.2026.
        """
    )
    return


@app.cell
def _():
    """Pydantic-Schemas."""
    from typing import Literal

    from pydantic import BaseModel

    class AudioModell(BaseModel):
        name: str
        typ: Literal["asr", "tts"]
        lizenz: Literal["apache-2.0", "mit", "cc-by-nc", "proprietaer", "cc-by-sa"]
        deutsch: Literal["sehr-gut", "gut", "mittel", "fehlt"]
        latenz_ms: int | None = None
        wann: str

    class AudioStack(BaseModel):
        asr: str
        tts: str
        gesamt_dsgvo_konform: bool
        gesamt_kommerziell_frei: bool
        latenz_p50_ms: int

    return AudioModell, AudioStack


@app.cell
def _(AudioModell):
    """Audio-Modell-Katalog Stand 29.04.2026."""
    katalog = [
        # ASR
        AudioModell(
            name="Faster-Whisper-large-v3",
            typ="asr",
            lizenz="mit",
            deutsch="sehr-gut",
            latenz_ms=200,
            wann="DACH-Default für ASR — RTF 0,1 auf RTX 4090",
        ),
        AudioModell(
            name="Faster-Whisper-Turbo",
            typ="asr",
            lizenz="mit",
            deutsch="sehr-gut",
            latenz_ms=100,
            wann="schneller, minimal schlechtere Qualität",
        ),
        AudioModell(
            name="Voxtral-STT 3B",
            typ="asr",
            lizenz="apache-2.0",
            deutsch="sehr-gut",
            latenz_ms=400,
            wann="Q&A direkt aus Audio (1 Modell statt ASR + LLM)",
        ),
        AudioModell(
            name="Deepgram Nova-3",
            typ="asr",
            lizenz="proprietaer",
            deutsch="gut",
            latenz_ms=150,
            wann="Realtime-Code-Switching, kommerziell",
        ),
        AudioModell(
            name="OpenAI Whisper API",
            typ="asr",
            lizenz="proprietaer",
            deutsch="sehr-gut",
            latenz_ms=300,
            wann="Drittland — nur mit AVV + SCC",
        ),
        # TTS
        AudioModell(
            name="Voxtral-TTS 4B",
            typ="tts",
            lizenz="apache-2.0",
            deutsch="sehr-gut",
            latenz_ms=90,
            wann="DACH-Default für kommerziell + Open-Weights",
        ),
        AudioModell(
            name="XTTS-v2 Idiap-Fork",
            typ="tts",
            lizenz="apache-2.0",
            deutsch="gut",
            latenz_ms=300,
            wann="Self-Hosted mit Voice-Cloning",
        ),
        AudioModell(
            name="F5-TTS-DE",
            typ="tts",
            lizenz="cc-by-nc",
            deutsch="sehr-gut",
            latenz_ms=200,
            wann="NUR Forschung — CC-BY-NC blockt kommerziell!",
        ),
        AudioModell(
            name="Cartesia Sonic 2",
            typ="tts",
            lizenz="proprietaer",
            deutsch="gut",
            latenz_ms=40,
            wann="Latenz-kritisch Realtime, proprietär",
        ),
        AudioModell(
            name="Sesame CSM-1B",
            typ="tts",
            lizenz="apache-2.0",
            deutsch="fehlt",
            latenz_ms=1200,
            wann="EN-only Stand 04/2026",
        ),
    ]
    return (katalog,)


@app.cell
def _(katalog):
    """Stack-Empfehlungs-Logik."""

    def empfehle_stack(profil: dict) -> dict:
        # Filter ASR
        asr_kandidaten = [m for m in katalog if m.typ == "asr"]
        if profil["compliance"] == "dsgvo-strict":
            asr_kandidaten = [
                m
                for m in asr_kandidaten
                if m.lizenz in ("apache-2.0", "mit") and "Drittland" not in m.wann
            ]
        if profil["deutsch_pflicht"]:
            asr_kandidaten = [m for m in asr_kandidaten if m.deutsch in ("sehr-gut", "gut")]
        if profil["realtime"]:
            asr_kandidaten = [m for m in asr_kandidaten if m.latenz_ms and m.latenz_ms <= 300]

        # Filter TTS
        tts_kandidaten = [m for m in katalog if m.typ == "tts"]
        if profil["kommerziell"]:
            tts_kandidaten = [m for m in tts_kandidaten if m.lizenz != "cc-by-nc"]
        if profil["compliance"] == "dsgvo-strict":
            tts_kandidaten = [
                m
                for m in tts_kandidaten
                if m.lizenz in ("apache-2.0", "mit") and "proprietaer" not in m.lizenz
            ]
        if profil["deutsch_pflicht"]:
            tts_kandidaten = [m for m in tts_kandidaten if m.deutsch in ("sehr-gut", "gut")]
        if profil["realtime"]:
            tts_kandidaten = [m for m in tts_kandidaten if m.latenz_ms and m.latenz_ms <= 200]

        # Sortiere nach Latenz
        asr_kandidaten.sort(key=lambda m: m.latenz_ms or 99999)
        tts_kandidaten.sort(key=lambda m: m.latenz_ms or 99999)

        if not asr_kandidaten or not tts_kandidaten:
            return {"asr": "—", "tts": "—", "warnung": "Keine passende Kombi."}

        return {
            "asr": asr_kandidaten[0].name,
            "tts": tts_kandidaten[0].name,
            "asr_latenz": asr_kandidaten[0].latenz_ms,
            "tts_latenz": tts_kandidaten[0].latenz_ms,
            "total_latenz_p50_ms": (
                (asr_kandidaten[0].latenz_ms or 0)
                + 800  # LLM
                + (tts_kandidaten[0].latenz_ms or 0)
            ),
        }

    return (empfehle_stack,)


@app.cell
def _(empfehle_stack, mo):
    """Test-Profile."""
    profile = [
        {
            "name": "DACH-Mittelstand-Voice-Agent",
            "compliance": "dsgvo-strict",
            "deutsch_pflicht": True,
            "kommerziell": True,
            "realtime": True,
        },
        {
            "name": "Forschungs-Demo (CC-BY-NC ok)",
            "compliance": "standard",
            "deutsch_pflicht": True,
            "kommerziell": False,
            "realtime": True,
        },
        {
            "name": "Batch-Transkriptions-Service",
            "compliance": "dsgvo-strict",
            "deutsch_pflicht": True,
            "kommerziell": True,
            "realtime": False,
        },
        {
            "name": "Englisch-Voice-Conversation",
            "compliance": "standard",
            "deutsch_pflicht": False,
            "kommerziell": True,
            "realtime": True,
        },
    ]

    rows_profile = []
    for p in profile:
        e = empfehle_stack(p)
        latenz = e.get("total_latenz_p50_ms", "—")
        rows_profile.append(
            f"| {p['name']} | {e.get('asr', '—')} | {e.get('tts', '—')} | {latenz} ms |"
        )

    mo.md(
        "## Stack-Empfehlungen\n\n"
        "| Profil | ASR | TTS | Total p50 |\n|---|---|---|---|\n" + "\n".join(rows_profile)
    )
    return


@app.cell
def _(katalog, mo):
    """Modell-Katalog."""
    asr = [m for m in katalog if m.typ == "asr"]
    tts = [m for m in katalog if m.typ == "tts"]

    rows_asr = []
    for m in asr:
        rows_asr.append(
            f"| **{m.name}** | {m.lizenz} | {m.deutsch} | {m.latenz_ms} ms | {m.wann} |"
        )

    rows_tts = []
    for m in tts:
        rows_tts.append(
            f"| **{m.name}** | {m.lizenz} | {m.deutsch} | {m.latenz_ms} ms | {m.wann} |"
        )

    mo.md(
        "## ASR-Katalog\n\n"
        "| Modell | Lizenz | DE | Latenz | Wann |\n|---|---|---|---|---|\n"
        + "\n".join(rows_asr)
        + "\n\n## TTS-Katalog\n\n"
        "| Modell | Lizenz | DE | Latenz | Wann |\n|---|---|---|---|---|\n" + "\n".join(rows_tts)
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Wichtige Hinweise

        - **Whisper-v4 existiert nicht** Stand 04/2026 — nur large-v3 + large-v3-Turbo
        - **F5-TTS = CC-BY-NC** — blockiert kommerziellen Einsatz
        - **Sesame ≠ Anthropic** — eigene Firma
        - **Voice = biometrisch** (DSGVO Art. 9) — explizite Einwilligung pflicht
        - **AI-Act Art. 50.2 ab 02.08.2026**: KI-Audio-Watermark pflicht

        ## Quellen

        - Whisper-large-v3 — <https://huggingface.co/openai/whisper-large-v3>
        - Voxtral-TTS — <https://mistral.ai/news/voxtral-tts>
        - F5-TTS — <https://github.com/SWivid/F5-TTS>
        - XTTS Idiap-Fork — <https://github.com/idiap/coqui-ai-TTS>
        - LiveKit Agents — <https://github.com/livekit/agents>
        - AI-Act Art. 50 — <https://artificialintelligenceact.eu/article/50/>
        """
    )
    return


if __name__ == "__main__":
    app.run()
