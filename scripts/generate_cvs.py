#!/usr/bin/env python3
"""Générateur de 30 CVs PDF fictifs pour ai-hirekit.

US-DATA-01 — Génère des CVs PDF (1-2 pages) avec profils variés:
dev React, dev Python, DevOps, designer, marketing, alternant, junior fullstack,
senior backend, data engineer, PO, etc.

Usage:
    python scripts/generate_cvs.py [--output data/cvs] [--count 30]

Les CVs sont nommés cv_001.pdf à cv_030.pdf.
Le script est idempotent (relance = écrase).
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

from fpdf import FPDF

# ─── Reproductibilité ──────────────────────────────────────────────────────
RANDOM_SEED = 42
random.seed(RANDOM_SEED)

# ─── Données de génération ──────────────────────────────────────────────────

PRENOMS_F = [
    "Marie", "Sophie", "Léa", "Camille", "Emma", "Chloé", "Sarah", "Inès",
    "Manon", "Laura", "Nadia", "Yasmine", "Claire", "Julie", "Alice",
]
PRENOMS_M = [
    "Karim", "Thomas", "Lucas", "Hugo", "Nathan", "Adam", "Youssef", "Mehdi",
    "Antoine", "Théo", "Gabriel", "Raphael", "Sami", "Bilal", "Esteban",
]
NOMS = [
    "Dubois", "Martin", "Benali", "Chen", "Petit", "Bernard", "Moreau", "Laurent",
    "Lefebvre", "Roux", "Fournier", "Girard", "Bonnet", "Garcia", "Dupont",
    "Lambert", "Fontaine", "Rousseau", "Müller", "Faure", "Nguyen", "Ravino",
]

# ─── Profils de CV (10 profils différents) ──────────────────────────────────

PROFILES = [
    {
        "titre": "Développeur React Senior",
        "categorie": "frontend",
        "skills": [
            ("React", "expert", 5), ("TypeScript", "avancé", 4),
            ("JavaScript", "expert", 6), ("HTML/CSS", "avancé", 7),
            ("Next.js", "intermédiaire", 3), ("Redux", "avancé", 4),
            ("Node.js", "intermédiaire", 3), ("GraphQL", "intermédiaire", 2),
        ],
        "experiences_template": [
            ("Lead Frontend", "TechCorp", "3 ans", "Refonte de l'architecture React, mentorat de 3 développeurs"),
            ("Développeur React", "StartupXYZ", "2 ans", "Migration Angular vers React, mise en place de tests Jest"),
            ("Développeur Frontend", "WebAgency", "2 ans", "Développement de sites vitrines et dashboards"),
        ],
        "formation": ["Master Informatique, Université Paris-Saclay (2018)"],
        "anglais": "Courant (C1)",
    },
    {
        "titre": "Développeur Python Backend",
        "categorie": "backend",
        "skills": [
            ("Python", "expert", 6), ("Django", "avancé", 5),
            ("FastAPI", "avancé", 3), ("PostgreSQL", "avancé", 4),
            ("Docker", "intermédiaire", 3), ("Redis", "intermédiaire", 2),
            ("Celery", "avancé", 3), ("pytest", "avancé", 4),
        ],
        "experiences_template": [
            ("Backend Engineer", "DataTech", "3 ans", "API REST et microservices en FastAPI, gestion de 10M+ requêtes/jour"),
            ("Développeur Django", "WebFactory", "2 ans", "Maintenance et évolution d'un back-office Django"),
            ("Développeur Python", "StartupML", "1 an", "Scripts d'ETL et pipelines de données"),
        ],
        "formation": ["Master Informatique, INSA Lyon (2017)"],
        "anglais": "Technique (B2)",
    },
    {
        "titre": "DevOps Engineer",
        "categorie": "devops",
        "skills": [
            ("Kubernetes", "avancé", 4), ("Docker", "expert", 5),
            ("Terraform", "avancé", 3), ("AWS", "expert", 5),
            ("GitLab CI", "avancé", 4), ("Ansible", "intermédiaire", 3),
            ("Prometheus", "avancé", 3), ("Linux", "expert", 7),
        ],
        "experiences_template": [
            ("DevOps Engineer", "CloudScale", "3 ans", "Migration vers Kubernetes, automatisation CI/CD avec GitLab"),
            ("SysAdmin / DevOps", "InfraPlus", "2 ans", "Gestion de l'infrastructure on-premise et migration AWS"),
            ("Administrateur Système", " HostingCorp", "2 ans", "Administration Linux, scripts Bash/Ansible"),
        ],
        "formation": ["Master Réseaux & Systèmes, Université de Bordeaux (2016)"],
        "anglais": "Courant (C1)",
    },
    {
        "titre": "UX/UI Designer",
        "categorie": "design",
        "skills": [
            ("Figma", "expert", 5), ("Sketch", "avancé", 4),
            ("Photoshop", "avancé", 6), ("Illustrator", "avancé", 5),
            ("Design System", "avancé", 3), ("Prototypage", "expert", 4),
            ("User Research", "intermédiaire", 2), ("HTML/CSS", "intermédiaire", 3),
        ],
        "experiences_template": [
            ("Lead Designer", "DesignStudio", "3 ans", "Création de design systems, conception d'apps mobiles"),
            ("UX Designer", "AgencyCreative", "2 ans", "Recherche utilisateur, wireframes, prototypes Figma"),
            ("UI Designer", "WebDesignCorp", "2 ans", "Design d'interfaces web et mobiles"),
        ],
        "formation": ["DSAA Design Numérique, ENSAD Paris (2018)"],
        "anglais": "Intermédiaire (B1)",
    },
    {
        "titre": "Spécialiste Marketing Digital",
        "categorie": "marketing",
        "skills": [
            ("SEO/SEM", "avancé", 4), ("Google Ads", "avancé", 5),
            ("Content Marketing", "expert", 5), ("Analytics", "avancé", 4),
            ("Social Media", "expert", 6), ("Email Marketing", "avancé", 4),
            ("HubSpot", "intermédiaire", 3), ("Copywriting", "avancé", 5),
        ],
        "experiences_template": [
            ("Head of Marketing", "ScaleUp", "2 ans", "Stratégie marketing 360, +200% trafic organique"),
            (" Growth Manager", "TechStartup", "2 ans", "Acquisition, funnel, A/B testing, +150% conversions"),
            ("Chargée de Marketing", "AgenceCom", "2 ans", "Campagnes Facebook/Google Ads, gestion budget 50K€/mois"),
        ],
        "formation": ["Master Marketing Digital, ESSEC (2017)"],
        "anglais": "Courant (C1)",
    },
    {
        "titre": "Développeur Fullstack Junior",
        "categorie": "fullstack",
        "skills": [
            ("JavaScript", "intermédiaire", 2), ("React", "débutant", 1),
            ("Node.js", "débutant", 1), ("Python", "intermédiaire", 2),
            ("HTML/CSS", "avancé", 3), ("MongoDB", "débutant", 1),
            ("Git", "intermédiaire", 2), ("Express", "débutant", 1),
        ],
        "experiences_template": [
            ("Stage Développeur Fullstack", "WebStartup", "6 mois", "Développement frontend React et backend Node.js"),
            ("Projet école - App web", "EPITECH", "6 mois", "Création d'une app de gestion de tâches en MERN stack"),
        ],
        "formation": ["Bachelor Informatique, EPITECH (2024)"],
        "anglais": "Technique (B2)",
    },
    {
        "titre": "Alternant Développeur Backend",
        "categorie": "backend",
        "skills": [
            ("Python", "intermédiaire", 1), ("SQL", "intermédiaire", 1),
            ("Java", "débutant", 1), ("Git", "intermédiaire", 1),
            ("Spring Boot", "débutant", 1), ("Docker", "débutant", 1),
            ("Linux", "intermédiaire", 2), ("REST API", "intermédiaire", 1),
        ],
        "experiences_template": [
            ("Alternance - Backend Developer", "FinTechCorp", "1 an", "Développement d'API REST en Java Spring Boot"),
            ("Stage - Développeur Python", "DataLab", "3 mois", "Scripts d'automatisation et tests unitaires"),
        ],
        "formation": ["Master 1 Informatique, Sorbonne Université (en cours, 2025)"],
        "anglais": "Intermédiaire (B1)",
    },
    {
        "titre": "Senior Data Engineer",
        "categorie": "data",
        "skills": [
            ("Python", "expert", 6), ("Spark", "avancé", 4),
            ("Airflow", "avancé", 3), ("SQL", "expert", 7),
            ("Kafka", "avancé", 3), ("Snowflake", "intermédiaire", 2),
            ("dbt", "avancé", 2), ("AWS", "avancé", 4),
        ],
        "experiences_template": [
            ("Senior Data Engineer", "BigDataCorp", "3 ans", "Architecture de pipelines de données Spark + Airflow, 5TB/jour"),
            ("Data Engineer", "AnalyticsCo", "2 ans", "ETL, data warehouse, modélisation Snowflake"),
            ("Data Analyst", "InsightsLab", "2 ans", "Analyses SQL, dashboards Tableau, reporting"),
        ],
        "formation": ["Master Data Science, Télécom Paris (2016)"],
        "anglais": "Courant (C1)",
    },
    {
        "titre": "Product Owner",
        "categorie": "po",
        "skills": [
            ("Agile/Scrum", "expert", 5), ("Jira", "expert", 5),
            ("Product Management", "avancé", 4), ("User Stories", "expert", 5),
            ("Roadmap", "avancé", 4), ("KPI/OKR", "avancé", 3),
            ("Design Thinking", "intermédiaire", 2), ("Data Analysis", "intermédiaire", 2),
        ],
        "experiences_template": [
            ("Senior Product Owner", "ProductCorp", "3 ans", "Gestion de 3 squads, roadmap sur 18 mois, +40% NPS"),
            ("Product Owner", "AgileCorp", "2 ans", "Backlog, user stories, ceremonies Scrum"),
            ("Business Analyst", "ConsultingCo", "2 ans", "Recueil de besoins, specs fonctionnelles, MOA"),
        ],
        "formation": ["Master Management de l'Innovation, Mines Paris (2017)"],
        "anglais": "Courant (C1)",
    },
    {
        "titre": "Senior Backend Java Engineer",
        "categorie": "backend",
        "skills": [
            ("Java", "expert", 8), ("Spring Boot", "expert", 6),
            ("Microservices", "avancé", 4), ("Kafka", "avancé", 3),
            ("PostgreSQL", "expert", 6), ("Docker", "avancé", 4),
            ("Kubernetes", "intermédiaire", 2), ("JUnit", "expert", 5),
        ],
        "experiences_template": [
            ("Staff Engineer", "EnterpriseTech", "4 ans", "Architecture microservices Java, migration vers Kafka"),
            ("Senior Java Developer", "BankSoft", "3 ans", "Systèmes bancaires haute disponibilité, tests"),
            ("Java Developer", "CorpSolutions", "3 ans", "Développement d'API REST et batchs Java"),
        ],
        "formation": ["Master Informatique, Polytech Lyon (2014)"],
        "anglais": "Courant (C1)",
    },
]

# Personas de la spec produit (noms fixes pour les tests d'hallucination)
PERSONAS = [
    ("Marie", "Dubois", "Developpeuse Fullstack - 5 ans d'experience", 0),
    ("Karim", "Benali", "Developpeur Backend - 4 ans d'experience", 1),
    ("Sophie", "Martin", "Product Owner - 6 ans d'experience", 8),
    ("Léa", "Chen", "DevOps Engineer - 3 ans d'experience", 2),
    ("Thomas", "Petit", "Developpeur React - 4 ans d'experience", 0),
]

# Mapping question AT01 → réponse attendue (pour le QA dataset)
PERSONA_ANSWERS = {
    "Quelle est l'expérience de Marie Dubois en React ?": "Marie Dubois a 4 ans d'expérience en React (niveau avancé).",
    "Combien d'années d'expérience en Python a Karim Benali ?": "Karim Benali a 6 ans d'expérience en Python (niveau expert).",
    "Quel est le dernier poste de Sophie Martin ?": "Sophie Martin a été Senior Product Owner chez ProductCorp pendant 3 ans.",
    "Quelles compétences DevOps a Léa Chen ?": "Léa Chen maîtrise Kubernetes, Docker, Terraform, AWS, GitLab CI, Ansible, Prometheus et Linux.",
    "Quel est le niveau d'anglais de Thomas Petit ?": "Thomas Petit a un niveau d'anglais technique (B2).",
}


def generate_name(profile_idx: int, cv_idx: int) -> tuple[str, str]:
    """Génère un nom reproductible. Les 5 premiers CVs utilisent les personas."""
    if cv_idx < len(PERSONAS):
        return PERSONAS[cv_idx][0], PERSONAS[cv_idx][1]
    rng = random.Random(RANDOM_SEED + cv_idx)
    if cv_idx % 2 == 0:
        prenom = rng.choice(PRENOMS_F)
    else:
        prenom = rng.choice(PRENOMS_M)
    nom = rng.choice(NOMS)
    return prenom, nom


def generate_email(prenom: str, nom: str, cv_idx: int) -> str:
    """Génère un email reproductible."""
    rng = random.Random(RANDOM_SEED + cv_idx + 100)
    domains = ["gmail.com", "outlook.fr", "yahoo.fr", "proton.me", "icloud.com", "email.fr"]
    domaine = rng.choice(domains)
    return f"{prenom.lower()}.{nom.lower()}@{domaine}"


def generate_phone(cv_idx: int) -> str:
    """Génère un numéro de téléphone reproductible."""
    rng = random.Random(RANDOM_SEED + cv_idx + 200)
    parts = [str(rng.randint(0, 9)) for _ in range(8)]
    return f"06 {parts[0]}{parts[1]} {parts[2]}{parts[3]} {parts[4]}{parts[5]} {parts[6]}{parts[7]}"


def select_experiences(profile: dict, cv_idx: int) -> list[dict]:
    """Sélectionne les expériences du profil, avec variation selon l'index."""
    rng = random.Random(RANDOM_SEED + cv_idx + 300)
    exps = list(profile["experiences_template"])
    # Les 5 premiers CVs (personas) gardent toutes les expériences
    if cv_idx >= len(PERSONAS):
        # Pour les autres, on peut en retirer une aléatoirement pour la diversité
        if len(exps) > 2 and rng.random() < 0.3:
            exps.pop(rng.randint(0, len(exps) - 1))
    result = []
    for poste, entreprise, duree, desc in exps:
        result.append({
            "poste": poste.strip(),
            "entreprise": entreprise.strip(),
            "duree": duree,
            "description": desc,
        })
    return result


