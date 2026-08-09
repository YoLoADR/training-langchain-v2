#!/bin/bash
# check_atelier_ready.sh — Vérifie qu'un atelier est prêt (deps, .env, données)
#
# Usage: bash scripts/check_atelier_ready.sh [AT_NUM]
#   AT_NUM: numéro de l'atelier (1-6), défaut: 01
#
# Sortie: code 0 si tout est OK, 1 si quelque chose manque.

set -euo pipefail

AT_NUM="${1:-01}"
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
EXIT_CODE=0

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

ok()   { echo -e "  ${GREEN}✓${NC} $1"; }
fail() { echo -e "  ${RED}✗${NC} $1"; EXIT_CODE=1; }
warn() { echo -e "  ${YELLOW}!${NC} $1"; }

echo "════════════════════════════════════════════════════════════"
echo "  Vérification atelier ${AT_NUM} — ai-hirekit"
echo "════════════════════════════════════════════════════════════"
echo ""

# ─── 1. Environnement Python ────────────────────────────────────────────────
echo "[1/5] Environnement Python"
if command -v python3 &>/dev/null; then
    PY_VER=$(python3 --version 2>&1)
    ok "Python: ${PY_VER}"
else
    fail "python3 non trouvé"
fi

if [ -f "${PROJECT_ROOT}/.venv/bin/activate" ]; then
    ok "Virtualenv .venv détecté"
else
    warn "Pas de .venv — utilisez: python3 -m venv .venv && source .venv/bin/activate"
fi

if python3 -c "import hirekit" 2>/dev/null; then
    ok "Package hirekit importable"
else
    fail "Package hirekit non installé — lancez: pip install -e \".[dev]\""
fi

echo ""

# ─── 2. Configuration .env ──────────────────────────────────────────────────
echo "[2/5] Configuration .env"
if [ -f "${PROJECT_ROOT}/.env" ]; then
    ok "Fichier .env présent"
    # Vérifier les clés API selon l'atelier
    case "${AT_NUM}" in
        01|1)
            if grep -q "ANTHROPIC_API_KEY=sk-" "${PROJECT_ROOT}/.env" 2>/dev/null || \
               grep -q "OPENAI_API_KEY=sk-" "${PROJECT_ROOT}/.env" 2>/dev/null; then
                ok "Clé API LLM configurée"
            else
                warn "ANTHROPIC_API_KEY ou OPENAI_API_KEY non trouvée dans .env"
            fi
            ;;
        *)
            if grep -q "ANTHROPIC_API_KEY=sk-" "${PROJECT_ROOT}/.env" 2>/dev/null || \
               grep -q "OPENAI_API_KEY=sk-" "${PROJECT_ROOT}/.env" 2>/dev/null; then
                ok "Clé API LLM configurée"
            else
                warn "Clé API LLM non configurée (nécessaire pour les tests d'intégration)"
            fi
            ;;
    esac
else
    warn "Pas de .env — copiez: cp .env.example .env && éditez avec votre clé API"
fi

echo ""

# ─── 3. Données simulées ────────────────────────────────────────────────────
echo "[3/5] Données simulées"
DATA_DIR="${PROJECT_ROOT}/data"

check_data() {
    local search_dir="$1"
    local pattern="$2"
    local label="$3"
    local min_count="$4"
    local count
    count=$(find "${search_dir}" -maxdepth 1 -name "${pattern}" 2>/dev/null | wc -l)
    if [ "${count}" -ge "${min_count}" ]; then
        ok "${label}: ${count} fichiers"
    else
        fail "${label}: ${count}/${min_count} — lancez: python scripts/generate_*.py"
    fi
}

check_data "${DATA_DIR}/cvs" "cv_*.pdf" "CVs PDF" 30
check_data "${DATA_DIR}/offers" "offer_*.json" "Offres JSON" 15

if [ -f "${DATA_DIR}/skills.csv" ]; then
    ok "skills.csv présent"
else
    fail "skills.csv manquant — lancez: python scripts/generate_skills.py"
fi

if [ -f "${DATA_DIR}/qa_dataset.jsonl" ]; then
    QA_LINES=$(wc -l < "${DATA_DIR}/qa_dataset.jsonl")
    if [ "${QA_LINES}" -ge 150 ]; then
        ok "qa_dataset.jsonl: ${QA_LINES} paires"
    else
        fail "qa_dataset.jsonl incomplet: ${QA_LINES}/150"
    fi
else
    fail "qa_dataset.jsonl manquant — lancez: python scripts/generate_qa_dataset.py"
fi

if [ -f "${DATA_DIR}/availability.json" ]; then
    ok "availability.json présent"
else
    fail "availability.json manquant — lancez: python scripts/generate_availability.py"
fi

# Code repo (AT05+)
if [ "${AT_NUM}" -ge "05" ] || [ "${AT_NUM}" = "5" ]; then
    CODE_COUNT=$(find "${DATA_DIR}/code_repo" -maxdepth 1 -name "*.py" 2>/dev/null | wc -l)
    if [ "${CODE_COUNT}" -ge 10 ]; then
        ok "code_repo: ${CODE_COUNT} fichiers"
    else
        fail "code_repo incomplet: ${CODE_COUNT}/10 fichiers"
    fi
fi

echo ""

# ─── 4. Tests ──────────────────────────────────────────────────────────────
echo "[4/5] Tests"
if python3 -m pytest --version &>/dev/null; then
    ok "pytest disponible"
else
    fail "pytest non installé — lancez: pip install pytest"
fi

echo ""

# ─── 5. Atelier spécifique ──────────────────────────────────────────────────
echo "[5/5] Atelier ${AT_NUM}"
ATELIER_DIR="${PROJECT_ROOT}/ateliers/atelier-${AT_NUM}-*"
ATELIER_PATH=$(ls -d ${ATELIER_DIR} 2>/dev/null | head -1 || true)
if [ -n "${ATELIER_PATH}" ] && [ -d "${ATELIER_PATH}" ]; then
    ok "Dossier atelier: $(basename "${ATELIER_PATH}")"

    if [ -f "${ATELIER_PATH}/GUIDE-ELEVE.md" ]; then
        ok "GUIDE-ELEVE.md présent"
    else
        fail "GUIDE-ELEVE.md manquant"
    fi

    if [ -f "${ATELIER_PATH}/exercice.py" ]; then
        ok "exercice.py présent"
    else
        warn "exercice.py manquant (placeholder non créé)"
    fi

    if [ -f "${ATELIER_PATH}/.claude/CLAUDE.md" ]; then
        ok "Scope guard (.claude/CLAUDE.md) présent"
    else
        warn "Scope guard manquant"
    fi
else
    fail "Dossier atelier ${AT_NUM} non trouvé"
fi

echo ""

# ─── Résumé ─────────────────────────────────────────────────────────────────
echo "════════════════════════════════════════════════════════════"
if [ "${EXIT_CODE}" -eq 0 ]; then
    echo -e "  ${GREEN}✓ Atelier ${AT_NUM} est prêt${NC}"
else
    echo -e "  ${RED}✗ Atelier ${AT_NUM} n'est pas prêt — voir les erreurs ci-dessus${NC}"
fi
echo "════════════════════════════════════════════════════════════"

exit ${EXIT_CODE}