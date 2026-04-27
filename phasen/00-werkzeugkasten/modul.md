---
id: 0
titel: Werkstatt einrichten — Hardware, Cloud, uv, Marimo
dauer_stunden: 4
schwierigkeit: einsteiger
stand: 2026-04-27
lernziele:
  - Reproduzierbare KI-Werkstatt auf Mac/Linux/Windows aufsetzen
  - Hardware-Klasse einschätzen (was läuft lokal, was braucht Cloud)
  - DSGVO-konforme EU-Cloud-Optionen kennen (StackIT, IONOS, OVH, Scaleway)
  - uv + Marimo + Ollama als Standard-Stack 2026 nutzen
---

# Werkstatt einrichten

> Stop installing 47 tools manually. — eine reproduzierbare KI-Werkstatt in unter 10 Minuten.

Diese Phase ist Pflicht. Ohne grünes `just smoke` läuft nichts anderes.

## Was du danach kannst

- `uv` einsetzen statt pip/poetry/pyenv (2026-Default)
- Marimo-Notebooks öffnen, editieren, headless ausführen
- Lokal Modelle starten (Ollama auf Mac/Linux/Win)
- Eine DSGVO-konforme Cloud-Alternative für Bilder/große Modelle wählen
- Einschätzen, was deine Hardware kann

## Inhalts-Übersicht

| Lektion | Titel | Dauer |
|---|---|---|
| 00.01 | Hardware-Matrix: was geht auf welcher Maschine | 30 min |
| 00.02 | uv installieren und ein Projekt anlegen | 30 min |
| 00.03 | Marimo statt Jupyter (warum und wie) | 30 min |
| 00.04 | Ollama lokal — dein erster lokaler LLM-Aufruf | 30 min |
| 00.05 | EU-Cloud-Stack im Vergleich (StackIT, IONOS, OVH, Scaleway) | 60 min |
| 00.06 | Dev-Container mit Docker (optional, für Linux/WSL) | 30 min |
| 00.07 | Markt & Realität: KI-Adoption im DACH-Mittelstand | 30 min |

## Praxis-Projekt (Pflicht-Quickstart)

Du installierst `uv`, holst Pharia-1-control via IONOS API (oder Llama-3 via Ollama lokal) und schreibst einen 5-Zeilen-Marimo-Notebook, der „Hallo, Werkstatt." zurückbekommt — auf Deutsch.

## Voraussetzungen

- Funktionierende Internet-Verbindung
- Mind. 8 GB RAM (16 GB für lokale 7B-Modelle, 32 GB für 13B)
- Optional: Apple-Silicon-Mac (MLX), CUDA-fähige NVIDIA-Karte (≥8 GB VRAM), oder Cloud-Account

## Was diese Phase NICHT macht

- Sie lehrt kein Python — Grundkenntnisse werden vorausgesetzt (siehe `docs/lernpfade/quereinsteigerin.md` für Crashkurs-Verweise).
- Sie installiert nichts auf deinem System ohne explizite Befehle. Alles per `uv` in einer isolierten venv.