def build_cv_data(cv_idx: int, profile: dict, profile_idx: int) -> dict:
    """Construit le dictionnaire de données d'un CV."""
    prenom, nom = generate_name(profile_idx, cv_idx)
    titre = profile["titre"]
    # Pour les personas, utiliser le titre défini dans PERSONAS
    if cv_idx < len(PERSONAS):
        titre = PERSONAS[cv_idx][2]

    experiences = select_experiences(profile, cv_idx)

    return {
        "id": f"cv_{cv_idx + 1:03d}",
        "nom": f"{prenom} {nom}",
        "prenom": prenom,
        "nom_de_famille": nom,
        "email": generate_email(prenom, nom, cv_idx),
        "telephone": generate_phone(cv_idx),
        "titre": titre,
        "categorie": profile["categorie"],
        "competences": [
            {"nom": s[0], "niveau": s[1], "annees": s[2]}
            for s in profile["skills"]
        ],
        "experiences": experiences,
        "formations": profile["formation"],
        "anglais": profile["anglais"],
    }


class CVPDF(FPDF):
    """Générateur de PDF de CV avec mise en page simple."""

    def header(self):
        pass

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self._safe_cell(0, 10, f"CV genere par ai-hirekit - {self.page_no()}/{{nb}}", align="C")

    def _safe_cell(self, w, h=8, txt="", border=0, ln=0, align="L"):
        """Cell avec encodage sécurisé (remplace les caractères non Latin-1)."""
        safe = txt.encode("latin-1", errors="replace").decode("latin-1")
        self.cell(w, h, safe, border=border, ln=ln, align=align)


