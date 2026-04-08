#!/usr/bin/env bash
# ============================================================================
# AI Legal Codex — Uninstaller
# ============================================================================
set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
SKILLS_DIR="$CODEX_HOME/skills"
AGENTS_DIR="$CODEX_HOME/agents"

echo ""
echo -e "${BLUE}Uninstalling AI Legal Codex...${NC}"
echo ""

# Remove skills
SKILLS=(legal legal-review legal-risks legal-compare legal-plain legal-negotiate legal-missing legal-nda legal-terms legal-privacy legal-agreement legal-compliance legal-freelancer legal-report-pdf)

for skill in "${SKILLS[@]}"; do
    if [ -d "$SKILLS_DIR/$skill" ]; then
        rm -rf "$SKILLS_DIR/$skill"
        echo -e "  ${GREEN}✓${NC} Removed $skill"
    fi
done

# Remove agents
AGENTS=(legal-clauses legal-risks legal-compliance legal-terms legal-recommendations)

for agent in "${AGENTS[@]}"; do
    if [ -f "$AGENTS_DIR/$agent.md" ]; then
        rm "$AGENTS_DIR/$agent.md"
        echo -e "  ${GREEN}✓${NC} Removed agent: $agent"
    fi
done

echo ""
echo -e "${GREEN}Uninstall complete.${NC} All AI Legal Codex skills and analysis frameworks have been removed."
echo -e "Your Codex installation is otherwise unchanged."
echo ""
