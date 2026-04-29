# Übung 04.01 — VLM-Auswahl für drei DACH-Vision-Use-Cases

> Schwierigkeit: mittel · Zeit: 60–90 Min · Voraussetzungen: Lektionen 04.01–04.05

## Ziel

Du baust einen **VLM- + Hardware- + Latenz-Selektor** für drei DACH-Bild-/Vision-Use-Cases. Pro Use-Case: VLM-Familie (Qwen3-VL / SigLIP-2 / LightOnOCR / MiniCPM-o), Inference-Stack, Datenresidenz-Plan und KUG-Compliance-Pflichten.

## Use-Case

1. **Werkstatt-Schadenshilfe** (Werkstatt-Kette): Mitarbeiter:in fotografiert Schaden → VLM identifiziert Bauteil + Schadenstyp → Reparatur-Anleitung. **Lokal auf Tablet**, < 800 ms Latenz, keine Cloud erlaubt
2. **Behörden-OCR** (Bauamt): Posteingang-Briefe scannen → Text + Tabellen + handschriftliche Notizen extrahieren. EU-Cloud okay, ~ 5.000 Briefe/Tag
3. **Personen-Foto-Galerie** (Tierheim Hannover, Capstone 19.C-bezug): Adoptions-Tiere katalogisieren + ähnliche Tiere finden. Personen sind manchmal mit drauf — KUG Art. 22 Pflicht!

## Aufgabe

1. **Pydantic-Profil-Schema** mit `name`, `task` (`bauteil_klassifikation` / `ocr` / `image_search` / `multimodal_chat`), `latenz_ms`, `hosting`, `personen_im_bild`, `volumen_pro_tag`
2. **VLM-Empfehlungs-Funktion**: Edge → MiniCPM-o oder SmolVLM2; OCR → LightOnOCR-2-1B; Multimodal-Chat → Qwen3-VL; Image-Search → SigLIP-2 oder jina-clip-v2
3. **Inference-Stack-Empfehlung**: Edge → llama.cpp / MLX / Ollama; Cloud → vLLM / SGLang
4. **KUG-Compliance-Funktion**: bei `personen_im_bild=True` → Einwilligung-Workflow + Auto-Lösch-Pipeline + Pseudonymisierungs-Layer
5. **Datenresidenz-Plan**: bei „Cloud" → AVV-Liste mit EU-Anbietern (IONOS, OVH, Scaleway, STACKIT)
6. **Smoke-Test**: 4 Asserts (Edge-Modell, OCR-Modell, KUG-Pflicht, AVV)

## Bonus (für Schnelle)

- **Latenz-Schätzung**: für Werkstatt-Tablet (Apple Silicon M3 Pro 18 GB) — passt MiniCPM-o-2.6 in 5 GB? Wie groß die Activation-Memory?
- **Bias-Check**: SigLIP-2 vs. CLIP — welche Marketing-Bilder werden geringer eingestuft (Race / Gender Bias)?
- **Wasserzeichen-Pipeline** für Tierheim-Galerie: C2PA-Manifest + AudioSeal-Image-Variante (siehe Phase 08.04)
- **GPS-EXIF-Strip-Pflicht** vor Upload (DSGVO Art. 25)

## Abgabe

- Marimo-Notebook in `loesungen/01_loesung.py` (smoke-test-tauglich, kein VLM-Inference)
- Kurze `BERICHT.md`: für Behörden-OCR — wie würdest du Personen-Daten in Briefen vor der OCR-Pipeline schützen?

## Wann gilt es als gelöst?

- Werkstatt-Schaden → Edge-Modell (MiniCPM-o oder SmolVLM2) + lokales Hosting
- Behörden-OCR → LightOnOCR-2-1B oder Vergleichbares
- Tierheim-Galerie → KUG Art. 22 in Compliance-Output
- Smoke-Test grün

## Wenn du steckenbleibst

- [Qwen3-VL-32B-Instruct](https://huggingface.co/Qwen/Qwen3-VL-32B-Instruct)
- [LightOnOCR-2-1B](https://huggingface.co/lightonai/LightOnOCR-2-1B)
- [MiniCPM-o-2.6 Tech Report](https://huggingface.co/openbmb/MiniCPM-o-2_6) — Edge-Multimodal
- [KUG Art. 22 — Recht am eigenen Bild](https://www.gesetze-im-internet.de/kunsturhg/__22.html)

## Compliance-Check

- [ ] KUG Art. 22 bei Personen im Bild (Einwilligung + ggf. Auto-Lösch-Pipeline)
- [ ] DSGVO Art. 9 bei biometrischen Daten (Gesichts-Erkennung) → DSFA-Pflicht
- [ ] AI-Act Anhang III Nr. 1 bei biometrischer Identifizierung → Hochrisiko
- [ ] AVV-Vertrag mit Cloud-Anbieter (Phase 17.04 + 20.02)
- [ ] EXIF-Strip vor Upload (PII in Metadaten)
- [ ] Bei kommerziellem Bild-Upload: Lizenz-Kette dokumentieren (Phase 20.04)
