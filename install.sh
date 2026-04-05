#!/usr/bin/env bash
# ============================================================================
# AI Legal Assistant — Codex Skills Installer
# 14 Skills · 5 Analysis Frameworks · PDF Reports
# ============================================================================
set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

echo ""
echo -e "${BLUE}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                                                              ║${NC}"
echo -e "${BLUE}║${NC}   ${CYAN}AI Legal Assistant — Codex Skills${NC}                         ${BLUE}║${NC}"
echo -e "${BLUE}║${NC}   ${GREEN}14 Skills · 5 Analysis Frameworks · PDF Reports${NC}          ${BLUE}║${NC}"
echo -e "${BLUE}║                                                              ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""

# ---------------------------------------------------------------------------
# Detect script directory (handle both local and curl | bash)
# ---------------------------------------------------------------------------
GITHUB_REPO="${GITHUB_REPO:-pa4uslf/ai-legal-codex}"
TEMP_DIR=""

if [ -n "${BASH_SOURCE[0]}" ] && [ "${BASH_SOURCE[0]}" != "bash" ]; then
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    if [ -f "$SCRIPT_DIR/install.sh" ] && [ -d "$SCRIPT_DIR/skills" ]; then
        SOURCE_DIR="$SCRIPT_DIR"
        echo -e "${GREEN}Installing from local directory:${NC} $SOURCE_DIR"
    else
        SCRIPT_DIR=""
    fi
fi

if [ -z "${SCRIPT_DIR:-}" ] || [ ! -d "${SOURCE_DIR:-}" ]; then
    echo -e "${YELLOW}Cloning from GitHub...${NC}"
    TEMP_DIR=$(mktemp -d)
    if command -v git &>/dev/null; then
        git clone --depth 1 "https://github.com/$GITHUB_REPO.git" "$TEMP_DIR/repo" 2>/dev/null
        SOURCE_DIR="$TEMP_DIR/repo"
    else
        echo -e "${RED}Error: git is required for remote installation.${NC}"
        echo "Install git or run install.sh from a local clone."
        exit 1
    fi
    echo -e "${GREEN}Cloned successfully.${NC}"
fi

# ---------------------------------------------------------------------------
# Target directories
# ---------------------------------------------------------------------------
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
SKILLS_DIR="$CODEX_HOME/skills"
AGENTS_DIR="$CODEX_HOME/agents"

# ---------------------------------------------------------------------------
# Check for Codex
# ---------------------------------------------------------------------------
echo -e "${BLUE}Checking prerequisites...${NC}"
if command -v codex &>/dev/null; then
    echo -e "  ${GREEN}✓${NC} Codex CLI found"
else
    echo -e "  ${YELLOW}⚠${NC} Codex CLI not found (skills will still be installed)"
fi

# ---------------------------------------------------------------------------
# Create directories
# ---------------------------------------------------------------------------
echo -e "${BLUE}Creating directories...${NC}"
mkdir -p "$SKILLS_DIR"
echo -e "  ${GREEN}✓${NC} Skills directory ready"

mkdir -p "$AGENTS_DIR"
echo -e "  ${GREEN}✓${NC} Analysis framework directory ready"

# ---------------------------------------------------------------------------
# Install main skill orchestrator
# ---------------------------------------------------------------------------
echo -e "${BLUE}Installing skills...${NC}"

INSTALL_COUNT=0

if [ -f "$SOURCE_DIR/legal/SKILL.md" ]; then
    mkdir -p "$SKILLS_DIR/legal"
    cp "$SOURCE_DIR/legal/SKILL.md" "$SKILLS_DIR/legal/SKILL.md"
    echo -e "  ${GREEN}✓${NC} legal (orchestrator)"
    INSTALL_COUNT=$((INSTALL_COUNT + 1))
fi

# ---------------------------------------------------------------------------
# Install 13 sub-skills
# ---------------------------------------------------------------------------
SKILLS=(
    legal-review
    legal-risks
    legal-compare
    legal-plain
    legal-negotiate
    legal-missing
    legal-nda
    legal-terms
    legal-privacy
    legal-agreement
    legal-compliance
    legal-freelancer
    legal-report-pdf
)

for skill in "${SKILLS[@]}"; do
    if [ -f "$SOURCE_DIR/skills/$skill/SKILL.md" ]; then
        mkdir -p "$SKILLS_DIR/$skill"
        cp "$SOURCE_DIR/skills/$skill/SKILL.md" "$SKILLS_DIR/$skill/SKILL.md"
        echo -e "  ${GREEN}✓${NC} $skill"
        INSTALL_COUNT=$((INSTALL_COUNT + 1))
    else
        echo -e "  ${YELLOW}⚠${NC} $skill (not found in source)"
    fi
done

# ---------------------------------------------------------------------------
# Install 5 analysis frameworks
# ---------------------------------------------------------------------------
echo -e "${BLUE}Installing analysis frameworks...${NC}"

AGENT_COUNT=0
AGENTS=(
    legal-clauses
    legal-risks
    legal-compliance
    legal-terms
    legal-recommendations
)

