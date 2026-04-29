# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "marimo",
#   "pydantic>=2.9",
# ]
# ///

"""Generative-Modell-Selektor — Image / Video / Audio / 3D nach Use-Case + Lizenz.

Smoke-Test-tauglich. Modell-Daten Stand 29.04.2026.
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
        # 🎨 Generative-Modell-Selektor · Phase 08

        Wählt Modell nach:

        - Modalität (Image / Video / Audio / 3D)
        - Lizenz (Apache 2.0 / Community / proprietär / **EU-Ausschluss**)
        - DACH-Region-Tauglichkeit (wichtig: Hunyuan3D = ❌)

        Stand: 29.04.2026.
        """
    )
    return


@app.cell
def _():
    """Pydantic-Schemas."""
    from typing import Literal

    from pydantic import BaseModel

    class GenModell(BaseModel):
        name: str
        modalitaet: Literal["t2i", "t2v", "i2v", "audio", "music", "3d"]
        lizenz_typ: Literal["apache-2.0", "mit", "community", "proprietaer", "eu-ausschluss"]
        eu_dsgvo_ok: bool
        kommerziell_frei: bool
        wann: str

    return (GenModell,)


@app.cell
def _(GenModell):
    """Modell-Katalog Stand 29.04.2026."""
    katalog = [
        # T2I
        GenModell(
            name="FLUX.2 [klein] 4B",
            modalitaet="t2i",
            lizenz_typ="apache-2.0",
            eu_dsgvo_ok=True,
            kommerziell_frei=True,
            wann="DACH-Default 2026 (BFL Freiburg)",
        ),
        GenModell(
            name="SD 3.5 Large",
            modalitaet="t2i",
            lizenz_typ="community",
            eu_dsgvo_ok=True,
            kommerziell_frei=True,  # < 1 Mio. USD
            wann="kommerziell frei < 1 Mio. USD Umsatz",
        ),
        GenModell(
            name="Midjourney V7/V8",
            modalitaet="t2i",
            lizenz_typ="proprietaer",
            eu_dsgvo_ok=False,  # US-Cloud
            kommerziell_frei=True,
            wann="Subscription, US-Cloud",
        ),
        # T2V
        GenModell(
            name="LTX-2.3 (22B)",
            modalitaet="t2v",
            lizenz_typ="apache-2.0",
            eu_dsgvo_ok=True,
            kommerziell_frei=True,
            wann="Open-Weights-Spitze 2026, 4K + Audio",
        ),
        GenModell(
            name="Sora 2",
            modalitaet="t2v",
            lizenz_typ="proprietaer",
            eu_dsgvo_ok=False,
            kommerziell_frei=True,
            wann="OpenAI Plus/Pro Subscription",
        ),
        GenModell(
            name="Runway Gen-4.5",
            modalitaet="t2v",
            lizenz_typ="proprietaer",
            eu_dsgvo_ok=False,
            kommerziell_frei=True,
            wann="aktuell #1 Benchmark",
        ),
        GenModell(
            name="HunyuanVideo (13B)",
            modalitaet="t2v",
            lizenz_typ="community",
            eu_dsgvo_ok=True,
            kommerziell_frei=True,
            wann="bis 100M MAU; License-Detail prüfen",
        ),
        # 3D
        GenModell(
            name="TRELLIS.2 (Microsoft, 4B)",
            modalitaet="3d",
            lizenz_typ="apache-2.0",
            eu_dsgvo_ok=True,
            kommerziell_frei=True,
            wann="DACH-Default 3D — Image-to-3D bis 1536³",
        ),
        GenModell(
            name="Hunyuan3D-2 (Tencent)",
            modalitaet="3d",
            lizenz_typ="eu-ausschluss",
            eu_dsgvo_ok=False,
            kommerziell_frei=False,  # in EU/UK/SK
            wann="⚠️ EU/UK/SK explizit AUSGESCHLOSSEN",
        ),
        # Audio
        GenModell(
            name="MusicGen large (Meta)",
            modalitaet="music",
            lizenz_typ="mit",
            eu_dsgvo_ok=True,
            kommerziell_frei=True,
            wann="Open-Source-Standard, instrumental-only",
        ),
        GenModell(
            name="Stable Audio Open Small",
            modalitaet="audio",
            lizenz_typ="community",
            eu_dsgvo_ok=True,
            kommerziell_frei=True,
            wann="< 1 Mio. USD; Sound-Effects",
        ),
        GenModell(
            name="Suno v5/v5.5",
            modalitaet="music",
            lizenz_typ="proprietaer",
            eu_dsgvo_ok=False,
            kommerziell_frei=True,
            wann="Music-as-a-Service, US-Cloud",
        ),
    ]
    return (katalog,)


