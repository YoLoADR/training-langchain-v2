#!/usr/bin/env python3
"""Générateur de 15 offres d'emploi JSON pour ai-hirekit.

US-DATA-02 — Génère des offres d'emploi au format JSON, alignées avec les profils CV.

Usage:
    python scripts/generate_offers.py [--output data/offers] [--count 15]

Les offres sont nommées offer_001.json à offer_015.json.
Le script est idempotent (relance = écrase).
"""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

RANDOM_SEED = 42
random.seed(RANDOM_SEED)

# ─── Offres d'emploi (15 offres alignées avec les profils CV) ────────────────

OFFERS = [
    {
        "titre": "Lead Développeur React",
        "entreprise": "TechVibes",
        "description": (
            "Nous recherchons un Lead Développeur React pour piloter la refonte de notre "
            "plateforme SaaS. Vous encadrez une équipe de 4 développeurs et définissez "
            "l'architecture frontend."
        ),
        "competences": ["React", "TypeScript", "Next.js", "Redux", "Node.js"],
        "localisation": "Paris",
        "salaire_min": 65000,
        "salaire_max": 85000,
        "contrat": "CDI",
        "experience_requise": "5+ ans",
        "teletravail": "hybride (3j/s)",
        "categorie": "frontend",
    },
    {
        "titre": "Développeur Python Backend",
        "entreprise": "DataFlow Systems",
        "description": (
            "Rejoignez notre équipe backend pour développer des APIs REST en FastAPI "
            "et maintenir nos microservices. Stack: Python, Django, FastAPI, PostgreSQL."
        ),
        "competences": ["Python", "FastAPI", "Django", "PostgreSQL", "Docker"],
        "localisation": "Lyon",
        "salaire_min": 45000,
        "salaire_max": 60000,
        "contrat": "CDI",
        "experience_requise": "3+ ans",
        "teletravail": "full remote",
        "categorie": "backend",
    },
    {
        "titre": "DevOps Engineer AWS",
        "entreprise": "CloudNatives",
        "description": (
            "Nous cherchons un DevOps Engineer pour gérer notre infrastructure AWS, "
            "automatiser nos déploiements Kubernetes et améliorer notre observabilité."
        ),
        "competences": ["Kubernetes", "Docker", "Terraform", "AWS", "GitLab CI"],
        "localisation": "Nantes",
        "salaire_min": 55000,
        "salaire_max": 75000,
        "contrat": "CDI",
        "experience_requise": "4+ ans",
        "teletravail": "hybride (2j/s)",
        "categorie": "devops",
    },
    {
        "titre": "UX/UI Designer Senior",
        "entreprise": "PixelCraft Studio",
        "description": (
            "Designer senior pour piloter la conception de nos produits digitaux. "
            "Vous créez des design systems et menez la recherche utilisateur."
        ),
        "competences": ["Figma", "Design System", "User Research", "Prototypage", "Photoshop"],
        "localisation": "Paris",
        "salaire_min": 50000,
        "salaire_max": 70000,
        "contrat": "CDI",
        "experience_requise": "4+ ans",
        "teletravail": "hybride (3j/s)",
        "categorie": "design",
    },
    {
        "titre": "Growth Marketing Manager",
        "entreprise": "ScaleUp Labs",
        "description": (
            "Pilotez la stratégie d'acquisition et d'engagement. Gestion des campagnes "
            "Google Ads, SEO, et analyse des funnel de conversion."
        ),
        "competences": ["SEO/SEM", "Google Ads", "Analytics", "Content Marketing", "HubSpot"],
        "localisation": "Bordeaux",
        "salaire_min": 45000,
        "salaire_max": 60000,
        "contrat": "CDI",
        "experience_requise": "3+ ans",
        "teletravail": "full remote",
        "categorie": "marketing",
    },
    {
        "titre": "Développeur Fullstack Junior",
        "entreprise": "StartupMakers",
        "description": (
            "Premier poste en développement fullstack. Vous travaillez sur une app "
            "MERN stack et apprenez les bonnes pratiques avec une équipe senior."
        ),
        "competences": ["JavaScript", "React", "Node.js", "MongoDB", "HTML/CSS"],
        "localisation": "Toulouse",
        "salaire_min": 32000,
        "salaire_max": 40000,
        "contrat": "CDI",
        "experience_requise": "0-2 ans",
        "teletravail": "hybride (2j/s)",
        "categorie": "fullstack",
    },
    {
        "titre": "Alternant Développeur Backend Java",
        "entreprise": "FinTechCorp",
        "description": (
            "Alternance en développement backend Java Spring Boot. Vous participez "
            "au développement d'API REST et aux tests unitaires."
        ),
        "competences": ["Java", "Spring Boot", "SQL", "Git", "Docker"],
        "localisation": "Paris",
        "salaire_min": 18000,
        "salaire_max": 24000,
        "contrat": "Alternance",
        "experience_requise": "Bac+3 en cours",
        "teletravail": "présentiel",
        "categorie": "backend",
    },
    {
        "titre": "Senior Data Engineer",
        "entreprise": "BigData Insights",
        "description": (
            "Architecture de pipelines de données à grande échelle. Stack: Spark, "
            "Airflow, Kafka, Snowflake. Vous gérez 5TB+ de données par jour."
        ),
        "competences": ["Python", "Spark", "Airflow", "Kafka", "Snowflake"],
        "localisation": "Paris",
        "salaire_min": 70000,
        "salaire_max": 95000,
        "contrat": "CDI",
        "experience_requise": "6+ ans",
        "teletravail": "hybride (3j/s)",
        "categorie": "data",
    },
    {
        "titre": "Product Owner Sénior",
        "entreprise": "ProductMakers",
        "description": (
            "PO senior pour gérer 3 squads Agile. Vous êtes responsable de la roadmap, "
            "du backlog, et des ceremonies Scrum. Expérience B2B SaaS requise."
        ),
        "competences": ["Agile/Scrum", "Jira", "User Stories", "Roadmap", "KPI/OKR"],
        "localisation": "Lille",
        "salaire_min": 60000,
        "salaire_max": 80000,
        "contrat": "CDI",
        "experience_requise": "5+ ans",
        "teletravail": "hybride (2j/s)",
        "categorie": "po",
    },
    {
        "titre": "Senior Backend Java Engineer",
        "entreprise": "Enterprise Systems",
        "description": (
            "Architecte et développe des microservices Java haute disponibilité. "
            "Migration vers Kafka et refonte de l'architecture. Systèmes bancaires."
        ),
        "competences": ["Java", "Spring Boot", "Microservices", "Kafka", "PostgreSQL"],
        "localisation": "Paris",
        "salaire_min": 75000,
        "salaire_max": 100000,
        "contrat": "CDI",
        "experience_requise": "7+ ans",
        "teletravail": "hybride (3j/s)",
        "categorie": "backend",
    },
    {
        "titre": "Développeur Frontend React",
        "entreprise": "WebApp Solutions",
        "description": (
            "Développeur React pour rejoindre une équipe de 6 personnes. Vous travaillez "
            "sur une app de gestion interne avec dashboard et visualisations."
        ),
        "competences": ["React", "JavaScript", "TypeScript", "HTML/CSS", "Redux"],
        "localisation": "Rennes",
        "salaire_min": 40000,
        "salaire_max": 55000,
        "contrat": "CDI",
        "experience_requise": "2+ ans",
        "teletravail": "full remote",
        "categorie": "frontend",
    },
    {
        "titre": "Site Reliability Engineer",
        "entreprise": "InfraOps",
        "description": (
            "SRE pour garantir la disponibilité de nos services. Monitoring Prometheus, "
            "automatisation Ansible, gestion d'incidents."
        ),
        "competences": ["Kubernetes", "Docker", "Prometheus", "Ansible", "Linux"],
        "localisation": "Strasbourg",
        "salaire_min": 50000,
        "salaire_max": 70000,
        "contrat": "CDI",
        "experience_requise": "4+ ans",
        "teletravail": "hybride (2j/s)",
        "categorie": "devops",
    },
    {
        "titre": "Content Designer / UX Writer",
        "entreprise": "DesignHub",
        "description": (
            "UX Writer pour créer le contenu de nos interfaces et améliorer l'expérience "
            "utilisateur par le mot. Microcopy, design system, recherche utilisateur."
        ),
        "competences": ["Figma", "Copywriting", "Design System", "User Research", "Content Marketing"],
        "localisation": "Lyon",
        "salaire_min": 38000,
        "salaire_max": 50000,
        "contrat": "CDI",
        "experience_requise": "2+ ans",
        "teletravail": "full remote",
        "categorie": "design",
    },
    {
        "titre": "Data Analyst Junior",
        "entreprise": "InsightsCorp",
        "description": (
            "Premier poste en data analysis. Vous créez des dashboards, des rapports "
            "et analysez les métriques produit. SQL et Python requis."
        ),
        "competences": ["SQL", "Python", "Analytics", "Tableau", "Data Analysis"],
        "localisation": "Marseille",
        "salaire_min": 35000,
        "salaire_max": 45000,
        "contrat": "CDI",
        "experience_requise": "0-2 ans",
        "teletravail": "hybride (3j/s)",
        "categorie": "data",
    },
    {
        "titre": "Scrum Master",
        "entreprise": "AgileCorp",
        "description": (
            "Scrum Master pour accompagner 2 équipes dans leur transformation Agile. "
            "Facilitation des ceremonies, coaching, amélioration continue."
        ),
        "competences": ["Agile/Scrum", "Jira", "KPI/OKR", "Coaching", "Facilitation"],
        "localisation": "Nantes",
        "salaire_min": 45000,
        "salaire_max": 60000,
        "contrat": "CDI",
        "experience_requise": "3+ ans",
        "teletravail": "hybride (2j/s)",
        "categorie": "po",
    },
]