def cv_to_pdf(cv_data: dict, output_path: Path) -> None:
    """Génère un PDF de CV à partir des données structurées."""
    pdf = CVPDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # ─── En-tête: nom et titre ──────────────────────────────────────────────
    pdf.set_font("Helvetica", "B", 20)
    pdf._safe_cell(0, 10, cv_data["nom"], ln=1)
    pdf.set_font("Helvetica", "", 13)
    pdf._safe_cell(0, 8, cv_data["titre"], ln=1)
    pdf.ln(3)

    # ─── Coordonnées ────────────────────────────────────────────────────────
    pdf.set_font("Helvetica", "", 10)
    pdf._safe_cell(0, 6, f"Email: {cv_data['email']}", ln=1)
    pdf._safe_cell(0, 6, f"Telephone: {cv_data['telephone']}", ln=1)
    pdf.ln(5)

    # ─── Compétences ────────────────────────────────────────────────────────
    pdf.set_font("Helvetica", "B", 12)
    pdf._safe_cell(0, 8, "Competences", ln=1)
    pdf.ln(2)
    pdf.set_font("Helvetica", "", 10)
    for skill in cv_data["competences"]:
        line = f"  - {skill['nom']} ({skill['niveau']}, {skill['annees']} ans)"
        pdf._safe_cell(0, 6, line, ln=1)
    pdf.ln(5)

    # ─── Expériences ─────────────────────────────────────────────────────────
    pdf.set_font("Helvetica", "B", 12)
    pdf._safe_cell(0, 8, "Experiences professionnelles", ln=1)
    pdf.ln(2)
    pdf.set_font("Helvetica", "", 10)
    for exp in cv_data["experiences"]:
        pdf.set_font("Helvetica", "B", 10)
        pdf._safe_cell(0, 6, f"  {exp['poste']} - {exp['entreprise']}", ln=1)
        pdf.set_font("Helvetica", "I", 9)
        pdf._safe_cell(0, 5, f"  Duree: {exp['duree']}", ln=1)
        pdf.set_font("Helvetica", "", 10)
        pdf._safe_cell(0, 6, f"  {exp['description']}", ln=1)
        pdf.ln(3)
    pdf.ln(3)

    # ─── Formation ──────────────────────────────────────────────────────────
    pdf.set_font("Helvetica", "B", 12)
    pdf._safe_cell(0, 8, "Formation", ln=1)
    pdf.ln(2)
    pdf.set_font("Helvetica", "", 10)
    for formation in cv_data["formations"]:
        pdf._safe_cell(0, 6, f"  - {formation}", ln=1)
    pdf.ln(5)

    # ─── Langues ────────────────────────────────────────────────────────────
    pdf.set_font("Helvetica", "B", 12)
    pdf._safe_cell(0, 8, "Langues", ln=1)
    pdf.ln(2)
    pdf.set_font("Helvetica", "", 10)
    pdf._safe_cell(0, 6, f"  - Anglais: {cv_data['anglais']}", ln=1)

    pdf.output(str(output_path))


