"""Headless-Smoke-Test für ein einzelnes Marimo-Notebook.

Führt `marimo run --headless` mit Timeout aus. Exit-Code != 0 = Fehler.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import click

DEFAULT_TIMEOUT = 300  # 5 Min. pro Notebook


@click.command()
@click.argument("notebook", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option("--timeout", default=DEFAULT_TIMEOUT, help="Sekunden bis Abbruch")
def main(notebook: Path, timeout: int) -> None:
    """Smoke-Test: Marimo-Notebook headless ausführen."""
    cmd = [
        "marimo",
        "run",
        str(notebook),
        "--headless",
        "--no-token",
    ]
    try:
        res = subprocess.run(
            cmd,
            timeout=timeout,
            capture_output=True,
            text=True,
            check=False,
        )
    except subprocess.TimeoutExpired:
        click.echo(f"✗ Timeout nach {timeout}s: {notebook}", err=True)
        sys.exit(124)

    if res.returncode != 0:
        click.echo(f"✗ Fehler in {notebook}", err=True)
        click.echo(res.stderr, err=True)
        sys.exit(res.returncode)

    click.echo(f"✓ {notebook}")


if __name__ == "__main__":
    main()
