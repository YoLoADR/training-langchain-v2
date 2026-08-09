#!/bin/bash
# verify_branch_scope.sh — Vérifie que les scope guards sont en place
#
# Usage: bash scripts/verify_branch_scope.sh
#
# Vérifie que chaque atelier (01-06) a un .claude/CLAUDE.md scope guard.

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
EXIT_CODE=0

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

ok()   { echo -e "  ${GREEN}✓${NC} $1"; }
fail() { echo -e "  ${RED}✗${NC} $1"; EXIT_CODE=1; }
warn() { echo -e "  ${YELLOW}!${NC} $1"; }

echo "════════════════════════════════════════════════════════════"
echo "  Vérification des scope guards — ai-hirekit"
echo "════════════════════════════════════════════════════════════"
echo ""

# Liste des ateliers
ATELIERS=(
    "atelier-01-llm-prompts-parsers"
    "atelier-02-lcel-memoire"
    "atelier-03-rag"
    "atelier-04-agents-tools"
    "atelier-05-chatbot-code-review"
    "atelier-06-eval-benchmark-deploy"
)

for atelier in "${ATELIERS[@]}"; do
    ATELIER_DIR="${PROJECT_ROOT}/ateliers/${atelier}"
    echo "[${atelier}]"

    if [ ! -d "${ATELIER_DIR}" ]; then
        fail "Dossier manquant"
        echo ""
        continue
    fi

    # .claude/CLAUDE.md
    CLAUDE_MD="${ATELIER_DIR}/.claude/CLAUDE.md"
    if [ -f "${CLAUDE_MD}" ]; then
        ok ".claude/CLAUDE.md présent"
        # Vérifier qu'il contient "Hors scope" ou "scope"
        if grep -qi "scope" "${CLAUDE_MD}"; then
            ok "Contient une section scope"
        else
            warn "Pas de section scope détectée dans CLAUDE.md"
        fi
    else
        fail ".claude/CLAUDE.md manquant"
    fi

    # .cursorrules (alternative)
    CURSORRULES="${ATELIER_DIR}/.cursorrules"
    if [ -f "${CURSORRULES}" ]; then
        ok ".cursorrules présent"
    else
        warn ".cursorrules manquant (optionnel)"
    fi

    echo ""
done

# ─── Résumé ─────────────────────────────────────────────────────────────────
echo "════════════════════════════════════════════════════════════"
if [ "${EXIT_CODE}" -eq 0 ]; then
    echo -e "  ${GREEN}✓ Tous les scope guards sont en place${NC}"
else
    echo -e "  ${RED}✗ Des scope guards sont manquants${NC}"
fi
echo "════════════════════════════════════════════════════════════"

exit ${EXIT_CODE}