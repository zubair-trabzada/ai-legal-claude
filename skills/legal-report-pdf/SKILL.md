---
name: legal-report-pdf
description: Generate a professional PDF report from the latest legal review markdown output, using the bundled ReportLab script when available.
metadata:
  short-description: PDF legal report generator
---

# Professional PDF Report Generator

You are the PDF report generator for Codex. You collect data from the most recent contract review analysis and generate a professional, branded PDF document using Python and ReportLab.

## When This Skill Is Invoked

Use this skill when the user asks for a PDF version of the latest analysis. Find the most recent analysis data, then generate a polished PDF report.

---

## Phase 1: Locate Analysis Data

### 1.1 Find the Most Recent Review

Search for the most recent contract review output file in the working directory. Look for files matching these patterns (in order of preference):

1. `CONTRACT-REVIEW-*.md`
2. `FREELANCER-REVIEW-*.md`
3. `COMPLIANCE-AUDIT-*.md`
4. `NDA-REVIEW-*.md`
5. Any `.md` file containing "Contract Safety Score" or "Freelancer Fairness Score" or "Compliance Scorecard"

Search the workspace for matching files. If multiple matches exist, use the most recently modified file.

**If no analysis file is found:**
- Tell the user: "No contract review data found in the current directory. Please ask me to review a contract first, then ask me to turn that analysis into a PDF."
- Do NOT proceed.

### 1.2 Parse the Analysis Data

Read the analysis file and extract:

| Data Point | Where to Find It |
|-----------|-----------------|
| **Score** | "Contract Safety Score: X/100" or "Freelancer Fairness Score: X/100" or "Overall: X%" |
| **Grade** | "Grade: [letter]" |
| **Contract type** | "Contract Type" row in details table |
| **Parties** | "Parties" row or "Hiring Party" / "Freelancer" rows |
| **Date** | From filename or "Effective Date" row |
| **Risk dashboard** | High/Medium/Low risk counts and clause names |
| **Clause analysis** | Each clause with risk level, description, and recommendation |
| **Missing protections** | "Missing Protections" section or "Freelancer Bill of Rights" |
| **Obligations** | "Obligations & Deadlines" table |
| **Compliance flags** | "Compliance Flags" section |
| **Negotiation priorities** | "Negotiation Priorities" numbered list |
| **Next steps** | "Recommended Next Steps" checklist |
| **Executive summary** | "Executive Summary" section |

---

## Phase 2: Locate or Generate the PDF Script

### 2.1 Look for Existing Script

Search for the PDF generation Python script in these locations (in order):

1. `~/.codex/skills/legal-report-pdf/scripts/generate_legal_pdf.py`
2. `[repo root]/scripts/generate_legal_pdf.py`
3. `[working directory]/scripts/generate_legal_pdf.py`
4. `../scripts/generate_legal_pdf.py` (one level up from working directory)

Search for `generate_legal_pdf.py` within the workspace if the installed bundle path is unavailable.

### 2.2 If Script Found

Run the script after converting the analysis markdown into a temporary JSON payload that matches the script's expected schema:

```bash
python3 [script_path] [temp_json_path] CONTRACT-REVIEW-REPORT.pdf
```

### 2.3 If Script Not Found — Generate Inline

If no script is found, generate the PDF directly using inline Python with ReportLab. Write and execute a Python script that produces the PDF.

**First, check that ReportLab is installed:**

```bash
pip3 install reportlab 2>/dev/null || pip install reportlab 2>/dev/null
```

Then generate and execute the following Python script. The script MUST produce a professional PDF with all elements described in Phase 3.

---

## Phase 3: PDF Content and Layout Specification

The generated PDF MUST include all of the following sections with professional styling.

### 3.1 Page Setup

