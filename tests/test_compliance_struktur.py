"""Validiert, dass jede phase/*/compliance.md ein gültiges Schema hat."""

from __future__ import annotations

from pathlib import Path

from werkzeuge.compliance_lint import validiere_compliance, validiere_modul


def test_alle_compliance_md_valide(phasen_dir: Path) -> None:
    fehler: list[str] = []
    for compliance_md in sorted(phasen_dir.rglob("compliance.md")):
        b = validiere_compliance(compliance_md)
        if b.fehler:
            fehler.extend(f"{compliance_md.relative_to(phasen_dir)}: {e}" for e in b.fehler)
    assert not fehler, "compliance.md-Fehler:\n" + "\n".join(fehler)


def test_alle_modul_md_valide(phasen_dir: Path) -> None:
    fehler: list[str] = []
    for modul_md in sorted(phasen_dir.glob("*/modul.md")):
        b = validiere_modul(modul_md)
        if b.fehler:
            fehler.extend(f"{modul_md.relative_to(phasen_dir)}: {e}" for e in b.fehler)
    assert not fehler, "modul.md-Fehler:\n" + "\n".join(fehler)
