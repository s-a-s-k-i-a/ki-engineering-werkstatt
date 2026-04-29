# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "marimo",
#   "numpy>=2.0",
# ]
# ///

"""Embedding-Explorer & Cross-Entropy-Demo — Phase 01.

Smoke-test-tauglich. Keine Internet-Calls, keine HuggingFace-Downloads.
Alles auf synthetischen aber didaktisch realistischen Vektoren.
"""

import marimo

__generated_with = "0.23.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np

    return mo, np


@app.cell
def _(mo):
    mo.md(
        r"""
        # 📐 Mathe-Werkstatt · Phase 01

        Drei interaktive Demos:

        1. **Embedding-Nachbarn** — Kosinus-Ähnlichkeit auf deutschen Wörtern
        2. **Cross-Entropy-Demo** — drei Modell-Verteilungen, drei Loss-Werte
        3. **Gradient-Descent-Trajektorie** — Vanilla-SGD auf 2D-Toy-Loss

        Stand: 29.04.2026.
        """
    )
    return


@app.cell
def _(np):
    """Synthetisches DE-Wort-Vokabular mit handgebauten Embedding-Richtungen.

    8-dimensional, didaktisch konstruiert: ähnliche Bedeutung = nahe Vektoren.
    Alle L2-normalisiert, sodass Skalarprodukt = Kosinus-Ähnlichkeit.
    """

    rng = np.random.default_rng(42)

    def normalisiere(v):
        return v / np.linalg.norm(v)

    # Cluster: Tiere, Fahrzeuge, Möbel, Recht, Werkstatt
    cluster_richtungen = {
        "tier": np.array([1.0, 0.2, 0, 0, 0, 0, 0, 0]),
        "fahrzeug": np.array([0, 1.0, 0.2, 0, 0, 0, 0, 0]),
        "moebel": np.array([0, 0, 1.0, 0.2, 0, 0, 0, 0]),
        "recht": np.array([0, 0, 0, 1.0, 0.2, 0, 0, 0]),
        "werkstatt": np.array([0, 0, 0, 0, 1.0, 0.2, 0, 0]),
    }

    woerter_im_cluster = {
        "tier": ["Hund", "Katze", "Pferd", "Maus", "Vogel", "Fisch"],
        "fahrzeug": ["Auto", "LKW", "Fahrrad", "Zug", "Schiff", "Motorrad"],
        "moebel": ["Stuhl", "Tisch", "Sofa", "Schrank", "Bett", "Regal"],
        "recht": ["Vertrag", "Klage", "Anwalt", "Gericht", "Gesetz", "Urteil"],
        "werkstatt": ["Hammer", "Schraube", "Werkbank", "Bohrer", "Säge", "Zange"],
    }

    embeddings: dict[str, np.ndarray] = {}
    for cluster, woerter in woerter_im_cluster.items():
        richtung = cluster_richtungen[cluster]
        for wort in woerter:
            v = richtung + 0.15 * rng.standard_normal(8)
            embeddings[wort] = normalisiere(v)

    return cluster_richtungen, embeddings, rng


@app.cell
def _(embeddings, mo, np):
    """Demo 1: Top-5 Nachbarn per Kosinus."""

    def top_k_nachbarn(wort: str, k: int = 5) -> list[tuple[str, float]]:
        if wort not in embeddings:
            return []
        v = embeddings[wort]
        scores = []
        for w_kandidat, v_kandidat in embeddings.items():
            if w_kandidat == wort:
                continue
            scores.append((w_kandidat, float(np.dot(v, v_kandidat))))
        scores.sort(key=lambda x: -x[1])
        return scores[:k]

    rows_nb = []
    for ziel in ["Hund", "Auto", "Vertrag", "Hammer"]:
        nb_liste = top_k_nachbarn(ziel, 4)
        nb_str = ", ".join(f"{w} ({s:.2f})" for w, s in nb_liste)
        rows_nb.append(f"| **{ziel}** | {nb_str} |")

    mo.md(
        "## 1. Embedding-Nachbarn (Kosinus-Ähnlichkeit)\n\n"
        "| Ziel-Wort | Top-4 Nachbarn |\n"
        "|---|---|\n" + "\n".join(rows_nb)
    )
    return (top_k_nachbarn,)


