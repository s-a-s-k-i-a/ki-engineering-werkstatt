# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "marimo",
#   "pydantic>=2.9",
# ]
# ///

"""Lösungs-Skelett — Übung 08.01 — Watermark-Pipeline-Audit.

Smoke-test-tauglich. Reine Pydantic-Logik, kein FLUX-/LTX-Inference.
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
        # 🎯 Lösung Übung 08.01 — Watermark-Pipeline-Audit

        Drei generative Use-Cases → Modell + Watermark + Lizenz + § 201b.
        """
    )
    return


@app.cell
def _():
    """Pydantic-Profil-Schema."""
    from pydantic import BaseModel, Field

    class GenerativeProfil(BaseModel):
        name: str
        modell: str
        medium: str  # "bild", "video", "3d", "audio"
        kommerziell: bool
        volumen_pro_tag: int = Field(ge=1)
        personen_im_output: bool

    return (GenerativeProfil,)


@app.cell
def _():
    """Lizenz- + Compliance-Funktionen."""

    lizenz_db = {
        "FLUX.2": {"lizenz": "Apache 2.0", "eu_kommerziell": True, "anbieter": "BFL Freiburg"},
        "TRELLIS.2": {"lizenz": "MIT", "eu_kommerziell": True, "anbieter": "Microsoft"},
        "Hunyuan3D-2": {
            "lizenz": "Tencent Custom",
            "eu_kommerziell": False,
            "anbieter": "Tencent — ⛔ EU/UK/SK ausgeschlossen",
        },
        "LTX-2.3": {"lizenz": "RAIL-S (Custom)", "eu_kommerziell": True, "anbieter": "Lightricks"},
        "SD-3.5": {
            "lizenz": "Stability AI Community",
            "eu_kommerziell": True,
            "anbieter": "Stability AI",
        },
    }

    def lizenz_check(p) -> dict:
        info = lizenz_db.get(p.modell, {"lizenz": "?", "eu_kommerziell": False})
        ok = info["eu_kommerziell"] and (info["lizenz"] not in {"?"})
        return {**info, "ok_fuer_use_case": ok if p.kommerziell else True}

    def watermark_empfehlung(p) -> dict:
        if p.medium == "bild":
            return {
                "unsichtbar": "Stable Signature",
                "sichtbar": "C2PA-Manifest + Mini-Marke",
                "manifest": "C2PA mit `claim_generator`, `signature_info`, `assertions`",
            }
        if p.medium == "video":
            return {
                "unsichtbar": "Frame-weise C2PA + Audio-Watermark",
                "sichtbar": "Sichtbarer KI-Hinweis im Video",
                "manifest": "C2PA-Manifest pro Clip",
            }
        if p.medium == "3d":
            return {
                "unsichtbar": "Metadaten-Hash in 3D-File",
                "sichtbar": "C2PA-Marke im Asset-Paket",
                "manifest": "C2PA-Manifest im Asset-Bundle",
            }
        if p.medium == "audio":
            return {
                "unsichtbar": "AudioSeal",
                "sichtbar": "Sprecher-Disclaimer am Anfang",
                "manifest": "C2PA-Manifest neben dem Audio",
            }
        return {}

    def stgb_201b_check(p) -> list[str]:
        warnungen = []
        if p.personen_im_output:
            if p.medium in {"video", "audio"}:
                warnungen.append(
                    "⚠️ § 201b StGB-Entwurf: bei realer Person → Stimm-/Video-Klon-Verbot ohne Einwilligung"
                )
            warnungen.append("KUG Art. 22 — Recht am eigenen Bild, Einwilligung pflicht")
            warnungen.append("DSGVO Art. 9 falls biometrische Daten")
        return warnungen

    def ai_act_50_2_pflicht(p) -> str:
        return (
            "AI-Act Art. 50.2 (in Kraft 02.08.2026): "
            "maschinenlesbare KI-Markierung Pflicht für jedes generative Output"
        )

    return (
        ai_act_50_2_pflicht,
        lizenz_check,
        stgb_201b_check,
        watermark_empfehlung,
    )


