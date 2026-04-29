# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "marimo",
#   "pydantic>=2.9",
# ]
# ///

"""Mehrsprachiger Voice-Agent Stub — Capstone 19.E.

Smoke-Test-tauglich: keine echten ASR/TTS/DeepL-Calls. Stub-Pipeline zeigt
DE↔EN↔TR-Übersetzungs-Architektur. Vollversion siehe README.md.
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
        # 🌍 Mehrsprachiger Voice-Agent · Capstone 19.E

        Stub-Pipeline für DE↔EN↔TR Live-Übersetzung mit Kontext-Memory:

        - **Whisper-large-v3** für ASR + Sprach-Detektion
        - **DeepL / Mistral** als Übersetzungs-Layer
        - **LangGraph** mit Postgres-Memory
        - **F5-TTS / Sesame** für TTS

        Smoke-Test-tauglich (keine externen Calls). Vollversion siehe README.md.
        """
    )
    return


@app.cell
def _():
    """Pydantic-Schemas."""
    from typing import Literal

    from pydantic import BaseModel, Field

    class Transkript(BaseModel):
        text: str = Field(min_length=1, max_length=2000)
        sprache: Literal["de", "en", "tr"]
        konfidenz: float = Field(ge=0.0, le=1.0)
        pii_redacted: list[str] = []

    class Uebersetzung(BaseModel):
        original_text: str
        original_sprache: Literal["de", "en", "tr"]
        ziel_sprache: Literal["de", "en", "tr"]
        uebersetzt: str

    class VoiceTurn(BaseModel):
        turn_nr: int
        user_pseudonym: str
        transkript: Transkript
        antwort_text: str
        antwort_sprache: Literal["de", "en", "tr"]
        uebersetzungen_im_loop: int  # für Multi-Sprach-Konversation

    return Transkript, Uebersetzung, VoiceTurn


@app.cell
def _(Transkript, Uebersetzung, VoiceTurn):
    """Stub-Pipeline."""

    def stub_asr(audio_id: str, hint_sprache: str | None = None) -> Transkript:
        """Stub: simuliert Whisper-ASR mit Sprach-Detektion."""
        # Naive Mapping audio_id → Transkript
        beispiele = {
            "audio-de-001": ("Guten Tag, ich brauche Hilfe bei der Wohnsitz-Anmeldung.", "de"),
            "audio-en-001": ("Hello, I need help with the residence registration.", "en"),
            "audio-tr-001": ("Merhaba, oturma kayıt için yardıma ihtiyacım var.", "tr"),
        }
        text, sprache = beispiele.get(audio_id, ("Hallo", "de"))
        return Transkript(
            text=text,
            sprache=sprache,
            konfidenz=0.91,
            pii_redacted=[],
        )

    def stub_translate(
        text: str,
        from_sprache: str,
        to_sprache: str,
    ) -> Uebersetzung:
        """Stub: einfache lookup-Tabelle."""
        # In Production: DeepL Pro API
        beispiele = {
            ("de", "en", "Guten Tag"): "Good day",
            ("en", "de", "Hello"): "Hallo",
            ("tr", "de", "Merhaba"): "Hallo",
            ("de", "tr", "Hallo"): "Merhaba",
        }
        # Naive: bei unbekannten Pairs returne Original
        key = (from_sprache, to_sprache, text[:9])
        uebersetzt = beispiele.get(key, f"[stub-translate {from_sprache}→{to_sprache}] {text}")
        return Uebersetzung(
            original_text=text,
            original_sprache=from_sprache,
            ziel_sprache=to_sprache,
            uebersetzt=uebersetzt,
        )

    def stub_pii_redact(text: str, sprache: str) -> tuple[str, list[str]]:
        """Stub: Presidio-Style PII-Redaction."""
        import re

        gefunden = []
        if re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", text):
            gefunden.append("email")
            text = re.sub(r"[\w.+-]+@[\w-]+\.[\w.-]+", "<EMAIL>", text)
        if re.search(r"\b\+?\d[\d\s-]{8,}\b", text):
            gefunden.append("telefon")
            text = re.sub(r"\b\+?\d[\d\s-]{8,}\b", "<PHONE>", text)
        return text, gefunden

    def stub_voice_turn(
        turn_nr: int, user_pseudonym: str, audio_id: str, ziel_sprache: str
    ) -> VoiceTurn:
        """Vollständiger Voice-Turn (Stub)."""
        # 1. ASR
        transkript = stub_asr(audio_id)

        # 2. PII-Redaction
        text_clean, pii = stub_pii_redact(transkript.text, transkript.sprache)
        transkript = transkript.model_copy(update={"text": text_clean, "pii_redacted": pii})

        # 3. Falls User-Sprache != Ziel: übersetzen für LLM
        if transkript.sprache != ziel_sprache:
            uebersetzt = stub_translate(text_clean, transkript.sprache, ziel_sprache)
            for_llm_text = uebersetzt.uebersetzt
        else:
            for_llm_text = text_clean

        # 4. Stub-Antwort vom LLM (in Production: Pydantic AI mit Mistral)
        stub_antwort_de = (
            f"Verstanden — Ihr Anliegen ist '{for_llm_text[:40]}...'. Ich helfe Ihnen weiter."
        )

        # 5. Antwort zurück in User-Sprache übersetzen (falls nötig)
        if ziel_sprache != transkript.sprache:
            antwort_zurueck = stub_translate(stub_antwort_de, ziel_sprache, transkript.sprache)
            antwort_text = antwort_zurueck.uebersetzt
        else:
            antwort_text = stub_antwort_de

        return VoiceTurn(
            turn_nr=turn_nr,
            user_pseudonym=user_pseudonym,
            transkript=transkript,
            antwort_text=antwort_text,
            antwort_sprache=transkript.sprache,
            uebersetzungen_im_loop=2 if transkript.sprache != ziel_sprache else 0,
        )

    return stub_translate, stub_voice_turn


