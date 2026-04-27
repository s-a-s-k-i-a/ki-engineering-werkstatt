"""Smoke-Tests für die Repo-Grundstruktur — laufen ohne uv-Extras."""

from __future__ import annotations

from pathlib import Path

PFLICHT_DATEIEN = [
    "README.md",
    "LICENSE",
    "NOTICE",
    "CHANGELOG.md",
    "SECURITY.md",
    "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md",
    "GOVERNANCE.md",
    "CITATION.cff",
    "pyproject.toml",
    "marimo.toml",
    "justfile",
    ".editorconfig",
    ".python-version",
    ".gitignore",
    ".gitattributes",
    ".env.example",
    "ai.txt",
    "robots.txt",
    ".pre-commit-config.yaml",
    ".markdownlint.json",
    "ROADMAP.md",
]

PFLICHT_VERZEICHNISSE = [
    "phasen",
    "docs",
    "docs/lernpfade",
    "docs/rechtliche-perspektive",
    "docs/assets",
    "datasets",
    "datasets/samples",
    "datasets/manifests",
    "datasets/lizenzen",
    "infrastruktur",
    "infrastruktur/eu-modelle",
    "werkzeuge",
    "tests",
    ".github",
    ".github/workflows",
    ".github/ISSUE_TEMPLATE",
]

ERWARTETE_PHASEN = [
    "00-werkzeugkasten",
    "01-mathematik-grundlagen",
    "02-klassisches-ml",
    "03-deep-learning-grundlagen",
    "04-computer-vision",
    "05-deutsche-tokenizer",
    "06-sprache-und-audio",
    "07-transformer-architektur",
    "08-generative-modelle",
    "09-state-space-und-hybride",
    "10-llm-von-null",
    "11-llm-engineering",
    "12-finetuning-und-adapter",
    "13-rag-tiefenmodul",
    "14-agenten-und-mcp",
    "15-autonome-systeme",
    "16-reasoning-und-test-time",
    "17-production-und-eu-hosting",
    "18-ethik-safety-alignment",
    "19-abschlussprojekte",
    "20-recht-und-governance",
]

ERWARTETE_WORKFLOWS = [
    "lint.yml",
    "typecheck.yml",
    "notebooks-build.yml",
    "notebooks-smoke.yml",
    "link-check.yml",
    "secrets-scan.yml",
    "compliance-check.yml",
    "release.yml",
]


def test_pflicht_dateien_existieren(repo_root: Path) -> None:
    fehlend = [f for f in PFLICHT_DATEIEN if not (repo_root / f).exists()]
    assert not fehlend, f"Fehlende Pflicht-Dateien: {fehlend}"


def test_pflicht_verzeichnisse_existieren(repo_root: Path) -> None:
    fehlend = [d for d in PFLICHT_VERZEICHNISSE if not (repo_root / d).is_dir()]
    assert not fehlend, f"Fehlende Pflicht-Verzeichnisse: {fehlend}"


def test_alle_phasen_vorhanden(phasen_dir: Path) -> None:
    vorhanden = sorted(p.name for p in phasen_dir.iterdir() if p.is_dir())
    fehlend = [p for p in ERWARTETE_PHASEN if p not in vorhanden]
    assert not fehlend, f"Fehlende Phasen: {fehlend}"


def test_jede_phase_hat_modul_md(phasen_dir: Path) -> None:
    fehlend = [p.name for p in phasen_dir.iterdir() if p.is_dir() and not (p / "modul.md").exists()]
    assert not fehlend, f"Phasen ohne modul.md: {fehlend}"


def test_jede_phase_hat_compliance_md(phasen_dir: Path) -> None:
    fehlend = [
        p.name for p in phasen_dir.iterdir() if p.is_dir() and not (p / "compliance.md").exists()
    ]
    assert not fehlend, f"Phasen ohne compliance.md: {fehlend}"


def test_alle_workflows_existieren(repo_root: Path) -> None:
    wf_dir = repo_root / ".github" / "workflows"
    fehlend = [w for w in ERWARTETE_WORKFLOWS if not (wf_dir / w).exists()]
    assert not fehlend, f"Fehlende Workflows: {fehlend}"


def test_keine_geheimnisse_im_env_example(repo_root: Path) -> None:
    """`.env.example` darf NIE echte Werte enthalten."""
    text = (repo_root / ".env.example").read_text(encoding="utf-8")
    for line in text.splitlines():
        if "=" in line and not line.startswith("#"):
            key, _, val = line.partition("=")
            if val.strip() and not val.strip().startswith(("http", "INFO", "ki-")):
                pytest.fail(f"`.env.example` hat einen Wert für {key}: {val!r}")


def test_ai_txt_blockiert_kern_crawler(repo_root: Path) -> None:
    text = (repo_root / "ai.txt").read_text(encoding="utf-8")
    pflicht_crawler = [
        "GPTBot",
        "ClaudeBot",
        "Google-Extended",
        "CCBot",
        "PerplexityBot",
        "anthropic-ai",
    ]
    fehlend = [c for c in pflicht_crawler if c not in text]
    assert not fehlend, f"ai.txt blockt nicht: {fehlend}"


# pytest-Import-Stub für `pytest.fail` in einzelnen Tests
import pytest  # noqa: E402
