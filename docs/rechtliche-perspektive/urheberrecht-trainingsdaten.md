# Urheberrecht & Trainingsdaten

> Stand: 2026-04-27. Volatile Lage — siehe Hinweis am Ende.

## TDM-Schranken im UrhG

### § 44b UrhG — TDM für kommerzielle Zwecke

- **Erlaubt**: Vervielfältigung rechtmäßig zugänglicher Werke für Text- und Data-Mining
- **Voraussetzung**: kein maschinenlesbarer Vorbehalt durch Rechteinhaber
- **Bei Online-Inhalten**: Vorbehalt **muss** maschinenlesbar sein (`ai.txt`, `robots.txt`, Meta-Tag, robots-extension `noai`)

### § 60d UrhG — TDM für wissenschaftliche Forschung

- **Erlaubt**: gemeinnützige Forschungs­einrichtungen, Hochschulen, Bibliotheken, Museen
- **Voraussetzung**: nicht kommerzieller Zweck
- **Pflicht**: nach Forschungs­abschluss Daten löschen oder zugriffs­beschränkt aufbewahren

## Aktuelle Rechtsprechung DE

### Kneschke vs. LAION

- **LG Hamburg 27.09.2024** (Az. 310 O 227/23): Klage abgewiesen, LAION als Forschungs­einrichtung nach § 60d anerkannt.
- **OLG Hamburg 10.12.2025** (Az. 5 U 104/24): Berufung verworfen. Maschinenlesbarkeit von Vorbehalten in natürlicher Sprache angenommen, **aber** für 2021er-Formulierung verneint.
- **BGH-Revision** möglich.

### Implications

- Wer **rein wissenschaftlich** trainiert: § 60d hilft.
- Wer **kommerziell** trainiert: § 44b — und Vorbehalte müssen beachtet werden.
- **Maschinen­lesbarkeit**: aktuell nicht abschließend definiert; sicherer Weg = `ai.txt` + `robots.txt` + Meta-Tag.

## US-Rechtsprechung (zur Einordnung, nicht direkt anwendbar)

- **NYT vs. OpenAI** (MDL): konsolidiert seit 04/2025. Vorlage von 20 Mio. ChatGPT-Logs angeordnet 05.01.2026. Fair-Use-Entscheidungen erwartet Sommer 2026.
- **Andere US-Verfahren**: laufen weiter, beobachten.

## EU AI Act Art. 53 — Copyright-Policy

GPAI-Anbieter (Modell-Anbieter) müssen seit 02.08.2025:

- **Copyright-Policy** dokumentieren
- **TDM-Vorbehalte** technisch respektieren
- **Trainingsdaten-Zusammenfassung** nach AI-Office-Template veröffentlichen

## Outputs — Schutzfähigkeit

- **DE/EU**: KI-Outputs sind **nicht** urheberrechtlich geschützt (Mensch-Schöpfer-Prinzip)
- **Bei menschlicher Bearbeitung**: kann ein neues Werk entstehen
- **Datenbank-Schutz** (§ 87a UrhG): kann auch ohne Schöpfungshöhe greifen, falls KI-Output systematisch zusammengestellt

## Dein eigenes Repo

- Setze `ai.txt` und `robots.txt` (siehe `werkzeuge/ai_txt_generator.py`)
- Bei eigenen Modellen: dokumentiere Trainings­datenherkunft
- Bei Inhalten von Dritten: Lizenz-Snapshot in `datasets/lizenzen/`

## Quellen

- [§ 44b UrhG](https://www.gesetze-im-internet.de/urhg/__44b.html)
- [§ 60d UrhG](https://www.gesetze-im-internet.de/urhg/__60d.html)
- [LTO LG Hamburg LAION](https://www.lto.de/recht/hintergruende/h/kuenstliche-intelligenz-ki-urheberrecht-text-data-mining-lg-hamburg-310o22723)
- [Elbkanzlei OLG Hamburg LAION 10.12.2025](https://www.elbkanzlei.com/ki-training-mit-fremden-fotos-was-das-olg-hamburg-jetzt-erlaubt-az-5-u-104-24-laion-kneschke/)
- [Norton Rose Fulbright AI Copyright 2026](https://www.nortonrosefulbright.com/en/knowledge/publications/ce8eaa5f/ai-in-litigation-series-an-update-on-ai-copyright-cases-in-2026)
- [Bird & Bird Kommentar zur LAION-Entscheidung](https://www.twobirds.com/de/insights/2024/germany/long-awaited-german-judgment-by-the-district-court-of-hamburg-kneschke-v-laion)
