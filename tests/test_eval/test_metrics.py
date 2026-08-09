"""Tests pour hirekit.eval.metrics — AT06."""
import pytest


class TestComputeRecallAtK:
    @pytest.mark.xfail(reason="AT06 non implémenté sur cette branche")
    def test_compute_recall_at_k(self):
        from hirekit.eval.metrics import compute_recall_at_k
        recall = compute_recall_at_k(["a", "b", "c"], ["b"], k=3)
        assert recall == 1.0
