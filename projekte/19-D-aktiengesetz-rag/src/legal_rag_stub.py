# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "marimo",
#   "pydantic>=2.9",
# ]
# ///

"""Aktiengesetz-Rechtsfrage-Beantworter Stub — Capstone 19.D.

Smoke-Test-tauglich: keine echten LLM-Calls, keine Qdrant-Abhängigkeit.
Stub-RAG zeigt Quellen-Attribution + § RDG-Disclaimer-Pattern.
Vollversion siehe README.md.

⚠️ KEIN Rechtsrat. Recherche-Tool gem. § 2 RDG.
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
        # ⚖️ Aktiengesetz-Rechtsfrage-Beantworter · Capstone 19.D

        > ⚠️ **Kein Rechtsrat (§ 2 RDG)**. Recherche-Tool für AktG-Fragen mit
        > Paragraf-genauer Quellen-Attribution.

        Stub-Pipeline:

        - **AktG-Ingestion** (~ 410 Paragrafen)
        - **Hybrid-RAG** (BM25 + Dense)
        - **Pydantic-AI** mit Quellen-Attribution
        - **Reasoning** für Multi-Hop-Fragen

        Smoke-Test-tauglich (keine externen Calls).
        """
    )
    return


@app.cell
def _():
    """Pydantic-Schemas."""
    from typing import Literal

    from pydantic import BaseModel, Field

    class AktGParagraph(BaseModel):
        nummer: str  # z. B. "111", "111a", "111b"
        titel: str
        text: str = Field(max_length=2000)
        url: str

    class RechtsAntwort(BaseModel):
        antwort_kurz: str = Field(min_length=20, max_length=500)
        primaer_paragrafen: list[str]
        rechtsgebiet: Literal[
            "vorstand",
            "aufsichtsrat",
            "hauptversammlung",
            "kapital",
            "verschmelzung",
            "haftung",
            "andere",
        ]
        konfidenz: float = Field(ge=0.0, le=1.0)
        multi_hop: list[dict]
        disclaimer: str

    return AktGParagraph, RechtsAntwort


@app.cell
def _(AktGParagraph):
    """Stub-Korpus mit 5 Beispiel-Paragrafen."""
    aktg_korpus = [
        AktGParagraph(
            nummer="76",
            titel="Leitung der Aktiengesellschaft",
            text="(1) Der Vorstand hat unter eigener Verantwortung die Gesellschaft zu leiten.",
            url="https://www.gesetze-im-internet.de/aktg/__76.html",
        ),
        AktGParagraph(
            nummer="84",
            titel="Bestellung und Abberufung des Vorstands",
            text=(
                "(1) Vorstandsmitglieder bestellt der Aufsichtsrat auf höchstens fünf Jahre. "
                "Eine wiederholte Bestellung oder Verlängerung der Amtszeit, jeweils für höchstens "
                "fünf Jahre, ist zulässig."
            ),
            url="https://www.gesetze-im-internet.de/aktg/__84.html",
        ),
        AktGParagraph(
            nummer="111",
            titel="Aufgaben und Rechte des Aufsichtsrats",
            text=(
                "(1) Der Aufsichtsrat hat die Geschäftsführung zu überwachen. "
                "(2) Der Aufsichtsrat kann die Bücher und Schriften der Gesellschaft einsehen und prüfen."
            ),
            url="https://www.gesetze-im-internet.de/aktg/__111.html",
        ),
        AktGParagraph(
            nummer="116",
            titel="Sorgfaltspflicht und Verantwortlichkeit der Aufsichtsratsmitglieder",
            text=(
                "Für die Sorgfaltspflicht und Verantwortlichkeit der Aufsichtsratsmitglieder gilt "
                "§ 93 sinngemäß über die Verantwortlichkeit der Vorstandsmitglieder."
            ),
            url="https://www.gesetze-im-internet.de/aktg/__116.html",
        ),
        AktGParagraph(
            nummer="171",
            titel="Prüfung des Jahresabschlusses durch den Aufsichtsrat",
            text=(
                "(1) Der Aufsichtsrat hat den Jahresabschluss, den Lagebericht und den Vorschlag "
                "für die Verwendung des Bilanzgewinns zu prüfen."
            ),
            url="https://www.gesetze-im-internet.de/aktg/__171.html",
        ),
    ]
    return (aktg_korpus,)


