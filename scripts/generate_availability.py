#!/usr/bin/env python3
"""Générateur de calendrier de disponibilité JSON pour ai-hirekit.

US-DATA-05 — Génère un calendrier JSON de 30 jours de créneaux pour l'outil
de planning (AT04). 30 candidats avec des créneaux sur 30 jours.

Usage:
    python scripts/generate_availability.py [--output data/availability.json] [--days 30]

Le script est idempotent (relance = écrase, seed fixe pour reproductibilité).
"""

from __future__ import annotations

import argparse
import json
import random
from datetime import datetime, timedelta
from pathlib import Path

RANDOM_SEED = 42

# ─── Noms des candidats (alignés avec les CVs générés) ──────────────────────

CANDIDATE_NAMES = [
    "Marie Dubois", "Karim Benali", "Sophie Martin", "Léa Chen", "Thomas Petit",
    "Camille Bernard", "Hugo Moreau", "Emma Laurent", "Lucas Lefebvre", "Chloé Roux",
    "Nathan Fournier", "Sarah Girard", "Adam Bonnet", "Inès Garcia", "Théo Dupont",
    "Yasmine Lambert", "Gabriel Fontaine", "Manon Rousseau", "Sami Müller", "Laura Faure",
    "Antoine Nguyen", "Nadia Ravino", "Mehdi Bernard", "Julie Moreau", "Raphael Laurent",
    "Alice Lefebvre", "Bilal Roux", "Esteban Fournier", "Claire Girard", "Youssef Bonnet",
]


def generate_slots(base_date: datetime, num_days: int, rng: random.Random) -> list[dict]:
    """Génère des créneaux pour num_days jours, 9h-18h, créneaux d'1h."""
    slots = []
    for day_offset in range(num_days):
        current_date = base_date + timedelta(days=day_offset)
        # Samedi et dimanche = pas de créneaux
        if current_date.weekday() >= 5:
            continue
        date_str = current_date.strftime("%Y-%m-%d")
        for hour in range(9, 18):  # 9h à 17h (9 créneaux d'1h)
            # ~60% des créneaux disponibles
            available = rng.random() < 0.6
            slots.append({
                "date": date_str,
                "start": f"{hour:02d}:00",
                "end": f"{hour + 1:02d}:00",
                "available": available,
            })
    return slots


def generate_availability(output_path: Path, num_days: int = 30, num_candidates: int = 30) -> dict:
    """Génère le calendrier de disponibilité complet."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Date de base = 1er lundi à venir (reproductible: jour fixe)
    base_date = datetime(2025, 9, 1)  # lundi 1 septembre 2025

    candidates = []
    for i in range(min(num_candidates, len(CANDIDATE_NAMES))):
        rng = random.Random(RANDOM_SEED + i)
        slots = generate_slots(base_date, num_days, rng)
        available_count = sum(1 for s in slots if s["available"])
        candidates.append({
            "candidate_id": f"cv_{i + 1:03d}",
            "name": CANDIDATE_NAMES[i],
            "slots": slots,
            "total_slots": len(slots),
            "available_slots": available_count,
        })

    data = {
        "generated_at": datetime.now().isoformat(),
        "base_date": base_date.strftime("%Y-%m-%d"),
        "num_days": num_days,
        "num_candidates": len(candidates),
        "candidates": candidates,
    }

    output_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return data


def main():
    parser = argparse.ArgumentParser(description="Génère le calendrier de disponibilité pour ai-hirekit")
    parser.add_argument("--output", default="data/availability.json", help="Fichier de sortie")
    parser.add_argument("--days", type=int, default=30, help="Nombre de jours (défaut: 30)")
    parser.add_argument("--candidates", type=int, default=30, help="Nombre de candidats (défaut: 30)")
    args = parser.parse_args()

    output_path = Path(args.output)
    print(f"Génération du calendrier dans {output_path} ...")

    data = generate_availability(output_path, args.days, args.candidates)

    total_available = sum(c["available_slots"] for c in data["candidates"])
    total_slots = sum(c["total_slots"] for c in data["candidates"])
    print(f"  OK: {data['num_candidates']} candidats sur {data['num_days']} jours")
    print(f"  Total créneaux: {total_slots} (dont {total_available} disponibles)")
    print(f"  Taux de disponibilité: {total_available / total_slots * 100:.1f}%")
    print(f"\nTotal: calendrier généré avec succès.")


if __name__ == "__main__":
    main()