# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "marimo",
#   "numpy>=2.0",
# ]
# ///

"""Lösungs-Skelett — Übung 01.01 — Mini-Embedding + Perplexitäts-Eval.

Smoke-test-tauglich. Nur NumPy. Keine externen API-Calls.
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
        # 🎯 Lösung Übung 01.01 — Mini-Embedding + Perplexität

        Mini-Embedding-Modell auf 25 deutschen Wörtern aus 5 Themen-Clustern.
        Eval von drei LLM-Verteilungen mit Cross-Entropy + Perplexität.
        """
    )
    return


@app.cell
def _(np):
    """Mini-Korpus + Embedding-Funktion."""

    rng = np.random.default_rng(42)

    cluster_richtungen = {
        "tier": np.array([1.0, 0.2, 0, 0, 0, 0, 0, 0]),
        "fahrzeug": np.array([0, 1.0, 0.2, 0, 0, 0, 0, 0]),
        "moebel": np.array([0, 0, 1.0, 0.2, 0, 0, 0, 0]),
        "recht": np.array([0, 0, 0, 1.0, 0.2, 0, 0, 0]),
        "werkstatt": np.array([0, 0, 0, 0, 1.0, 0.2, 0, 0]),
    }

    woerter_im_cluster = {
        "tier": ["Hund", "Katze", "Pferd", "Maus", "Vogel"],
        "fahrzeug": ["Auto", "LKW", "Fahrrad", "Zug", "Schiff"],
        "moebel": ["Stuhl", "Tisch", "Sofa", "Schrank", "Bett"],
        "recht": ["Vertrag", "Klage", "Anwalt", "Gericht", "Gesetz"],
        "werkstatt": ["Hammer", "Schraube", "Werkbank", "Bohrer", "Säge"],
    }

    embeddings: dict[str, np.ndarray] = {}
    wort_zu_cluster: dict[str, str] = {}
    for cluster, woerter in woerter_im_cluster.items():
        richtung = cluster_richtungen[cluster]
        for wort in woerter:
            v = richtung + 0.15 * rng.standard_normal(8)
            embeddings[wort] = v / np.linalg.norm(v)  # L2-normalisiert
            wort_zu_cluster[wort] = cluster

    return embeddings, wort_zu_cluster


@app.cell
def _(embeddings, np):
    """Kosinus-Ähnlichkeit (= Skalarprodukt bei L2-normalisierten Vektoren)."""

    def kosinus(a: np.ndarray, b: np.ndarray) -> float:
        return float(np.dot(a, b))

    def top_k_nachbarn(wort: str, k: int = 3) -> list[tuple[str, float]]:
        v = embeddings[wort]
        scores = [(w, kosinus(v, vk)) for w, vk in embeddings.items() if w != wort]
        scores.sort(key=lambda x: -x[1])
        return scores[:k]

    return (top_k_nachbarn,)


@app.cell
def _(np):
    """Cross-Entropy + Perplexität."""

    def cross_entropy(p_wahr: np.ndarray, q_modell: np.ndarray) -> float:
        return float(-np.sum(p_wahr * np.log(q_modell + 1e-12)))

    def perplexitaet(ce: float) -> float:
        return float(np.exp(ce))

    return cross_entropy, perplexitaet


@app.cell
def _(mo, top_k_nachbarn):
    """Top-3-Nachbarn pro Cluster-Vertreter."""
    rows_nb = []
    for ziel in ["Hund", "Auto", "Vertrag", "Hammer", "Schrank"]:
        nb = top_k_nachbarn(ziel, 3)
        rows_nb.append(f"| **{ziel}** | {', '.join(f'{w} ({s:.2f})' for w, s in nb)} |")

    mo.md(
        "## Top-3-Nachbarn pro Cluster\n\n"
        "| Wort | Top-3 Nachbarn |\n|---|---|\n" + "\n".join(rows_nb)
    )
    return


@app.cell
def _(cross_entropy, mo, np, perplexitaet):
    """LLM-Verteilungs-Eval."""
    p_wahr = np.array([1.0, 0.0, 0.0, 0.0])
    modelle = {
        "sehr-sicher (richtig)": np.array([0.95, 0.02, 0.02, 0.01]),
        "unsicher (richtig)": np.array([0.40, 0.30, 0.20, 0.10]),
        "sehr-sicher (falsch)": np.array([0.02, 0.95, 0.02, 0.01]),
    }

    rows_eval = []
    ppls = {}
    for name, q in modelle.items():
        ce_v = cross_entropy(p_wahr, q)
        ppl_v = perplexitaet(ce_v)
        ppls[name] = ppl_v
        rows_eval.append(f"| {name} | {ce_v:.3f} | {ppl_v:.2f} |")

    mo.md(
        "## Cross-Entropy + Perplexität\n\n"
        "| Modell | CE | Perplexität |\n|---|---|---|\n"
        + "\n".join(rows_eval)
        + "\n\n**Erwartung**: sehr-sicher-richtig < unsicher-richtig < sehr-sicher-falsch"
    )
    return (ppls,)


@app.cell
def _(embeddings, ppls, top_k_nachbarn, wort_zu_cluster):
    """Smoke-Test: 5 Akzeptanz-Asserts."""

    # 1. Vokabular-Größe
    assert len(embeddings) == 25, f"Erwarte 25 Wörter, hab {len(embeddings)}"

    # 2. 5 Cluster mit je 5 Wörtern
    cluster_sizes = {}
    for c in wort_zu_cluster.values():
        cluster_sizes[c] = cluster_sizes.get(c, 0) + 1
    assert all(v == 5 for v in cluster_sizes.values()), f"Cluster-Größen: {cluster_sizes}"
    assert len(cluster_sizes) == 5

    # 3. Hund-Top-3 sind alle Tier-Cluster
    hund_nb = top_k_nachbarn("Hund", 3)
    assert all(wort_zu_cluster[w] == "tier" for w, _ in hund_nb), f"Hund-Nachbarn: {hund_nb}"

    # 4. Auto-Top-3 enthalten kein Tier
    auto_nb = top_k_nachbarn("Auto", 3)
    assert not any(wort_zu_cluster[w] == "tier" for w, _ in auto_nb), f"Auto: {auto_nb}"

    # 5. Perplexität steigt monoton
    assert ppls["sehr-sicher (richtig)"] < ppls["unsicher (richtig)"]
    assert ppls["unsicher (richtig)"] < ppls["sehr-sicher (falsch)"]

    print("✅ Übung 01.01 — alle 5 Asserts grün")
    return


if __name__ == "__main__":
    app.run()
