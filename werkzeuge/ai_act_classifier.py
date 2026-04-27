"""Klassifiziert ein KI-System nach EU AI Act Risikostufen.

Stand: 2026-04-27. Wichtig: Das Tool ersetzt keine juristische Beratung —
es operationalisiert nur die in der VO (EU) 2024/1689 verwendeten Kategorien
und Anhänge anhand einer Modell-Karte (YAML).
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

import click
import yaml
from rich.console import Console
from rich.panel import Panel
from rich.table import Table


class Risikostufe(str, Enum):
    INAKZEPTABEL = "inakzeptabel"
    HOCHRISIKO = "hochrisiko"
    BEGRENZT = "begrenzt"
    MINIMAL = "minimal"
    GPAI_SYSTEMIC = "gpai-mit-systemischem-risiko"
    GPAI = "gpai"


VERBOTENE_PRAKTIKEN_ART5 = {
    "social-scoring": "Art. 5 Abs. 1 lit. c — Social Scoring durch Behörden",
    "kognitive-manipulation": "Art. 5 Abs. 1 lit. a — unterschwellige/manipulative Techniken",
    "ausnutzung-vulnerabler-gruppen": "Art. 5 Abs. 1 lit. b — Ausnutzung von Schwächen Minderjähriger/Behinderter",
    "rueckwirkende-emotionserkennung-arbeit": "Art. 5 Abs. 1 lit. f — Emotionserkennung am Arbeitsplatz/in Bildung",
    "biometrische-kategorisierung-sensibel": "Art. 5 Abs. 1 lit. g — biometrische Kategorisierung nach sensiblen Merkmalen",
    "wahllose-gesichtserkennung-internet": "Art. 5 Abs. 1 lit. e — Aufbau von Gesichtserkennungs-DBs aus Internet-Scraping",
    "predictive-policing-personenbezogen": "Art. 5 Abs. 1 lit. d — Predictive Policing rein auf Profiling",
    "echtzeit-rbi-oeffentlich": "Art. 5 Abs. 1 lit. h — Echtzeit-Fernidentifikation in öffentlich zugänglichen Räumen",
}

HOCHRISIKO_ANHANG_III = {
    "biometrie": "Anh. III Nr. 1 — biometrische Identifikation/Kategorisierung",
    "kritische-infrastruktur": "Anh. III Nr. 2 — Verkehr, Wasser/Gas/Strom-Versorgung",
    "bildung-pruefung": "Anh. III Nr. 3 — Zugang zu/Bewertung in Bildung",
    "beschaeftigung-hr": "Anh. III Nr. 4 — Personalauswahl, Performance, Beendigung",
    "wesentliche-private-dienste": "Anh. III Nr. 5 — Kreditscoring, Kfz-/Lebens-Versicherung, Notfall-Triage",
    "wesentliche-oeffentliche-dienste": "Anh. III Nr. 5 — Sozialleistungen-Vergabe",
    "strafverfolgung": "Anh. III Nr. 6 — Strafverfolgung",
    "migration-asyl-grenzkontrolle": "Anh. III Nr. 7 — Migration & Grenzkontrolle",
    "justiz-demokratie": "Anh. III Nr. 8 — Justiz und demokratische Prozesse",
}

TRANSPARENZPFLICHT_ART50 = {
    "chatbot": "Art. 50 Abs. 1 — Chatbots: Hinweis auf KI-Interaktion",
    "synthetische-inhalte": "Art. 50 Abs. 2 — generierte/manipulierte Inhalte maschinenlesbar markieren",
    "deepfake": "Art. 50 Abs. 4 — Deepfakes erkennbar kennzeichnen",
    "emotionserkennung-zulaessig": "Art. 50 Abs. 3 — Information bei Emotionserkennung/biometrischer Kategorisierung",
}


@dataclass
class Befund:
    risiko: Risikostufe
    begruendung: list[str]
    pflichten: list[str]
    artikel_referenzen: list[str]


def klassifiziere(modell_karte: dict) -> Befund:
    """Bestimmt Risikostufe aus Modell-Karte."""
    begruendung: list[str] = []
    pflichten: list[str] = []
    artikel: list[str] = []

    risk_indikatoren = modell_karte.get("risiko_indikatoren", {}) or {}
    use_case = modell_karte.get("use_case_kategorien", []) or []
    transparenz_trigger = modell_karte.get("transparenz_trigger", []) or []
    flops = modell_karte.get("training_compute_flops")
    is_gpai = bool(modell_karte.get("ist_gpai", False))

    # 1. Verbote (Art. 5)
    for k, beschreibung in VERBOTENE_PRAKTIKEN_ART5.items():
        if risk_indikatoren.get(k):
            begruendung.append(f"Verbotene Praxis erkannt: {beschreibung}")
            artikel.append(beschreibung)

    if begruendung:
        pflichten.append("System darf NICHT in Verkehr gebracht/genutzt werden")
        return Befund(Risikostufe.INAKZEPTABEL, begruendung, pflichten, artikel)

    # 2. Hochrisiko (Anhang III)
    for kat in use_case:
        if kat in HOCHRISIKO_ANHANG_III:
            begruendung.append(f"Hochrisiko-Kategorie: {HOCHRISIKO_ANHANG_III[kat]}")
            artikel.append(HOCHRISIKO_ANHANG_III[kat])

    # 2b. GPAI mit systemischem Risiko (Art. 51)
    if is_gpai and flops and flops >= 10**25:
        artikel.append(
            "Art. 51 — GPAI mit systemischem Risiko (Schwelle 10^25 FLOPs überschritten)"
        )
        pflichten.extend(
            [
                "Modell-Evaluierung inkl. Adversarial Tests (Art. 55)",
                "Cybersicherheits-Schutz (Art. 55)",
                "Schwerwiegende Vorfälle ans AI-Office melden (Art. 55)",
                "Energieverbrauch dokumentieren (Art. 55)",
            ]
        )
        return Befund(Risikostufe.GPAI_SYSTEMIC, begruendung, pflichten, artikel)

    if begruendung:
        pflichten.extend(
            [
                "Risk-Management-System (Art. 9)",
                "Daten-Governance (Art. 10)",
                "Technische Dokumentation (Art. 11)",
                "Logging (Art. 12)",
                "Transparenz und Information für Betreiber (Art. 13)",
                "Menschliche Aufsicht (Art. 14)",
                "Genauigkeit, Robustheit, Cybersicherheit (Art. 15)",
                "Konformitätsbewertung & CE-Kennzeichnung (Art. 43)",
                "EU-Datenbank-Eintrag (Art. 49 / Anhang VIII)",
            ]
        )
        return Befund(Risikostufe.HOCHRISIKO, begruendung, pflichten, artikel)

    # 3. Begrenztes Risiko (Art. 50)
    for trigger in transparenz_trigger:
        if trigger in TRANSPARENZPFLICHT_ART50:
            begruendung.append(f"Transparenzpflicht: {TRANSPARENZPFLICHT_ART50[trigger]}")
            artikel.append(TRANSPARENZPFLICHT_ART50[trigger])

    if begruendung:
        pflichten.extend(
            [
                "Endnutzer:innen klar informieren, dass KI im Spiel ist",
                "Synthetische/manipulierte Inhalte technisch markieren (C2PA o.ä.)",
            ]
        )
        return Befund(Risikostufe.BEGRENZT, begruendung, pflichten, artikel)

    # 4. GPAI (ohne systemisches Risiko) — eigene Pflichten Art. 53
    if is_gpai:
        artikel.append("Art. 53 — GPAI-Modell-Anbieter")
        pflichten.extend(
            [
                "Technische Dokumentation für Behörden bereithalten (Art. 53 Abs. 1 lit. a)",
                "Information an Bereitsteller (Art. 53 Abs. 1 lit. b)",
                "Copyright-Policy: TDM-Vorbehalte respektieren (Art. 53 Abs. 1 lit. c)",
                "Trainingsdaten-Zusammenfassung nach AI-Office-Template (Art. 53 Abs. 1 lit. d)",
            ]
        )
        return Befund(Risikostufe.GPAI, begruendung, pflichten, artikel)

    # 5. Minimal (kein direkter Pflichtkatalog jenseits AI Literacy + DSGVO)
    pflichten.extend(
        [
            "AI Literacy nach Art. 4 (für Bereitsteller verpflichtend seit 02.02.2025)",
            "DSGVO bleibt vollständig anwendbar",
            "Empfohlen: freiwilliger Code of Conduct (Art. 95)",
        ]
    )
    return Befund(Risikostufe.MINIMAL, begruendung, pflichten, artikel)


def render(befund: Befund, modell_name: str) -> None:
    console = Console()
    farbe = {
        Risikostufe.INAKZEPTABEL: "red on white",
        Risikostufe.HOCHRISIKO: "bright_red",
        Risikostufe.BEGRENZT: "yellow",
        Risikostufe.MINIMAL: "green",
        Risikostufe.GPAI_SYSTEMIC: "magenta",
        Risikostufe.GPAI: "blue",
    }[befund.risiko]

    console.print(
        Panel.fit(
            f"[{farbe}]Risikostufe: {befund.risiko.value.upper()}[/{farbe}]",
            title=f"AI-Act-Klassifizierung — {modell_name}",
            border_style=farbe.split()[0],
        )
    )

    if befund.begruendung:
        tab = Table(title="Begründung", show_lines=False)
        tab.add_column("#", style="dim")
        tab.add_column("Befund")
        for i, b in enumerate(befund.begruendung, 1):
            tab.add_row(str(i), b)
        console.print(tab)

    if befund.pflichten:
        tab2 = Table(title="Pflichten")
        tab2.add_column("#", style="dim")
        tab2.add_column("Pflicht")
        for i, p in enumerate(befund.pflichten, 1):
            tab2.add_row(str(i), p)
        console.print(tab2)

    if befund.artikel_referenzen:
        tab3 = Table(title="Artikel-Referenzen (VO 2024/1689)")
        tab3.add_column("Referenz")
        for a in befund.artikel_referenzen:
            tab3.add_row(a)
        console.print(tab3)

    console.print(
        "\n[dim]Hinweis: Dies ist keine Rechtsberatung. "
        "Stand 2026-04-27. Aktuelle Rechtslage prüfen.[/dim]"
    )


@click.command()
@click.option(
    "--modell-karte",
    "-m",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    required=True,
    help="Pfad zu YAML-Modell-Karte",
)
@click.option(
    "--als-json",
    is_flag=True,
    help="Maschinenlesbares JSON statt Rich-Output",
)
def main(modell_karte: Path, als_json: bool) -> None:
    """Klassifiziert ein KI-System nach EU AI Act."""
    karte = yaml.safe_load(modell_karte.read_text(encoding="utf-8"))
    befund = klassifiziere(karte)

    if als_json:
        import json

        out = {
            "modell": karte.get("name", modell_karte.stem),
            "risiko": befund.risiko.value,
            "begruendung": befund.begruendung,
            "pflichten": befund.pflichten,
            "artikel_referenzen": befund.artikel_referenzen,
            "stand": "2026-04-27",
        }
        click.echo(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        render(befund, karte.get("name", modell_karte.stem))

    if befund.risiko == Risikostufe.INAKZEPTABEL:
        sys.exit(2)


if __name__ == "__main__":
    main()
