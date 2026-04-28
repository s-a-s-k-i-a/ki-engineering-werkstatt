# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "marimo",
#   "pyyaml>=6.0",
# ]
# ///

"""Audit-Logging-Skelett nach AI-Act Art. 12 — minimaler Prototyp.

Strukturierte Logs in JSON-Lines pro KI-Aufruf. In Produktion ersetzt
durch OpenTelemetry GenAI + Phoenix/Langfuse — siehe `infrastruktur/observability/`.
"""

import marimo

__generated_with = "0.10.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    mo.md(
        r"""
        # Audit-Logging nach AI-Act Art. 12

        Pflicht für Hochrisiko-Systeme: jeder Aufruf wird so geloggt, dass
        nachvollziehbar ist, wer/was/wann/womit/warum.

        Mindestfelder:

        - Zeitstempel (ISO 8601 UTC)
        - User-ID (pseudonymisiert!)
        - Modell-ID + Version
        - Prompt-Hash (SHA-256, NICHT Plaintext)
        - Output-Hash
        - Tool-Calls (welche, mit welchen Argumenten)
        - Latenz, Token-Anzahl, Kosten

        > **Wichtig**: Der Plaintext-Prompt darf in der Regel **nicht** geloggt werden — er kann personenbezogene Daten enthalten. Hashes erfüllen Audit-Pflicht ohne Datenschutz-Verstoß.
        """
    )
    return


@app.cell
def _():
    """Strukturierter Logger als JSON-Lines."""
    import datetime as dt
    import hashlib
    import json
    import time
    import uuid
    from dataclasses import asdict, dataclass, field

    @dataclass
    class AuditEintrag:
        timestamp: str
        request_id: str
        user_pseudonym: str
        model: str
        model_version: str
        prompt_sha256: str
        output_sha256: str
        tool_calls: list[dict] = field(default_factory=list)
        input_tokens: int | None = None
        output_tokens: int | None = None
        latency_ms: float | None = None
        cost_eur: float | None = None
        risiko_klasse: str = "minimal"  # aus model-card.yaml

        def to_jsonl(self) -> str:
            return json.dumps(asdict(self), ensure_ascii=False)

    def hash_str(s: str) -> str:
        return hashlib.sha256(s.encode("utf-8")).hexdigest()[:16]

    def pseudonymize(user_id: str, salt: str = "wechselbar") -> str:
        return hashlib.sha256(f"{salt}::{user_id}".encode()).hexdigest()[:12]

    def log_aufruf(
        user_id: str,
        prompt: str,
        output: str,
        model: str = "Pharia-1-LLM-7B-control",
        model_version: str = "2026-04",
        tool_calls: list[dict] | None = None,
    ) -> AuditEintrag:
        return AuditEintrag(
            timestamp=dt.datetime.now(dt.UTC).isoformat(),
            request_id=str(uuid.uuid4()),
            user_pseudonym=pseudonymize(user_id),
            model=model,
            model_version=model_version,
            prompt_sha256=hash_str(prompt),
            output_sha256=hash_str(output),
            tool_calls=tool_calls or [],
        )

    return AuditEintrag, hash_str, log_aufruf, pseudonymize, time


@app.cell
def _(log_aufruf, mo, time):
    """Demo-Logging eines Charity-Adoptions-Bot-Aufrufs."""
    start = time.perf_counter()
    eintrag = log_aufruf(
        user_id="user-12345@example.de",
        prompt="Wie kann ich einen Hund aus dem deutsche Tierschutz-Organisation adoptieren?",
        output=(
            "Du kannst dich beim Tierschutzverein Hannover in Burgwedel melden. "
            "Vorab gibt es ein Beratungsgespräch und Hausbesuch."
        ),
        tool_calls=[{"tool": "termin-frei", "args": {"woche": 18}, "result_type": "list[Termin]"}],
    )
    eintrag.latency_ms = (time.perf_counter() - start) * 1000
    eintrag.input_tokens = 18
    eintrag.output_tokens = 32
    eintrag.cost_eur = round((eintrag.input_tokens * 5 + eintrag.output_tokens * 10) / 1_000_000, 6)
    eintrag.risiko_klasse = "begrenzt"
    mo.md(
        f"### Audit-Log-Eintrag\n```json\n{eintrag.to_jsonl()}\n```\n\n"
        f"**Plaintext-Prompt**: NICHT geloggt — nur Hash `{eintrag.prompt_sha256}`."
    )
    return (eintrag,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Aufbewahrung

        - **Mindestens 6 Monate** für AI-Act-Hochrisiko-Systeme (Art. 12 Abs. 3)
        - **Dokumentations-Pflicht**: 10 Jahre für Konformitätsbewertung (Art. 18)
        - **DSGVO**: Logs sind selbst Verarbeitung — eigene Rechtsgrundlage + Löschfrist (z. B. 12 Monate)

        ### Production-Migration

        Für echte Workloads: OpenTelemetry GenAI Semantic Conventions + Phoenix oder Langfuse.

        ```yaml
        # infrastruktur/observability/otel-collector.yml
        receivers:
          otlp:
            protocols: { grpc: { endpoint: 0.0.0.0:4317 } }
        exporters:
          phoenix:
            endpoint: http://phoenix:6006
        ```

        ### Quellen

        - [AI Act Art. 12 (Logging)](https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:32024R1689)
        - [OpenTelemetry GenAI Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/)
        - [Arize Phoenix](https://phoenix.arize.com/)
        - [Langfuse](https://langfuse.com/)
        """
    )
    return


if __name__ == "__main__":
    app.run()
