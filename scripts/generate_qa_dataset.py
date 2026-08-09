#!/usr/bin/env python3
"""Générateur de dataset Q/A (150 paires) pour l'évaluation (AT06) de ai-hirekit.

US-DATA-04 — Génère data/qa_dataset.jsonl avec 150 paires question/réponse.
Les questions référencent les vrais CVs générés (ids correspondants).

Types de questions:
  - screening (50) : questions sur un CV spécifique (extraire une info)
  - matching (50)  : questions de matching candidat↔offre
  - availability (25) : questions sur les disponibilités des candidats
  - general (25)  : questions générales sur le pool de candidats

Usage:
    python scripts/generate_qa_dataset.py [--output data/qa_dataset.jsonl]

Le script est idempotent (relance = écrase, seed fixe pour reproductibilité).
"""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

RANDOM_SEED = 42

# ─── Réponses aux questions personas (AT01 hallucination test) ─────────────

PERSONA_ANSWERS = {
    "Quelle est l'expérience de Marie Dubois en React ?":
        "Marie Dubois a 4 ans d'expérience en React (niveau avancé).",
    "Combien d'années d'expérience en Python a Karim Benali ?":
        "Karim Benali a 6 ans d'expérience en Python (niveau expert).",
    "Quel est le dernier poste de Sophie Martin ?":
        "Sophie Martin a été Senior Product Owner chez ProductCorp pendant 3 ans.",
    "Quelles compétences DevOps a Léa Chen ?":
        "Léa Chen maîtrise Kubernetes, Docker, Terraform, AWS, GitLab CI, Ansible, Prometheus et Linux.",
    "Quel est le niveau d'anglais de Thomas Petit ?":
        "Thomas Petit a un niveau d'anglais technique (B2).",
}


def load_cvs_data(data_dir: Path) -> list[dict]:
    """Charge les données des CVs générés depuis cvs_data.json."""
    cvs_json = data_dir / "cvs" / "cvs_data.json"
    if not cvs_json.exists():
        raise FileNotFoundError(
            f"{cvs_json} introuvable. Lancez d'abord: python scripts/generate_cvs.py"
        )
    return json.loads(cvs_json.read_text(encoding="utf-8"))


def load_offers_data(data_dir: Path) -> list[dict]:
    """Charge les offres d'emploi générées."""
    offers_dir = data_dir / "offers"
    offers = []
    for offer_file in sorted(offers_dir.glob("offer_*.json")):
        offers.append(json.loads(offer_file.read_text(encoding="utf-8")))
    return offers


# ─── Génération des questions de screening (50) ────────────────────────────

SCREENING_TEMPLATES = [
    ("Quelle est l'expérience de {nom} en {skill} ?", "experience_skill"),
    ("Quel est le niveau de {nom} en {skill} ?", "niveau_skill"),
    ("Quelles sont les compétences de {nom} en {categorie} ?", "competences_categorie"),
    ("Quelle est la dernière expérience professionnelle de {nom} ?", "derniere_exp"),
    ("Quel est le niveau d'anglais de {nom} ?", "niveau_anglais"),
    ("Quelle est la formation de {nom} ?", "formation"),
    ("Combien d'années d'expérience a {nom} au total ?", "annees_total"),
    ("Quel est le titre de {nom} ?", "titre"),
    ("Quelle est l'entreprise la plus récente de {nom} ?", "entreprise_recente"),
    ("Quelles sont toutes les compétences de {nom} ?", "toutes_competences"),
]


