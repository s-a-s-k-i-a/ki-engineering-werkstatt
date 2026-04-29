---
id: 12.04
titel: Qualitätsfilter für deutsche Datasets — Sprache, PII, Stereotypen
phase: 12-finetuning-und-adapter
dauer_minuten: 60
schwierigkeit: mittel
stand: 2026-04-29
voraussetzungen: [12.03]
lernziele:
  - Sprach-spezifische Filter für deutsche Datasets
  - Komposita- und Umlaut-Tokenizer-Probleme bei der Daten-Erstellung berücksichtigen
  - Stereotyp-Filter mit GerBBQ+ als Test-Set
  - Pflicht-Pipeline für Production-Datasets in DACH
compliance_anker:
  - bias-audit-pflicht
  - artikel-10-data-governance
ai_act_artikel:
  - art-10
  - art-15
dsgvo_artikel:
  - art-5
---

## Worum es geht

> Stop ignoring „Müller" being tokenized as 4 tokens. — deutsche Datasets haben spezifische Probleme: Komposita, Umlaute, Du/Sie, Genus-Konstruktionen, regionale Stereotypen. Diese Lektion zeigt die DACH-spezifische Filter-Pipeline.

## Voraussetzungen

- Lektion 12.03 (Datensatz-Aufbau, allgemeine Filter)
- Phase 05.01 (BPE + Deutsch — Tokenizer-Effizienz)

## Konzept

### Probleme deutscher Datasets

| Problem | Beispiel | Filter-Strategie |
|---|---|---|
| **Englisch-Mix** | „Du kannst das mit pip installieren..." | fasttext-Detektor mit threshold ≥ 0.85 |
| **Schweizer Hochdeutsch** | „ss" statt „ß" | optional zulassen, dokumentieren |
| **Du/Sie inkonsistent** | Mix in einem Beispiel | Stil-Konsistenz-Score |
| **Komposita-Fehler** | „Personen-Auto" statt „Personenauto" | Rechtschreib-Hunspell-Check |
| **Regionale Stereotypen** | „Bayern sind dumm" | GerBBQ+-Filter |
| **Übersetzungs-DE** | „Klick hier um fortzufahren" | Stilistik-LLM-Score |

### Sprach-Detektor mit Stil-Konsistenz

```python
import fasttext

modell_de = fasttext.load_model("lid.176.bin")

def stil_konsistenz(text: str) -> dict:
    """Gibt Du/Sie-Verhältnis und Konsistenz zurück."""
    du_marker = ["du ", "dich ", "dir ", "dein", "deinem", "deiner"]
    sie_marker = ["sie ", "ihnen ", "ihr ", "ihre", "ihrem", "ihrer"]

    text_lower = text.lower()
    du_count = sum(text_lower.count(m) for m in du_marker)
    sie_count = sum(text_lower.count(m) for m in sie_marker)

    total = du_count + sie_count
    if total == 0:
        return {"stil": "neutral", "konsistent": True}

    du_ratio = du_count / total
    return {
        "stil": "du" if du_ratio > 0.7 else "sie" if du_ratio < 0.3 else "gemischt",
        "konsistent": du_ratio > 0.85 or du_ratio < 0.15,
    }


def deutsch_filter(text: str) -> bool:
    """Pflicht-Filter für DE-Datasets."""
    pred = modell_de.predict(text.replace("\n", " "), k=1)
    if pred[0][0] != "__label__de" or pred[1][0] < 0.85:
        return False
    konsistenz = stil_konsistenz(text)
    if konsistenz["stil"] == "gemischt":
        return False  # Du/Sie-Mix verschmutzt das Modell
    return True
```

### Komposita + Rechtschreibung mit Hunspell