def generate_all_offers(output_dir: Path, count: int = 15) -> list[dict]:
    """Génère toutes les offres JSON."""
    output_dir.mkdir(parents=True, exist_ok=True)

    offers = []
    for i in range(min(count, len(OFFERS))):
        offer = dict(OFFERS[i])
        offer["id"] = f"offer_{i + 1:03d}"
        offers.append(offer)

        offer_path = output_dir / f"offer_{i + 1:03d}.json"
        offer_path.write_text(json.dumps(offer, ensure_ascii=False, indent=2), encoding="utf-8")

    return offers


def main():
    parser = argparse.ArgumentParser(description="Génère des offres d'emploi JSON pour ai-hirekit")
    parser.add_argument("--output", default="data/offers", help="Dossier de sortie")
    parser.add_argument("--count", type=int, default=15, help="Nombre d'offres (défaut: 15)")
    args = parser.parse_args()

    output_dir = Path(args.output)
    print(f"Génération de {args.count} offres JSON dans {output_dir}/ ...")

    offers = generate_all_offers(output_dir, args.count)

    json_files = list(output_dir.glob("offer_*.json"))
    print(f"  OK: {len(json_files)} fichiers JSON générés")
    categories = set(o["categorie"] for o in offers)
    print(f"  Categories: {categories}")
    print(f"\nTotal: {len(offers)} offres générées avec succès.")


if __name__ == "__main__":
    main()