for agent in "${AGENTS[@]}"; do
    if [ -f "$SOURCE_DIR/agents/$agent.md" ]; then
        mkdir -p "$SKILLS_DIR/legal-review/agents"
        cp "$SOURCE_DIR/agents/$agent.md" "$SKILLS_DIR/legal-review/agents/$agent.md"
        cp "$SOURCE_DIR/agents/$agent.md" "$AGENTS_DIR/$agent.md"
        echo -e "  ${GREEN}✓${NC} $agent"
        AGENT_COUNT=$((AGENT_COUNT + 1))
    else
        echo -e "  ${YELLOW}⚠${NC} $agent (not found in source)"
    fi
done

# ---------------------------------------------------------------------------
# Install Python scripts for PDF generation
# ---------------------------------------------------------------------------
echo -e "${BLUE}Installing scripts...${NC}"

SCRIPT_COUNT=0
mkdir -p "$SKILLS_DIR/legal-report-pdf/scripts"
for script in "$SOURCE_DIR"/scripts/*.py; do
    if [ -f "$script" ]; then
        cp "$script" "$SKILLS_DIR/legal-report-pdf/scripts/"
        echo -e "  ${GREEN}✓${NC} $(basename "$script")"
        SCRIPT_COUNT=$((SCRIPT_COUNT + 1))
    fi
done

# ---------------------------------------------------------------------------
# Install templates
# ---------------------------------------------------------------------------
echo -e "${BLUE}Installing templates...${NC}"

TEMPLATE_COUNT=0
mkdir -p "$SKILLS_DIR/legal-report-pdf/templates"
for template in "$SOURCE_DIR"/templates/*.md; do
    if [ -f "$template" ]; then
        cp "$template" "$SKILLS_DIR/legal-report-pdf/templates/"
        echo -e "  ${GREEN}✓${NC} $(basename "$template")"
        TEMPLATE_COUNT=$((TEMPLATE_COUNT + 1))
    fi
done

# ---------------------------------------------------------------------------
# Check Python dependencies
# ---------------------------------------------------------------------------
echo -e "${BLUE}Checking Python environment...${NC}"

if command -v python3 &>/dev/null; then
    echo -e "  ${GREEN}✓${NC} Python 3 found: $(python3 --version 2>&1)"
else
    echo -e "  ${RED}✗${NC} Python 3 not found — required for PDF reports"
fi

# Check reportlab
if python3 -c "import reportlab" 2>/dev/null; then
    echo -e "  ${GREEN}✓${NC} reportlab installed"
else
    echo -e "  ${YELLOW}⚠${NC} reportlab not installed (needed for PDF reports)"
    echo -e "      Install with: ${CYAN}pip3 install reportlab${NC}"
fi

# ---------------------------------------------------------------------------
# Cleanup temp dir if used
# ---------------------------------------------------------------------------
if [ -n "$TEMP_DIR" ] && [ -d "$TEMP_DIR" ]; then
    rm -rf "$TEMP_DIR"
    echo -e "  ${GREEN}✓${NC} Cleaned up temporary files"
fi

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  Installation Complete!                                      ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "  ${CYAN}Skills:${NC}    $INSTALL_COUNT installed  →  $SKILLS_DIR"
echo -e "  ${CYAN}Frameworks:${NC} $AGENT_COUNT installed  →  $AGENTS_DIR"
echo -e "  ${CYAN}Scripts:${NC}   $SCRIPT_COUNT installed  →  $SKILLS_DIR/legal-report-pdf/scripts"
echo -e "  ${CYAN}Templates:${NC} $TEMPLATE_COUNT installed  →  $SKILLS_DIR/legal-report-pdf/templates"
echo ""

# ---------------------------------------------------------------------------
# Capability reference
# ---------------------------------------------------------------------------
echo -e "${BLUE}Capability Examples:${NC}"
echo ""
echo -e "  ${CYAN}Review this contract and give me a full risk report${NC}"
echo -e "  ${CYAN}Analyze the risk level of every clause in this contract${NC}"
echo -e "  ${CYAN}Compare these two contract versions and tell me what changed${NC}"
echo -e "  ${CYAN}Translate this contract into plain English${NC}"
echo -e "  ${CYAN}Draft negotiation language for the risky clauses in this contract${NC}"
echo -e "  ${CYAN}Tell me what protections are missing from this contract${NC}"
echo -e "  ${CYAN}Generate a mutual NDA for these two parties${NC}"
echo -e "  ${CYAN}Generate terms of service for this website${NC}"
echo -e "  ${CYAN}Generate a privacy policy for this website${NC}"
echo -e "  ${CYAN}Draft a freelancer agreement / MSA / SOW / partnership agreement${NC}"
echo -e "  ${CYAN}Review this contract from the freelancer's perspective${NC}"
echo -e "  ${CYAN}Audit this website for compliance gaps${NC}"
echo -e "  ${CYAN}Turn the latest legal analysis into a PDF report${NC}"
echo ""
echo -e "  ${YELLOW}Tip:${NC} Start with ${CYAN}Review this contract and give me a full risk report${NC}"
echo -e "  ${YELLOW}Note:${NC} This bundle is optimized for Codex natural-language triggering."
echo ""