@app.cell
def _(GenerativeProfil):
    """Drei Use-Cases."""
    profile = [
        GenerativeProfil(
            name="Marketing-Bilder-Generator",
            modell="FLUX.2",
            medium="bild",
            kommerziell=True,
            volumen_pro_tag=1_000,
            personen_im_output=True,  # Modelfotos, Werbe-Personen
        ),
        GenerativeProfil(
            name="3D-Asset-Pipeline (Maschinenbau)",
            modell="TRELLIS.2",
            medium="3d",
            kommerziell=True,
            volumen_pro_tag=50,
            personen_im_output=False,
        ),
        GenerativeProfil(
            name="Video-Erklärbar-Assistent",
            modell="LTX-2.3",
            medium="video",
            kommerziell=True,
            volumen_pro_tag=200,
            personen_im_output=True,  # Erklärbar-Avatar oder echte Sprecher:in
        ),
    ]
    return (profile,)


@app.cell
def _(
    ai_act_50_2_pflicht,
    lizenz_check,
    mo,
    profile,
    stgb_201b_check,
    watermark_empfehlung,
):
    """Detail pro Use-Case."""
    blocks = []
    for p in profile:
        liz = lizenz_check(p)
        wm = watermark_empfehlung(p)
        stgb = stgb_201b_check(p)
        ok_emoji = "✅" if liz.get("ok_fuer_use_case") else "⛔"
        stgb_str = "\n".join(f"  - {w}" for w in stgb) if stgb else "  - keine § 201b-Bedenken"
        blocks.append(
            f"### {p.name} ({p.modell})\n\n"
            f"- **Lizenz**: {liz['lizenz']} ({liz.get('anbieter', '?')}) {ok_emoji}\n"
            f"- **Watermark unsichtbar**: {wm.get('unsichtbar', '?')}\n"
            f"- **Watermark sichtbar**: {wm.get('sichtbar', '?')}\n"
            f"- **C2PA-Manifest**: {wm.get('manifest', '?')}\n"
            f"- **{ai_act_50_2_pflicht(p)}**\n"
            f"- **§ 201b / KUG-Pflichten**:\n{stgb_str}\n"
        )
    mo.md("## Detail pro Use-Case\n\n" + "\n".join(blocks))
    return


@app.cell
def _(GenerativeProfil, lizenz_check, stgb_201b_check, watermark_empfehlung):
    """Smoke-Test: 5 Akzeptanz-Asserts."""
    flux = GenerativeProfil(
        name="t1",
        modell="FLUX.2",
        medium="bild",
        kommerziell=True,
        volumen_pro_tag=10,
        personen_im_output=True,
    )
    trellis = GenerativeProfil(
        name="t2",
        modell="TRELLIS.2",
        medium="3d",
        kommerziell=True,
        volumen_pro_tag=10,
        personen_im_output=False,
    )
    hunyuan = GenerativeProfil(
        name="t3",
        modell="Hunyuan3D-2",
        medium="3d",
        kommerziell=True,
        volumen_pro_tag=10,
        personen_im_output=False,
    )
    ltx = GenerativeProfil(
        name="t4",
        modell="LTX-2.3",
        medium="video",
        kommerziell=True,
        volumen_pro_tag=10,
        personen_im_output=True,
    )

    # 1. FLUX.2 → Apache 2.0 + EU-kommerziell okay
    flux_liz = lizenz_check(flux)
    assert flux_liz["lizenz"] == "Apache 2.0"
    assert flux_liz["ok_fuer_use_case"]

    # 2. TRELLIS.2 → MIT, EU-kommerziell okay
    trellis_liz = lizenz_check(trellis)
    assert trellis_liz["ok_fuer_use_case"]

    # 3. Hunyuan3D-2 → EU/UK/SK-Sperre, NICHT okay für EU-kommerziellen Use-Case
    hunyuan_liz = lizenz_check(hunyuan)
    assert not hunyuan_liz["ok_fuer_use_case"]
    assert "EU/UK/SK" in hunyuan_liz["anbieter"]

    # 4. LTX-2.3 mit Personen → § 201b-Warnung
    ltx_stgb = stgb_201b_check(ltx)
    assert any("§ 201b" in w for w in ltx_stgb)

    # 5. FLUX.2 mit Personen → KUG Art. 22 in Output
    flux_stgb = stgb_201b_check(flux)
    assert any("KUG" in w for w in flux_stgb)

    # 6. Watermark-Empfehlung pro Medium
    assert "Stable Signature" in watermark_empfehlung(flux)["unsichtbar"]
    assert (
        "AudioSeal"
        in watermark_empfehlung(
            GenerativeProfil(
                name="audio",
                modell="?",
                medium="audio",
                kommerziell=False,
                volumen_pro_tag=1,
                personen_im_output=False,
            )
        )["unsichtbar"]
    )

    print("✅ Übung 08.01 — alle Asserts grün")
    return


if __name__ == "__main__":
    app.run()
