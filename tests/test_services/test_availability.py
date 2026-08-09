"""Tests pour hirekit.services.availability — AT04."""
import pytest


class TestCheckAvailability:
    @pytest.mark.xfail(reason="AT04 non implémenté sur cette branche")
    def test_check_availability(self):
        from hirekit.services.availability import check_availability
        result = check_availability("2026-01-15")
        assert isinstance(result, dict)