def answer_screening(cv: dict, question_type: str, skill_name: str | None = None) -> str:
    """Génère la réponse attendue pour une question de screening."""
    nom = cv["nom"]

    if question_type == "experience_skill":
        for s in cv["competences"]:
            if skill_name and s["nom"].lower() == skill_name.lower():
                return f"{nom} a {s['annees']} ans d'expérience en {skill_name} (niveau {s['niveau']})."
        return f"{nom} n'a pas d'expérience documentée en {skill_name}."

    if question_type == "niveau_skill":
        for s in cv["competences"]:
            if skill_name and s["nom"].lower() == skill_name.lower():
                return f"{nom} a un niveau {s['niveau']} en {skill_name} ({s['annees']} ans d'expérience)."
        return f"{nom} n'a pas de {skill_name} dans son CV."

    if question_type == "competences_categorie":
        cat_skills = [s["nom"] for s in cv["competences"]]
        return f"{nom} a les compétences suivantes: {', '.join(cat_skills)}."

    if question_type == "derniere_exp":
        if cv["experiences"]:
            exp = cv["experiences"][0]
            return f"{nom} a été {exp['poste']} chez {exp['entreprise']} ({exp['duree']})."
        return f"{nom} n'a pas d'expérience listée."

    if question_type == "niveau_anglais":
        return f"{nom} a un niveau d'anglais: {cv['anglais']}."

    if question_type == "formation":
        formations = cv.get("formations", [])
        if formations:
            return f"{nom} a la formation suivante: {formations[0]}"
        return f"{nom} n'a pas de formation listée."

    if question_type == "annees_total":
        # Estimation: somme des années des expériences
        total = 0
        for exp in cv["experiences"]:
            duree = exp["duree"]
            if "an" in duree:
                try:
                    total += int(duree.split()[0])
                except (ValueError, IndexError):
                    pass
        return f"{nom} a environ {total} ans d'expérience professionnelle au total."

    if question_type == "titre":
        return f"Le titre de {nom} est: {cv['titre']}."

    if question_type == "entreprise_recente":
        if cv["experiences"]:
            exp = cv["experiences"][0]
            return f"L'entreprise la plus récente de {nom} est {exp['entreprise']}."
        return f"{nom} n'a pas d'expérience listée."

    if question_type == "toutes_competences":
        skills = [s["nom"] for s in cv["competences"]]
        return f"{nom} maîtrise: {', '.join(skills)}."

    return ""


def generate_screening_questions(cvs: list[dict]) -> list[dict]:
    """Génère 50 questions de screening."""
    rng = random.Random(RANDOM_SEED)
    questions = []

    # 5 questions personas (fixes)
    for i, (question, answer) in enumerate(PERSONA_ANSWERS.items()):
        cv = cvs[i]
        questions.append({
            "id": f"qa_{len(questions) + 1:03d}",
            "question": question,
            "reponse_attendue": answer,
            "sources": [cv["id"]],
            "type": "screening",
        })

    # 45 questions générées
    remaining = 50 - len(questions)
    for _ in range(remaining):
        cv = rng.choice(cvs)
        template, q_type = rng.choice(SCREENING_TEMPLATES)

        skill_name = None
        if "skill" in q_type and cv["competences"]:
            skill = rng.choice(cv["competences"])
            skill_name = skill["nom"]
            question = template.format(nom=cv["nom"], skill=skill_name)
        elif "categorie" in q_type:
            question = template.format(nom=cv["nom"], categorie=cv["categorie"])
        else:
            question = template.format(nom=cv["nom"])

        answer = answer_screening(cv, q_type, skill_name)
        questions.append({
            "id": f"qa_{len(questions) + 1:03d}",
            "question": question,
            "reponse_attendue": answer,
            "sources": [cv["id"]],
            "type": "screening",
        })

    return questions


# ─── Génération des questions de matching (50) ──────────────────────────────

MATCHING_TEMPLATES = [
    "Quels candidats correspondent le mieux à l'offre {offer_title} ?",
    "Le profil de {nom} correspond-il à l'offre {offer_title} ?",
    "Quels candidats ont les compétences requises pour l'offre {offer_title} ?",
    "Compare {nom} et {nom2} pour l'offre {offer_title}.",
    "Quel est le meilleur candidat pour le poste de {offer_title} ?",
]


