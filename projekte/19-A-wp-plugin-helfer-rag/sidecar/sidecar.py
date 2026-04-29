# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "fastapi>=0.115",
#   "uvicorn>=0.32",
#   "pydantic>=2.9",
#   "httpx>=0.27",
# ]
# ///

"""Python-Sidecar für KI-Plugin-Helfer RAG.

FastAPI-Service, der vom WordPress-Plugin via REST aufgerufen wird:

- POST /frage → RAG-basierte Antwort aus Plugin-Doku / Code / Issues
- GET  /health → Lebenszeichen + Konfigurations-Hint

Smoke-test-tauglich ohne Qdrant / vLLM (Stub-Modus, wenn Env-Vars fehlen).
Production: Qdrant via QDRANT_URL, LLM via LLM_BACKEND (ollama|vllm|openai-compatible).
"""

from __future__ import annotations

import hashlib
import logging
import os
import sys
from typing import Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("wphr-sidecar")

# Konfiguration aus Umgebungsvariablen — keine hardcoded Secrets.
QDRANT_URL = os.environ.get("QDRANT_URL", "")  # leer = Stub-Modus
LLM_BACKEND = os.environ.get("LLM_BACKEND", "stub")  # stub | ollama | vllm | openai
LLM_BASE_URL = os.environ.get("LLM_BASE_URL", "http://localhost:11434")
LLM_MODEL = os.environ.get("LLM_MODEL", "llama3.3:8b")
LLM_API_KEY = os.environ.get("LLM_API_KEY", "")
PLUGIN_REPO_PATH = os.environ.get("PLUGIN_REPO_PATH", "/data/plugins")

app = FastAPI(
    title="KI-Plugin-Helfer Sidecar",
    version="0.1.0",
    description="RAG-Sidecar für WP-Plugin-Helfer — DSGVO-konform, EU-self-hosted.",
)


class FrageRequest(BaseModel):
    frage: str = Field(min_length=3, max_length=2000)
    kontext: Literal["doku", "code", "issue"] = "doku"


class Quelle(BaseModel):
    datei: str
    ausschnitt: str
    score: float = Field(ge=0.0, le=1.0)


class FrageAntwort(BaseModel):
    antwort: str
    quellen: list[Quelle] = Field(default_factory=list)
    konfidenz: float = Field(ge=0.0, le=1.0)
    backend: str
    request_hash: str  # SHA-Hash der Frage für Audit-Trail (kein Klartext)


@app.get("/health")
def health() -> dict:
    """Lebenszeichen + Konfigurations-Hint für Plugin-Settings-Seite."""
    return {
        "status": "ok",
        "version": "0.1.0",
        "qdrant_konfiguriert": bool(QDRANT_URL),
        "llm_backend": LLM_BACKEND,
        "llm_modell": LLM_MODEL,
    }


@app.post("/frage")
def frage(req: FrageRequest) -> FrageAntwort:
    """Hauptendpoint — leitet je nach Kontext an Sub-Pipeline."""
    request_hash = hashlib.sha256(req.frage.encode("utf-8")).hexdigest()[:16]
    log.info("frage(kontext=%s, hash=%s)", req.kontext, request_hash)

    if LLM_BACKEND == "stub" or not QDRANT_URL:
        return _stub_antwort(req, request_hash)

    if req.kontext == "doku":
        return _doku_rag(req, request_hash)
    if req.kontext == "code":
        return _code_search(req, request_hash)
    if req.kontext == "issue":
        return _issue_triage(req, request_hash)

    raise HTTPException(400, f"unbekannter kontext: {req.kontext}")


def _stub_antwort(req: FrageRequest, request_hash: str) -> FrageAntwort:
    """Stub-Modus: deterministische Demo-Antwort ohne externe Calls.

    Wird aktiv, wenn QDRANT_URL leer oder LLM_BACKEND="stub" — sodass das
    Plugin auch ohne aufwändigen GPU-Stack lokal getestet werden kann.
    """
    return FrageAntwort(
        antwort=(
            f"[STUB] Frage zu Kontext '{req.kontext}' empfangen. "
            "Setze QDRANT_URL und LLM_BACKEND in der Sidecar-Umgebung, "
            "um echte RAG-Antworten zu bekommen."
        ),
        quellen=[
            Quelle(
                datei="DEMO/readme.txt",
                ausschnitt="Demo-Inhalt — ersetze durch echten Plugin-Korpus.",
                score=0.42,
            )
        ],
        konfidenz=0.5,
        backend="stub",
        request_hash=request_hash,
    )


def _doku_rag(req: FrageRequest, request_hash: str) -> FrageAntwort:
    """Plugin-Doku-RAG — Suche in indizierter Doku via Qdrant + LLM-Generierung."""
    chunks = _qdrant_search(req.frage, collection="plugin_doku", k=5)
    antwort_text = _llm_generate(
        prompt=_build_doku_prompt(req.frage, chunks),
        max_tokens=512,
    )
    return FrageAntwort(
        antwort=antwort_text,
        quellen=[Quelle(**c) for c in chunks],
        konfidenz=_durchschnitts_konfidenz(chunks),
        backend=LLM_BACKEND,
        request_hash=request_hash,
    )


