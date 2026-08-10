"""Streamlit UI — interface chat multi-pages.

AT05 — UX Chatbot : recréer une expérience de type ChatGPT.

L'application Streamlit a 3 pages :
1. Chat — interface de chat avec l'agent hirekit
2. Dashboard Matching — visualisation des scores de matching
3. Bibliothèque CVs — liste et recherche de CVs

Lancez avec : streamlit run hirekit/ui/app.py
"""

from __future__ import annotations

from typing import Any


def render_chat_page() -> None:
    """AT05 — page Chat : interface de chat avec l'agent hirekit.

    Utilise st.chat_message, st.chat_input pour l'UX ChatGPT-like.
    """
    import streamlit as st

    st.title("💬 HireKit Chat")
    st.markdown("Assistant IA pour recruteurs — posez vos questions")

    # Initialiser l'historique de chat
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = [
            {"role": "assistant", "content": "Bonjour ! Je suis HireKit. Comment puis-je vous aider ?"}
        ]

    # Afficher l'historique
    for message in st.session_state.chat_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input de chat
    if prompt := st.chat_input("Posez votre question..."):
        # Ajouter le message utilisateur
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Réponse de l'assistant
        with st.chat_message("assistant"):
            with st.spinner("Réflexion..."):
                response = _process_chat_message(prompt)
                st.markdown(response)

        st.session_state.chat_messages.append({"role": "assistant", "content": response})


def _process_chat_message(message: str) -> str:
    """Traite un message de chat et retourne la réponse.

    Route vers l'agent ou les tools selon le contenu du message.
    """
    # Détection de commande
    if message.startswith("/"):
        parts = message[1:].split(" ", 1)
        command = parts[0]
        args = parts[1] if len(parts) > 1 else ""
        from hirekit.ui.telegram_bot import process_command
        return process_command(command, args)

    # Message libre → recherche de candidats
    try:
        from hirekit.agent.tools import search_cvs_tool
        result = search_cvs_tool.invoke({"query": message})
        return result
    except Exception:
        return f"Je n'ai pas pu traiter votre demande: {message}"


def render_matching_dashboard() -> None:
    """AT05 — page Dashboard Matching : visualisation des scores.

    Permet de matcher un CV avec une offre et visualise le score
    avec une jauge et les points forts/faibles.
    """
    import streamlit as st

    st.title("📊 Dashboard Matching")
    st.markdown("Évaluez la correspondance candidat ↔ offre")

    # Inputs
    col1, col2 = st.columns(2)
    with col1:
        cv_text = st.text_area("CV du candidat", height=200, placeholder="Collez le CV ici...")
    with col2:
        offer_text = st.text_area("Offre d'emploi", height=200, placeholder="Collez l'offre ici...")

    if st.button("Évaluer le matching", type="primary"):
        if not cv_text or not offer_text:
            st.warning("Veuillez remplir le CV et l'offre.")
            return

        with st.spinner("Évaluation..."):
            try:
                from hirekit.services.matching import get_matching_chain
                chain = get_matching_chain()
                result = chain.invoke({"cv": cv_text, "offer": offer_text})

                # Afficher le score
                col_s1, col_s2 = st.columns([1, 2])
                with col_s1:
                    st.metric("Score", f"{result.score:.0%}")
                with col_s2:
                    st.metric("Recommandation", result.recommandation)

                # Points forts et faibles
                col_f1, col_f2 = st.columns(2)
                with col_f1:
                    st.success("**Points forts**")
                    for pf in result.points_forts:
                        st.write(f"✓ {pf}")
                with col_f2:
                    st.warning("**Points faibles**")
                    for pfa in result.points_faibles:
                        st.write(f"✗ {pfa}")

                st.info(f"**Justification:** {result.justification}")
            except Exception as e:
                st.error(f"Erreur: {e}")


def render_cv_library() -> None:
    """AT05 — page Bibliothèque CVs : liste et recherche de CVs.

    Affiche tous les CVs disponibles et permet de rechercher
    par mot-clé via l'index FAISS.
    """
    import streamlit as st

    st.title("📚 Bibliothèque CVs")
    st.markdown(f"{30} CVs disponibles")

    # Recherche
    search_query = st.text_input("🔍 Rechercher un candidat...", placeholder="React, Python, DevOps...")

    if search_query:
        with st.spinner("Recherche..."):
            try:
                from hirekit.rag.vectorstore_faiss import search_cvs
                results = search_cvs(search_query, k=5)
                for i, doc in enumerate(results, 1):
                    filename = doc.metadata.get("filename", "unknown")
                    with st.expander(f"CV #{i} — {filename}"):
                        st.text(doc.page_content[:500])
            except Exception as e:
                st.warning(f"Index non disponible. Lancez la solution AT03 d'abord.\nErreur: {e}")

    # Lister tous les CVs depuis cvs_data.json
    try:
        import json
        from hirekit.config import CVS_DIR

        cvs_data_path = CVS_DIR.parent / "cvs" / "cvs_data.json"
        if cvs_data_path.exists():
            cvs = json.loads(cvs_data_path.read_text(encoding="utf-8"))
            st.subheader("Tous les candidats")
            for cv in cvs:
                with st.expander(f"{cv['nom']} — {cv['titre']}"):
                    st.write(f"**Email:** {cv['email']}")
                    st.write(f"**Catégorie:** {cv['categorie']}")
                    st.write(f"**Anglais:** {cv['anglais']}")
                    skills = [f"{s['nom']} ({s['niveau']}, {s['annees']} ans)" for s in cv["competences"]]
                    st.write(f"**Compétences:** {', '.join(skills)}")
    except Exception:
        st.info("Données CVs non disponibles.")


def render_multimodal_page() -> None:
    """AT05 — page Multimodal : transcription vocale (mock) + TTS (mock).

    Introduit les assistants multimodaux audio/vocal via des mocks.
    """
    import streamlit as st

    st.title("🎙️ Multimodal (Audio/Vocal)")
    st.markdown("Transcription vocale → texte → LLM, et Text-to-Speech")

    st.subheader("Transcription vocale (mock)")
    audio_input = st.text_input("Simulez une transcription vocale...", placeholder="Qui a de l'expérience en React ?")

    if audio_input and st.button("Traiter"):
        st.info(f"Transcription reçue: \"{audio_input}\"")
        response = _process_chat_message(audio_input)
        st.write(f"**Réponse:** {response}")

    st.subheader("Text-to-Speech (mock)")
    text_to_speak = st.text_area("Texte à vocaliser", placeholder="Marie Dubois a 4 ans d'expérience en React.")
    if text_to_speak and st.button("🔊 Vocaliser (mock)"):
        st.info(f"[TTS simulé] {text_to_speak}")


def main() -> None:
    """AT05 — lance l'application Streamlit (chat + dashboard + bibliothèque)."""
    import streamlit as st

    st.set_page_config(
        page_title="AI-HireKit",
        page_icon="🎯",
        layout="wide",
    )

    # Navigation multi-pages
    page = st.sidebar.selectbox(
        "Navigation",
        ["💬 Chat", "📊 Dashboard Matching", "📚 Bibliothèque CVs", "🎙️ Multimodal"],
    )

    if "Chat" in page:
        render_chat_page()
    elif "Dashboard" in page:
        render_matching_dashboard()
    elif "Bibliothèque" in page:
        render_cv_library()
    elif "Multimodal" in page:
        render_multimodal_page()

    # Sidebar info
    st.sidebar.divider()
    st.sidebar.markdown("### À propos")
    st.sidebar.markdown("AI-HireKit v2.0\nFormation LangChain — Ambient IT")


if __name__ == "__main__":
    main()