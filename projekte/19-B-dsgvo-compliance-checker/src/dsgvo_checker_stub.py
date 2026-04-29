# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "marimo",
#   "pydantic>=2.9",
# ]
# ///

"""DSGVO-Compliance-Checker Stub — Capstone 19.B.

Smoke-Test-tauglich: keine echten Web-Calls, keine Playwright-Abhängigkeit.
Stub-Pipeline zeigt Architektur. Vollversion siehe README.md.
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
        # ⚖️ DSGVO-Compliance-Checker · Capstone 19.B

        Stub-Pipeline für Webseiten-Compliance-Audit:

        - **Cookie-Banner-Check** (TTDSG § 25)
        - **Tracker-Inventar** (vor/nach Konsens)
        - **Server-Geo-Lookup**
        - **DSFA-Light-Bericht**

        Smoke-Test-tauglich (keine externen Calls). Vollversion siehe README.md.
        """
    )
    return


@app.cell
def _():
    """Pydantic-Schemas."""
    from typing import Literal

    from pydantic import BaseModel, Field

    class CookieBannerCheck(BaseModel):
        banner_vorhanden: bool
        reject_all_button: bool
        pre_selected_checkboxes: bool
        ttdsg_konform: bool
        verstoesse: list[str]

    class TrackerDetected(BaseModel):
        name: str
        kategorie: Literal["analytics", "ad", "social", "session", "performance"]
        anzahl_requests: int = Field(ge=0)
        vor_konsens_geladen: bool

    class ServerStandort(BaseModel):
        domain: str
        ip: str
        land: str
        ist_eu: bool

    class DSFALightBericht(BaseModel):
        url: str
        cookie_banner: CookieBannerCheck
        tracker: list[TrackerDetected]
        server_standort: ServerStandort
        risiko_score: int = Field(ge=1, le=10)
        empfohlene_massnahmen: list[str]

    return CookieBannerCheck, DSFALightBericht, ServerStandort, TrackerDetected


@app.cell
def _(CookieBannerCheck, DSFALightBericht, ServerStandort, TrackerDetected):
    """Stub-Audit für eine Beispiel-URL."""

    def audit_stub(url: str) -> DSFALightBericht:
        """Simuliert ein Audit — in der Vollversion: Playwright + LLM-Klassifikator."""
        return DSFALightBericht(
            url=url,
            cookie_banner=CookieBannerCheck(
                banner_vorhanden=True,
                reject_all_button=False,  # Verstoss
                pre_selected_checkboxes=True,  # Verstoss
                ttdsg_konform=False,
                verstoesse=[
                    "Reject-All-Button fehlt — verstößt gegen TTDSG § 25 + EuGH Planet49",
                    "Pre-selected Checkboxes für Marketing-Cookies — verstößt gegen DSGVO Art. 4 Nr. 11",
                ],
            ),
            tracker=[
                TrackerDetected(
                    name="google_analytics_4",
                    kategorie="analytics",
                    anzahl_requests=5,
                    vor_konsens_geladen=True,  # Verstoss
                ),
                TrackerDetected(
                    name="meta_pixel",
                    kategorie="ad",
                    anzahl_requests=3,
                    vor_konsens_geladen=True,  # Verstoss
                ),
                TrackerDetected(
                    name="hotjar",
                    kategorie="performance",
                    anzahl_requests=2,
                    vor_konsens_geladen=False,  # ok
                ),
            ],
            server_standort=ServerStandort(
                domain=url.replace("https://", "").replace("http://", "").split("/")[0],
                ip="1.2.3.4",
                land="USA",
                ist_eu=False,  # Drittland-Transfer-Issue
            ),
            risiko_score=7,
            empfohlene_massnahmen=[
                "Reject-All-Button gleichwertig zu Accept-All gestalten (TTDSG § 25)",
                "Pre-Konsens-Tracker (GA4, Meta Pixel) entfernen oder hinter Banner",
                "Hosting-Provider auf EU-Server migrieren (Hetzner, IONOS, OVH)",
                "Datenschutz-Erklärung ergänzen: Drittland-Transfer + SCC-Hinweise",
            ],
        )

    return (audit_stub,)


@app.cell
def _(audit_stub, mo):
    """Test-Audit auf 3 Beispiel-URLs (Stub-Werte)."""
    test_urls = [
        "https://beispiel-shop.de",
        "https://kanzlei-mueller.de",
        "https://blog-saskia.de",
    ]

    rows = []
    for url in test_urls:
        b = audit_stub(url)
        verstoesse_anz = (
            len(b.cookie_banner.verstoesse)
            + sum(1 for t in b.tracker if t.vor_konsens_geladen)
            + (0 if b.server_standort.ist_eu else 1)
        )
        marker = "🔴" if b.risiko_score >= 7 else "🟡" if b.risiko_score >= 4 else "🟢"
        rows.append(
            f"| {url} | {marker} {b.risiko_score}/10 | "
            f"{verstoesse_anz} | {b.server_standort.land} | "
            f"{'✅' if b.server_standort.ist_eu else '⚠️ Drittland'} |"
        )

    mo.md(
        "## Test-Audit (Stub-Werte)\n\n"
        "| URL | Risiko | Verstöße | Server | EU? |\n|---|---|---|---|---|\n" + "\n".join(rows)
    )
    return


@app.cell
def _(audit_stub, mo):
    """DSFA-Light-Bericht-Beispiel."""
    bericht = audit_stub("https://beispiel-shop.de")
    yaml_text = (
        f"url: {bericht.url}\n"
        f"risiko_score: {bericht.risiko_score}\n"
        f"cookie_banner:\n"
        f"  ttdsg_konform: {bericht.cookie_banner.ttdsg_konform}\n"
        f"  verstoesse: {bericht.cookie_banner.verstoesse}\n"
        f"tracker_anz: {len(bericht.tracker)}\n"
        f"  davon_vor_konsens: {sum(1 for t in bericht.tracker if t.vor_konsens_geladen)}\n"
        f"server:\n"
        f"  land: {bericht.server_standort.land}\n"
        f"  ist_eu: {bericht.server_standort.ist_eu}\n"
        f"empfohlene_massnahmen:\n"
    )
    for m in bericht.empfohlene_massnahmen:
        yaml_text += f"  - {m}\n"

    mo.md(f"## DSFA-Light-Bericht-Beispiel\n\n```yaml\n{yaml_text}```")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Vollversion-Wegweiser

        - **Playwright-Crawler**: `pip install playwright && playwright install chromium`
        - **Pydantic AI** für Cookie-Banner + DSE-Klassifikation
        - **WHOIS / ipapi.co** für Server-Geo-Lookup
        - **PDF-Export** mit `weasyprint` für Mandant:innen-Reports

        ## Compliance-Anker

        - **TTDSG § 25**: Cookie-Einwilligung mit Reject-All-Button
        - **DSGVO Art. 13 + 14**: Pflichtangaben in Datenschutz-Erklärung
        - **DSGVO Art. 44**: Drittland-Transfer dokumentieren
        - **EuGH Planet49 (C-673/17)**: explizite Einwilligung pflicht

        ## Quellen

        - TTDSG § 25 — <https://www.gesetze-im-internet.de/ttdsg/__25.html>
        - EuGH Planet49 — <https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:62017CJ0673>
        - Playwright Python — <https://playwright.dev/python/>
        """
    )
    return


if __name__ == "__main__":
    app.run()
