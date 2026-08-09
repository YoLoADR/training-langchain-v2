"""Bug v2 test — Mémoire non persistée (k=0).

ConversationBufferWindowMemory avec k=0 ne retient aucun message.
Ce test vérifie que la mémoire retient bien les messages avec k=10.
"""

import pytest


class TestBugV2:
    """Bug v2 : ConversationBufferWindowMemory doit avoir k > 0."""

    def test_memory_retains_messages(self):
        """La mémoire doit retenir les messages ajoutés."""
        from hirekit.services.matching import get_recruiter_memory
        from langchain_core.messages import HumanMessage, AIMessage

        memory = get_recruiter_memory(k=10)
        memory.chat_memory.add_message(HumanMessage(content="Test"))
        memory.chat_memory.add_message(AIMessage(content="Réponse"))

        vars = memory.load_memory_variables({})
        assert "history" in vars
        assert len(vars["history"]) >= 2

    def test_memory_k_is_positive(self):
        """k doit être > 0 pour que la mémoire fonctionne."""
        from hirekit.services.matching import get_recruiter_memory

        memory = get_recruiter_memory(k=10)
        assert memory.k > 0
        assert memory.k == 10

    def test_memory_window_limits(self):
        """La fenêtre glissante doit limiter le nombre de messages retenus."""
        from hirekit.services.matching import get_recruiter_memory
        from langchain_core.messages import HumanMessage, AIMessage

        memory = get_recruiter_memory(k=2)
        # Ajouter 5 échanges (10 messages)
        for i in range(5):
            memory.chat_memory.add_message(HumanMessage(content=f"Question {i}"))
            memory.chat_memory.add_message(AIMessage(content=f"Réponse {i}"))

        vars = memory.load_memory_variables({})
        # k=2 échanges = 4 messages maximum
        assert len(vars["history"]) <= 4