# Übung 07.01 — Inference-Plan + KV-Cache-Sizing für drei Production-Szenarien

> Schwierigkeit: mittel-fortgeschritten · Zeit: 60–90 Min · Voraussetzungen: Lektionen 07.01–07.03

## Ziel

Du baust einen **Inference-Planungs-Selektor** für drei Production-Szenarien. Pro Szenario: KV-Cache-Sizing, GPU-Empfehlung, FlashAttention-Variante (FA-3 vs. FA-4), vLLM-Konfigurations-Eckdaten. Schwerpunkt: **Hardware-Plan vor dem ersten Production-Deploy**.

## Use-Case

1. **DACH-Mittelstand-Chat** (40 concurrent users, 4k-Tokens-Sessions): Llama 3.3 70B oder Mistral Large 3, Pricing-sensitiv, < 2 sec TTFB
2. **Long-Context-Vertrags-Q&A** (Anwaltskanzlei, 80k-Tokens-Single-Shot, 10 req/Tag): muss saubere Multi-Doc-Recall haben (echte 80k, nicht behauptet)
3. **Realtime-Coding-Assistent** (50 Devs, 8k-Tokens-Median, < 500 ms Latenz): Qwen3-Coder oder GPT-OSS-120B, Apache 2.0 Pflicht (Lizenz-Constraint)

## Aufgabe

1. **Pydantic-Profil-Schema** mit `name`, `modell_name`, `n_layers`, `n_q_heads`, `n_kv_heads`, `d_head`, `gewichte_gb`, `seq_len_max`, `concurrent_users`, `latenz_budget_ms`
2. **KV-Cache-Funktion**: `kv_cache_gb(layers, kv_heads, d_head, seq_len, dtype_bytes=2)` (bf16 Standard)
3. **Total-VRAM-Funktion** = `gewichte_gb + kv_cache_gb × concurrent_users + 10 % overhead`
4. **GPU-Empfehlung**: Single H100/H200/B200 oder Tensor-Parallelism (TP) über mehrere GPUs
5. **FlashAttention-Wahl**: FA-3 für H100/H200, FA-4 für B200/GB200
6. **vLLM-Config-Skizze**: `gpu_memory_utilization`, `max_num_seqs`, `enable_chunked_prefill=True`, `enable_prefix_caching=True`
7. **Long-Context-Eval-Hinweis**: bei `seq_len_max > 32k` → RULER-Eval-Pflicht (siehe Phase 09.03)
8. **Smoke-Test**: 5 Asserts (KV-Cache-Korrektheit, GPU-Wahl, TP-Trigger)

## Bonus (für Schnelle)

- **MQA/GQA/MHA-Vergleich**: Llama 3.3 70B (GQA, 8 KV-Heads) vs. Vanilla MHA (64 KV-Heads) — wie viel Faktor Memory-Reduktion?
- **Speculative Decoding**: für Coding-Assistent — welches Draft-Modell, welche Acceptance-Rate?
- **PagedAttention**-Skizze: wie groß die Block-Größe in vLLM (Default 16 Tokens)?
- **Quantization-Plan**: Int8 vs. AWQ vs. GPTQ für Llama 3.3 70B → wie viel VRAM einsparen?

## Abgabe

- Marimo-Notebook in `loesungen/01_loesung.py` (smoke-test-tauglich, kein vLLM-Import)
- Kurze `BERICHT.md`: für Long-Context-Vertrags-Q&A — würdest du echtes 80k oder RAG mit 32k? Begründung.

## Wann gilt es als gelöst?

- Mittelstand-Chat → Single H100 oder H200 reicht
- Long-Context → H200 oder B200 (echte 80k braucht ≥ 30 GB KV-Cache)
- Realtime-Coding-Assistent → Qwen3-Coder oder GPT-OSS-120B (Apache 2.0)
- Smoke-Test grün

## Wenn du steckenbleibst

- [Kwon et al. 2023 — vLLM Paper](https://arxiv.org/abs/2309.06180)
- [Dao 2024 — FlashAttention-3](https://arxiv.org/abs/2407.08608)
- [vLLM V1 Documentation](https://docs.vllm.ai/en/latest/)
- [Llama 3.3 70B Model Card](https://huggingface.co/meta-llama/Llama-3.3-70B-Instruct)

## Compliance-Check

- [ ] EU-Hosting für Pricing-sensitive Use-Cases (Phase 17.04)
- [ ] AI-Act Art. 15 — Robustness-Eval bei langen Kontexten (RULER für > 32k)
- [ ] Modell-Lizenz dokumentiert (Apache 2.0 / MIT / Custom — Phase 20.07)
- [ ] AVV mit GPU-Cloud (OVH SecNumCloud, Scaleway HDS, STACKIT C5 Type 2)
- [ ] Reproduzierbarkeit via vLLM-Config-Hash (AI-Act Art. 11)
