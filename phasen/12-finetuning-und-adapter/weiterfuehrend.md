# Weiterführend — Phase 12 Finetuning & Adapter

## Foundational Papers

- **LoRA** (Hu et al. 2021) — <https://arxiv.org/abs/2106.09685>
- **QLoRA** (Dettmers et al. 2023) — <https://arxiv.org/abs/2305.14314>
- **DoRA** (Liu et al. 2024) — <https://arxiv.org/abs/2402.09353>
- **LoRA+** (Hayou et al. 2024) — <https://arxiv.org/abs/2402.12354>
- **rsLoRA / Rank-Stabilized LoRA** (Kalajdzievski 2023) — <https://arxiv.org/abs/2312.03732>

## Trainings-Stacks (Stand 29.04.2026)

- **Unsloth** — <https://github.com/unslothai/unsloth> (rolling `2026.4.x`)
- **Unsloth Notebooks** (250+) — <https://github.com/unslothai/notebooks>
- **Unsloth Docs** — <https://unsloth.ai/docs>
- **axolotl** — <https://github.com/axolotl-ai-cloud/axolotl> (v0.16.1)
- **axolotl Docs** — <https://docs.axolotl.ai>
- **TRL** — <https://github.com/huggingface/trl> (v1.3.0)
- **TRL Docs** — <https://huggingface.co/docs/trl>
- **PEFT** — <https://github.com/huggingface/peft> (v0.19.1)
- **PEFT Docs** — <https://huggingface.co/docs/peft>
- **Transformers** — <https://github.com/huggingface/transformers>
- **bitsandbytes** (8-bit Optimizer) — <https://github.com/bitsandbytes-foundation/bitsandbytes>
- **AutoAWQ** (post-merge Quant) — <https://github.com/casper-hansen/AutoAWQ>

## Multi-LoRA-Inference

- **vLLM LoRA** — <https://docs.vllm.ai/en/latest/features/lora/>
- **Unsloth vLLM-Hot-Swap-Guide** — <https://unsloth.ai/docs/basics/inference-and-deployment/vllm-guide/lora-hot-swapping-guide>
- **HF PEFT-Multi-Adapter** — <https://huggingface.co/docs/peft/main/en/task_guides/lora_based_methods>

## Deutsche Trainings-Datasets

- **GermanQuAD** — <https://huggingface.co/datasets/deepset/germanquad> (CC-BY-4.0)
- **10kGNAD** — <https://github.com/tblock/10kGNAD> (CC-BY-NC-SA — nur Forschung!)
- **GermEval-Reihe** — <https://huggingface.co/datasets?search=germeval>
- **GermEval 2024 GerMS-Detect** — <https://ofai.github.io/GermEval2024-GerMS/>
- **LLäMmlein-Dataset** — <https://huggingface.co/datasets/LSX-UniWue/LLaMmlein-Dataset>
- **Aleph-Alpha-GermanWeb** (628 Mrd. Wörter) — <https://huggingface.co/datasets/Aleph-Alpha/Aleph-Alpha-GermanWeb>
- **Aleph-Alpha-GermanWeb Paper** — <https://arxiv.org/abs/2505.00022>
- **EuroLLM-22B-Instruct** — <https://huggingface.co/utter-project/EuroLLM-22B-Instruct-2512>
- **SauerkrautLM-DPO** (VAGOsolutions) — <https://huggingface.co/VAGOsolutions/SauerkrautLM-v2-14b-DPO>
- **DiscoLM-German-Mix** — <https://huggingface.co/DiscoResearch>

## Daten-Tooling

- **Microsoft Presidio** (PII-Detection) — <https://microsoft.github.io/presidio/>
- **Llama Guard 3** (Toxic-Filter) — <https://huggingface.co/meta-llama/Llama-Guard-3-8B>
- **fasttext Sprach-Detektion** — <https://fasttext.cc/docs/en/language-identification.html>
- **Hunspell DE** — <https://github.com/wooorm/dictionaries/tree/main/dictionaries/de>
- **datasketch (MinHash-LSH)** — <https://github.com/ekzhu/datasketch>
- **DVC** (Daten-Versionierung) — <https://dvc.org/doc>

## EU-Cloud-GPU für QLoRA

- **Scaleway H100** (€ 2,73/h) — <https://www.scaleway.com/en/h100/>
- **OVHcloud H100** — <https://www.ovhcloud.com/en/public-cloud/gpu/h100/>
- **OVHcloud H200** — <https://www.ovhcloud.com/en/public-cloud/gpu/h200/>
- **STACKIT SKE GPU-Operator** — <https://docs.stackit.cloud/products/runtime/kubernetes-engine/how-tos/use-nvidia-gpus/>
- **introl Fine-Tuning Cost-Guide** — <https://introl.com/blog/fine-tuning-infrastructure-lora-qlora-peft-scale-guide-2025>

## Modell-Lizenzen (Pflicht-Lektüre vor Finetuning)

- **Llama 3.3 / 4 Community License** — <https://www.llama.com/llama3/license/>
- **Mistral Apache 2.0** — <https://huggingface.co/mistralai>
- **Qwen3 Apache 2.0** — <https://huggingface.co/Qwen>
- **DeepSeek-License** — <https://github.com/deepseek-ai/DeepSeek-LLM/blob/main/LICENSE-MODEL>
- **Gemma-License** — <https://ai.google.dev/gemma/terms>
- **EXAONE-NC** ⚠️ — <https://huggingface.co/LGAI-EXAONE> (nicht kommerziell)
- **Aleph-Alpha-Open-License** — <https://huggingface.co/Aleph-Alpha>

## Verwandte Phasen

- → Phase **05** (Tokenizer + Embeddings — Komposita-Effizienz fürs Finetuning relevant)
- → Phase **11** (Pydantic AI + Eval — was Finetuning **nicht** löst)
- → Phase **13** (RAG — fast immer der bessere Pfad)
- → Phase **14** (Agenten + Tools — was Finetuning erweitert)
- → Phase **17** (Production EU-Hosting — Multi-LoRA-Deployment)
- → Phase **18** (Bias-Audit + DPO/GRPO als zweite Stufe)
- → Phase **20** (UrhG-§-44b + DSGVO-Trainings-Disziplin)
