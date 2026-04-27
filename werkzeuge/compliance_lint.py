"""Validiert das YAML-Frontmatter-Schema je `compliance.md` und `modul.md`.

Pflichtfelder:
    - compliance.md: id, phase, stand, anker[], dsgvo_artikel[], ai_act_artikel[]
    - modul.md: id, titel, dauer_stunden, schwierigkeit, stand, lernziele[]

Mit `--modul`-Flag prüft modul.md statt compliance.md.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

import click
import yaml

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


COMPLIANCE_REQUIRED: dict[str, object] = {
    "id": (str, int),
    "phase": str,
    "stand": (str, date),
    "anker": list,
    "dsgvo_artikel": list,
    "ai_act_artikel": list,
}

MODUL_REQUIRED: dict[str, object] = {
    "id": (str, int),
    "titel": str,
    "dauer_stunden": (int, float),
    "schwierigkeit": str,
    "stand": (str, date),
    "lernziele": list,
}

SCHWIERIGKEITS_WERTE = {"einsteiger", "leicht", "mittel", "fortgeschritten", "experte"}


@dataclass
class Befund:
    pfad: Path
    fehler: list[str] = field(default_factory=list)
    warnungen: list[str] = field(default_factory=list)


def parse_frontmatter(text: str) -> dict | None:
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None
    return yaml.safe_load(m.group(1))


def validiere_typ(name: str, wert, erwartet, befund: Befund) -> None:
    if isinstance(erwartet, tuple):
        if not isinstance(wert, erwartet):
            befund.fehler.append(
                f"Feld '{name}' hat Typ {type(wert).__name__}, erwartet {erwartet}"
            )
    elif not isinstance(wert, erwartet):
        befund.fehler.append(
            f"Feld '{name}' hat Typ {type(wert).__name__}, erwartet {erwartet.__name__}"
        )


def validiere_compliance(pfad: Path) -> Befund:
    befund = Befund(pfad)
    text = pfad.read_text(encoding="utf-8")
    fm = parse_frontmatter(text)
    if fm is None:
        befund.fehler.append("Kein YAML-Frontmatter (`---` ... `---`) gefunden")
        return befund

    for feld, typ in COMPLIANCE_REQUIRED.items():
        if feld not in fm:
            befund.fehler.append(f"Pflichtfeld '{feld}' fehlt")
        else:
            validiere_typ(feld, fm[feld], typ, befund)

    if "stand" in fm:
        stand_value = fm["stand"]
        try:
            stand_dt = (
                stand_value
                if isinstance(stand_value, date)
                else date.fromisoformat(str(stand_value))
            )
            if (date.today() - stand_dt).days > 180:
                befund.warnungen.append(
                    f"'stand' ist {(date.today() - stand_dt).days} Tage alt — bitte review"
                )
        except (ValueError, TypeError):
            befund.fehler.append(f"'stand' ist kein ISO-Datum: {fm['stand']}")

    if "ai_act_artikel" in fm and isinstance(fm["ai_act_artikel"], list):
        for art in fm["ai_act_artikel"]:
            if not re.match(r"^art-\d+(-abs-\d+)?(-lit-[a-z])?$", str(art)):
                befund.warnungen.append(
                    f"'ai_act_artikel' Eintrag '{art}' folgt nicht dem Schema 'art-N' / 'art-N-abs-M' / 'art-N-abs-M-lit-x'"
                )

    if "dsgvo_artikel" in fm and isinstance(fm["dsgvo_artikel"], list):
        for art in fm["dsgvo_artikel"]:
            if not re.match(r"^art-\d+(-abs-\d+)?(-lit-[a-z])?$", str(art)):
                befund.warnungen.append(f"'dsgvo_artikel' Eintrag '{art}' folgt nicht dem Schema")

    return befund


def validiere_modul(pfad: Path) -> Befund:
    befund = Befund(pfad)
    text = pfad.read_text(encoding="utf-8")
    fm = parse_frontmatter(text)
    if fm is None:
        befund.fehler.append("Kein YAML-Frontmatter gefunden")
        return befund

    for feld, typ in MODUL_REQUIRED.items():
        if feld not in fm:
            befund.fehler.append(f"Pflichtfeld '{feld}' fehlt")
        else:
            validiere_typ(feld, fm[feld], typ, befund)

    if "schwierigkeit" in fm and fm["schwierigkeit"] not in SCHWIERIGKEITS_WERTE:
        befund.fehler.append(
            f"'schwierigkeit' = {fm['schwierigkeit']!r}, erlaubt: {sorted(SCHWIERIGKEITS_WERTE)}"
        )

    if "lernziele" in fm and isinstance(fm["lernziele"], list) and len(fm["lernziele"]) < 2:
        befund.warnungen.append(f"Nur {len(fm['lernziele'])} Lernziel(e) — empfohlen sind 3–6")

    return befund


@click.command()
@click.argument("pfad", type=click.Path(exists=True, path_type=Path))
@click.option("--modul", is_flag=True, help="modul.md statt compliance.md prüfen")
def main(pfad: Path, modul: bool) -> None:
    """Validiert compliance.md (default) oder modul.md (--modul) Schema rekursiv."""
    glob_pat = "modul.md" if modul else "compliance.md"
    if pfad.is_file():
        dateien = [pfad]
    else:
        dateien = sorted(pfad.rglob(glob_pat))

    if not dateien:
        click.echo(f"Keine {glob_pat} unter {pfad} gefunden — OK (nichts zu prüfen)")
        return

    validierer = validiere_modul if modul else validiere_compliance
    fehler_gesamt = 0
    warnungen_gesamt = 0

    for f in dateien:
        b = validierer(f)
        if not b.fehler and not b.warnungen:
            click.echo(f"✓ {f}")
            continue
        for e in b.fehler:
            click.echo(f"✗ {f}: {e}", err=True)
            fehler_gesamt += 1
        for w in b.warnungen:
            click.echo(f"⚠ {f}: {w}")
            warnungen_gesamt += 1

    click.echo(
        f"\n{len(dateien)} {glob_pat} geprüft, "
        f"{fehler_gesamt} Fehler, {warnungen_gesamt} Warnungen."
    )
    if fehler_gesamt > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
