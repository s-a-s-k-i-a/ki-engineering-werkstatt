# Übung 17.01 — Production-Stack-Architektur für ein konkretes DACH-Projekt

> Schwierigkeit: fortgeschritten · Zeit: 180–300 Min · Voraussetzungen: Lektionen 17.01–17.10

## Ziel

Du baust eine **vollständige Production-Architektur** für ein konkretes Projekt-Profil — mit Stack-Wahl, Cost-Estimate, Compliance-Checkliste, deployment-fähiger `docker-compose.yml` und Audit-Pipeline. Ergebnis ist ein **PR-fertiges Architektur-Dokument** plus lauffähiger Code-Stack.

## Use-Case

Wähle eines der drei Profile (oder ein eigenes mit ähnlicher Tiefe):

### Profil A — „Bürger-Service-Bot" (Stadtverwaltung)

- 50 Mitarbeiter:innen interner Support, plus öffentlicher Chat-Bot
- ~ 15M Tokens / Monat (mittel)
- Latenz-Budget p95 < 1.500 ms
- Compliance: **BSI C5 Type 2** (öffentliche Hand), DSFA Pflicht
- Modell-Klasse: 8B–70B reicht
- Budget: 250 €/Monat

### Profil B — „Steuerkanzlei-Mandantenchat" (Berufsgeheimnisträger)

- 12 Steuerberater:innen, 800 Mandanten-Accounts
- ~ 5M Tokens / Monat (klein-mittel)
- Latenz-Budget p95 < 2.000 ms
- Compliance: **strenge AVV + Mandanten-Geheimnis**, EU-Cloud Pflicht
- Modell-Klasse: 8B–70B
- Budget: 150 €/Monat

### Profil C — „Code-Assistent intern" (Software-Mittelständler)

- 60 Entwickler:innen
- ~ 60M Tokens / Monat (hoch — Code-Heavy mit langen Context-Windows)
- Latenz-Budget p95 < 800 ms
- Compliance: ISO 27001 reicht, kein KRITIS
- Modell-Klasse: **70B** (Code-Qualität), Multi-LoRA für interne Codebases
- Budget: 1.200 €/Monat

## Aufgabe

1. **Profil wählen** und in `BERICHT.md` als YAML-Frontmatter dokumentieren
2. **Stack-Empfehlung** mit dem Notebook `01_eu_hosting_selector.py` als Startpunkt — pass den `UseCaseProfil` an dein Profil an
3. **Architektur-Diagramm** als Mermaid (siehe Lektion 17.05/17.06 für Beispiele)
4. **`docker-compose.yml`** für die kleinere Stack-Variante (Single-Box) ODER **`values.yaml`** für die K8s-Helm-Variante
5. **LiteLLM-Config** mit drei Provider-Tiers, Routing, Fallback, Cache (Redis-Semantic oder Qdrant-Semantic)
6. **TCO-Modell** mit Cache-Hit-Rate-Annahme und Sensitivität (was passiert, wenn Cache-Hit-Rate von 50 % auf 30 % fällt?)
7. **Compliance-Checkliste** abarbeiten (analog Lektion 17.11) — kreuze ab, was schon erfüllt ist, markiere offene Punkte
8. **Smoke-Test**: `docker compose up` mit Stub-Vllm (oder echtem vLLM, wenn GPU verfügbar) — `curl /v1/chat/completions` muss antworten
9. **Audit-Trail**: ein einzelner Test-Call muss in Phoenix oder Langfuse als Span sichtbar werden — Screenshot in `BERICHT.md`

## Bonus (für Schnelle)

- **GitOps-Variante** mit ArgoCD-Application-Manifest
- **Anomalie-Alert** in Grafana / Prometheus für Spend-Spike + US-Routing-Anstieg (Lektion 17.09)
- **Multi-LoRA-Setup** für Profil C — zwei Codebases als separate LoRAs, Hot-Swap pro Request
- **Self-Hosted-Langfuse** statt managed-EU-Region (Helm mit Bitnami-Restruktur-Fix)
- **Cost-Forecast** für Skalierung auf 3× User-Count — bricht der Stack bei 3× Token-Volumen?

## Abgabe

Im `loesungen/`-Ordner deiner Lösung:

- `BERICHT.md` (~ 2 Seiten) mit YAML-Profil + Architektur + TCO + Compliance-Checkliste
- `docker-compose.yml` ODER `values.yaml` (deployment-ready)
- `litellm-config.yaml` mit Provider-Tiers
- `audit-snapshot.png` (Phoenix oder Langfuse-Screenshot mit Test-Call-Trace)
- `mein_profil.py` (Marimo-Notebook-Snippet, das deinen `UseCaseProfil` lädt + Empfehlung generiert)

## Wann gilt es als gelöst?

- Stack-Empfehlung passt zum Profil (Compliance erfüllt, Budget realistisch)
- `docker compose up` startet den Stack ohne Fehler
- Test-Call landet als Span in Phoenix / Langfuse
- TCO ist transparent + sensibilitäts-getestet
- Compliance-Checkliste ist > 80 % gegrünt (Rest dokumentiert mit Plan)

## Wenn du steckenbleibst

- [LiteLLM Production Deployment](https://docs.litellm.ai/docs/proxy/prod)
- [vLLM Production Stack Helm](https://github.com/vllm-project/production-stack)
- [Phoenix Self-Hosting](https://arize.com/docs/phoenix/self-hosting)
- [Langfuse Helm Deployment](https://langfuse.com/self-hosting/deployment/kubernetes-helm)
- [STACKIT SKE GPU-Operator](https://docs.stackit.cloud/products/runtime/kubernetes-engine/how-tos/use-nvidia-gpus/)

## Compliance-Check (Pflicht-Pattern)

- [ ] AVV mit allen Cloud-Providern signiert (Self-Service oder Enterprise-Vertrag)
- [ ] DSFA durchgeführt (Phase 20.03)
- [ ] AI-Act-Klassifizierung dokumentiert (Phase 20.01)
- [ ] PII-Filter im OTel-Span-Processor aktiv (Lektion 17.08)
- [ ] Pseudonymisierung der User-IDs vor LiteLLM
- [ ] Audit-Logging-Aufbewahrung min. 6 Monate (Phase 20.05)
- [ ] Cost-Caps pro Mandant aktiv + getestet (Lektion 17.09)
- [ ] NIS2-Incident-Runbook vorhanden (falls KRITIS-relevant)
- [ ] Backup-Pipeline Postgres + Restore-Test alle 3 Monate
- [ ] gitleaks + trufflehog in CI gegen Secret-Leaks

## Reflexion

Schreib am Ende von `BERICHT.md` 3–5 Sätze:

- Was war die schwierigste Architektur-Entscheidung?
- Welche Compliance-Anforderung hätte das Projekt fast unmöglich gemacht?
- Was würdest du an deinem Stack ändern, wenn das Token-Volumen 5× höher wäre?
