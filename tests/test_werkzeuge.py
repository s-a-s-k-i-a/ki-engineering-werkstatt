"""Smoke-Tests für die CLI-Werkzeuge."""

from __future__ import annotations

import json
from pathlib import Path

from click.testing import CliRunner

from werkzeuge.ai_act_classifier import Risikostufe, klassifiziere
from werkzeuge.ai_act_classifier import main as ai_act_main
from werkzeuge.ai_txt_generator import main as ai_txt_main
from werkzeuge.ai_txt_generator import render_ai_txt, render_robots_txt

# ---------- ai_act_classifier ----------


def test_inakzeptabel_social_scoring() -> None:
    karte = {
        "name": "TestSystem",
        "risiko_indikatoren": {"social-scoring": True},
    }
    befund = klassifiziere(karte)
    assert befund.risiko == Risikostufe.INAKZEPTABEL
    assert any("Social Scoring" in b for b in befund.begruendung)


def test_hochrisiko_kreditscoring() -> None:
    karte = {
        "name": "Kreditscoring-Bot",
        "use_case_kategorien": ["wesentliche-private-dienste"],
    }
    befund = klassifiziere(karte)
    assert befund.risiko == Risikostufe.HOCHRISIKO
    assert any("Konformitätsbewertung" in p for p in befund.pflichten)


def test_begrenzt_chatbot() -> None:
    karte = {"name": "FAQ-Bot", "transparenz_trigger": ["chatbot"]}
    befund = klassifiziere(karte)
    assert befund.risiko == Risikostufe.BEGRENZT


def test_minimal_keine_indikatoren() -> None:
    karte = {"name": "Spam-Filter"}
    befund = klassifiziere(karte)
    assert befund.risiko == Risikostufe.MINIMAL
    assert any("AI Literacy" in p for p in befund.pflichten)


def test_gpai_systemic_flops_threshold() -> None:
    karte = {
        "name": "Mega-LLM",
        "ist_gpai": True,
        "training_compute_flops": 2 * 10**25,
    }
    befund = klassifiziere(karte)
    assert befund.risiko == Risikostufe.GPAI_SYSTEMIC


def test_ai_act_cli_rendert_minimal(tmp_path: Path) -> None:
    karte = tmp_path / "karte.yaml"
    karte.write_text("name: Spam-Filter\nrisiko_indikatoren: {}\n", encoding="utf-8")
    runner = CliRunner()
    res = runner.invoke(ai_act_main, ["--modell-karte", str(karte)])
    assert res.exit_code == 0, res.output
    assert "MINIMAL" in res.output


def test_ai_act_cli_json_output(tmp_path: Path) -> None:
    karte = tmp_path / "karte.yaml"
    karte.write_text(
        "name: Test\nrisiko_indikatoren: {social-scoring: true}\n",
        encoding="utf-8",
    )
    runner = CliRunner()
    res = runner.invoke(ai_act_main, ["--modell-karte", str(karte), "--als-json"])
    assert res.exit_code == 2  # exit-2 bei inakzeptabel — wir wollen das festhalten
    data = json.loads(res.output)
    assert data["risiko"] == "inakzeptabel"


# ---------- ai_txt_generator ----------


def test_ai_txt_enthaelt_pflicht_crawler() -> None:
    text = render_ai_txt("example.de", "2026-04-27")
    for c in ["GPTBot", "ClaudeBot", "CCBot", "Google-Extended"]:
        assert c in text


def test_robots_txt_hat_sitemap_wenn_gegeben() -> None:
    text = render_robots_txt("example.de", "https://example.de/sitemap.xml")
    assert "Sitemap: https://example.de/sitemap.xml" in text


def test_ai_txt_cli_schreibt_dateien(tmp_path: Path) -> None:
    runner = CliRunner()
    res = runner.invoke(
        ai_txt_main,
        ["--domain", "example.de", "-o", str(tmp_path)],
    )
    assert res.exit_code == 0, res.output
    assert (tmp_path / "ai.txt").exists()
    assert (tmp_path / "robots.txt").exists()


# ---------- compliance_lint (Schema) ----------


def test_compliance_lint_compliance_md_ok(tmp_path: Path) -> None:
    from werkzeuge.compliance_lint import validiere_compliance

    md = tmp_path / "compliance.md"
    md.write_text(
        """---
id: 13
phase: 13-rag-tiefenmodul
stand: 2026-04-27
anker:
  - quellen-attribution
dsgvo_artikel:
  - art-5-abs-1-lit-b
ai_act_artikel:
  - art-50-abs-4
---

Inhalt.
""",
        encoding="utf-8",
    )
    befund = validiere_compliance(md)
    assert not befund.fehler, befund.fehler


def test_compliance_lint_modul_md_minimal(tmp_path: Path) -> None:
    from werkzeuge.compliance_lint import validiere_modul

    md = tmp_path / "modul.md"
    md.write_text(
        """---
id: 5
titel: Deutsche Tokenizer
dauer_stunden: 6
schwierigkeit: mittel
stand: 2026-04-27
lernziele:
  - Tokenizer auswählen
  - Token-Effizienz messen
  - Kosten in EUR berechnen
---

Inhalt.
""",
        encoding="utf-8",
    )
    befund = validiere_modul(md)
    assert not befund.fehler, befund.fehler


def test_compliance_lint_findet_fehlendes_pflichtfeld(tmp_path: Path) -> None:
    from werkzeuge.compliance_lint import validiere_compliance

    md = tmp_path / "compliance.md"
    md.write_text(
        """---
id: 13
phase: 13-rag-tiefenmodul
---

Ohne stand/anker.
""",
        encoding="utf-8",
    )
    befund = validiere_compliance(md)
    assert any("stand" in f for f in befund.fehler)
    assert any("anker" in f for f in befund.fehler)