```python
import hunspell

speller = hunspell.HunSpell("/usr/share/hunspell/de_DE.dic", "/usr/share/hunspell/de_DE.aff")

def rechtschreib_score(text: str) -> float:
    """Anteil korrekt geschriebener Wörter."""
    woerter = [w.strip(".,!?") for w in text.split() if len(w) > 2]
    if not woerter:
        return 1.0
    korrekt = sum(speller.spell(w) for w in woerter)
    return korrekt / len(woerter)
```

> Pattern: nur Beispiele mit Score ≥ 0.92 zulassen. Bei < 0.92: oft maschinell übersetzt oder grobe Fehler.

### PII-Filter — DE-spezifisch

Deutsche PII-Pattern, die englische Tools übersehen:

```python
import re

DE_PII = {
    "personalausweis": re.compile(r"\b[T-Z]\d{8}[A-Z]\d{6}[A-Z]\d{0,2}\b"),
    "iban_de": re.compile(r"\bDE\d{20}\b"),
    "kfz_kennzeichen": re.compile(r"\b[A-ZÄÖÜ]{1,3}-?[A-Z]{1,2}\s?\d{1,4}\b"),
    "steuer_id": re.compile(r"\b\d{11}\b"),  # 11-stellig
    "ust_id_de": re.compile(r"\bDE\d{9}\b"),
    "telefon_de": re.compile(r"\+49\s?\d[\d\s-]{8,15}|\b0\d[\d\s-]{8,15}\b"),
    "plz": re.compile(r"\b\d{5}\b"),  # Vorsicht: hohe False-Positive-Rate
    "iban_at": re.compile(r"\bAT\d{18}\b"),
    "iban_ch": re.compile(r"\bCH\d{19}\b"),
    "ahv_ch": re.compile(r"\b756\.\d{4}\.\d{4}\.\d{2}\b"),  # Schweizer Sozialversicherungs-Nr.
}

def de_pii_redaktiere(text: str) -> tuple[str, list[str]]:
    """Redaktiert + meldet, welche PII-Typen gefunden wurden."""
    gefunden = []
    for typ, pat in DE_PII.items():
        if pat.search(text):
            gefunden.append(typ)
            text = pat.sub(f"<{typ.upper()}>", text)
    return text, gefunden
```

> **Wichtig**: PLZ ist riskant — ein 5-stelliger Code könnte auch eine Postleitzahl sein. Use-Case-Test pflichtig.

### Stereotyp-Filter mit GerBBQ+

