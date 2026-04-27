"""Liefert Repo-Statistik für README-Badges (Module-Coverage, Stand-Datum)."""

from __future__ import annotations

import json
import re
from pathlib import Path

import click

REPO_ROOT = Path(__file__).resolve().parent.parent


def status_einer_phase(phase_dir: Path) -> str:
    """Status: 'ready' wenn lektionen/*.md + code/*.py vorhanden, sonst 'wip' / 'planned'."""
    lektionen = list(phase_dir.glob("lektionen/*.md"))
    code = list(phase_dir.glob("code/*.py"))
    modul = phase_dir / "modul.md"
    if lektionen and code:
        return "ready"
    if modul.exists() and modul.read_text(encoding="utf-8").strip():
        return "wip"
    return "planned"


@click.command()
@click.option("--als-json", is_flag=True, help="JSON für Badges (.github/badge.json)")
def main(als_json: bool) -> None:
    """Zeigt Phasen-Status."""
    phasen_dir = REPO_ROOT / "phasen"
    phasen = sorted(phasen_dir.iterdir())
    counts = {"ready": 0, "wip": 0, "planned": 0}
    detail: list[dict] = []
    for p in phasen:
        if not p.is_dir():
            continue
        m = re.match(r"^(\d{2})-(.+)$", p.name)
        if not m:
            continue
        status = status_einer_phase(p)
        counts[status] += 1
        detail.append({"id": m.group(1), "name": m.group(2), "status": status})

    total = len(detail)
    if als_json:
        badge = {
            "schemaVersion": 1,
            "label": "Module",
            "message": f"{counts['ready']}/{total} ✓",
            "color": "blue" if counts["ready"] >= 3 else "lightgrey",
        }
        click.echo(json.dumps(badge, ensure_ascii=False))
    else:
        click.echo(
            f"Module: {counts['ready']}/{total} ready, {counts['wip']} WIP, {counts['planned']} geplant"
        )
        for d in detail:
            mark = {"ready": "✅", "wip": "🚧", "planned": "⏳"}[d["status"]]
            click.echo(f"  {mark} Phase {d['id']} — {d['name']}")


if __name__ == "__main__":
    main()
