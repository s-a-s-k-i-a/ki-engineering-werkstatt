# Übung 00.01 — Eigene Werkstatt einrichten und dokumentieren

> Schwierigkeit: einsteiger · Zeit: 60 Min · Voraussetzung: Lektionen 00.01 bis 00.04

## Ziel

Du richtest deine eigene Werkstatt komplett ein und schreibst eine kurze Dokumentation, die du im Team / vor dir selbst nachschauen kannst, wenn du in 6 Monaten zurückkommst.

## Aufgabe

1. **Hardware-Klasse bestimmen** (Lektion 00.01)
   - RAM, VRAM (falls vorhanden), Apple-Silicon-Generation
   - Eintrag: in welche Tabellenzeile fällt deine Hardware?

2. **uv installieren und verifizieren** (Lektion 00.02)
   - Befehl: `uv --version` zeigt 0.11.x oder neuer
   - Eintrag: deine `uv` Version

3. **Dieses Werkstatt-Repo lokal klonen**

   ```bash
   gh repo clone s-a-s-k-i-a/ki-engineering-werkstatt
   cd ki-engineering-werkstatt
   uv sync --extra dev --extra tokenizer
   ```

4. **Setup-Verifier ausführen** (Lektion 00.03)

   ```bash
   uv run marimo edit phasen/00-werkzeugkasten/code/01_setup_verifier.py
   ```

   Browser sollte `http://localhost:2718` öffnen, alle Pflicht-Checks grün.

5. **Ollama installieren und ein Modell ziehen** (Lektion 00.04)
   - Wähle ein Modell, das zu deiner Hardware-Klasse passt (Tabelle in Lektion 00.04)
   - Beispiel: bei 16 GB RAM → `ollama pull qwen3:8b`
   - Teste: `ollama run <modell> "Erkläre den AI Act in 2 Sätzen."`

6. **EU-Cloud-Account anlegen (optional)** (Lektion 00.05)
   - Eine der vier Anbieter: STACKIT, IONOS, OVHcloud, Scaleway
   - Empfehlung: **Scaleway Free-Tier** (1M Token kostenlos, schnell anzulegen)
   - Eintrag: AVV-Status (signiert? Self-Service vorhanden?)

7. **Dokumentation schreiben** in `loesungen/01_loesung.py` (Marimo-Notebook):
   - Hardware-Klasse mit Begründung
   - Versionen aller Tools (uv, marimo, ollama)
   - Welches lokale Modell läuft, was bekommst du als Antwort?
   - Welcher EU-Cloud-Anbieter (falls gewählt), AVV-Status, EUR-Token-Preis
   - Mind. 3 Reflexions-Sätze: was war einfach, was war schwer?

## Bonus (für Schnelle)

- Lege eine `.devcontainer/devcontainer.json` an (Lektion 00.06)
- Teste den Container in VS Code („Reopen in Container")
- Falls du Codespaces hast: Repo dort öffnen, Setup-Verifier laufen lassen

## Abgabe

- Marimo-Notebook in `loesungen/01_loesung.py` (im Werkstatt-Repo bei dir lokal — du musst es nicht hochladen)
- Plus: ein Issue oder Discussion-Post auf GitHub mit deinem Hardware-Setup, falls du eine Frage hast oder ein Problem dokumentierst, das anderen helfen könnte

## Wann gilt es als gelöst?

- Setup-Verifier zeigt 5 grüne Häkchen (oder 4 mit Ollama als optional)
- `just smoke` (oder `uv run pytest tests/ -q`) läuft im Repo grün durch
- Lokales Ollama-Modell antwortet auf eine deutsche Frage in unter 10 Sekunden

## Wenn du steckenbleibst

- [Discussions](https://github.com/s-a-s-k-i-a/ki-engineering-werkstatt/discussions) eröffnen mit:
  - OS + Python-Version (`uv python list`)
  - Output von `uv run marimo edit ...`
  - Welche Lektion / welcher Schritt
- [`GETTING_STARTED.md` Troubleshooting](../../../GETTING_STARTED.md#troubleshooting)