@app.cell
def _(RechtsAntwort, aktg_korpus):
    """Stub-RAG-Pipeline."""

    rdg_disclaimer = (
        "⚠️ Kein Rechtsrat (§ 2 RDG). Dieses Tool gibt Recherche-Ergebnisse "
        "auf Basis des AktG-Wortlauts. Für rechtsverbindliche Beratung im "
        "konkreten Fall konsultieren Sie bitte zugelassene Anwält:innen."
    )

    def stub_rag(frage: str) -> RechtsAntwort:
        """Stub: naive Keyword-basierte Suche im Korpus."""
        f = frage.lower()
        relevante = []
        for p in aktg_korpus:
            score = 0
            if "aufsichtsrat" in f and "aufsichtsrat" in p.titel.lower():
                score += 2
            if "vorstand" in f and "vorstand" in p.titel.lower():
                score += 2
            if "bestellung" in f and "bestellung" in p.titel.lower():
                score += 1
            if "haftung" in f and "haftung" in p.titel.lower():
                score += 1
            if "jahresabschluss" in f and "jahresabschluss" in p.titel.lower():
                score += 2
            if score > 0:
                relevante.append((p, score))

        relevante.sort(key=lambda x: x[1], reverse=True)
        top3 = [r[0] for r in relevante[:3]]

        # Bestimme Rechtsgebiet
        rechtsgebiet = (
            "aufsichtsrat"
            if "aufsichtsrat" in f
            else "vorstand"
            if "vorstand" in f
            else "hauptversammlung"
            if "hauptversammlung" in f
            else "kapital"
            if "kapital" in f
            else "andere"
        )

        # Multi-Hop-Erkennung (Stub: § 111 + § 116 sind verlinkt)
        multi_hop = []
        if any(p.nummer == "111" for p in top3) and any(p.nummer == "116" for p in top3):
            multi_hop.append(
                {
                    "von": "§ 111 AktG",
                    "auf": "§ 116 AktG",
                    "grund": "Aufsichtsrats-Sorgfalt verweist via § 93 auf Vorstands-Sorgfalt",
                }
            )

        antwort_kurz = (
            (
                f"Relevante Paragrafen: {', '.join(p.nummer for p in top3)}. "
                f"Hauptaussage aus § {top3[0].nummer if top3 else 'AktG'}: "
                f"{top3[0].text[:120] if top3 else 'Keine direkte Antwort gefunden'}..."
            )
            if top3
            else "Keine direkten AktG-Treffer. Bitte präzisiere die Frage."
        )

        return RechtsAntwort(
            antwort_kurz=antwort_kurz,
            primaer_paragrafen=[f"§ {p.nummer} AktG" for p in top3],
            rechtsgebiet=rechtsgebiet,
            konfidenz=min(0.6 + len(top3) * 0.1, 0.9),
            multi_hop=multi_hop,
            disclaimer=rdg_disclaimer,
        )

    return (stub_rag,)


@app.cell
def _(mo, stub_rag):
    """Test mit 5 AktG-Fragen."""
    test_fragen = [
        "Welche Pflichten hat der Aufsichtsrat bei der Bestellung des Vorstands?",
        "Wie lange darf ein Vorstandsvertrag maximal abgeschlossen werden?",
        "Welche Sorgfaltspflicht haben Aufsichtsratsmitglieder?",
        "Was muss der Aufsichtsrat zum Jahresabschluss prüfen?",
        "Welche Multi-Hop-Verweise gibt es zwischen § 111 + § 116 AktG?",
    ]

    rows = []
    for f in test_fragen:
        a = stub_rag(f)
        multi = "✓" if a.multi_hop else "—"
        rows.append(
            f"| {f[:50]}{'...' if len(f) > 50 else ''} | "
            f"{', '.join(a.primaer_paragrafen)} | {a.rechtsgebiet} | "
            f"{a.konfidenz:.2f} | {multi} |"
        )

    mo.md(
        "## Test-Recherche-Anfragen (Stub)\n\n"
        "| Frage | Paragrafen | Rechtsgebiet | Konfidenz | Multi-Hop |\n"
        "|---|---|---|---|---|\n" + "\n".join(rows)
    )
    return


@app.cell
def _(mo, stub_rag):
    """Beispiel-Antwort mit Disclaimer."""
    bsp = stub_rag("Welche Sorgfaltspflicht haben Aufsichtsratsmitglieder?")
    mo.md(
        f"## Beispiel-Antwort\n\n"
        f"**Frage**: Welche Sorgfaltspflicht haben Aufsichtsratsmitglieder?\n\n"
        f"**Antwort (kurz)**: {bsp.antwort_kurz}\n\n"
        f"**Primäre Paragrafen**: {', '.join(bsp.primaer_paragrafen)}\n\n"
        f"**Rechtsgebiet**: {bsp.rechtsgebiet}\n\n"
        f"**Konfidenz**: {bsp.konfidenz:.2f}\n\n"
        f"---\n\n{bsp.disclaimer}"
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Vollversion-Wegweiser

        ```python
        from pydantic_ai import Agent
        from qdrant_client import QdrantClient

        # AktG-Volltext + Beck-Online + BGH-Urteile als Korpus
        client = QdrantClient(url="https://qdrant-eu.example.de", ...)

        # Hybrid-RAG mit BM25 + Dense + bge-reranker-v2-m3
        legal_agent = Agent(
            "anthropic:claude-opus-4-7",  # Reasoning für Multi-Hop
            output_type=RechtsAntwort,
            system_prompt=(
                "Recherche-Assistent für AktG-Fragen. "
                "Paragraf-genaue Zitate. Keine Beratung."
            ),
        )

        @legal_agent.tool_plain
        async def rag_search(query: str, k: int = 5) -> list[dict]:
            return await hybrid_search(query, k=k)
        ```

        ## Compliance-Anker

        - **§ RDG**: Disclaimer pflicht — kein Rechtsrat
        - **AI-Act Art. 50.4**: Quellen-Attribution mit § AktG + URL
        - **AI-Act Anhang III Nr. 8**: möglicherweise Hochrisiko (Justiz)
        - **DSGVO Art. 22**: keine automatisierte Rechtsentscheidung — nur Recherche
        - **DSGVO Art. 32**: TOM mit Audit-Logging + Encryption

        ## Quellen

        - AktG — <https://www.gesetze-im-internet.de/aktg/>
        - BGH-Rechtsprechung — <https://www.bundesgerichtshof.de/>
        - RDG — <https://www.gesetze-im-internet.de/rdg/>
        - AI-Act Art. 50.4 — <https://artificialintelligenceact.eu/article/50/>
        - bge-reranker-v2-m3 — <https://huggingface.co/BAAI/bge-reranker-v2-m3>
        """
    )
    return


if __name__ == "__main__":
    app.run()
