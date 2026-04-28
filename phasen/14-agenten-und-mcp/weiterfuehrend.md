# Weiterführend — Phase 14 Agenten & MCP

## Frameworks (Primärquellen, geprüft 28.04.2026)

- **Pydantic AI Docs** — <https://ai.pydantic.dev/> (aktuell v1.66.0)
- **Pydantic AI Multi-Agent Examples** — <https://ai.pydantic.dev/multi-agent/>
- **LangGraph Docs** — <https://langchain-ai.github.io/langgraph/> (aktuell v1.1.9)
- **LangGraph Supervisor** — <https://github.com/langchain-ai/langgraph/tree/main/libs/langgraph-supervisor>
- **LangGraph HITL** — <https://langchain-ai.github.io/langgraph/concepts/human_in_the_loop/>
- **DSPy Docs** — <https://dspy.ai/> (aktuell v3.1.3)
- **OpenAI Agents SDK** — <https://platform.openai.com/docs/guides/agents>
- **MCP Spec 2025-11-25** — <https://modelcontextprotocol.io/specification/latest>
- **MCP Python SDK** — <https://github.com/modelcontextprotocol/python-sdk> (aktuell v1.27.0)

## Foundational Texts

- Anthropic „Building Effective Agents" (Dez. 2024, weiter aktuell) —
  <https://www.anthropic.com/research/building-effective-agents>
- Anthropic „How we built Claude Code" (10/2025) —
  <https://www.anthropic.com/news/claude-code>
- LangChain „State of AI Agents 2025" — <https://www.langchain.com/state-of-ai-agents-2025>
- DeepMind „SIMA: A Generalist AI Agent for 3D Virtual Environments" —
  <https://deepmind.google/discover/blog/sima-generalist-ai-agent-for-3d-virtual-environments/>

## Multi-Agent-Patterns

- LangGraph Multi-Agent Tutorials —
  <https://langchain-ai.github.io/langgraph/tutorials/multi_agent/multi-agent-collaboration/>
- LangGraph Hierarchical Agent Teams —
  <https://langchain-ai.github.io/langgraph/tutorials/multi_agent/hierarchical_agent_teams/>
- AutoGen v0.4 — <https://microsoft.github.io/autogen/>
- CrewAI Docs — <https://docs.crewai.com/> (zweistufige Hierarchie out-of-the-box)
- OpenAI Swarm (Educational) — <https://github.com/openai/swarm>

## DSPy & Pipeline-Optimierung

- DSPy Tutorial: Optimizing Agents — <https://dspy.ai/tutorials/agents/>
- DSPy MIPROv2 — <https://dspy.ai/api/optimizers/MIPROv2/>
- DSPy GEPA Optimizer (Reflection-based) — <https://dspy.ai/api/optimizers/GEPA/>
- DSPy Pydantic-AI-Integration —
  <https://ai.pydantic.dev/examples/dspy-prompt-optimization/>

## MCP Ecosystem

- MCP Inspector (Debug-Tool) — <https://github.com/modelcontextprotocol/inspector>
- MCP Server Verzeichnis — <https://github.com/modelcontextprotocol/servers>
- MCP-Server für GitHub, Postgres, Filesystem, Slack, Google Drive — alle offiziell
- Anthropic MCP-Quickstart — <https://modelcontextprotocol.io/quickstart>
- Pydantic AI MCP-Integration — <https://ai.pydantic.dev/mcp/>

## Sicherheit (Prompt Injection + Tool-Authorization)

- OWASP LLM Top 10 v2.0 — <https://genai.owasp.org/llm-top-10/>
- OWASP LLM01 Prompt Injection — <https://genai.owasp.org/llmrisk/llm01-prompt-injection/>
- OWASP LLM06 Excessive Agency — <https://genai.owasp.org/llmrisk/llm06-excessive-agency/>
- Anthropic „Indirect Prompt Injection" —
  <https://www.anthropic.com/research/indirect-prompt-injection>
- Simon Willison Prompt-Injection-Sammlung — <https://simonwillison.net/tags/prompt-injection/>
- Microsoft AI Red Team Playbook — <https://learn.microsoft.com/security/ai-red-team/>

## Sandboxing für Code-Execution

- **E2B** — <https://e2b.dev/docs> (Cloud-Sandbox, Firecracker-microVM)
- **Daytona** — <https://www.daytona.io/> (Self-Hosted, EU-tauglich)
- **Modal** — <https://modal.com/> (generischer Sandbox-Compute)
- gVisor — <https://gvisor.dev/> (Container-Sandbox-Layer)

## Observability für Agenten

- **Phoenix (Arize)** Multi-Agent-Tracing —
  <https://docs.arize.com/phoenix/tracing/multi-agent-tracing>
- **Langfuse** Agent-Tracing — <https://langfuse.com/docs/integrations/langgraph>
- **OpenTelemetry GenAI Agent Spans** —
  <https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-agent-spans/>
- **OpenLLMetry** — <https://github.com/traceloop/openllmetry>

## State-Management & Persistenz

- LangGraph Checkpointer — <https://langchain-ai.github.io/langgraph/reference/checkpoints/>
- LangGraph Postgres-Checkpointer —
  <https://langchain-ai.github.io/langgraph/reference/checkpoints/#postgressaver>
- Redis-Checkpointer (Community) — <https://github.com/langchain-ai/langgraph/tree/main/libs/checkpoint-redis>

## Recht & Compliance (Bezug)

- AI Act Art. 14 (Human Oversight) —
  <https://artificialintelligenceact.eu/article/14/>
- AI Act Art. 50 (Transparenz für KI-Interaktionen) —
  <https://artificialintelligenceact.eu/article/50/>
- DSGVO Art. 22 (Automatisierte Entscheidungen) —
  <https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:32016R0679#d1e2746-1-1>
- EDPB Opinion 28/2024 (LLMs + Personenbezug) —
  <https://www.edpb.europa.eu/system/files/2024-12/edpb_opinion_202428_ai-models_en.pdf>
- BfDI Stellungnahme zu KI-Agents (Stand 03/2026) —
  <https://www.bfdi.bund.de/DE/Service/Newsletter/Listen/start.html>

## Praxis-Berichte (DACH)

- DATEV-Erfahrungsbericht zu Pydantic AI in Steuer-Workflows (10/2025) —
  <https://www.datev-magazin.de/news-stream/news/ai-engineering-praxis>
- IONOS AI Agent Hub Launch (12/2025) —
  <https://cloud.ionos.com/managed/ai-model-hub>
- Bitkom Studie „Agentic AI im Mittelstand" (geplant Q3/2026) —
  <https://www.bitkom.org/Themen/Technologien-Software/Kuenstliche-Intelligenz>

## Verwandte Phasen

- → Phase **11** (LLM-Engineering — Pydantic AI Basics, Pricing, Eval)
- → Phase **13** (RAG — als Tool für Wissens-Agenten)
- → Phase **15** (Autonome Systeme — wenn Agents in der Wildnis laufen)
- → Phase **16** (Reasoning — Test-Time-Compute, Reflexion in Agent-Loops)
- → Phase **17** (Production EU-Hosting — Agent-Deployment, Postgres-Checkpointer)
- → Phase **18** (Ethik — Self-Censorship-Audit asiatischer Sub-Agents)
- → Phase **19.C** (Capstone — vollständiger Charity-Adoptions-Bot)
- → Phase **20** (Recht & Governance — AVV, DSFA, Audit-Logging)
