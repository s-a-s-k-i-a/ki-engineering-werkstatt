# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "marimo",
#   "pydantic>=2.9",
# ]
# ///

"""KV-Cache-Kalkulator + Attention-Sizing — Phase 07 Hands-on.

Berechnet:

- KV-Cache-Größe pro Modell × Sequenz-Länge × Precision
- VRAM-Bedarf-Vergleich (GPU-Klassen)
- GQA-Reduktion vs. Full-MHA

Smoke-test-tauglich. Reine Pydantic-/Berechnungs-Logik, kein PyTorch.
Stand 04/2026 für Modell-Parameter (Llama 3.3, Mistral Large 3, Qwen3,
Pharia, GPT-OSS, DeepSeek-V4).
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
        # 🧠 KV-Cache-Kalkulator · Phase 07

        Berechnet **KV-Cache-Größe** und **VRAM-Bedarf** für 2026er-Modelle.

        - Quellen für Architektur-Parameter: jeweilige Modell-Karten und
          Tech-Reports (Stand 29.04.2026)
        - GQA-Faktoren: aus Modell-Konfigurationen
        - GPU-Klassen: H100 (80 GB), H200 (141 GB), B200 (192 GB)

        Stand: 29.04.2026.
        """
    )
    return


@app.cell
def _():
    """Pydantic-Schema für ein Modell."""
    from pydantic import BaseModel, Field

    class Modell(BaseModel):
        name: str
        n_layers: int = Field(ge=1, le=200)
        n_q_heads: int = Field(ge=1, le=128)
        n_kv_heads: int = Field(ge=1, le=128)
        d_head: int = Field(ge=32, le=256)
        gewichte_gb: float = Field(ge=0.5, le=2000.0)
        license: str
        herkunft: str

    return (Modell,)


@app.cell
def _(Modell):
    """Modell-Katalog Stand 29.04.2026.

    Quellen pro Modell:
    - Llama 3.3 70B: meta-llama/Llama-3.3-70B-Instruct (HF Model Card)
    - Mistral Large 3: Mistral Tech Blog 02/2026
    - Qwen3-32B: Qwen Tech Report 03/2026
    - Pharia-1: Aleph Alpha Modell-Karte (post-Cohere-Merger 04/2026)
    - GPT-OSS-120B: OpenAI Open-Weights-Release 11/2025
    - DeepSeek-V4: DeepSeek Tech Report 02/2026
    """
    katalog = [
        Modell(
            name="Llama 3.3 70B",
            n_layers=80,
            n_q_heads=64,
            n_kv_heads=8,
            d_head=128,
            gewichte_gb=140.0,
            license="Llama Community License",
            herkunft="Meta (USA)",
        ),
        Modell(
            name="Mistral Large 3 (123B)",
            n_layers=88,
            n_q_heads=96,
            n_kv_heads=8,
            d_head=128,
            gewichte_gb=246.0,
            license="Mistral Research / kommerziell",
            herkunft="Mistral (FR/EU)",
        ),
        Modell(
            name="Qwen3-32B",
            n_layers=64,
            n_q_heads=32,
            n_kv_heads=8,
            d_head=128,
            gewichte_gb=64.0,
            license="Apache 2.0",
            herkunft="Alibaba (CN)",
        ),
        Modell(
            name="Pharia-1 (post-Cohere)",
            n_layers=27,
            n_q_heads=36,
            n_kv_heads=4,
            d_head=128,
            gewichte_gb=14.0,
            license="Aleph Alpha Community License",
            herkunft="Aleph Alpha + Cohere (DE/CA, post-Merger 04/2026)",
        ),
        Modell(
            name="GPT-OSS-120B",
            n_layers=96,
            n_q_heads=96,
            n_kv_heads=8,
            d_head=128,
            gewichte_gb=240.0,
            license="Apache 2.0",
            herkunft="OpenAI (USA, Open-Weights 11/2025)",
        ),
        Modell(
            name="DeepSeek-V4-Pro (1.6T MoE — aktive 49B)",
            n_layers=61,
            n_q_heads=128,
            n_kv_heads=128,
            d_head=128,
            gewichte_gb=380.0,  # Gesamt-Gewichte
            license="DeepSeek Custom",
            herkunft="DeepSeek (CN) — ⚠️ DSGVO bei API",
        ),
    ]
    return (katalog,)


@app.cell
def _():
    """Berechnungs-Funktionen."""

    def kv_cache_gb(
        n_layers: int,
        n_kv_heads: int,
        d_head: int,
        seq_len: int,
        dtype_bytes: int = 2,
    ) -> float:
        """KV-Cache in GB. Faktor 2 = K + V."""
        return 2 * n_layers * n_kv_heads * d_head * seq_len * dtype_bytes / (1024**3)

    def gesamt_vram_gb(modell, seq_len: int, dtype_bytes: int = 2) -> float:
        return modell.gewichte_gb + kv_cache_gb(
            modell.n_layers, modell.n_kv_heads, modell.d_head, seq_len, dtype_bytes
        )

    def kv_cache_ohne_gqa_gb(modell, seq_len: int, dtype_bytes: int = 2) -> float:
        return kv_cache_gb(modell.n_layers, modell.n_q_heads, modell.d_head, seq_len, dtype_bytes)

    return gesamt_vram_gb, kv_cache_gb, kv_cache_ohne_gqa_gb


