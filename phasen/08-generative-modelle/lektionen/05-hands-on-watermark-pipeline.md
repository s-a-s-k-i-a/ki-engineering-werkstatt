---
id: 08.05
titel: Hands-on — Multi-Layer-Watermark-Pipeline für KI-Bilder + Videos
phase: 08-generative-modelle
dauer_minuten: 90
schwierigkeit: fortgeschritten
stand: 2026-04-29
voraussetzungen: [08.01, 08.04]
lernziele:
  - End-to-End Watermark-Pipeline (C2PA + unsichtbar + Fingerprint)
  - FLUX.2 [klein] mit Watermark-Pflicht-Bändigung
  - Verifikations-Pfad für Behörden / Medien
compliance_anker:
  - mehrschicht-watermark
ai_act_artikel:
  - art-50
---

## Worum es geht

> Stop generating without watermarks. — diese Lektion baut **end-to-end** eine Multi-Layer-Watermark-Pipeline für FLUX.2-Bilder. C2PA + Stable Signature + Fingerprint. Pflicht-Pattern für AI-Act Art. 50.2 ab 02.08.2026.

## Voraussetzungen

- Lektion 08.01 (FLUX.2)
- Lektion 08.04 (Recht + Watermark-Theorie)

## Konzept

### Pipeline-Übersicht

```mermaid
flowchart LR
    Prompt[Text-Prompt] --> Gen[FLUX.2 [klein]<br/>Generation]
    Gen --> Bild[PNG/JPEG]

    Bild --> S1[Schicht 1<br/>Stable Signature<br/>unsichtbar im Pixel]
    S1 --> S2[Schicht 2<br/>C2PA-Manifest<br/>Metadata]
    S2 --> S3[Schicht 3<br/>Fingerprint-DB<br/>Hash + Modell-Version]
    S3 --> Out[Bild + Manifest]

    Out --> Verify[Verify-Pfad<br/>Behörden / Medien]

    classDef gen fill:#FF6B3D,color:#0E1116
    classDef wm fill:#3D8BFF,color:#FFF
    class Prompt,Gen,Bild gen
    class S1,S2,S3,Out,Verify wm
```

### Schritt 1 — Generation mit FLUX.2 [klein]

```python
from diffusers import FluxPipeline
import torch

pipe = FluxPipeline.from_pretrained(
    "black-forest-labs/FLUX.2-klein",
    torch_dtype=torch.bfloat16,
).to("cuda")


def generate_bild(prompt: str, seed: int = 42) -> bytes:
    generator = torch.Generator(device="cuda").manual_seed(seed)
    bild = pipe(
        prompt,
        height=1024,
        width=1024,
        num_inference_steps=28,
        guidance_scale=4.5,
        generator=generator,
    ).images[0]
    import io

    buf = io.BytesIO()
    bild.save(buf, format="PNG")
    return buf.getvalue()
```

### Schritt 2 — Schicht 1: Stable Signature (unsichtbar)

URL: <https://github.com/facebookresearch/stable_signature>

```python
import torch
from stable_signature import StableSignature

# Laden eines pre-trained Watermark-Decoders
decoder = StableSignature.load_decoder("stable_signature_decoder.pt")
embedder = StableSignature.load_embedder("stable_signature_embedder.pt")


def add_pixel_watermark(bild_bytes: bytes, message: str = "AI-2026-04") -> bytes:
    """Embedded unsichtbares Watermark in Pixel-Domain."""
    # message wird als 48-Bit-Pattern in DCT-Coefficients eingebettet
    bild_marked = embedder.encode(bild_bytes, message)
    return bild_marked


def detect_pixel_watermark(bild_bytes: bytes) -> str | None:
    """Verifikation."""
    return decoder.decode(bild_bytes)
```

### Schritt 3 — Schicht 2: C2PA-Manifest (Metadata)

URL: <https://github.com/contentauth/c2pa-python>

```python
from c2pa import builder, Reader
import json


def add_c2pa_manifest(bild_pfad: str, modell_info: dict) -> str:
    """C2PA-Manifest in EXIF / XMP einbetten."""
    manifest = {
        "claim_generator": "ki-engineering-werkstatt/1.0",
        "title": "AI-erstellt mit FLUX.2-klein",
        "assertions": [
            {
                "label": "c2pa.training-mining",
                "data": {
                    "entries": {
                        "c2pa.ai_inference": {"use": "allowed"},
                        "c2pa.ai_generative_training": {"use": "notAllowed"},
                    }
                },
            },
            {
                "label": "stds.schema-org.CreativeWork",
                "data": {
                    "@context": "https://schema.org",
                    "@type": "CreativeWork",
                    "creator": {"@type": "SoftwareApplication", "name": "FLUX.2-klein"},
                    "isBasedOn": modell_info,
                },
            },
        ],
    }

    output_pfad = bild_pfad.replace(".png", "_c2pa.png")
    builder.sign_file(
        input_path=bild_pfad,
        output_path=output_pfad,
        manifest=json.dumps(manifest),
        # Cert + Private-Key für Signatur (Adobe Demo-Zertifikate für Test)
    )
    return output_pfad


def verify_c2pa(bild_pfad: str) -> dict:
    """Manifest auslesen + verifizieren."""
    reader = Reader.from_file(bild_pfad)
    return reader.json()
```

### Schritt 4 — Schicht 3: Fingerprint-Datenbank

