"""Generiert ai.txt + robots.txt für TDM-Opt-out nach § 44b UrhG / DSM-Richtlinie Art. 4.

Stand: 2026-04-27. Liste der KI-Crawler wird laufend erweitert.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

import click

KI_CRAWLER = [
    # OpenAI
    "GPTBot",
    "ChatGPT-User",
    "OAI-SearchBot",
    # Anthropic
    "anthropic-ai",
    "Claude-Web",
    "ClaudeBot",
    # Google
    "Google-Extended",
    # Common Crawl (wird von vielen LLMs genutzt)
    "CCBot",
    # Perplexity
    "PerplexityBot",
    "Perplexity-User",
    # ByteDance
    "ByteSpider",
    "Bytedance",
    # Meta
    "FacebookBot",
    "Meta-ExternalAgent",
    "meta-externalagent",
    # Apple
    "Applebot-Extended",
    # Cohere
    "cohere-ai",
    # Diverse
    "Diffbot",
    "ImagesiftBot",
    "omgilibot",
    "Timpibot",
]


def render_ai_txt(domain: str, datum: str, hinweis: str | None = None) -> str:
    parts = [
        "# ai.txt — Text & Data Mining-Vorbehalt nach § 44b UrhG / DSM-Richtlinie Art. 4",
        f"# Domain: {domain}",
        f"# Stand: {datum}",
        "#",
        "# Inhalte dieser Domain dürfen für KI-Training NICHT verwendet werden.",
        "# Dies ist ein maschinenlesbarer Nutzungsvorbehalt nach § 44b Abs. 3 UrhG.",
    ]
    if hinweis:
        parts.append(f"# {hinweis}")
    parts.append("")

    for crawler in KI_CRAWLER:
        parts.append(f"User-agent: {crawler}")
        parts.append("Disallow: /")
        parts.append("")

    return "\n".join(parts).rstrip() + "\n"


def render_robots_txt(domain: str, sitemap: str | None = None) -> str:
    parts = [
        f"# robots.txt — {domain}",
        "# Klassische Such-Crawler dürfen indexieren. KI-Training siehe ai.txt.",
        "",
        "User-agent: *",
        "Allow: /",
        "",
    ]
    for crawler in KI_CRAWLER:
        parts.append(f"User-agent: {crawler}")
        parts.append("Disallow: /")
        parts.append("")
    if sitemap:
        parts.append(f"Sitemap: {sitemap}")
    return "\n".join(parts).rstrip() + "\n"


@click.command()
@click.option("--domain", "-d", required=True, help="Domain-Name (z.B. example.de)")
@click.option(
    "--ausgabe-verzeichnis",
    "-o",
    type=click.Path(file_okay=False, path_type=Path),
    default=None,
    help="Schreibt ai.txt und robots.txt in dieses Verzeichnis (default: stdout)",
)
@click.option("--sitemap", default=None, help="Sitemap-URL für robots.txt")
@click.option("--hinweis", default=None, help="Zusätzlicher Hinweis-Kommentar in ai.txt")
@click.option("--nur-ai-txt", is_flag=True, help="Nur ai.txt ausgeben/schreiben")
@click.option("--nur-robots", is_flag=True, help="Nur robots.txt ausgeben/schreiben")
def main(
    domain: str,
    ausgabe_verzeichnis: Path | None,
    sitemap: str | None,
    hinweis: str | None,
    nur_ai_txt: bool,
    nur_robots: bool,
) -> None:
    """Generiert TDM-Opt-out-Dateien für KI-Crawler."""
    datum = date.today().isoformat()
    ai_txt = render_ai_txt(domain, datum, hinweis)
    robots = render_robots_txt(domain, sitemap)

    if ausgabe_verzeichnis:
        ausgabe_verzeichnis.mkdir(parents=True, exist_ok=True)
        if not nur_robots:
            (ausgabe_verzeichnis / "ai.txt").write_text(ai_txt, encoding="utf-8")
            click.echo(f"✓ {ausgabe_verzeichnis / 'ai.txt'} geschrieben")
        if not nur_ai_txt:
            (ausgabe_verzeichnis / "robots.txt").write_text(robots, encoding="utf-8")
            click.echo(f"✓ {ausgabe_verzeichnis / 'robots.txt'} geschrieben")
    else:
        if not nur_robots:
            click.echo("# === ai.txt ===")
            click.echo(ai_txt)
        if not nur_ai_txt:
            click.echo("# === robots.txt ===")
            click.echo(robots)


if __name__ == "__main__":
    main()