[GerBBQ+](https://huggingface.co/datasets?search=gerbbq) (deutsche Adaption von BBQ) liefert ~ 5.000 Beispiele für deutsche Bias-Kategorien. Pattern: lade GerBBQ+ als **Test-Set**, nicht als Trainings-Set.

```python
from datasets import load_dataset

# Pattern: GerBBQ+ als Eval-Filter
gerbbq = load_dataset("path/to/gerbbq-plus", split="test")

def baut_stereotyp_assertion(beispiel: dict) -> str:
    """Aus GerBBQ+ generiert man einen Test-Pattern."""
    return f"Stereotyp-Check: {beispiel['frage']}"
```

Im Eval-Loop nach dem Training: läuft das Modell durch die GerBBQ+-Probes und Bias-Score wird gemessen (Phase 18.02 detailliert).

### LLM-Quality-Score auf Deutsch

```python
from pydantic_ai import Agent
from pydantic import BaseModel, Field

class DeutschQualitaet(BaseModel):
    grammatik: int = Field(ge=1, le=5, description="1=fehlerhaft, 5=perfekt")
    natuerlichkeit: int = Field(ge=1, le=5, description="1=übersetzt-klingend, 5=Native-DE")
    kompositum_korrekt: bool
    pii_clean: bool
    stil_konsistent: bool
    begruendung: str = Field(min_length=10, max_length=200)

de_qualitaets_agent = Agent(
    "anthropic:claude-haiku-4-5",
    output_type=DeutschQualitaet,
    system_prompt=(
        "Bewerte den deutschen Text auf Grammatik, Natürlichkeit (Native vs. Übersetzung), "
        "Kompositum-Korrektheit, PII-Freiheit und Stil-Konsistenz (Du oder Sie durchgehend)."
    ),
)
```

Filter-Kriterium: `grammatik >= 4 AND natuerlichkeit >= 4 AND kompositum_korrekt AND pii_clean AND stil_konsistent`.

### Pipeline-Komposition

```python
from typing import Iterator

def de_qualitaets_pipeline(samples: Iterator[dict]) -> Iterator[dict]:
    """Pflicht-Pipeline für DACH-Datasets vor Finetuning."""
    for s in samples:
        text = s["messages"][-1]["content"]

        # 1. DE-Sprache + Stil-Konsistenz
        if not deutsch_filter(text):
            continue

        # 2. PII-Redaktion (mit Audit-Log)
        text_redaktiert, pii_typen = de_pii_redaktiere(text)
        if pii_typen:
            s["pii_redacted"] = pii_typen
            s["messages"][-1]["content"] = text_redaktiert

        # 3. Rechtschreibung
        if rechtschreib_score(text_redaktiert) < 0.92:
            continue

        # 4. LLM-Quality-Score (teuer, am Ende)
        score = de_qualitaets_agent.run_sync(text_redaktiert).output
        if score.grammatik < 4 or not score.kompositum_korrekt or not score.stil_konsistent:
            continue

        s["quality_score"] = score.model_dump()
        yield s
```

### Erwartete „Yield-Rate"

Bei rohen Web-Daten: ~ 5–15 % überleben die Pipeline. Bei kuratierten Quellen (interne MA-Trainings, Support-Logs): ~ 60–80 %.

> Faustregel: weniger Daten + bessere Qualität schlagen mehr Daten + schlechtere Qualität. Lieber 1.000 saubere Beispiele als 10.000 verschmutzte.

## Hands-on

1. Pipeline auf 100 Beispiele aus 10kGNAD anwenden — Yield-Rate dokumentieren
2. PII-Pattern auf einer eigenen Test-Datei testen (mit künstlich eingebauten Steuer-IDs, IBANs)
3. GerBBQ+ herunterladen — wieviele Stereotyp-Pattern findet dein Test-Modell?
4. LLM-Quality-Score auf 50 Beispiele — Cost-Analyse: lohnt sich der Aufwand?

## Selbstcheck

- [ ] Du nennst die DE-spezifischen Daten-Probleme (Komposita, Umlaute, Du/Sie).
- [ ] Du baust einen DE-PII-Filter mit Hunspell + Regex.
- [ ] Du nutzt fasttext für Sprach-Detektion mit Threshold ≥ 0.85.
- [ ] Du integrierst GerBBQ+ als Eval-Filter (nicht Training-Filter!).
- [ ] Du dokumentierst Yield-Rate und Filter-Schritte für Audit.

## Compliance-Anker

- **Daten-Governance (AI-Act Art. 10)**: Filter-Pipeline + Yield-Rate dokumentiert
- **Bias-Audit (Art. 15)**: GerBBQ+ vor und nach Training laufen lassen — Drift dokumentieren
- **Privacy by Design (DSGVO Art. 25)**: PII-Redaktion in Pipeline statt nachträglich

## Quellen

- fasttext Sprach-Detektion — <https://fasttext.cc/docs/en/language-identification.html>
- Hunspell DE — <https://github.com/wooorm/dictionaries/tree/main/dictionaries/de>
- Microsoft Presidio (DE-Support) — <https://microsoft.github.io/presidio/>
- GerBBQ+ Variant — <https://huggingface.co/datasets?search=gerbbq>
- GermanQuAD-Paper — <https://arxiv.org/abs/2104.12741>

## Weiterführend

→ Lektion **12.05** (Trainings-Stack mit dem gefilterten Datenset)
→ Phase **18.02** (Bias-Audit nach Training)
→ Phase **05.02** (Komposita + Tokenizer-Effizienz)
