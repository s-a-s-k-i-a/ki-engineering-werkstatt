"""Konvertiert Marimo-`.py`-Notebooks zu `.ipynb` für Colab-Sharing.

Marimo ist source-of-truth (.py committed). .ipynb wird in CI generiert.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import click

REPO_ROOT = Path(__file__).resolve().parent.parent


def finde_notebooks() -> list[Path]:
    """Alle Marimo-`.py` unter `phasen/**/code/` und `phasen/**/loesungen/`."""
    pattern_dirs = ["phasen/*/code", "phasen/*/loesungen"]
    nb: list[Path] = []
    for pattern in pattern_dirs:
        for d in REPO_ROOT.glob(pattern):
            if d.is_dir():
                nb.extend(sorted(d.glob("*.py")))
    return nb


def konvertiere(nb: Path, ziel: Path) -> bool:
    """Marimo .py → .ipynb. True bei Erfolg."""
    ziel.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["marimo", "export", "ipynb", str(nb), "-o", str(ziel)]
    res = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if res.returncode != 0:
        click.echo(f"✗ {nb}: {res.stderr}", err=True)
        return False
    click.echo(f"✓ {nb.relative_to(REPO_ROOT)} → {ziel.relative_to(REPO_ROOT)}")
    return True


@click.command()
@click.option("--check-only", is_flag=True, help="Nur prüfen, dass alle .py Marimo-valide sind")
@click.option(
    "--ziel-verzeichnis",
    "-o",
    type=click.Path(file_okay=False, path_type=Path),
    default=REPO_ROOT / "dist-notebooks",
    help="Wo die .ipynb-Dateien hin sollen",
)
def main(check_only: bool, ziel_verzeichnis: Path) -> None:
    """Baut alle Marimo-Notebooks im Repo zu .ipynb."""
    nb = finde_notebooks()
    if not nb:
        click.echo("Keine Marimo-Notebooks gefunden — OK (nichts zu tun)")
        return

    fehler = 0
    for n in nb:
        if check_only:
            cmd = ["marimo", "check", str(n)]
            res = subprocess.run(cmd, capture_output=True, text=True, check=False)
            if res.returncode != 0:
                click.echo(f"✗ {n}: {res.stderr}", err=True)
                fehler += 1
            else:
                click.echo(f"✓ {n.relative_to(REPO_ROOT)}")
        else:
            rel = n.relative_to(REPO_ROOT)
            ziel = ziel_verzeichnis / rel.with_suffix(".ipynb")
            if not konvertiere(n, ziel):
                fehler += 1

    click.echo(f"\n{len(nb)} Notebooks bearbeitet, {fehler} Fehler.")
    if fehler:
        sys.exit(1)


if __name__ == "__main__":
    main()
