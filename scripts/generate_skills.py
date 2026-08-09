#!/usr/bin/env python3
"""Générateur de la taxonomie de compétences (skills.csv) pour ai-hirekit.

US-DATA-03 — Génère data/skills.csv avec 100 compétences catégorisées.

Usage:
    python scripts/generate_skills.py [--output data/skills.csv]

Colonnes: id, nom, categorie, mots_cles
Le script est idempotent (relance = écrase).
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

# ─── 100 compétences réparties en 8 catégories ──────────────────────────────

SKILLS = [
    # ── Frontend (14) ──
    ("React", "frontend", "react js frontend hooks redux composant spa"),
    ("Vue.js", "frontend", "vue js frontend framework composant reactive"),
    ("Angular", "frontend", "angular framework typescript frontend composant"),
    ("JavaScript", "frontend", "javascript js ecmascript web frontend"),
    ("TypeScript", "frontend", "typescript ts typage javascript frontend"),
    ("HTML/CSS", "frontend", "html css web markup style responsive"),
    ("Next.js", "frontend", "next js react ssr seo frontend"),
    ("Svelte", "frontend", "svelte js frontend framework compile"),
    ("Tailwind CSS", "frontend", "tailwind css utility design frontend"),
    ("Redux", "frontend", "redux state management react frontend"),
    ("Sass/SCSS", "frontend", "sass scss css preprocessor style"),
    ("Web Components", "frontend", "web components custom elements shadow dom"),
    ("Webpack", "frontend", "webpack bundler module frontend build"),
    ("Vite", "frontend", "vite bundler frontend build fast hmr"),

    # ── Backend (22) ──
    ("Python", "backend", "python langage programmation backend scripting"),
    ("Django", "backend", "django python web framework backend orm"),
    ("FastAPI", "backend", "fastapi python api rest async backend"),
    ("Flask", "backend", "flask python web micro framework backend"),
    ("Java", "backend", "java jvm backend enterprise spring"),
    ("Spring Boot", "backend", "spring boot java backend framework microservice"),
    ("Node.js", "backend", "node js javascript backend server runtime"),
    ("Express", "backend", "express js node web framework backend"),
    ("Go", "backend", "go golang backend langage compile concurrent"),
    ("Rust", "backend", "rust langage backend systemes securise"),
    ("GraphQL", "backend", "graphql api query schema backend"),
    ("REST API", "backend", "rest api http endpoints backend microservice"),
    ("gRPC", "backend", "grpc rpc protobuf microservice backend"),
    ("NestJS", "backend", "nestjs node typescript framework backend"),
    ("C#", "backend", "c# dotnet backend microsoft framework"),
    ("PHP", "backend", "php web backend langage serveur"),
    ("Laravel", "backend", "laravel php framework backend mvc"),
    ("Ruby on Rails", "backend", "ruby rails framework backend mvc"),
    ("Microservices", "backend", "microservices architecture distributed backend"),
    ("Celery", "backend", "celery python async task queue backend"),
    ("Redis", "backend", "redis cache key-value backend session"),
    ("RabbitMQ", "backend", "rabbitmq message queue broker backend"),

    # ── DevOps (14) ──
    ("Docker", "devops", "docker conteneur container devops virtualisation"),
    ("Kubernetes", "devops", "kubernetes k8s orchestration conteneur devops"),
    ("Terraform", "devops", "terraform iac infrastructure code devops"),
    ("Ansible", "devops", "ansible automation configuration devops playbook"),
    ("AWS", "devops", "aws amazon cloud ec2 s3 devops"),
    ("GitLab CI", "devops", "gitlab ci cd pipeline devops automation"),
    ("Jenkins", "devops", "jenkins ci cd pipeline automation devops"),
    ("Prometheus", "devops", "prometheus monitoring metrics devops observabilite"),
    ("Grafana", "devops", "grafana dashboard monitoring visualisation devops"),
    ("Linux", "devops", "linux systeme unix shell devops administration"),
    ("Nginx", "devops", "nginx reverse proxy web server devops load balancer"),
    ("Helm", "devops", "helm kubernetes package manager devops chart"),
    ("ArgoCD", "devops", "argocd gitops kubernetes deploy devops"),
    ("Vault", "devops", "vault secrets management devops security"),

    # ── Data (12) ──
    ("SQL", "data", "sql base de donnees requetage data query"),
    ("PostgreSQL", "data", "postgresql postgres sql database data relationnel"),
    ("MongoDB", "data", "mongodb nosql document database data json"),
    ("Spark", "data", "spark big data distributed processing etl"),
    ("Airflow", "data", "airflow pipeline data orchestration etl dag"),
    ("Kafka", "data", "kafka streaming data event message broker"),
    ("Snowflake", "data", "snowflake data warehouse cloud analytics"),
    ("dbt", "data", "dbt data build tool transformation analytics"),
    ("Tableau", "data", "tableau bi dashboard visualisation analytics data"),
    ("Power BI", "data", "power bi microsoft dashboard analytics data"),
    ("Pandas", "data", "pandas python data analysis dataframe manipulation"),
    ("Elasticsearch", "data", "elasticsearch search engine data indexing lucene"),

    # ── Mobile (8) ──
    ("React Native", "mobile", "react native mobile cross platform ios android"),
    ("Flutter", "mobile", "flutter dart mobile cross platform google"),
    ("Swift", "mobile", "swift ios mobile apple xcode"),
    ("Kotlin", "mobile", "kotlin android mobile jvm google"),
    ("iOS", "mobile", "ios apple mobile development swift"),
    ("Android", "mobile", "android google mobile java kotlin sdk"),
    ("Xamarin", "mobile", "xamarin c# mobile cross platform microsoft"),
    ("Ionic", "mobile", "ionic hybrid mobile web angular"),

    # ── Design (10) ──
    ("Figma", "design", "figma design ui prototype collaboratif"),
    ("Sketch", "design", "sketch design ui mac vectoriel"),
    ("Photoshop", "design", "photoshop adobe design image retouchage"),
    ("Illustrator", "design", "illustrator adobe design vectoriel logo"),
    ("Design System", "design", "design system components guidelines ui library"),
    ("Prototypage", "design", "prototypage design wireframe mockup interaction"),
    ("User Research", "design", "user research ux recherche utilisateur test"),
    ("After Effects", "design", "after effects motion design animation adobe"),
    ("InVision", "design", "invision design prototype collaboration handoff"),
    ("Copywriting", "design", "copywriting content design texte ux writing"),

    # ── Soft Skills (14) ──
    ("Communication", "soft_skills", "communication expression ecrit oral clarte"),
    ("Travail en équipe", "soft_skills", "travail equipe collaboration cooperation groupe"),
    ("Leadership", "soft_skills", "leadership management encadrement vision influence"),
    ("Résolution de problèmes", "soft_skills", "resolution problemes analyse solution creativite"),
    ("Gestion du temps", "soft_skills", "gestion temps priorites organisation planning"),
    ("Adaptabilité", "soft_skills", "adaptabilite flexibilite changement resilience"),
    ("Esprit critique", "soft_skills", "esprit critique analyse reflexion judgement"),
    ("Créativité", "soft_skills", "creativite innovation idee originalite brainstorming"),
    ("Négociation", "soft_skills", "negociation persuasion argumentation deal"),
    ("Prise de décision", "soft_skills", "decision choix jugement autonomie responsabilite"),
    ("Gestion du stress", "soft_skills", "stress pression resilience calme gestion"),
    ("Empathie", "soft_skills", "empathie ecoute comprehension autrui relation"),
    ("Mentorat", "soft_skills", "mentorat coaching formation accompagnement transmission"),
    ("Curiosité", "soft_skills", "curiosite apprentissage exploration initiative"),

    # ── Languages (6) ──
    ("Anglais", "languages", "anglais english international business communication"),
    ("Espagnol", "languages", "espagnol spanish latin international"),
    ("Allemand", "languages", "allemand german europe international"),
    ("Chinois", "languages", "chinois mandarin chine international business"),
    ("Arabe", "languages", "arabe arabic moyen-orient international"),
    ("Italien", "languages", "italien italian europe latin"),
]


def generate_skills_csv(output_path: Path) -> int:
    """Génère le fichier skills.csv et retourne le nombre de compétences."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "nom", "categorie", "mots_cles"])
        for i, (nom, categorie, mots_cles) in enumerate(SKILLS, 1):
            writer.writerow([f"skill_{i:03d}", nom, categorie, mots_cles])

    return len(SKILLS)


def main():
    parser = argparse.ArgumentParser(description="Génère skills.csv pour ai-hirekit")
    parser.add_argument("--output", default="data/skills.csv", help="Fichier de sortie")
    args = parser.parse_args()

    output_path = Path(args.output)
    print(f"Génération de skills.csv dans {output_path} ...")

    count = generate_skills_csv(output_path)

    # Vérification des catégories
    categories = set()
    with open(output_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            categories.add(row["categorie"])

    print(f"  OK: {count} compétences dans {output_path}")
    print(f"  Categories ({len(categories)}): {sorted(categories)}")
    print(f"\nTotal: {count} compétences générées avec succès.")


if __name__ == "__main__":
    main()