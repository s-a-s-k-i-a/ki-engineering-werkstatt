# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "marimo",
#   "pydantic>=2.9",
# ]
# ///

"""WP-Plugin-Helfer-RAG Stub — Marimo-Notebook für Capstone 19.A.

Smoke-Test-tauglich: keine externen API-Calls, keine Qdrant-Abhängigkeit.
Stub-Pipeline zeigt Architektur-Pattern. Vollversion siehe README.md.
"""

import marimo

__generated_with = "0.23.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    mo.md(
        r"""
        # 🔌 WP-Plugin-Helfer-RAG · Capstone 19.A

        Stub-Architektur eines multilingualen Plugin-Doku-RAG-Systems mit:

        - **Doku-Agent** (Markdown-RAG)
        - **Code-Agent** (PHP-AST-RAG)
        - **Issue-Agent** (GitHub-Issue-Triage)

        Smoke-Test-tauglich (keine externen Calls). Vollversion siehe README.md
        und Lektionen 11/13/14/17.
        """
    )
    return


@app.cell
def _():
    """Pydantic-Schemas."""
    from typing import Literal

    from pydantic import BaseModel, Field

    class WPHelferAntwort(BaseModel):
        typ: Literal["doku", "code", "issue", "unklar"]
        antwort: str = Field(min_length=10, max_length=4000)
        quellen: list[dict]
        konfidenz: float = Field(ge=0.0, le=1.0)
        used_agent: str

    class IssueLabel(BaseModel):
        label: Literal["bug", "feature", "docs", "question", "duplicate"]
        priority: Literal["low", "medium", "high", "critical"]
        relevante_dateien: list[str]
        schritt_1: str = Field(min_length=10, max_length=300)

    class CodeChunk(BaseModel):
        datei: str
        funktion_oder_klasse: str
        line_start: int
        line_end: int
        snippet: str = Field(max_length=500)

    return CodeChunk, IssueLabel, WPHelferAntwort


@app.cell
def _(CodeChunk, IssueLabel, WPHelferAntwort):
    """Stub-Sub-Agents."""

    def stub_doku_agent(frage: str) -> WPHelferAntwort:
        """Stub: simuliert RAG-Antwort auf Plugin-Doku."""
        return WPHelferAntwort(
            typ="doku",
            antwort=(
                "Um das Feature zu aktivieren, gehe in Plugin-Settings → "
                "Allgemein → Aktivierungs-Schalter. Dort kannst du auch die "
                "API-Keys hinterlegen."
            ),
            quellen=[
                {
                    "datei": "docs/installation.md",
                    "abschnitt": "Aktivierung",
                    "score": 0.92,
                },
                {
                    "datei": "docs/api-referenz.md",
                    "abschnitt": "Setup",
                    "score": 0.78,
                },
            ],
            konfidenz=0.85,
            used_agent="doku",
        )

    def stub_code_agent(query: str) -> WPHelferAntwort:
        """Stub: simuliert Code-Suche auf PHP-Source."""
        chunks = [
            CodeChunk(
                datei="src/admin/SettingsPage.php",
                funktion_oder_klasse="enqueue_admin_scripts",
                line_start=42,
                line_end=58,
                snippet=("function enqueue_admin_scripts() {\n    wp_enqueue_script(...);\n}"),
            ),
        ]
        return WPHelferAntwort(
            typ="code",
            antwort=(
                f"`wp_enqueue_scripts` wird in {len(chunks)} Stellen verwendet. "
                "Hauptverwendung in admin/SettingsPage.php Zeile 42–58."
            ),
            quellen=[c.model_dump() for c in chunks],
            konfidenz=0.91,
            used_agent="code",
        )

    def stub_issue_agent(issue_text: str) -> WPHelferAntwort:
        """Stub: simuliert Issue-Triage."""
        label = IssueLabel(
            label="bug",
            priority="medium",
            relevante_dateien=[
                "src/frontend/Hooks.php",
                "src/api/RestController.php",
            ],
            schritt_1=("Reproduziere Bug lokal mit WP-Test-Setup, dann hooks.php Z. 120 prüfen."),
        )
        return WPHelferAntwort(
            typ="issue",
            antwort=(
                f"Klassifikation: {label.label} (Priorität: {label.priority}). "
                f"Relevante Dateien: {', '.join(label.relevante_dateien)}. "
                f"Empfohlener erster Schritt: {label.schritt_1}"
            ),
            quellen=[label.model_dump()],
            konfidenz=0.78,
            used_agent="issue",
        )

    return stub_code_agent, stub_doku_agent, stub_issue_agent