@app.cell
def _(mo, np):
    """Demo 2: Cross-Entropy für drei Modell-Verteilungen."""

    def cross_entropy(p_wahr: np.ndarray, q_modell: np.ndarray) -> float:
        return float(-np.sum(p_wahr * np.log(q_modell + 1e-12)))

    def perplexitaet(ce: float) -> float:
        return float(np.exp(ce))

    p_wahr = np.array([1.0, 0.0, 0.0, 0.0])  # One-Hot, "Garten" ist richtig

    modelle = {
        "Sehr-sicher (richtig)": np.array([0.95, 0.02, 0.02, 0.01]),
        "Unsicher (richtig)": np.array([0.40, 0.30, 0.20, 0.10]),
        "Sehr-sicher (falsch)": np.array([0.02, 0.95, 0.02, 0.01]),
    }

    rows_ce = []
    for name_ce, q in modelle.items():
        ce_val = cross_entropy(p_wahr, q)
        ppl_val = perplexitaet(ce_val)
        rows_ce.append(f"| {name_ce} | `{q.tolist()}` | {ce_val:.3f} | {ppl_val:.2f} |")

    mo.md(
        "## 2. Cross-Entropy-Demo\n\n"
        "Wahres Token an Index 0 (Wahrscheinlichkeitsverteilung One-Hot).\n\n"
        "| Modell-Konfidenz | Verteilung | CE-Loss | Perplexität |\n"
        "|---|---|---|---|\n"
        + "\n".join(rows_ce)
        + "\n\n**Beobachtung**: hohe Konfidenz für **falsches** Token = "
        "deutlich höherer Loss als unsichere Verteilung."
    )
    return cross_entropy, perplexitaet


@app.cell
def _(mo, np):
    """Demo 3: Gradient Descent — Vanilla SGD vs. zu große Lernrate."""

    def loss(w: np.ndarray) -> float:
        return float((w[0] - 3) ** 2 + (w[1] + 1) ** 2)

    def gradient(w: np.ndarray) -> np.ndarray:
        return np.array([2 * (w[0] - 3), 2 * (w[1] + 1)])

    def trajektorie(start: np.ndarray, eta: float, schritte: int = 30):
        w = start.copy()
        verlauf = [(w.copy(), loss(w))]
        for _ in range(schritte):
            w = w - eta * gradient(w)
            verlauf.append((w.copy(), loss(w)))
        return verlauf

    runs = {
        "η = 0.10 (gut)": trajektorie(np.array([0.0, 0.0]), 0.10),
        "η = 0.50 (zu groß)": trajektorie(np.array([0.0, 0.0]), 0.50),
        "η = 1.05 (divergent)": trajektorie(np.array([0.0, 0.0]), 1.05, 10),
    }

    rows_gd = []
    for name_gd, verlauf in runs.items():
        end_w, end_loss = verlauf[-1]
        rows_gd.append(
            f"| {name_gd} | {len(verlauf) - 1} | "
            f"({end_w[0]:+.3f}, {end_w[1]:+.3f}) | {end_loss:.4f} |"
        )

    mo.md(
        "## 3. Gradient-Descent-Trajektorie\n\n"
        "Toy-Loss `(w₀ - 3)² + (w₁ + 1)²`, Minimum bei `(3, -1)`. "
        "Start in `(0, 0)`.\n\n"
        "| Lauf | Schritte | End-Position | End-Loss |\n"
        "|---|---|---|---|\n"
        + "\n".join(rows_gd)
        + "\n\n**Beobachtung**: η = 0.10 konvergiert sauber, "
        "η = 0.50 oszilliert, η = 1.05 divergiert."
    )
    return


@app.cell
def _(cross_entropy, embeddings, np, perplexitaet, top_k_nachbarn):
    """Smoke-Test: alle drei Demos einmal komplett ausführen."""
    assert len(embeddings) == 30, "Erwartet 30 Wörter im Vokabular"
    nb_test = top_k_nachbarn("Hund", 3)
    assert len(nb_test) == 3
    assert nb_test[0][1] > 0.5, "Nachbar zu Hund sollte hohe Ähnlichkeit haben"

    p_smoke = np.array([1.0, 0.0])
    q_smoke = np.array([0.99, 0.01])
    ce_smoke = cross_entropy(p_smoke, q_smoke)
    assert 0 < ce_smoke < 0.05, f"CE für nahe-perfekte Verteilung sollte klein sein, war {ce_smoke}"

    ppl_smoke = perplexitaet(np.log(10))
    assert abs(ppl_smoke - 10) < 0.01, f"Perplexität von log(10) sollte 10 sein, war {ppl_smoke}"

    print("✅ Phase 01 Smoke-Test grün")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Faustregeln aus Phase 01

        - **Kosinus** statt **Skalarprodukt**, wenn Vektoren nicht normalisiert sind
        - **Cross-Entropy** ist **THE** Loss für LLMs — alles andere (Perplexität, KL) sind
          Verwandte
        - **Lernrate** ist der wichtigste Hyperparameter — zu groß = Divergenz, zu klein =
          Schnecke
        - **AdamW** ist 2026 Pretraining-Standard

        ## Wichtige Hinweise

        - Synthetische Embeddings hier sind **didaktisch**, nicht repräsentativ.
          Echte deutsche Embeddings: `BAAI/bge-m3` (Apache 2.0, lokal), `mistral-embed`
          (EU-Cloud), `Aleph Alpha luminous-embedding` (Heidelberg/post-Cohere)
        - 10kGNAD ist **CC BY-NC-SA 4.0** → für kommerzielle Nutzung anderes Korpus
          (Wikitext-DE, GermEval)
        - Perplexität ist **nur intra-Modell** vergleichbar (Tokenizer-Effekt → Phase 05)
        """
    )
    return


if __name__ == "__main__":
    app.run()
