# ki-engineering-werkstatt

> **From linear algebra to autonomous agent swarms. Learn AI with AI — and ship tools that work under EU law.**
>
> *21 phases of AI Engineering. In German. With sources that hold up.*

This repository is the German-language companion to AI engineering curricula like
[`rohitg00/ai-engineering-from-scratch`](https://github.com/rohitg00/ai-engineering-from-scratch) — but rebuilt
for the European reality of 2026: GDPR, EU AI Act, copyright (TDM-Opt-out), German
datasets, EU LLM hosting (Aleph Alpha, Mistral, IONOS, StackIT), and a frank discussion
of Asian open-weights (Qwen, DeepSeek, GLM, Kimi, MiniCPM, EXAONE) with their
self-censorship caveats.

The primary reading audience is German-speaking. Most prose, lessons, and
exercises are in German. Code identifiers are English. An English fork is on
the roadmap (Q4/2026).

## Why a German-language sister repo?

- **EU AI Act, GDPR, German copyright** are the actual constraints DACH builders face — and they are absent from English curricula.
- **German tokenizers, German datasets, German bias tests** matter for production quality.
- **EU LLM stack** (Aleph Alpha Pharia, Mistral, IONOS, StackIT, Black Forest Labs FLUX) is invisible in most English content.
- **Belegbarkeit**: every market claim cites Bitkom/KfW/VDMA/IfM with date.

## Quick start (English bullet points)

```bash
gh repo clone s-a-s-k-i-a/ki-engineering-werkstatt
cd ki-engineering-werkstatt
just setup    # uv sync + pre-commit
just smoke    # lint + typecheck + headless notebook tests
just edit 05-deutsche-tokenizer    # open the German tokenizer showcase
```

Requirements: Python 3.13, [uv](https://docs.astral.sh/uv/), [just](https://just.systems/), 8+ GB RAM.

## Showcase modules (fully developed at launch)

- **Phase 05** — German tokenizers: efficiency showdown across GPT-5, Claude 4.7, Llama 4, Mistral Large, Pharia, Teuken with EUR cost comparison
- **Phase 13** — RAG deep-dive: vanilla → hybrid → ColBERT → GraphRAG → LazyGraphRAG → agentic, all on a German Wikipedia subset
- **Phase 20** — Law & governance: AI-Act risk classifier CLI, DPA checklist, DPIA template, AI-literacy onboarding, audit logging

## License

[MIT](LICENSE). Inspiration credit: [`rohitg00/ai-engineering-from-scratch`](https://github.com/rohitg00/ai-engineering-from-scratch).

## Maintainer

Saskia Teichmann ([@s-a-s-k-i-a](https://github.com/s-a-s-k-i-a)) — full-stack web developer in Hannover, founder of [citelayer®](https://citelayer.ai), [isla-stud.io](https://isla-stud.io).
