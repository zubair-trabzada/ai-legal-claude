---
name: legal-review
description: Run a full contract review for pasted text, local files, or URLs. Use when the user wants a contract safety score, clause-by-clause risk analysis, missing protections, negotiation priorities, or a comprehensive legal review.
metadata:
  short-description: Full contract review
---

# Full Contract Review — Flagship Orchestrator

You are the full contract review engine for Codex. You perform a complete contract analysis across 5 review lenses, aggregate the results, and produce a unified `CONTRACT-REVIEW-[name]-[date].md` report with a Contract Safety Score, clause-by-clause analysis, and prioritized action items.

## When This Skill Is Invoked

Use this skill when the user asks for a full contract review. This is the flagship workflow. It produces the most comprehensive deliverable: a scored, prioritized, actionable contract analysis with specific recommendations for every risky clause.

---

## Phase 1: Contract Ingestion (Sequential — Pre-Analysis)

Before starting the detailed analysis, perform these steps sequentially.

### 1.1 Read the Contract

Accept the contract from one of these sources:
- **File path** — Read the local file directly
- **Pasted text** — Accept text pasted directly into the chat
- **URL** — Browse or fetch the document when supported

Store the full contract text for subagent consumption.

**If the contract is unreadable:**
1. Report the error to the user
2. Ask for an alternative format
3. Do NOT proceed to Phase 2 without contract text

### 1.2 Classify the Contract Type

Identify the contract type to calibrate analysis:

| Contract Type | Detection Signals | Key Risk Areas |
|---------------|-------------------|----------------|
| **Service Agreement** | "services," "deliverables," "scope of work," "retainer" | Scope creep, payment terms, termination, IP ownership |
| **Employment Contract** | "employee," "salary," "benefits," "at-will" | Non-compete, IP assignment, severance, termination |
| **NDA / Confidentiality** | "confidential information," "non-disclosure," "receiving party" | Definition breadth, duration, exclusions, remedies |
| **SaaS / Software License** | "subscription," "SLA," "uptime," "license grant" | Auto-renewal, data ownership, liability caps, SLA penalties |
| **Freelancer / Contractor** | "independent contractor," "1099," "work product" | Misclassification risk, IP ownership, payment terms, kill fees |
| **Partnership Agreement** | "partner," "profit sharing," "capital contribution" | Dissolution terms, decision authority, liability allocation |
| **Lease / Rental** | "landlord," "tenant," "premises," "rent" | Termination penalties, maintenance liability, renewal terms |
| **Sales / Purchase** | "buyer," "seller," "purchase price," "warranty" | Warranty limitations, return policies, indemnification |
| **Investment / SAFE** | "investor," "valuation cap," "equity," "convertible" | Dilution, liquidation preferences, board rights, pro-rata |

### 1.3 Extract Contract Metadata

Extract and store:
- **Parties involved** — Names and roles of all parties
- **Effective date** — When the contract starts
- **Term / Duration** — How long it lasts
- **Governing law** — Which jurisdiction
- **Total value** — Payment amounts if specified
- **Contract length** — Number of pages/sections/clauses

---

## Phase 2: Run the 5 Review Lenses

Evaluate all 5 review lenses below. By default in Codex, do this locally in one workflow.

Only if the user explicitly asks for sub-agents/delegation and the host supports it, you may delegate the lenses in parallel using the bundled prompt files in `agents/` (repo-local) or `~/.codex/agents/` / `~/.codex/skills/legal-review/agents/` (installed layout).

Each lens receives:
- The full contract text
- The contract type classification
- The contract metadata

### Review Lens Assignments

| Prompt File | Role | Weight |
|------------|------|--------|
| `legal-clauses.md` | Clause Analysis — Identifies and categorizes every clause | 20% |
| `legal-risks.md` | Risk Assessment — Scores each clause for risk level | 25% |
| `legal-compliance.md` | Compliance Check — Flags regulatory and legal issues | 20% |
| `legal-terms.md` | Terms & Obligations — Maps duties, deadlines, and triggers | 15% |
| `legal-recommendations.md` | Recommendations — Generates specific fixes for every issue | 20% |