@app.cell
def _(katalog):
    """Empfehlung-Logik."""

    def empfehle(profil: dict) -> list[str]:
        kandidaten = [m for m in katalog if m.modalitaet == profil["modalitaet"]]
        if profil["dsgvo_strict"]:
            kandidaten = [m for m in kandidaten if m.eu_dsgvo_ok]
        if profil["kommerziell"]:
            kandidaten = [m for m in kandidaten if m.kommerziell_frei]
        if profil["region"] == "EU":
            kandidaten = [m for m in kandidaten if m.lizenz_typ != "eu-ausschluss"]

        return [m.name for m in kandidaten[:3]]

    return (empfehle,)


@app.cell
def _(empfehle, mo):
    """Test-Profile."""
    profile = [
        {
            "name": "DACH-Marketing-Bilder",
            "modalitaet": "t2i",
            "dsgvo_strict": True,
            "kommerziell": True,
            "region": "EU",
        },
        {
            "name": "Bürger-Service-Wartemusik",
            "modalitaet": "music",
            "dsgvo_strict": True,
            "kommerziell": True,
            "region": "EU",
        },
        {
            "name": "DACH-Produkt-3D-Asset",
            "modalitaet": "3d",
            "dsgvo_strict": True,
            "kommerziell": True,
            "region": "EU",
        },
        {
            "name": "Open-Weights-Video für DACH-Werbung",
            "modalitaet": "t2v",
            "dsgvo_strict": True,
            "kommerziell": True,
            "region": "EU",
        },
        {
            "name": "Forschungs-Demo (US-Cloud ok)",
            "modalitaet": "t2v",
            "dsgvo_strict": False,
            "kommerziell": False,
            "region": "global",
        },
    ]

    rows_p = []
    for p in profile:
        empf = empfehle(p)
        rows_p.append(
            f"| {p['name']} | {p['modalitaet']} | "
            f"{p['dsgvo_strict']} | {', '.join(empf) if empf else '⚠️ keine Match'} |"
        )

    mo.md(
        "## Profil-Empfehlungen\n\n"
        "| Profil | Modalität | DSGVO-strict | Top-3-Modelle |\n"
        "|---|---|---|---|\n" + "\n".join(rows_p)
    )
    return


@app.cell
def _(katalog, mo):
    """Modell-Katalog."""
    rows_kat = []
    for m in katalog:
        eu = "✅" if m.eu_dsgvo_ok else "❌"
        komm = "✅" if m.kommerziell_frei else "❌"
        rows_kat.append(
            f"| **{m.name}** | {m.modalitaet} | {m.lizenz_typ} | {eu} | {komm} | {m.wann} |"
        )

    mo.md(
        "## Modell-Katalog (Stand 29.04.2026)\n\n"
        "| Modell | Modalität | Lizenz | EU/DSGVO | Kommerziell | Wann |\n"
        "|---|---|---|---|---|---|\n" + "\n".join(rows_kat)
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Wichtige Hinweise

        - **Black Forest Labs (Freiburg, DE)** ist der DACH-T2I-Champion mit FLUX.2 Apache 2.0
        - **Hunyuan3D-2 schließt EU/UK/SK explizit AUS** — niemals in DACH-Production
        - **DALL-E EOL 12.05.2026** — auf FLUX.2 oder SD 3.5 migrieren
        - **AI-Act Art. 50.2 ab 02.08.2026**: KI-Output-Watermark Pflicht
        - **§ 201b StGB-Entwurf** im Bundestag: Deepfake-Strafbarkeit Q2/Q3/2026

        ## Quellen

        - FLUX.2 BFL — <https://bfl.ai/blog/flux-2>
        - LTX-2.3 — <https://github.com/Lightricks/LTX-Video>
        - TRELLIS.2 — <https://microsoft.github.io/TRELLIS.2/>
        - Hunyuan3D LICENSE — <https://github.com/Tencent-Hunyuan/Hunyuan3D-2/blob/main/LICENSE>
        - AI-Act Art. 50 — <https://artificialintelligenceact.eu/article/50/>
        """
    )
    return


if __name__ == "__main__":
    app.run()
