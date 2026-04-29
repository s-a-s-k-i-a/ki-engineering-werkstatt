# Übung 08.01 — Watermark-Pipeline-Audit für drei generative DACH-Use-Cases

> Schwierigkeit: mittel · Zeit: 60–90 Min · Voraussetzungen: Lektionen 08.01–08.05

## Ziel

Du auditierst **Watermark- + C2PA-Pipelines** für drei generative DACH-Use-Cases nach AI-Act Art. 50.2 (in Kraft 02.08.2026) und § 201b StGB-Entwurf (Deepfake-Schutz). Pro Use-Case: Modell-Wahl, Watermark-Stack (Stable Signature / AudioSeal / TRELLIS), C2PA-Manifest, Lizenz-Kette.

## Use-Case

1. **Marketing-Bilder-Generator** (Werbeagentur Hannover): FLUX.2 (BFL Freiburg, Apache 2.0), 1.000 Bilder/Tag, müssen alle als KI-generiert markiert sein
2. **3D-Asset-Pipeline** (Maschinenbau, Visualisierungen): TRELLIS.2 für 3D-Modelle aus Single-Image, später in CAD-Software, **Hunyuan3D-2 NICHT erlaubt** (EU/UK/SK ausgeschlossen)
3. **Video-Erklärbar-Assistent** (E-Learning-Plattform): LTX-2.3 für 5-30-sec-Erklärvideos auf Skript, mit Stimm-Klon-Verbot (§ 201b StGB)

## Aufgabe

1. **Pydantic-Profil-Schema** mit `name`, `modell`, `medium` (`bild` / `video` / `3d` / `audio`), `kommerziell`, `volumen_pro_tag`, `personen_im_output`
2. **Modell-Lizenz-Check**: FLUX.2 Apache 2.0 ✓, TRELLIS.2 ✓, Hunyuan3D-2 EU-/UK-/SK-Sperre ✗
3. **Watermark-Empfehlung**: Bild → Stable Signature (SD-Familie) oder C2PA + Sichtbar-Marke; Video → C2PA + Sichtbarer Hinweis im Frame; 3D → Metadaten-Hash + C2PA
4. **C2PA-Manifest-Skizze** mit `claim_generator`, `signature_info`, `assertions` (was wurde generiert, von wem, wann)
5. **§ 201b-Check**: bei Stimm- oder Video-Klon realer Person → Watermark-Pflicht + Einwilligung dokumentiert
6. **Lizenz-Kette**: Modell-Lizenz → Trainings-Daten-Lizenz → Output-Lizenz (Apache 2.0 in der Kette → Output kommerziell nutzbar)
7. **AI-Act Art. 50.2-Konformitäts-Check**: maschinenlesbare Markierung Pflicht ab 02.08.2026
8. **Smoke-Test**: 5 Asserts (Lizenz-Korrektheit, Watermark-Pflicht, Hunyuan3D-2-Sperre)

## Bonus (für Schnelle)

- **AudioSeal**-Skizze für TTS-Use-Cases (Phase 06): wie funktioniert die unsichtbare Audio-Markierung?
- **C2PA-Hash-Kette** über Edit-Operationen: Bild generiert → bearbeitet → exportiert
- **Adversarial-Watermark-Robustheit**: was passiert beim Re-Encode (JPEG-Round-Trip)?
- **DSGVO Art. 22 + Art. 50.2**: gilt das auch für KI-Inhalt-Klassifikatoren („wurde dieser Text von KI generiert?")

## Abgabe

- Marimo-Notebook in `loesungen/01_loesung.py` (smoke-test-tauglich, kein FLUX-/LTX-Inference)
- Kurze `BERICHT.md`: für Marketing-Use-Case — wie validierst du die Wasserzeichen-Kette nach Re-Encoding (Instagram-Komprimierung)?

## Wann gilt es als gelöst?

- Marketing-Bilder → FLUX.2 + Stable Signature + C2PA-Manifest
- 3D-Pipeline → TRELLIS.2 (NICHT Hunyuan3D-2 wegen EU-Sperre)
- Video → § 201b-Check + Watermark + Stimm-Klon-Verbot
- Smoke-Test grün

## Wenn du steckenbleibst

- [FLUX.2 Modell-Karte (BFL Freiburg)](https://huggingface.co/black-forest-labs/FLUX.2-dev) — Apache 2.0
- [TRELLIS.2 GitHub](https://github.com/microsoft/TRELLIS) — 3D-Generation aus Single-Image
- [LTX-2.3 Tech Blog (Lightricks)](https://lightricks.com/lightricks-research)
- [C2PA-Spec](https://c2pa.org/specifications/specifications/2.1/index.html) — Content Authenticity
- [§ 201b StGB-Entwurf (BMJ)](https://www.bmj.de/SharedDocs/Gesetzgebungsverfahren/DE/Persoenlichkeitsschutz_Deepfake.html)

## Compliance-Check

- [ ] AI-Act Art. 50.2 — maschinenlesbare KI-Markierung (Pflicht ab 02.08.2026)
- [ ] § 201b StGB-Entwurf bei Personen-/Stimmen-Klonen (Deepfake-Verbot)
- [ ] KUG Art. 22 bei Personen im generierten Bild
- [ ] Modell-Lizenz dokumentiert (Apache 2.0 / Custom / proprietary)
- [ ] Trainings-Daten-Lizenz-Kette für kommerzielle Nutzung
- [ ] Hunyuan3D-2 NICHT für EU-/UK-/SK-Nutzer (Lizenz-Sperre)