```python
import hashlib
from datetime import datetime, UTC


def add_fingerprint_db_entry(bild_bytes: bytes, prompt: str, modell_version: str):
    """Hash + Generation-Metadata in zentraler DB."""
    sha = hashlib.sha256(bild_bytes).hexdigest()

    db_entry = {
        "sha256": sha,
        "prompt_hash": hashlib.sha256(prompt.encode()).hexdigest()[:16],
        "modell": modell_version,
        "ts": datetime.now(UTC).isoformat(),
        "user_pseudonym_hash": "...",
    }
    insert_into_postgres("ai_outputs", db_entry)
    return sha
```

> **Wann sinnvoll**: Behörden-Anfrage prüft, ob ein verdächtiges Bild aus deinem System stammt. Fingerprint-DB-Lookup gibt Antwort mit Audit-Trail.

### Schritt 5 — Komplette Pipeline

```python
async def watermark_pipeline(prompt: str, user_pseudonym: str) -> dict:
    # 1. Generation
    bild_bytes = generate_bild(prompt)

    # 2. Schicht 1: Pixel-Watermark
    bild_marked = add_pixel_watermark(bild_bytes, message="AI-2026-04")

    # 3. Schicht 2: C2PA-Manifest
    bild_pfad = save_temp(bild_marked, ".png")
    bild_c2pa = add_c2pa_manifest(bild_pfad, {
        "name": "FLUX.2-klein",
        "version": "1.0",
        "license": "Apache 2.0",
    })

    # 4. Schicht 3: Fingerprint-DB
    sha = add_fingerprint_db_entry(
        bild_c2pa.read_bytes(),
        prompt,
        modell_version="FLUX.2-klein-v1",
    )

    # 5. Audit-Log
    log_audit({
        "user_pseudonym_hash": hash(user_pseudonym),
        "sha256": sha,
        "ai_act_compliance": "art-50.2-mehrschicht-watermark",
        "ts": datetime.now(UTC).isoformat(),
    })

    return {
        "bild_pfad": bild_c2pa,
        "sha256": sha,
        "watermark_layers": ["stable-signature", "c2pa", "fingerprint-db"],
    }
```

### Verifikations-Pfad

Behörden / Medien können prüfen:

```python
def verify_ai_image(bild_bytes: bytes) -> dict:
    """3-Schicht-Verifikation."""
    result = {"is_ai_generated": False, "confidence": 0.0, "layers": []}

    # Layer 1: Pixel-Watermark
    pixel_msg = detect_pixel_watermark(bild_bytes)
    if pixel_msg and pixel_msg.startswith("AI-"):
        result["layers"].append({"type": "pixel", "message": pixel_msg})
        result["confidence"] = 0.7

    # Layer 2: C2PA-Manifest
    try:
        manifest = verify_c2pa_from_bytes(bild_bytes)
        if "FLUX.2" in manifest.get("title", "") or "ai_generative_training" in str(manifest):
            result["layers"].append({"type": "c2pa", "manifest": manifest})
            result["confidence"] = max(result["confidence"], 0.9)
    except Exception:
        pass

    # Layer 3: Fingerprint-DB-Lookup
    sha = hashlib.sha256(bild_bytes).hexdigest()
    if db_entry := lookup_fingerprint_db(sha):
        result["layers"].append({"type": "fingerprint", "entry": db_entry})
        result["confidence"] = 1.0

    result["is_ai_generated"] = result["confidence"] >= 0.5
    return result
```

### Robustheit gegen Manipulation

| Manipulation | Schicht 1 (Pixel) | Schicht 2 (C2PA) | Schicht 3 (Fingerprint) |
|---|---|---|---|
| JPEG-Re-Compression | überlebt | manifest verloren | hash ändert sich |
| Crop / Resize | überlebt teilweise | manifest verloren | hash ändert sich |
| Screenshot | verloren | verloren | hash ändert sich |
| Bewusstes Tampering | meistens verloren | verloren | hash ändert sich |

> **Realität**: kein Watermark ist 100 % robust. Mehrschicht-Pflicht durch AI-Act, weil **mindestens eine Schicht** in 80 % der Fälle erhalten bleibt.

## Hands-on

1. FLUX.2 [klein] mit Diffusers aufsetzen
2. Stable Signature lokal embedden + verifizieren
3. C2PA-Manifest mit Adobe-Demo-Zertifikat einbauen
4. Fingerprint-DB-Skelett mit Postgres
5. Manipulations-Test: JPEG-Compression auf 70 %, dann verifizieren — welche Schichten überleben?

## Selbstcheck

- [ ] Du baust 3-Schicht-Watermark-Pipeline.
- [ ] Du verstehst Robustheit + Manipulations-Resistenz.
- [ ] Du implementierst Verifikations-Pfad für Behörden.
- [ ] Du dokumentierst Pipeline für AI-Act Art. 50.2-Audit.

## Compliance-Anker

- **AI-Act Art. 50.2**: Mehrschicht-Pflicht ab 02.08.2026
- **§ 201b StGB-Entwurf**: bei Deepfakes mit erkennbaren Personen Disclaimer + Watermark **proaktiv**

## Quellen

- C2PA Python — <https://github.com/contentauth/c2pa-python>
- Stable Signature — <https://github.com/facebookresearch/stable_signature>
- AI-Act Art. 50 — <https://artificialintelligenceact.eu/article/50/>
- EU AI Office Code of Practice — <https://digital-strategy.ec.europa.eu/en/policies/code-practice-ai-generated-content>
- Adobe Verify Tool — <https://verify.contentauthenticity.org/>

## Weiterführend

→ Phase **20** (Recht & Governance — UrhG-§-44b-Werkzeug)
→ Phase **17.05** (Docker-Compose für Generation-Stack)
