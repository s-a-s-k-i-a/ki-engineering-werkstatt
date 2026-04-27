# Sicherheits-Policy

## Sicherheits-Bugs melden

Wenn du eine Sicherheitslücke in diesem Repo entdeckst, melde sie **nicht** als
öffentliches Issue. Stattdessen:

1. **GitHub Security Advisory** (bevorzugt): Klick im Repo auf
   `Security` → `Report a vulnerability`
2. Oder per E-Mail: **security [at] wp-studio.dev** mit Betreff
   `[KI-Engineering-Werkstatt] Security`

Beschreibe:

- Was ist betroffen (Datei, Workflow, Lektion)?
- Wie reproduzierst du es?
- Welcher Schaden ist denkbar?

Reaktion innerhalb von 7 Tagen.

## Was zählt als Sicherheits-Bug?

- API-Keys, Tokens oder Credentials in Code/Notebooks/Datasets
- CI-Secrets, die in PRs aus Forks ausgelesen werden könnten
- Code-Beispiele mit Command-Injection / SQL-Injection / RCE-Pfaden
- Verlinkte URLs, die zu Malware, Phishing oder Defacement führen
- Datasets mit personenbezogenen Daten ohne erkennbaren Rechtsgrund
- Schwachstellen in mitgelieferten Werkzeugen (`werkzeuge/`)

## Was zählt **nicht** als Sicherheits-Bug?

- Veraltete Quellen (bitte als reguläres Issue melden)
- Falsche Tokenizer-Vergleichstabelle
- Tippfehler in Lektionstexten
- Performance-Probleme

## Kein-Geheimnis-Garantie

Dieses Repo enthält **keine** API-Keys, Tokens oder Zugangsdaten. Wir setzen
mehrere Schutzschichten:

- **`.gitignore`**: blockt `.env*`, `secrets/`, `*.key`, `*.pem`
- **Pre-commit `gitleaks`**: scannt jeden Commit lokal
- **GitHub Secret Scanning + Push Protection**: aktiviert
- **CI-Workflow `secrets-scan.yml`**: gitleaks + trufflehog auf full-history
- **`.env.example`**: dokumentiert nur Variablennamen, niemals Werte

Wenn du in einem Pull Request versehentlich einen Key committest:

1. Sofort den Key beim Anbieter rotieren (OpenAI/Anthropic/etc. → revoke + new).
2. PR schließen, Branch löschen.
3. Bei Force-Push-Bedarf in Discussions melden — ich helfe.

## Supply-Chain

- `uv.lock` ist committet und gepinnt; Dependabot hält `pyproject.toml`-Bounds
  aktuell.
- Drittanbieter-LLM-Modelle werden ausschließlich per Verweis genutzt — keine
  Modell-Gewichte im Repo.
- GitHub Actions sind auf `@v<major>` gepinnt; Major-Version-Updates erfolgen
  manuell nach Review.

## EU AI Act / DSGVO-Bezüge

Wenn du eine Lektion findest, die gegen EU-Recht verstößt (z. B. unsachgemäße
Datenverarbeitung in Übungen, falsche Compliance-Aussagen, missverständliche
DSGVO-Tipps), melde sie als Security-Bug — nicht als regulares Issue. Falsche
Rechtsbehauptungen können Lernende konkret schädigen.