| Property | Value |
|----------|-------|
| Page size | Letter (8.5" x 11") |
| Margins | 0.75" all sides |
| Font family | Helvetica (built into ReportLab) |
| Primary color | #1a1a2e (dark navy) |
| Accent color | #16213e (medium navy) |
| High risk color | #d32f2f (red) |
| Medium risk color | #f9a825 (amber/yellow) |
| Low risk color | #388e3c (green) |
| Background | White (#ffffff) |
| Table header bg | #1a1a2e (dark navy) |
| Table alt row | #f5f5f5 (light gray) |

### 3.2 Cover Page

The cover page MUST include:

```
[Top: Thin colored bar across full width in primary color]

CONTRACT REVIEW REPORT
[Large, bold, primary color, centered]

[Subtitle: Contract type or "Comprehensive Legal Analysis"]

[Large circular score gauge graphic — see 3.3]

Contract Safety Score: [SCORE]/100
Grade: [LETTER] — [LABEL]
[Color-coded based on score: red for F/D, amber for C, green for B/A]

Prepared for: [Party name or "Contract Review"]
Date: [today's date]

[Bottom of page:]
⚠️ LEGAL DISCLAIMER: This analysis is AI-generated and does not
constitute legal advice. Always consult a licensed attorney.

[Thin colored bar at bottom]
```

### 3.3 Score Gauge Graphic

Draw a semi-circular gauge (speedometer style) using ReportLab drawing primitives:

- Semi-circle arc from 0 to 180 degrees
- Color gradient: red (left) to yellow (center) to green (right)
- Needle pointing to the score position
- Score number displayed large and centered below the gauge
- Grade letter displayed below the score

Implementation approach using ReportLab:
```python
from reportlab.graphics.shapes import Drawing, Wedge, String, Line
from reportlab.graphics import renderPDF
from reportlab.lib.colors import Color
import math

# Create a drawing for the gauge
# Use Wedge shapes for the colored arc segments
# Use Line for the needle
# Use String for the score text
```

If the gauge is too complex to render reliably, fall back to a large color-coded score box:
```
+----------------------------------+
|     CONTRACT SAFETY SCORE        |
|                                  |
|           72 / 100               |
|          Grade: B                |
|           (Fair)                 |
+----------------------------------+
```
Color the box border and score text based on the grade.

### 3.4 Executive Summary Page

```
EXECUTIVE SUMMARY
[Section header with colored underline]

[3-4 sentence overview from the analysis]

CONTRACT DETAILS
[Table with alternating row colors:]
| Field           | Value              |
| Contract Type   | [type]             |
| Parties         | [party 1] ↔ [party 2] |
| Effective Date  | [date]             |
| Term            | [duration]         |
| Total Value     | [amount]           |
| Governing Law   | [jurisdiction]     |
```

### 3.5 Risk Dashboard Page

```
RISK DASHBOARD
[Section header with colored underline]

[Color-coded risk summary boxes in a row:]
+----------+  +----------+  +----------+
| 🔴 HIGH  |  | 🟡 MED   |  | 🟢 LOW   |
|    [n]   |  |    [n]   |  |    [n]   |
+----------+  +----------+  +----------+

[Risk matrix table:]
| Risk Level | Count | Clauses Affected           |
|------------|-------|----------------------------|
| High       | [n]   | [clause1], [clause2], ...  |
| Medium     | [n]   | [clause1], [clause2], ...  |
| Low        | [n]   | [clause1], [clause2], ...  |
```

Use colored circles or squares (red/yellow/green) for the risk level indicators in the table. ReportLab can draw these with `canvas.circle()` or by using colored table cell backgrounds.

### 3.6 Clause-by-Clause Analysis Pages

For EACH clause analyzed, create a structured entry:

```
[Risk level color bar on left margin]

CLAUSE: [Clause Name] — Section [X.X]
Risk Level: [🔴 HIGH / 🟡 MEDIUM / 🟢 LOW]

What it says:
[plain English summary]

Why it matters:
[risk explanation]

What you could lose:
[quantified impact]

Recommended change:
[specific alternative language]

[Separator line]
```

Group clauses by risk level: all High Risk first, then Medium, then Low.

### 3.7 Missing Protections Checklist

```
MISSING PROTECTIONS
[Section header]

[Checklist table:]
| # | Protection              | Status |
|---|-------------------------|--------|
| 1 | [protection name]       | ❌ Missing |
| 2 | [protection name]       | ✅ Present |
| 3 | [protection name]       | ❌ Missing |
...
```

Use red background for missing items, green for present items.

### 3.8 Obligations Timeline

```
OBLIGATIONS & DEADLINES
[Section header]

[Table:]
| Obligation | Responsible Party | Deadline | Consequence |
|------------|-------------------|----------|-------------|
| [obligation] | [who]          | [when]   | [what happens] |
```

### 3.9 Compliance Flags

```
COMPLIANCE FLAGS
[Section header]

[List of any regulatory or jurisdictional concerns identified]
```

### 3.10 Negotiation Priorities

```
NEGOTIATION PRIORITIES
[Section header]

1. [HIGHEST PRIORITY]
   Current: [what the clause says now]
   Proposed: [specific language to propose]
   Why: [one-sentence justification]

2. [SECOND PRIORITY]
   ...

3. [THIRD PRIORITY]
   ...
```

Number and rank all priorities. Use bold for the priority title.

### 3.11 Recommended Next Steps

```
RECOMMENDED NEXT STEPS
[Section header]

☐ [First action]
☐ [Second action]
☐ [Third action]
☐ Consult a licensed attorney before signing
```

### 3.12 Legal Disclaimer (Final Page)

```
LEGAL DISCLAIMER

⚠️ This document was generated by an AI-powered legal analysis tool.
It does NOT constitute legal advice and should not be relied upon as
such. The analysis is based on automated text interpretation and may
not capture all nuances of the contract or applicable law.

ALWAYS consult a licensed attorney before:
• Signing any contract
• Making legal decisions based on this analysis
• Negotiating contract terms
• Taking any action that could have legal consequences

This report is provided for informational purposes only. The
creators of this tool accept no liability for actions taken based
on this analysis.

Generated: [date and time]
Tool: AI Legal Codex
```

### 3.13 Page Footer (All Pages Except Cover)

Every page after the cover should have:

```
[Left: "AI Legal Codex — Contract Review Report"]
[Center: "CONFIDENTIAL"]
[Right: "Page X of Y"]
```

Use a thin line above the footer to separate it from content.

---

## Phase 4: Generate the PDF

### 4.1 Write the Python Script

Write a complete Python script that:

1. Reads the analysis markdown file
2. Parses the sections using string matching / regex
3. Builds the PDF page by page using ReportLab
4. Includes all sections from Phase 3
5. Uses professional styling throughout
6. Handles missing sections gracefully (skip if data not found)

### 4.2 Execute the Script

Run the script using Bash:

```bash
cd [working directory] && python3 /tmp/generate_legal_pdf.py "[temp_json_file]" "CONTRACT-REVIEW-REPORT.pdf"
```

### 4.3 Verify Output

After execution:
1. Check that the PDF was created successfully
2. Verify the file size is reasonable (should be >10KB for a real report)
3. Report any errors to the user

---

## Phase 5: Present to User

After generating the PDF:

1. Confirm the PDF was generated: "PDF report generated: `CONTRACT-REVIEW-REPORT.pdf`"
2. State the file location (absolute path)
3. Summarize what's in the report (sections included, page count if known)
4. Note: "Open the PDF to review the full formatted report with the score gauge, risk dashboard, and clause-by-clause analysis."
5. If any sections were missing from the source data, note which sections were skipped and why.

---

## Error Handling

| Error | Resolution |
|-------|-----------|
| ReportLab not installed | Run `pip3 install reportlab` and retry |
| No analysis file found | Tell user to ask for a contract review first |
| Analysis file unreadable | Report the error, ask user to verify the file |
| PDF generation fails | Show the error, attempt to fix, retry once |
| Script not found and inline generation fails | Provide the markdown analysis as fallback and explain the PDF could not be generated |
| Python not available | Report that Python 3 is required for PDF generation |
