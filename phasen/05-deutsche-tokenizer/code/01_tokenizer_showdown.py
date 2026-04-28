# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "marimo",
#   "tiktoken>=0.8",
#   "tokenizers>=0.20",
#   "rich>=13.9",
# ]
# ///

"""Deutscher Tokenizer-Showdown — Marimo-Notebook.

Source-of-truth für `phasen/05-deutsche-tokenizer/lektionen/01-bpe-und-deutsch.md`.
Nutzt nur frei verfügbare Tokenizer (kein Modell-Download nötig). Smoke-Test-tauglich.
"""

import marimo

__generated_with = "0.10.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    mo.md(
        r"""
        # Deutscher Tokenizer-Showdown

        > Stop wasting tokens on German compound words.

        Wir tokenisieren denselben Satz mit fünf Tokenizern und vergleichen
        Token-Anzahl, ungefähre EUR-Kosten und Komposita-Verhalten.

        **Stand: 2026-04-27.** Preise sind Listenpreise und können sich
        wöchentlich ändern — siehe [`docs/quellen.md`](../../../docs/quellen.md).
        """
    )
    return


@app.cell
def _(mo):
    beispieltext = (
        "Die Donaudampfschifffahrtsgesellschaft erinnert ihre Mitglieder daran, "
        "dass die nächste Generalversammlung am Dienstag in Düsseldorf stattfindet. "
        "Vorstandskollegen aus Österreich und der Schweiz haben bereits zugesagt; "
        "über die Krankenhausverwaltungsrichtlinien und die "
        "Geschwindigkeitsbegrenzungssensoren wird ausführlich diskutiert. "
        "Vergessen Sie bitte nicht, Ihre Reichsmarktordnungsbeschlüsse mitzubringen."
    )
    mo.md(f"### Beispieltext\n> {beispieltext}")
    return (beispieltext,)


@app.cell
def _(beispieltext, mo):
    """Lade die fünf Tokenizer-Stellvertreter.

    Wir nutzen ausschließlich kleine Tokenizer-Files aus `tiktoken` (GPT-Familie)
    und `tokenizers`-Python (HuggingFace), damit der Smoke-Test offline-kompatibel
    bleibt. Echte Modell-Gewichte werden NICHT geladen.
    """
    import tiktoken
    from tokenizers import Tokenizer
    from tokenizers.models import BPE
    from tokenizers.pre_tokenizers import Whitespace
    from tokenizers.trainers import BpeTrainer

    cl100k = tiktoken.get_encoding("cl100k_base")  # GPT-4-Familie
    o200k = tiktoken.get_encoding("o200k_base")  # GPT-5.x-/o3-Familie

    # Mini-BPE auf rein deutschem Mini-Korpus (Stellvertreter für Pharia-Stil)
    deutsches_mini_korpus = [
        "Die Donaudampfschifffahrtsgesellschaft schickt einen Brief.",
        "Der Bundesinnenminister erklärt die Lage.",
        "Reichsmarktordnungsbeschluss und Geschwindigkeitsbegrenzungssensoren.",
        "Krankenhausverwaltungsrichtlinien und Generalversammlung in Düsseldorf.",
        "Österreich, Schweiz und Deutschland kooperieren.",
    ] * 50  # bisschen Volumen für die Stat
    pharia_stil = Tokenizer(BPE(unk_token="<unk>"))
    pharia_stil.pre_tokenizer = Whitespace()
    trainer = BpeTrainer(vocab_size=2_000, special_tokens=["<unk>", "<pad>", "<s>", "</s>"])
    pharia_stil.train_from_iterator(deutsches_mini_korpus, trainer)

    # Tokenisieren
    tokens_cl100k = cl100k.encode(beispieltext)
    tokens_o200k = o200k.encode(beispieltext)
    tokens_pharia_stil = pharia_stil.encode(beispieltext).ids

    # Stellvertreter für „Englisch-zentriert" (GPT-2-Tokenizer ohne BPE-Refresh)
    gpt2_stil = tiktoken.get_encoding("gpt2")
    tokens_gpt2 = gpt2_stil.encode(beispieltext)

    # Stellvertreter für Mistral / Llama (BPE auf gemischtem mehrsprachigem Korpus)
    # Wir nutzen erneut o200k_base als pragmatische Approximation für Smoke-Tests.
    # In der Vollversion holst du `mistral-large` / `meta-llama/Llama-3-8B`-Tokenizer.
    tokens_llama_stil = o200k.encode(beispieltext)  # Approximation

    ergebnis = {
        "GPT-2 (alt, sehr englisch)": len(tokens_gpt2),
        "GPT-4 cl100k": len(tokens_cl100k),
        "GPT-5.x / o3 o200k": len(tokens_o200k),
        "Llama-Stil (Approx.)": len(tokens_llama_stil),
        "Pharia-Stil (DE-only mini-BPE)": len(tokens_pharia_stil),
    }
    mo.md(f"### Token-Anzahl pro Tokenizer\n```\n{ergebnis!s}\n```")
    return (ergebnis,)