@app.cell
def _(WPHelferAntwort, stub_code_agent, stub_doku_agent, stub_issue_agent):
    """Supervisor-Routing."""

    def supervisor_route(anfrage: str) -> WPHelferAntwort:
        """Naive Routing-Heuristik (in Production: LLM-Klassifikator)."""
        a = anfrage.lower()
        if any(k in a for k in ["bug", "fehler", "crash", "error", "problem"]):
            return stub_issue_agent(anfrage)
        if any(k in a for k in ["code", "funktion", "klasse", "hook", "method"]):
            return stub_code_agent(anfrage)
        if any(k in a for k in ["wie", "anleitung", "doku", "feature"]):
            return stub_doku_agent(anfrage)
        return WPHelferAntwort(
            typ="unklar",
            antwort="Konnte Anfrage nicht klassifizieren. Bitte präzisiere.",
            quellen=[],
            konfidenz=0.2,
            used_agent="none",
        )

    return (supervisor_route,)


@app.cell
def _(mo, supervisor_route):
    """Test mit 5 Beispiel-Anfragen."""
    test_anfragen = [
        "Wie aktiviere ich das Plugin-Feature?",
        "Wo wird wp_enqueue_scripts im Code verwendet?",
        "Bug: Plugin crasht beim Speichern, Fehlermeldung 'Class not found'",
        "Welche Hooks bietet das Plugin?",
        "Anleitung zur Installation auf Multisite",
    ]

    rows = []
    for anfrage in test_anfragen:
        r = supervisor_route(anfrage)
        rows.append(
            f"| {anfrage[:55]}{'...' if len(anfrage) > 55 else ''} | "
            f"**{r.typ}** | {r.used_agent} | {r.konfidenz:.2f} | "
            f"{len(r.quellen)} |"
        )

    mo.md(
        "## Test-Anfragen + Routing\n\n"
        "| Anfrage | Typ | Agent | Konfidenz | Quellen |\n"
        "|---|---|---|---|---|\n" + "\n".join(rows)
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Architektur-Hinweise

        Drei Sub-Agents über Supervisor-Pattern (siehe Phase 14.07):

        - **Doku-Agent**: RAG auf Markdown-Dateien mit `multilingual-e5-large`
        - **Code-Agent**: PHP-AST-Splitting via `tree-sitter-php` + Embedding
        - **Issue-Agent**: Klassifikator + Code-Suche über Code-Agent

        ## Vollversion-Wegweiser

        ```python
        from pydantic_ai import Agent
        from pydantic_ai.mcp import MCPServerStdio

        # Sub-Agents als echte Pydantic-AI-Agents
        doku_agent = Agent("anthropic:claude-haiku-4-5", output_type=...)
        code_agent = Agent("anthropic:claude-haiku-4-5", output_type=...)
        issue_agent = Agent(
            "anthropic:claude-sonnet-4-6",  # stärker für Klassifikation
            output_type=IssueLabel,
            toolsets=[MCPServerStdio("uv", ["run", "python", "github_mcp.py"])],
        )

        supervisor = Agent("anthropic:claude-sonnet-4-6", output_type=WPHelferAntwort)
        ```

        ## DSGVO-Compliance

        - **AVV** mit Anthropic Enterprise (München-Office) signiert
        - **PII-Filter** auf Issue-Texten (Email, Namen pseudonymisieren)
        - **Audit-Logging** via Phoenix (Phase 17.08)
        - **Drittland-Vermeidung** via STACKIT-vLLM oder Pharia-1

        ## Quellen

        - Pydantic AI Multi-Agent — <https://ai.pydantic.dev/multi-agent/>
        - Qdrant — <https://qdrant.tech/>
        - tree-sitter-php — <https://github.com/tree-sitter/tree-sitter-php>
        - multilingual-e5-large — <https://huggingface.co/intfloat/multilingual-e5-large>

        ## Verwandte Phasen

        - **Phase 11** (Pydantic AI Foundation)
        - **Phase 13** (RAG-Tiefenmodul)
        - **Phase 14** (Agenten + MCP)
        - **Phase 17** (Production EU-Hosting)
        - **Phase 18** (Bias + Self-Censorship)
        - **Phase 20** (Recht & Governance)
        """
    )
    return


if __name__ == "__main__":
    app.run()
