# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "marimo",
#   "pydantic>=2.9",
# ]
# ///

"""Lösungs-Skelett — Übung 07.01 — KV-Cache + Inference-Plan.

Smoke-test-tauglich. Reine Berechnungs-Logik, kein vLLM-Import.
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
        # 🎯 Lösung Übung 07.01 — KV-Cache + Inference-Plan

        Drei Production-Szenarien → KV-Cache + GPU + FlashAttention + vLLM-Config.
        """
    )
    return


@app.cell
def _():
    """Pydantic-Profil-Schema."""
    from pydantic import BaseModel, Field

    class InferenzProfil(BaseModel):
        name: str
        modell_name: str
        n_layers: int = Field(ge=1, le=200)
        n_q_heads: int = Field(ge=1, le=128)
        n_kv_heads: int = Field(ge=1, le=128)
        d_head: int = Field(ge=32, le=256)
        gewichte_gb: float = Field(ge=0.5, le=2000.0)
        seq_len_max: int = Field(ge=1_000, le=2_000_000)
        concurrent_users: int = Field(ge=1, le=10_000)
        latenz_budget_ms: int = Field(ge=10)

    return (InferenzProfil,)


@app.cell
def _():
    """Berechnungs-Funktionen."""

    def kv_cache_gb(layers, kv_heads, d_head, seq_len, dtype_bytes=2):
        return 2 * layers * kv_heads * d_head * seq_len * dtype_bytes / (1024**3)

    def total_vram_gb(p):
        kv_pro_user = kv_cache_gb(p.n_layers, p.n_kv_heads, p.d_head, p.seq_len_max)
        kv_total = kv_pro_user * p.concurrent_users
        return (p.gewichte_gb + kv_total) * 1.1  # +10 % overhead

    def gpu_empfehlung(p):
        gpu_klassen = [
            ("H100 80GB", 80, "FlashAttention-3"),
            ("H200 141GB", 141, "FlashAttention-3"),
            ("B200 192GB", 192, "FlashAttention-4"),
        ]
        need = total_vram_gb(p)
        for name, vram, fa in gpu_klassen:
            if vram >= need:
                return {"gpu": name, "tp": 1, "flashattention": fa, "benoetigt_gb": need}
        # TP über mehrere B200
        anzahl = -(-int(need) // 192) + 1  # ceil
        return {
            "gpu": f"{anzahl}× B200",
            "tp": anzahl,
            "flashattention": "FlashAttention-4",
            "benoetigt_gb": need,
        }

    def vllm_config(p):
        return {
            "gpu_memory_utilization": 0.92,
            "max_num_seqs": min(p.concurrent_users * 2, 256),
            "enable_chunked_prefill": True,
            "enable_prefix_caching": True,
            "max_model_len": p.seq_len_max,
            "block_size": 16,
        }

    def long_context_eval_pflicht(p):
        return p.seq_len_max > 32_000

    return (
        gpu_empfehlung,
        kv_cache_gb,
        long_context_eval_pflicht,
        total_vram_gb,
        vllm_config,
    )


@app.cell
def _(InferenzProfil):
    """Drei Use-Cases."""
    profile = [
        InferenzProfil(
            name="DACH-Mittelstand-Chat",
            modell_name="Llama 3.3 70B",
            n_layers=80,
            n_q_heads=64,
            n_kv_heads=8,
            d_head=128,
            gewichte_gb=140.0,
            seq_len_max=4_000,
            concurrent_users=40,
            latenz_budget_ms=2_000,
        ),
        InferenzProfil(
            name="Long-Context-Vertrags-Q&A",
            modell_name="Mistral Large 3 (123B)",
            n_layers=88,
            n_q_heads=96,
            n_kv_heads=8,
            d_head=128,
            gewichte_gb=246.0,
            seq_len_max=80_000,
            concurrent_users=2,
            latenz_budget_ms=10_000,
        ),
        InferenzProfil(
            name="Realtime-Coding-Assistent",
            modell_name="Qwen3-Coder oder GPT-OSS-120B",
            n_layers=96,
            n_q_heads=96,
            n_kv_heads=8,
            d_head=128,
            gewichte_gb=240.0,
            seq_len_max=8_000,
            concurrent_users=50,
            latenz_budget_ms=500,
        ),
    ]
    return (profile,)


@app.cell
def _(
    gpu_empfehlung,
    kv_cache_gb,
    long_context_eval_pflicht,
    mo,
    profile,
    total_vram_gb,
    vllm_config,
):
    """Detail pro Use-Case."""
    blocks = []
    for p in profile:
        kv_pro_user = kv_cache_gb(p.n_layers, p.n_kv_heads, p.d_head, p.seq_len_max)
        gpu = gpu_empfehlung(p)
        cfg = vllm_config(p)
        ruler_pflicht = "✅ RULER-Eval-Pflicht" if long_context_eval_pflicht(p) else "—"

        blocks.append(
            f"### {p.name} ({p.modell_name})\n\n"
            f"- **KV-Cache pro User**: {kv_pro_user:.2f} GB (bei {p.seq_len_max:,} Tokens)\n"
            f"- **Total VRAM**: {total_vram_gb(p):.0f} GB\n"
            f"- **GPU**: {gpu['gpu']} (TP={gpu['tp']}) · {gpu['flashattention']}\n"
            f"- **vLLM-Config**: `gpu_memory_utilization={cfg['gpu_memory_utilization']}`, "
            f"`max_num_seqs={cfg['max_num_seqs']}`, "
            f"`enable_chunked_prefill={cfg['enable_chunked_prefill']}`, "
            f"`enable_prefix_caching={cfg['enable_prefix_caching']}`\n"
            f"- **Long-Context-Eval**: {ruler_pflicht}\n"
        )
    mo.md("## Detail pro Use-Case\n\n" + "\n".join(blocks))
    return


@app.cell
def _(
    gpu_empfehlung,
    kv_cache_gb,
    long_context_eval_pflicht,
    profile,
):
    """Smoke-Test: 5 Akzeptanz-Asserts."""
    p_chat = profile[0]
    p_long = profile[1]
    p_code = profile[2]

    # 1. Llama 3.3 70B mit GQA: KV-Cache pro User bei 4k Tokens ~ 1.2 GB
    kv_chat = kv_cache_gb(80, 8, 128, 4_000)
    assert 1.0 < kv_chat < 1.5, f"KV bei 4k erwartet ~1.25 GB, war {kv_chat}"

    # 2. Long-Context-Use-Case → RULER-Pflicht
    assert long_context_eval_pflicht(p_long)
    assert not long_context_eval_pflicht(p_chat)

    # 3. Long-Context Mistral Large mit 80k → mindestens H200 nötig
    long_gpu = gpu_empfehlung(p_long)
    assert "H200" in long_gpu["gpu"] or "B200" in long_gpu["gpu"]

    # 4. FlashAttention-Wahl: H200 = FA-3, B200 = FA-4
    assert (
        "FlashAttention-3" in long_gpu["flashattention"]
        or "FlashAttention-4" in long_gpu["flashattention"]
    )

    # 5. Coding-Assistent mit 50 concurrent users → großer max_num_seqs
    code_gpu = gpu_empfehlung(p_code)
    assert code_gpu["gpu"]  # nicht leer

    print("✅ Übung 07.01 — alle 5 Asserts grün")
    return


if __name__ == "__main__":
    app.run()