def generate_all_cvs(output_dir: Path, count: int = 30) -> list[dict]:
    """Génère tous les CVs PDF et retourne les données structurées."""
    output_dir.mkdir(parents=True, exist_ok=True)

    all_cv_data = []
    for i in range(count):
        profile_idx = i % len(PROFILES)
        profile = PROFILES[profile_idx]
        cv_data = build_cv_data(i, profile, profile_idx)
        all_cv_data.append(cv_data)

        pdf_path = output_dir / f"cv_{i + 1:03d}.pdf"
        cv_to_pdf(cv_data, pdf_path)

    # Sauvegarder aussi les données structurées en JSON (utile pour les tests et le RAG)
    json_path = output_dir / "cvs_data.json"
    json_path.write_text(json.dumps(all_cv_data, ensure_ascii=False, indent=2), encoding="utf-8")

    return all_cv_data


def main():
    parser = argparse.ArgumentParser(description="Génère des CVs PDF fictifs pour ai-hirekit")
    parser.add_argument("--output", default="data/cvs", help="Dossier de sortie (défaut: data/cvs)")
    parser.add_argument("--count", type=int, default=30, help="Nombre de CVs (défaut: 30)")
    args = parser.parse_args()

    output_dir = Path(args.output)
    print(f"Génération de {args.count} CVs PDF dans {output_dir}/ ...")

    cv_data_list = generate_all_cvs(output_dir, args.count)

    # Vérification
    pdfs = list(output_dir.glob("cv_*.pdf"))
    print(f"  OK: {len(pdfs)} fichiers PDF générés")
    print(f"  Données structurées: {output_dir / 'cvs_data.json'}")

    # Vérification des personas
    for i, (prenom, nom, _, _) in enumerate(PERSONAS):
        pdf = output_dir / f"cv_{i + 1:03d}.pdf"
        if pdf.exists():
            print(f"  Persona {i + 1}: {prenom} {nom} -> {pdf.name}")

    print(f"\nTotal: {len(cv_data_list)} CVs générés avec succès.")


if __name__ == "__main__":
    main()