@app.cell
def _(mo, stub_voice_turn):
    """Test mit 3 Voice-Turns in 3 Sprachen."""
    test_turns = [
        ("buerger-001", "audio-de-001"),
        ("buerger-002", "audio-en-001"),
        ("buerger-003", "audio-tr-001"),
    ]

    llm_pivot = "de"  # Pivot-Sprache für LLM

    rows_turns = []
    for i, (pseudonym, audio_id) in enumerate(test_turns, 1):
        turn = stub_voice_turn(i, pseudonym, audio_id, llm_pivot)
        rows_turns.append(
            f"| {i} | {pseudonym} | {turn.transkript.sprache} | "
            f"{turn.transkript.text[:40]}... | "
            f"{turn.antwort_text[:40]}... | "
            f"{turn.uebersetzungen_im_loop}× |"
        )

    mo.md(
        f"## Voice-Turns mit Pivot-Sprache `{llm_pivot}`\n\n"
        "| Turn | User | Sprache | Transkript | Antwort | Übersetz. |\n"
        "|---|---|---|---|---|---|\n" + "\n".join(rows_turns)
    )
    return


@app.cell
def _(mo, stub_translate):
    """Übersetzungs-Matrix-Demo."""
    pairs = [
        ("Guten Tag", "de", "en"),
        ("Guten Tag", "de", "tr"),
        ("Hello", "en", "de"),
        ("Merhaba", "tr", "de"),
    ]

    rows_matrix = []
    for text, von, nach in pairs:
        u = stub_translate(text, von, nach)
        rows_matrix.append(f"| {text} | {von} → {nach} | {u.uebersetzt} |")

    mo.md(
        "## Übersetzungs-Matrix (Stub)\n\n"
        "| Original | Richtung | Stub-Output |\n|---|---|---|\n" + "\n".join(rows_matrix)
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Vollversion-Wegweiser

        ```python
        # Vollständiger Stack mit echten APIs:
        import whisper
        import deepl
        from f5_tts.api import F5TTS
        from langgraph.graph import StateGraph
        from langgraph.checkpoint.postgres import PostgresSaver

        asr_modell = whisper.load_model("large-v3")
        deepl_client = deepl.Translator(auth_key=os.environ["DEEPL_API_KEY"])
        tts_modell = F5TTS()

        # LangGraph mit Postgres-Memory
        checkpointer = PostgresSaver.from_conn_string(os.environ["DATABASE_URL"])
        graph = StateGraph(VoiceAgentState).compile(checkpointer=checkpointer)
        ```

        ## DSGVO-Pattern (Pflicht)

        - **Voice = biometrisches Datum** (DSGVO Art. 9) — höhere Schwelle für Verarbeitung
        - **PII-Redaction** in Transkripten **vor** Memory-Speicherung
        - **Auto-Lösch-Pipeline**: Audio max. 60 Min, Transkripte max. 7 Tage
        - **AVV** mit DeepL (DE-Server) + Whisper-Hoster + Mistral

        ## Compliance-Anker

        - **AI-Act Art. 50**: Disclaimer „Du sprichst mit einer KI"
        - **AI-Act Anhang III Nr. 5**: möglicherweise Hochrisiko bei Behörden-Einsatz
        - **DSGVO Art. 9**: Voice = biometrisch — explizite Einwilligung pflicht
        - **DSGVO Art. 5 lit. e**: Speicherbegrenzung — Auto-Lösch-Pipeline

        ## Quellen

        - Whisper-large-v3 — <https://huggingface.co/openai/whisper-large-v3>
        - DeepL Pro API — <https://www.deepl.com/pro-api>
        - F5-TTS — <https://github.com/SWivid/F5-TTS>
        - Presidio — <https://microsoft.github.io/presidio/>
        - LangGraph Memory — <https://langchain-ai.github.io/langgraph/concepts/memory/>
        """
    )
    return


if __name__ == "__main__":
    app.run()
