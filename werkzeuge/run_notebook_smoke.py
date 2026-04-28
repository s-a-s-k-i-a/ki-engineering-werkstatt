"""Headless-Smoke-Test für ein einzelnes Marimo-Notebook.

Statt `marimo run --headless` (startet Webserver, terminiert nicht) nutzen wir
`marimo export script` + direkte Python-Ausführung. Das prüft, dass:
1. das Notebook Marimo-valide ist (Export-Schritt)
2. der Code ohne Exception durchläuft (Run-Schritt)

Exit-Code != 0 = Fehler.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

import click

DEFAULT_TIMEOUT = 180  # 3 Min. pro Notebook


@click.command()
@click.argument("notebook", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option("--timeout", default=DEFAULT_TIMEOUT, help="Sekunden bis Abbruch")
def main(notebook: Path, timeout: int) -> None:
    """Smoke-Test: Marimo-Notebook ohne Webserver ausführen."""
    with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as tmp:
        out_path = Path(tmp.name)

    # 1. Export als reguläres Python-Skript
    export_cmd = ["marimo", "export", "script", str(notebook), "-o", str(out_path)]
    try:
        export_res = subprocess.run(
            export_cmd, timeout=timeout, capture_output=True, text=True, check=False
        )
    except subprocess.TimeoutExpired:
        click.echo(f"✗ Export-Timeout nach {timeout}s: {notebook}", err=True)
        sys.exit(124)

    if export_res.returncode != 0:
        click.echo(f"✗ Export-Fehler in {notebook}", err=True)
        click.echo(export_res.stderr, err=True)
        sys.exit(export_res.returncode)

    # 2. Skript direkt ausführen
    run_cmd = [sys.executable, str(out_path)]
    try:
        run_res = subprocess.run(
            run_cmd, timeout=timeout, capture_output=True, text=True, check=False
        )
    except subprocess.TimeoutExpired:
        click.echo(f"✗ Run-Timeout nach {timeout}s: {notebook}", err=True)
        sys.exit(124)
    finally:
        out_path.unlink(missing_ok=True)

    if run_res.returncode != 0:
        click.echo(f"✗ Run-Fehler in {notebook}", err=True)
        click.echo(run_res.stderr, err=True)
        sys.exit(run_res.returncode)

    click.echo(f"✓ {notebook}")


if __name__ == "__main__":
    main()