def _code_search(req: FrageRequest, request_hash: str) -> FrageAntwort:
    """Code-Search — AST-Splitting + Vektor-Suche (Stub bis 0.2.0)."""
    chunks = _qdrant_search(req.frage, collection="plugin_code", k=5)
    antwort_text = _llm_generate(
        prompt=_build_code_prompt(req.frage, chunks),
        max_tokens=400,
    )
    return FrageAntwort(
        antwort=antwort_text,
        quellen=[Quelle(**c) for c in chunks],
        konfidenz=_durchschnitts_konfidenz(chunks),
        backend=LLM_BACKEND,
        request_hash=request_hash,
    )


def _issue_triage(req: FrageRequest, request_hash: str) -> FrageAntwort:
    """Issue-Triage — Klassifikation + Code-Stelle (Stub bis 0.2.0)."""
    return FrageAntwort(
        antwort=(
            "[Stub bis 0.2.0] Issue-Triage erfordert GitHub-App-Integration. "
            "Geplant: Webhook-Empfang + Klassifikation + Bot-Kommentar."
        ),
        quellen=[],
        konfidenz=0.0,
        backend="not_implemented",
        request_hash=request_hash,
    )


# ---------------------------------------------------------------------------
# Helpers (smoke-test-tauglich, ohne externe Dependencies)
# ---------------------------------------------------------------------------


def _qdrant_search(frage: str, *, collection: str, k: int = 5) -> list[dict]:
    """Stub-Suche, bis Qdrant-Client integriert ist (0.1.x → 0.2.0).

    Echte Variante: from qdrant_client import QdrantClient
        client = QdrantClient(url=QDRANT_URL)
        result = client.search(collection_name=collection, query_vector=embed(frage), limit=k)
    """
    return [
        {
            "datei": f"{collection}/example-1.md",
            "ausschnitt": f"[Stub] Beispiel-Treffer für: {frage[:80]}",
            "score": 0.78,
        },
    ]


def _llm_generate(*, prompt: str, max_tokens: int = 400) -> str:
    """Stub-Generierung — echter Code spricht Ollama / vLLM / OpenAI-kompatibel an.

    Production-Skizze (Ollama):
        client = httpx.Client(base_url=LLM_BASE_URL)
        r = client.post("/api/generate", json={"model": LLM_MODEL, "prompt": prompt})
        return r.json()["response"]
    """
    return f"[Stub-LLM-Antwort, max_tokens={max_tokens}] Prompt-Anfang: {prompt[:120]}…"


def _build_doku_prompt(frage: str, chunks: list[dict]) -> str:
    quellen_text = "\n\n".join(
        f"--- Quelle {i + 1} ({c['datei']}) ---\n{c['ausschnitt']}" for i, c in enumerate(chunks)
    )
    return (
        "Du beantwortest Fragen zu einem WordPress-Plugin auf Deutsch. "
        "Nutze NUR die folgenden Quellen — wenn die Antwort nicht aus den Quellen ableitbar ist, "
        "sag es explizit.\n\n"
        f"FRAGE: {frage}\n\n"
        f"QUELLEN:\n{quellen_text}\n\n"
        "ANTWORT:"
    )


def _build_code_prompt(frage: str, chunks: list[dict]) -> str:
    code_text = "\n\n".join(f"--- {c['datei']} ---\n{c['ausschnitt']}" for c in chunks)
    return (
        "Du bist ein Code-Search-Assistent für PHP/WordPress-Plugins. "
        "Beantworte die Frage mit konkreten Code-Stellen aus den Quellen.\n\n"
        f"FRAGE: {frage}\n\n"
        f"CODE-AUSZÜGE:\n{code_text}\n\n"
        "ANTWORT:"
    )


def _durchschnitts_konfidenz(chunks: list[dict]) -> float:
    if not chunks:
        return 0.0
    return sum(c.get("score", 0.0) for c in chunks) / len(chunks)


# ---------------------------------------------------------------------------
# Smoke-Test (wenn direkt mit `python sidecar.py test` gestartet)
# ---------------------------------------------------------------------------


def _smoke_test() -> int:
    """Minimal-Selbsttest — wird vom CI-Runner aufgerufen."""
    health_resp = health()
    assert health_resp["status"] == "ok"

    req = FrageRequest(frage="Wie registriere ich einen WP-Hook?", kontext="doku")
    resp = frage(req)
    assert resp.backend in {"stub", LLM_BACKEND}
    assert resp.request_hash
    assert 0.0 <= resp.konfidenz <= 1.0

    print("✅ Sidecar Smoke-Test grün")
    return 0


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        sys.exit(_smoke_test())
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", "8765")))
