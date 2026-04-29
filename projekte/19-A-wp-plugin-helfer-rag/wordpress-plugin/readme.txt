=== KI-Plugin-Helfer RAG ===
Contributors: saskialund
Tags: ai, rag, plugin-doku, code-search, dsgvo, eu-ai-act
Requires at least: 6.6
Tested up to: 6.7
Requires PHP: 8.1
Stable tag: 0.1.0
License: MIT
License URI: https://opensource.org/licenses/MIT

RAG-basierter Plugin-Doku-Helfer + Code-Search + Issue-Triage. Kommuniziert via REST mit selbstgehostetem Python-Sidecar (DSGVO-konform).

== Description ==

Der **KI-Plugin-Helfer RAG** ist ein Werkzeug für Plugin-Entwickler:innen, die ihre Plugin-Doku, ihren Code und ihre GitHub-Issues per LLM durchsuch- und beantwortbar machen wollen — **ohne Daten an Drittanbieter zu übergeben**.

= Architektur =

Das Plugin selbst ist ein dünner Adapter:

1. **WordPress-Admin-Seite** (Werkzeuge → KI-Plugin-Helfer) mit Suchformular
2. **REST-Endpoint** `/wp-json/ki-helfer/v1/frage`, abgesichert durch `manage_options`
3. **Python-Sidecar** (FastAPI) auf eigenem Server / Docker-Compose: vLLM oder Ollama + Qdrant + Pydantic-AI-Agent

Sämtliche LLM-Inference + Embedding läuft im Sidecar. Das Plugin selbst speichert keine personenbezogenen Daten.

= Drei Hauptfähigkeiten =

* **Plugin-Doku-RAG** — Frage stellen, Antwort + Quellen aus eigener Doku
* **Code-Search** — semantische Suche im eigenen Plugin-Code (AST-bewusst, nicht zeilenweise)
* **Issue-Triage** — GitHub-Issues automatisch klassifizieren + auf passende Code-Stelle hinweisen

= DSGVO + AI-Act =

* Kein Daten-Transfer an Drittanbieter
* Optional Audit-Hashing der Fragen (kein Klartext-Log)
* Sidecar auf EU-Cloud (STACKIT, IONOS, OVH, Scaleway) oder On-Prem
* AI-Act Art. 50: Hinweis-Banner aktiv, dass es KI-generierte Inhalte sind

== Installation ==

1. Plugin-Ordner nach `wp-content/plugins/wp-plugin-helfer-rag/` kopieren oder via ZIP hochladen
2. Plugin im Admin aktivieren
3. Sidecar starten — siehe [`projekte/19-A-wp-plugin-helfer-rag/sidecar/`](https://github.com/s-a-s-k-i-a/ki-engineering-werkstatt/tree/main/projekte/19-A-wp-plugin-helfer-rag/sidecar)
4. In **Einstellungen → KI-Plugin-Helfer** die Sidecar-URL setzen

== Frequently Asked Questions ==

= Brauche ich GPU? =

Für CPU-only-Sidecar (Ollama mit Llama 3.3 8B) reichen 16+ GB RAM.
Für vLLM mit Llama 3.3 70B brauchst du eine GPU mit min. 24 GB VRAM (RTX 4090 / A6000) oder besser.

= Wo läuft der Sidecar? =

Wahlfrei: Docker-Compose lokal, eigener Linux-Server, EU-Cloud (STACKIT, IONOS, OVH, Scaleway). Keine US-/CN-Cloud nötig.

= Werden meine Plugin-Daten gespeichert? =

Nur in deiner Qdrant-Instanz im Sidecar. Das WordPress-Plugin selbst speichert nichts (außer optional SHA-Hashes für Audit-Zwecke).

== Changelog ==

= 0.1.0 — 2026-04-29 =

* Initial Release: Admin-UI, REST-Endpoint, Settings-Page, Python-Sidecar (FastAPI), Docker-Compose-Setup
* Hinweis: AST-Splitting für PHP + GitHub-App-Integration kommen in 0.2.0

== Upgrade Notice ==

= 0.1.0 =
Initial Release. Sidecar muss separat aufgesetzt werden.