@app.cell
def _(ergebnis, mo):
    """Vergleichs-Tabelle mit EUR-Kosten."""
    # Listenpreise April 2026 (EUR / 1M Input-Tokens) — siehe phasen/11-llm-engineering/modul.md
    preise_eur = {
        "GPT-2 (alt, sehr englisch)": 0.00,  # nicht hosted
        "GPT-4 cl100k": 2.00,  # GPT-4-Turbo-Niveau
        "GPT-5.x / o3 o200k": 10.00,
        "Llama-Stil (Approx.)": 0.40,  # Self-hosted oder IONOS
        "Pharia-Stil (DE-only mini-BPE)": 5.00,
    }

    headers = ["Tokenizer", "Tokens", "EUR/1M Input", "EUR pro 1.000× Anfrage"]
    rows = []
    for name, n in ergebnis.items():
        eur_pro_million = preise_eur.get(name, 0)
        eur_pro_1000 = eur_pro_million * (n * 1000) / 1_000_000
        rows.append((name, n, f"{eur_pro_million:.2f}", f"{eur_pro_1000:.4f}"))

    table = "| " + " | ".join(headers) + " |\n"
    table += "| " + " | ".join(["---"] * len(headers)) + " |\n"
    for r in rows:
        table += "| " + " | ".join(str(x) for x in r) + " |\n"
    mo.md(f"### EUR-Kosten-Vergleich (Listenpreise 04/2026)\n\n{table}")
    return preise_eur, rows


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Was du in der Vollversion machst

        - Hole echte Tokenizer:
          - `from transformers import AutoTokenizer; AutoTokenizer.from_pretrained("mistralai/Mistral-Large-Instruct-2411")`
          - `AutoTokenizer.from_pretrained("Aleph-Alpha/Pharia-1-LLM-7B-control")`
          - `AutoTokenizer.from_pretrained("openGPT-X/Teuken-7B-instruct-research-v0.4")`
        - Nutze `datasets`, um 100 Artikel aus 10kGNAD zu ziehen.
        - Plotte Token-Anzahl pro Artikel als Boxplot.
        - Berechne `tokens_pro_1000_zeichen` als sprach-agnostische Effizienz-Kennzahl.
        - Erweitere die Tabelle um Output-Tokens und Output-Preise (Output ist 2-3× teurer als Input).

        Lösungsfile: [`loesungen/01_loesung.py`](../loesungen/01_loesung.py).
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Compliance-Anker

        - Embeddings & Tokenizer: Wenn du echte deutsche Texte schickst,
          muss der Provider AVV-konform sein → siehe [`compliance.md`](../compliance.md).
        - 10kGNAD ist CC BY-NC-SA → für kommerzielle Folgeprojekte:
          Wikitext-DE oder eigene anonymisierte Daten.
        - Pharia-1 ist BSI-C5/ISO-27001 zertifiziert (Heidelberg).

        ### Quellen (mit Datum)

        - [Sennrich et al. 2016 — BPE](https://arxiv.org/abs/1508.07909)
        - [Aleph Alpha Pharia-1 Tech Report 2024](https://aleph-alpha.com/introducing-pharia-1-llm-transparent-and-compliant/)
        - [LLäMmlein 2024](https://arxiv.org/abs/2411.11171)
        - [Listenpreise OpenAI/Anthropic/Mistral/Aleph Alpha — Stand 2026-04-27](../../../docs/quellen.md)
        """
    )
    return


if __name__ == "__main__":
    app.run()