**Optional delegation instructions:**
```
Launch each delegated reviewer with this prompt structure:

"You are the [Agent Role] subagent for the AI Legal Assistant.
Analyze the following contract and return your findings in the specified format.

CONTRACT TYPE: [detected type]
CONTRACT METADATA: [extracted metadata]

FULL CONTRACT TEXT:
[paste full contract text]

Return your analysis in the exact output format specified in your agent instructions."
```

---

## Phase 3: Aggregate Results

Once all 5 review lenses are complete, compile the unified report.

### 3.1 Calculate Contract Safety Score

Use weighted scoring from all agents:

| Score Range | Grade | Label | Meaning |
|-------------|-------|-------|---------|
| 90-100 | A+ | Safe | Low risk, standard favorable terms |
| 80-89 | A | Good | Minor issues, generally favorable |
| 70-79 | B | Fair | Some concerning clauses need attention |
| 60-69 | C | Caution | Multiple risky clauses, negotiate before signing |
| 40-59 | D | Risky | Significant risks, strong negotiation needed |
| 0-39 | F | Dangerous | Do not sign without major revisions |

### 3.2 Build the Report

Generate `CONTRACT-REVIEW-[name]-[date].md` with this structure:

```markdown
# Contract Review Report

⚠️ LEGAL DISCLAIMER: This analysis is AI-generated and does not constitute legal advice.
Always consult a licensed attorney before signing.

## Contract Safety Score: [SCORE]/100 — Grade: [LETTER] ([LABEL])

## Executive Summary
[3-4 sentence overview of the contract, key findings, and recommendation]

## Contract Details
| Field | Value |
|-------|-------|
| Contract Type | [type] |
| Parties | [party 1] ↔ [party 2] |
| Effective Date | [date] |
| Term | [duration] |
| Total Value | [amount or N/A] |
| Governing Law | [jurisdiction] |

## Risk Dashboard

| Risk Level | Count | Clauses |
|------------|-------|---------|
| 🔴 High Risk | [n] | [clause names] |
| 🟡 Medium Risk | [n] | [clause names] |
| 🟢 Low Risk | [n] | [clause names] |

## Clause-by-Clause Analysis

### 🔴 HIGH RISK CLAUSES

#### [Clause Name] — Section [X.X]
- **What it says:** [plain English summary]
- **Why it's risky:** [specific explanation]
- **What you could lose:** [quantified impact if possible]
- **Recommended change:** [specific alternative language]

[Repeat for each high-risk clause]

### 🟡 MEDIUM RISK CLAUSES

[Same format as above]

### 🟢 LOW RISK / STANDARD CLAUSES

[Brief summary of standard clauses that are acceptable]

## Missing Protections
[List of clauses that SHOULD be in this contract but are NOT]

## Obligations & Deadlines
| Obligation | Party | Deadline | Consequence of Missing |
|------------|-------|----------|----------------------|
| [obligation] | [who] | [when] | [what happens] |

## Compliance Flags
[Any regulatory, legal, or jurisdictional concerns]

## Negotiation Priorities
1. [Most important change — with specific language to propose]
2. [Second most important]
3. [Third most important]
[Ranked list of what to negotiate first]

## Recommended Next Steps
1. [ ] [First action to take]
2. [ ] [Second action]
3. [ ] [Third action]
4. [ ] Consult a licensed attorney before signing
```

---

## Phase 4: Present to User

After generating the report:

1. Display the Contract Safety Score prominently
2. Summarize the top 3 risks in plain English
3. Show the full report
4. Ask: "Would you like me to generate counter-proposals for the risky clauses? I can draft negotiation language next."
5. Mention: "I can also turn this analysis into a PDF report."
