"""Évaluation — métriques et monitoring des coûts.

AT07 — Évaluation, Benchmarking : Recall@k, MRR, cost monitoring.

Inspiré de sellkit : tests step5 mesurent Recall@5 et comparent les modes.
"""

from __future__ import annotations

# Pricing par modèle (euros pour 1M tokens) — approximatif, à ajuster
MODEL_PRICING: dict[str, dict[str, float]] = {
    "claude-sonnet-4-5": {"input": 3.0, "output": 15.0},
    "claude-sonnet-4-6": {"input": 3.0, "output": 15.0},
    "claude-haiku-3-5": {"input": 0.25, "output": 1.25},
    "gpt-4o": {"input": 2.5, "output": 10.0},
    "gpt-4o-mini": {"input": 0.15, "output": 0.6},
    "ollama": {"input": 0.0, "output": 0.0},
}


def compute_recall_at_k(
    retrieved_sources: list[str], expected_sources: list[str], k: int = 5
) -> float:
    """AT07 — calcule le Recall@k.

    Recall@k = |retrieved ∩ expected| dans le top-k / |expected|

    Args:
        retrieved_sources: liste des sources retrouvées (ordonnées par pertinence).
        expected_sources: liste des sources attendues (ground truth).
        k: nombre de résultats à considérer (défaut: 5).

    Returns:
        Float entre 0.0 et 1.0. 1.0 = toutes les sources attendues dans le top-k.
    """
    if not expected_sources:
        return 0.0
    top_k = retrieved_sources[:k]
    retrieved_set = set(top_k)
    expected_set = set(expected_sources)
    hits = len(retrieved_set & expected_set)
    return hits / len(expected_set)


def compute_mrr(retrieved_sources: list[str], expected_sources: list[str]) -> float:
    """AT07 — calcule le Mean Reciprocal Rank.

    MRR = 1 / rank de la première source attendue trouvée.
    Si aucune source attendue n'est trouvée, MRR = 0.

    Args:
        retrieved_sources: liste des sources retrouvées (ordonnées par pertinence).
        expected_sources: liste des sources attendues (ground truth).

    Returns:
        Float entre 0.0 et 1.0.
    """
    expected_set = set(expected_sources)
    for i, source in enumerate(retrieved_sources, 1):
        if source in expected_set:
            return 1.0 / i
    return 0.0


def compute_cost(usage_metadata: dict, model: str = "claude-sonnet-4-5") -> float:
    """AT07 — calcule le coût en euros d'une requête LLM.

    Utilise response.usage_metadata (input_tokens, output_tokens) et le pricing du modèle.

    Args:
        usage_metadata: dict avec 'input_tokens' et 'output_tokens'.
        model: nom du modèle pour le pricing.

    Returns:
        Coût en euros.
    """
    pricing = MODEL_PRICING.get(model, MODEL_PRICING["claude-sonnet-4-5"])
    input_tokens = usage_metadata.get("input_tokens", 0)
    output_tokens = usage_metadata.get("output_tokens", 0)
    input_cost = (input_tokens / 1_000_000) * pricing["input"]
    output_cost = (output_tokens / 1_000_000) * pricing["output"]
    return input_cost + output_cost


def evaluate_qa_dataset(
    results: list[dict],
    k: int = 5,
) -> dict:
    """AT07 — évalue un dataset QA complet.

    Args:
        results: liste de dicts avec 'retrieved_sources', 'expected_sources', 'usage_metadata', 'model'.
        k: k pour Recall@k.

    Returns:
        Dict avec 'recall_at_k', 'mrr', 'total_cost'.
    """
    if not results:
        return {"recall_at_k": 0.0, "mrr": 0.0, "total_cost": 0.0}

    total_recall = 0.0
    total_mrr = 0.0
    total_cost = 0.0

    for r in results:
        retrieved = r.get("retrieved_sources", [])
        expected = r.get("expected_sources", [])
        total_recall += compute_recall_at_k(retrieved, expected, k)
        total_mrr += compute_mrr(retrieved, expected)
        total_cost += compute_cost(r.get("usage_metadata", {}), r.get("model", "claude-sonnet-4-5"))

    n = len(results)
    return {
        "recall_at_k": total_recall / n,
        "mrr": total_mrr / n,
        "total_cost": total_cost,
        "avg_cost_per_query": total_cost / n,
    }
