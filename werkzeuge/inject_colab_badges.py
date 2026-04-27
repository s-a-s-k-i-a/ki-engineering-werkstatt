"""Injiziert Colab-Badges in alle Lektions-READMEs, deren Notebook in `code/` liegt."""

from __future__ import annotations

import re
import sys
from pathlib import Path

import click

REPO_ROOT = Path(__file__).resolve().parent.parent
GH_USER = "s-a-s-k-i-a"
GH_REPO = "ki-engineering-werkstatt"
COLAB_BADGE = (
    "[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)]"
    "(https://colab.research.google.com/github/{user}/{repo}/blob/main/{path})"
)
BADGE_MARKER_BEGIN = "<!-- colab-badge:begin -->"
BADGE_MARKER_END = "<!-- colab-badge:end -->"


def finde_lektionen_mit_code() -> list[tuple[Path, list[Path]]]:
    """Liefert (lektions-md, [zugeordnete code/.py-Dateien])."""
    out: list[tuple[Path, list[Path]]] = []
    for lektion_md in (REPO_ROOT / "phasen").rglob("lektionen/*.md"):
        phase_dir = lektion_md.parents[1]
        code_dir = phase_dir / "code"
        if not code_dir.exists():
            continue
        # Heuristik: gleicher Präfix (z.B. 01-vanilla-rag.md → 01_vanilla_rag.py)
        praefix = re.match(r"^(\d+)[-_]", lektion_md.stem)
        if not praefix:
            continue
        nummer = praefix.group(1)
        zugeordnet = sorted(code_dir.glob(f"{nummer}_*.py")) + sorted(
            code_dir.glob(f"{nummer}-*.py")
        )
        if zugeordnet:
            out.append((lektion_md, zugeordnet))
    return out


def render_badge_block(code_pfade: list[Path]) -> str:
    badges = []
    for c in code_pfade:
        rel = c.relative_to(REPO_ROOT).as_posix()
        # Colab erwartet .ipynb — wir verlinken auf den Marimo-Build-Output
        rel_ipynb = rel.replace(".py", ".ipynb").replace("phasen/", "dist-notebooks/phasen/")
        badges.append(COLAB_BADGE.format(user=GH_USER, repo=GH_REPO, path=rel_ipynb))
    return f"{BADGE_MARKER_BEGIN}\n" + "  ".join(badges) + f"\n{BADGE_MARKER_END}"


def update_lektion(md: Path, code_pfade: list[Path], check_only: bool) -> bool:
    """True wenn unverändert, False wenn Update nötig (oder gemacht)."""
    text = md.read_text(encoding="utf-8")
    block = render_badge_block(code_pfade)

    if BADGE_MARKER_BEGIN in text and BADGE_MARKER_END in text:
        new_text = re.sub(
            re.escape(BADGE_MARKER_BEGIN) + r".*?" + re.escape(BADGE_MARKER_END),
            block,
            text,
            count=1,
            flags=re.DOTALL,
        )
    else:
        # nach Frontmatter einfügen
        fm_end = re.search(r"^---\n.*?\n---\n", text, re.DOTALL | re.MULTILINE)
        if fm_end:
            i = fm_end.end()
            new_text = text[:i] + "\n" + block + "\n" + text[i:]
        else:
            new_text = block + "\n\n" + text

    if new_text == text:
        return True
    if not check_only:
        md.write_text(new_text, encoding="utf-8")
        click.echo(f"✓ Updated {md.relative_to(REPO_ROOT)}")
    else:
        click.echo(f"✗ Out-of-date {md.relative_to(REPO_ROOT)}", err=True)
    return False


@click.command()
@click.option("--check-only", is_flag=True, help="Fehler bei out-of-date statt zu schreiben")
def main(check_only: bool) -> None:
    """Synchronisiert Colab-Badges in Lektions-READMEs."""
    pairs = finde_lektionen_mit_code()
    if not pairs:
        click.echo("Keine Lektion mit zugeordnetem Notebook — OK")
        return

    out_of_date = 0
    for md, codes in pairs:
        if not update_lektion(md, codes, check_only):
            out_of_date += 1

    click.echo(f"\n{len(pairs)} Lektionen geprüft, {out_of_date} out-of-date.")
    if check_only and out_of_date:
        sys.exit(1)


if __name__ == "__main__":
    main()