def generate_matching_questions(cvs: list[dict], offers: list[dict]) -> list[dict]:
    """Génère 50 questions de matching."""
    rng = random.Random(RANDOM_SEED + 100)
    questions = []

    for _ in range(50):
        offer = rng.choice(offers)
        template = rng.choice(MATCHING_TEMPLATES)

        if "{nom2}" in template:
            cv1 = rng.choice(cvs)
            cv2 = rng.choice(cvs)
            while cv2["id"] == cv1["id"]:
                cv2 = rng.choice(cvs)
            question = template.format(nom=cv1["nom"], nom2=cv2["nom"], offer_title=offer["titre"])
            sources = [cv1["id"], cv2["id"]]
            # Réponse: identifier les compétences communes
            cv1_skills = {s["nom"] for s in cv1["competences"]}
            cv2_skills = {s["nom"] for s in cv2["competences"]}
            offer_skills = set(offer["competences"])
            match1 = cv1_skills & offer_skills
            match2 = cv2_skills & offer_skills
            answer = (
                f"{cv1['nom']} couvre {len(match1)}/{len(offer_skills)} compétences requises "
                f"({', '.join(match1) if match1 else 'aucune'}). "
                f"{cv2['nom']} couvre {len(match2)}/{len(offer_skills)} "
                f"({', '.join(match2) if match2 else 'aucune'})."
            )
        elif "{nom}" in template:
            cv = rng.choice(cvs)
            question = template.format(nom=cv["nom"], offer_title=offer["titre"])
            sources = [cv["id"]]
            cv_skills = {s["nom"] for s in cv["competences"]}
            offer_skills = set(offer["competences"])
            matched = cv_skills & offer_skills
            score = len(matched) / len(offer_skills) if offer_skills else 0
            answer = (
                f"{cv['nom']} couvre {len(matched)}/{len(offer_skills)} compétences requises "
                f"(score: {score:.0%}). Compétences matchées: {', '.join(matched) if matched else 'aucune'}."
            )
        else:
            question = template.format(offer_title=offer["titre"])
            # Trouver les meilleurs candidats
            scored = []
            for cv in cvs:
                cv_skills = {s["nom"] for s in cv["competences"]}
                offer_skills = set(offer["competences"])
                matched = cv_skills & offer_skills
                scored.append((cv["nom"], len(matched), matched))
            scored.sort(key=lambda x: x[1], reverse=True)
            top3 = scored[:3]
            answer = (
                f"Top 3 pour '{offer['titre']}': " +
                "; ".join(f"{n} ({m}/{len(offer['competences'])} compétences)" for n, m, _ in top3)
            )
            sources = [cv["id"] for cv in cvs[:5]]

        questions.append({
            "id": f"qa_screening_{len(questions) + 1:03d}".replace("screening_", ""),
            "question": question,
            "reponse_attendue": answer,
            "sources": sources,
            "type": "matching",
        })

    return questions


# ─── Génération des questions de disponibilité (25) ─────────────────────────

AVAILABILITY_TEMPLATES = [
    "{nom} est-il disponible la semaine du {date} ?",
    "Quels créneaux {nom} a-t-il disponibles ?",
    "{nom} a-t-il des créneaux disponibles le {date} ?",
    "Combien de créneaux {nom} a-t-il disponibles au total ?",
]


def generate_availability_questions(cvs: list[dict]) -> list[dict]:
    """Génère 25 questions de disponibilité."""
    rng = random.Random(RANDOM_SEED + 200)
    questions = []

    # Dates fixes pour la reproductibilité
    dates = ["2025-09-01", "2025-09-08", "2025-09-15", "2025-09-22", "2025-09-29"]

    for i in range(25):
        cv = cvs[i % len(cvs)]
        template = rng.choice(AVAILABILITY_TEMPLATES)
        date = rng.choice(dates)
        question = template.format(nom=cv["nom"], date=date)
        # Réponse simulée
        answer = f"Vérifiez les disponibilités de {cv['nom']} dans data/availability.json pour le {date}."
        questions.append({
            "id": f"qa_{i + 51:03d}",
            "question": question,
            "reponse_attendue": answer,
            "sources": [cv["id"]],
            "type": "availability",
        })

    return questions


