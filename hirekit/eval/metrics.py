"""Évaluation — métriques et monitoring des coûts.

AT06 — Évaluation, Benchmarking : Recall@k, MRR, cost monitoring.
"""

from __future__ import annotations


def compute_recall_at_k(
    retrieved_sources: list[str], expected_sources: list[str], k: int = 5
) -> float:
    """AT06 — calcule le Recall@k."""
    raise NotImplementedError(
        "AT06 — implémentez compute_recall_at_k() dans hirekit/eval/metrics.py"
    )


def compute_mrr(retrieved_sources: list[str], expected_sources: list[str]) -> float:
    """AT06 — calcule le Mean Reciprocal Rank."""
    raise NotImplementedError("AT06 — implémentez compute_mrr() dans hirekit/eval/metrics.py")


def compute_cost(usage_metadata: dict, model: str = "claude-sonnet-4-5") -> float:
    """AT06 — calcule le coût en euros d'une requête LLM.

    Utilise response.usage_metadata (input_tokens, output_tokens) et le pricing du modèle.
    """
    raise NotImplementedError("AT06 — implémentez compute_cost() dans hirekit/eval/metrics.py")