@app.cell
def _(gesamt_vram_gb, katalog, kv_cache_gb, kv_cache_ohne_gqa_gb, mo):
    """Tabelle: KV-Cache und Gesamt-VRAM bei Standard-Sequenz-Längen."""
    rows_kv = []
    for m_kv in katalog:
        gqa_faktor = m_kv.n_q_heads / m_kv.n_kv_heads
        kv_4k = kv_cache_gb(m_kv.n_layers, m_kv.n_kv_heads, m_kv.d_head, 4_000)
        kv_32k = kv_cache_gb(m_kv.n_layers, m_kv.n_kv_heads, m_kv.d_head, 32_000)
        kv_128k = kv_cache_gb(m_kv.n_layers, m_kv.n_kv_heads, m_kv.d_head, 128_000)
        kv_128k_no_gqa = kv_cache_ohne_gqa_gb(m_kv, 128_000)
        gesamt_128k = gesamt_vram_gb(m_kv, 128_000)

        rows_kv.append(
            f"| **{m_kv.name}** | {m_kv.n_q_heads} / {m_kv.n_kv_heads} ({gqa_faktor:.0f}×) "
            f"| {kv_4k:.2f} | {kv_32k:.2f} | {kv_128k:.2f} "
            f"| {kv_128k_no_gqa:.0f} | {gesamt_128k:.0f} |"
        )

    mo.md(
        "## 1. KV-Cache und VRAM-Bedarf (bf16)\n\n"
        "Sequenz-Längen: 4k / 32k / 128k\n\n"
        "| Modell | Q/KV-Heads (GQA-Faktor) | KV 4k GB | KV 32k GB | KV 128k GB | "
        "KV 128k *ohne GQA* | **Gesamt 128k** |\n"
        "|---|---|---|---|---|---|---|\n" + "\n".join(rows_kv) + "\n\n"
        "**Beobachtung**: GQA reduziert KV-Cache typisch um Faktor 4-12×. "
        "Ohne GQA wäre Long-Context (128k) auf einer einzelnen GPU oft "
        "**unmöglich**."
    )
    return


@app.cell
def _(gesamt_vram_gb, katalog, mo):
    """GPU-Empfehlung pro Modell × Kontext."""
    gpu_klassen = {
        "H100 80GB": 80,
        "H200 141GB": 141,
        "B200 192GB": 192,
    }

    rows_gpu = []
    for m_gpu in katalog:
        for seq in [8_000, 32_000, 128_000]:
            need = gesamt_vram_gb(m_gpu, seq)
            passende_gpus = [
                f"{name_gpu}" for name_gpu, vram in gpu_klassen.items() if vram >= need
            ]
            if passende_gpus:
                empfehlung = passende_gpus[0]
            else:
                anzahl = -(-need // gpu_klassen["B200 192GB"])  # ceil
                empfehlung = f"{int(anzahl)}× B200 (TP)"
            rows_gpu.append(f"| {m_gpu.name} | {seq:,} | {need:.0f} GB | {empfehlung} |")

    mo.md(
        "## 2. GPU-Klasse-Empfehlung (bf16, kein Quantization)\n\n"
        "| Modell | Seq-Länge | Total VRAM | Min. GPU |\n"
        "|---|---|---|---|\n"
        + "\n".join(rows_gpu)
        + "\n\n*TP = Tensor-Parallelism. Mit 4-bit-Quantization halbiert sich "
        "der Gewichte-Anteil ungefähr — Phase 17 vertieft.*"
    )
    return


@app.cell
def _(kv_cache_gb):
    """Smoke-Test."""
    # Llama 3.3 70B bei 8k Tokens
    kv_8k = kv_cache_gb(80, 8, 128, 8_000)
    assert 2.0 < kv_8k < 3.0, f"KV bei 8k erwartet ~2.4 GB, war {kv_8k}"

    # GQA-Reduktion: 64 vs. 8 KV-Heads = 8×
    kv_full_mha = kv_cache_gb(80, 64, 128, 8_000)
    assert abs(kv_full_mha / kv_8k - 8.0) < 0.01, "GQA-Faktor 8 erwartet"

    print("✅ Phase 07 Smoke-Test grün")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Faustregeln 2026

        - **KV-Cache** ist 80 % des VRAM-Verbrauchs in LLM-Inference, nicht das Modell
        - **GQA** (n_kv_heads << n_q_heads) ist deshalb 2026 in **fast jedem** LLM
        - **vLLM V1** mit PagedAttention + Chunked Prefill ist Inference-Standard
        - **FlashAttention-3** auf H100/H200, **FlashAttention-4** auf B200/GB200
        - **Long-Context** (128k) braucht GQA + viel VRAM — typisch H200 oder B200
        - **DeepSeek-V4** nutzt MLA statt GQA — extrem kompakt, aber proprietär

        ## Wichtige Hinweise

        - Modell-Architektur-Parameter sind aus offiziellen **Modell-Karten und
          Tech-Reports Stand 29.04.2026**. DeepSeek-V4 ist als MoE mit aktiven
          37B-Parametern aufgeführt — Gewichte-Total ist deutlich höher.
        - **Pharia-1** ist nach dem Aleph-Alpha-Cohere-Merger 04/2026 weiterhin
          unter ihrer Community-License verfügbar.
        - **vLLM/SGLang/TensorRT-LLM** abstrahieren die FlashAttention-Wahl —
          du musst sie nicht direkt callen.
        """
    )
    return


if __name__ == "__main__":
    app.run()
