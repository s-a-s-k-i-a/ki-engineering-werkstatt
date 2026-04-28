# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "marimo",
#   "tiktoken>=0.8",
#   "tokenizers>=0.20",
#   "pandas>=2.2",
# ]
# ///

"""Lösung Übung 05.01 — eigener Tokenizer-Showdown auf 5 Domänen.

Smoke-Test-tauglich: nutzt eingebettete Mini-Texte und nur tiktoken/tokenizers.
Volle Lösung mit transformers-Tokenizern in der Doku der Übung beschrieben.
"""

import marimo

__generated_with = "0.10.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    """Mini-Korpus mit fünf Domänen (gemeinfrei oder paraphrasiert)."""
    domaenen = {
        "Sport": (
            "Die Bundesliga-Tabellenführung wechselt erneut: Nach dem 3:1-Auswärtssieg "
            "in Wolfsburg übernimmt der Verein die Spitze, während Bayer Leverkusen "
            "im Verfolgerduell unentschieden spielte. Trainer und Vorstand werten den "
            "Sieg als Mannschaftsleistung aus."
        ),
        "Recht": (
            "Gemäß § 44b UrhG ist die Vervielfältigung rechtmäßig zugänglicher Werke "
            "für Text- und Data-Mining zulässig, sofern der Rechteinhaber sich diese "
            "Nutzung nicht ausdrücklich vorbehalten hat. Vorbehalte müssen in "
            "maschinenlesbarer Form erfolgen, soweit Online-Inhalte betroffen sind."
        ),
        "Technik": (
            "Open-Weight-Sprachmodelle wie Pharia-1 oder Teuken-7B verwenden "
            "deutsche Subword-Tokenizer und erreichen damit eine effizientere "
            "Kodierung deutscher Komposita. Bei Anbietern wie IONOS und StackIT "
            "stehen die Modelle mit AVV verfügbar."
        ),
        "Belletristik": (
            "Über allen Gipfeln ist Ruh, in allen Wipfeln spürest du kaum einen "
            "Hauch; die Vögelein schweigen im Walde. Warte nur, balde ruhest du "
            "auch."
        ),
        "Werbung": (
            "Sichern Sie sich jetzt 30 % Rabatt auf unsere Premium-Mitgliedschaft! "
            "Exklusive Inhalte, Webinare mit Branchenexpert:innen und ein "
            "monatlicher Newsletter direkt in Ihr Postfach. Kein Risiko — jederzeit "
            "kündbar."
        ),
    }
    return (domaenen,)


@app.cell
def _(domaenen, mo):
    """Tokenisierungs-Vergleich pro Tokenizer."""
    import tiktoken
    from tokenizers import Tokenizer
    from tokenizers.models import BPE
    from tokenizers.pre_tokenizers import Whitespace
    from tokenizers.trainers import BpeTrainer

    cl100k = tiktoken.get_encoding("cl100k_base")
    o200k = tiktoken.get_encoding("o200k_base")
    gpt2 = tiktoken.get_encoding("gpt2")

    # Stellvertreter für deutsche-zentrierte Tokenizer
    de_korpus = [
        "Bundeskanzler Friedrich Schmidt erklärte am Donnerstag.",
        "Krankenhausverwaltungsrichtlinien und Mitarbeiterausbildung.",
        "Sozialversicherungsabgaben werden monatlich abgerechnet.",
        "Die Datenschutzgrundverordnung ist seit 2018 in Kraft.",
        "Rechtssichere Auftragsverarbeitungsverträge sind Pflicht.",
    ] * 100
    de_tok = Tokenizer(BPE(unk_token="<unk>"))
    de_tok.pre_tokenizer = Whitespace()
    de_tok.train_from_iterator(
        de_korpus,
        BpeTrainer(vocab_size=2_500, special_tokens=["<unk>", "<pad>", "<s>", "</s>"]),
    )

    tokenizers = {
        "GPT-2 (legacy)": lambda t: len(gpt2.encode(t)),
        "GPT-4 cl100k": lambda t: len(cl100k.encode(t)),
        "GPT-5 o200k": lambda t: len(o200k.encode(t)),
        "DE-Mini-BPE (Pharia-Stil)": lambda t: len(de_tok.encode(t).ids),
    }

    rows = []
    for tok_name, fn in tokenizers.items():
        for dom, text in domaenen.items():
            n_tokens = fn(text)
            n_woerter = len(text.split())
            rows.append(
                {
                    "Tokenizer": tok_name,
                    "Domäne": dom,
                    "Tokens": n_tokens,
                    "Wörter": n_woerter,
                    "Tokens/Wort": round(n_tokens / max(n_woerter, 1), 2),
                }
            )

    import pandas as pd

    df = pd.DataFrame(rows)
    pivot = df.pivot_table(
        index="Tokenizer",
        columns="Domäne",
        values="Tokens",
        aggfunc="sum",
    )
    pivot["Summe"] = pivot.sum(axis=1)
    mo.md(f"### Token-Vergleich pro Domäne\n\n{pivot.to_markdown()}")
    return df, pivot, pd


@app.cell
def _(df, mo):
    """Tokens-pro-Wort-Verhältnis (sprach-agnostische Effizienz)."""
    eff = df.groupby("Tokenizer")["Tokens/Wort"].agg(["mean", "min", "max"])
    eff = eff.round(2)
    mo.md(
        f"### Effizienz: Tokens pro Wort\n\n"
        f"Niedriger = besser. DE-spezifischer Tokenizer schlägt englisch-zentrierte deutlich.\n\n"
        f"{eff.to_markdown()}"
    )
    return (eff,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Empfehlung (Vorlage)

        Für die untersuchten DACH-Use-Cases empfehle ich:

        - **Newsletter / Marketing-Texte** mit hohem Volumen → Pharia-1 / Teuken-7B
          (DE-zentriert, AVV mit Aleph Alpha bzw. StackIT, ≈ 30 % weniger Tokens
          als GPT-5 auf deutschem Text)
        - **Code-Generation für DE-Doku** → Mistral Large oder Llama-3-Instruct
          (mehrsprachiger Tokenizer + starke Code-Performance)
        - **Strikte Compliance / regulierter Sektor** → Pharia-1 als Default;
          GPT-5 nur mit EU-Datazone und vollständigem AVV
        - **Asiatische Open-Weights** (Qwen3, DeepSeek-R1) sind für deutsche
          Texte effizient und Open-Source — aber siehe DACH-Disclaimer in
          [`docs/rechtliche-perspektive/asiatische-llms.md`](../../../docs/rechtliche-perspektive/asiatische-llms.md).

        Konkrete Empfehlung in deinem Projekt: passe diesen Block an dein
        Setup, Volumen und deine Compliance-Anforderungen an.
        """
    )
    return


if __name__ == "__main__":
    app.run()