# ─── Génération des questions générales (25) ────────────────────────────────

GENERAL_QUESTIONS = [
    "Combien de candidats ont plus de 5 ans d'expérience ?",
    "Quels candidats sont disponibles en télétravail ?",
    "Quelle est la répartition des profils par catégorie ?",
    "Quel candidat a le plus d'années d'expérience en Python ?",
    "Combien de candidats maîtrisent Docker ?",
    "Quels candidats ont un niveau d'anglais courant (C1) ?",
    "Quels candidats sont basés à Paris ?",
    "Combien de candidats ont une expérience en DevOps ?",
    "Quels candidats maîtrisent à la fois React et Node.js ?",
    "Qui a le plus d'expérience en Kubernetes ?",
    "Combien de candidats sont des juniors (moins de 3 ans d'expérience) ?",
    "Quels candidats ont une formation en informatique ?",
    "Quel profil correspond le mieux à un poste de lead technique ?",
    "Quels candidats ont de l'expérience en startup ?",
    "Combien de candidats maîtrisent Python ?",
    "Quels candidats ont une expérience en data engineering ?",
    "Quels candidats ont des compétences en design ?",
    "Quels candidats ont de l'expérience en marketing ?",
    "Combien de candidats sont des alternants ?",
    "Quels candidats ont une expérience en entreprise internationale ?",
    "Quels candidats maîtrisent à la fois le frontend et le backend ?",
    "Combien de candidats ont un niveau d'anglais B2 ou supérieur ?",
    "Quels candidats ont de l'expérience en management d'équipe ?",
    "Quels candidats sont prêts à travailler en hybride ?",
    "Quels candidats ont le profil le plus senior ?",
]


def generate_general_questions(cvs: list[dict]) -> list[dict]:
    """Génère 25 questions générales."""
    questions = []
    for i, q in enumerate(GENERAL_QUESTIONS):
        questions.append({
            "id": f"qa_{i + 76:03d}",
            "question": q,
            "reponse_attendue": f"Consultez les {len(cvs)} CVs dans data/cvs/ pour répondre.",
            "sources": [cv["id"] for cv in cvs[:5]],
            "type": "general",
        })
    return questions


def generate_qa_dataset(output_path: Path, data_dir: Path) -> list[dict]:
    """Génère le dataset QA complet (150 paires)."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    cvs = load_cvs_data(data_dir)
    offers = load_offers_data(data_dir)

    screening = generate_screening_questions(cvs)
    matching = generate_matching_questions(cvs, offers)
    availability = generate_availability_questions(cvs)
    general = generate_general_questions(cvs)

    all_questions = screening + matching + availability + general

    # Renumeroter séquentiellement
    for i, q in enumerate(all_questions, 1):
        q["id"] = f"qa_{i:03d}"

    # Écrire en JSONL
    with open(output_path, "w", encoding="utf-8") as f:
        for q in all_questions:
            f.write(json.dumps(q, ensure_ascii=False) + "\n")

    return all_questions


def main():
    parser = argparse.ArgumentParser(description="Génère le dataset QA pour ai-hirekit")
    parser.add_argument("--output", default="data/qa_dataset.jsonl", help="Fichier de sortie")
    parser.add_argument("--data-dir", default="data", help="Dossier des données (CVs, offers)")
    args = parser.parse_args()

    output_path = Path(args.output)
    data_dir = Path(args.data_dir)
    print(f"Génération du dataset QA dans {output_path} ...")

    questions = generate_qa_dataset(output_path, data_dir)

    # Statistiques
    types = {}
    for q in questions:
        types[q["type"]] = types.get(q["type"], 0) + 1

    print(f"  OK: {len(questions)} paires Q/A générées")
    print(f"  Types: {types}")
    print(f"\nTotal: {len(questions)} paires générées avec succès.")


if __name__ == "__main__":
    main()