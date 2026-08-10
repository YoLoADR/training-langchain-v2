"""Bug v2 test — GenericLoader ne charge pas les .py (glob incorrect)."""

import pytest
from pathlib import Path


class TestBugV2:
    """Bug v2 : load_python_files doit charger les fichiers .py."""

    def test_load_python_files_loads_py(self):
        from hirekit.ui.code_reviewer import load_python_files

        code_dir = Path("data/code_repo")
        if not code_dir.exists():
            pytest.skip("code_repo non généré")

        docs = load_python_files(str(code_dir))
        assert len(docs) > 0, "Doit charger des fichiers .py"

    def test_load_python_files_count(self):
        from hirekit.ui.code_reviewer import load_python_files

        code_dir = Path("data/code_repo")
        if not code_dir.exists():
            pytest.skip("code_repo non généré")

        docs = load_python_files(str(code_dir))
        # Le repo a 10 fichiers .py
        assert len(docs) >= 10

    def test_load_python_files_has_code_content(self):
        from hirekit.ui.code_reviewer import load_python_files

        code_dir = Path("data/code_repo")
        if not code_dir.exists():
            pytest.skip("code_repo non généré")

        docs = load_python_files(str(code_dir))
        # Au moins un doc doit contenir du code Python
        full_text = " ".join(d.page_content for d in docs)
        assert "def" in full_text or "class" in full_text