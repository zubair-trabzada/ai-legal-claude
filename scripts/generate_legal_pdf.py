#!/usr/bin/env python3
"""
AI Legal Codex — PDF Report Generator
Generates professional contract review PDF reports using ReportLab.
"""

import sys
import os
import json
import math
from datetime import datetime

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import inch
    from reportlab.lib.colors import HexColor, white, black
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
        PageBreak, HRFlowable, KeepTogether
    )
    from reportlab.graphics.shapes import Drawing, Circle, Rect, String, Line, Wedge
    from reportlab.graphics import renderPDF
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
except ImportError:
    print("ERROR: reportlab is required. Install with: pip3 install reportlab")
    sys.exit(1)


# ---------------------------------------------------------------------------
# Color Palette
# ---------------------------------------------------------------------------
COLORS = {
    "primary": HexColor("#1a365d"),      # Dark navy
    "secondary": HexColor("#2d5f8a"),    # Medium blue
    "accent": HexColor("#3182ce"),       # Bright blue
    "success": HexColor("#38a169"),      # Green
    "warning": HexColor("#d69e2e"),      # Yellow/amber
    "danger": HexColor("#e53e3e"),       # Red
    "light_bg": HexColor("#f7fafc"),     # Light gray bg
    "dark_text": HexColor("#1a202c"),    # Near black
    "gray_text": HexColor("#718096"),    # Gray
    "white": white,
    "black": black,
    "light_border": HexColor("#e2e8f0"), # Light border
    "high_risk_bg": HexColor("#fff5f5"), # Light red bg
    "med_risk_bg": HexColor("#fffff0"),  # Light yellow bg
    "low_risk_bg": HexColor("#f0fff4"),  # Light green bg
}


# ---------------------------------------------------------------------------
# Score Gauge Drawing
# ---------------------------------------------------------------------------
def create_score_gauge(score, size=200):
    """Create a semi-circular gauge showing the contract safety score."""
    d = Drawing(size, size * 0.65)
    cx, cy = size / 2, size * 0.55
    radius = size * 0.4

    # Background arc segments
    segments = [
        (0, 36, COLORS["danger"]),
        (36, 72, HexColor("#ed8936")),
        (72, 108, COLORS["warning"]),
        (108, 144, HexColor("#68d391")),
        (144, 180, COLORS["success"]),
    ]

    for start, end, color in segments:
        w = Wedge(cx, cy, radius, 180 + start, 180 + end,
                  fillColor=color, strokeColor=white, strokeWidth=2)
        d.add(w)

    # Inner circle (white center)
    inner = Circle(cx, cy, radius * 0.65, fillColor=white, strokeColor=None)
    d.add(inner)

    # Score text
    score_str = str(int(score))
    score_text = String(cx, cy - 5, score_str,
                        fontSize=36, fillColor=COLORS["primary"],
                        textAnchor="middle", fontName="Helvetica-Bold")
    d.add(score_text)

    label = String(cx, cy - 22, "/ 100",
                   fontSize=12, fillColor=COLORS["gray_text"],
                   textAnchor="middle", fontName="Helvetica")
    d.add(label)

    # Needle
    angle_deg = 180 + (score / 100) * 180
    angle_rad = math.radians(angle_deg)
    needle_len = radius * 0.55
    nx = cx + needle_len * math.cos(angle_rad)
    ny = cy + needle_len * math.sin(angle_rad)
    needle = Line(cx, cy, nx, ny, strokeColor=COLORS["primary"], strokeWidth=2.5)
    d.add(needle)

    # Center dot
    center_dot = Circle(cx, cy, 5, fillColor=COLORS["primary"], strokeColor=None)
    d.add(center_dot)

    return d


# ---------------------------------------------------------------------------
# Risk Bar Chart
# ---------------------------------------------------------------------------
def create_risk_bar_chart(high, medium, low, width=400, height=100):
    """Create a horizontal stacked bar chart showing risk distribution."""
    d = Drawing(width, height)
    total = high + medium + low
    if total == 0:
        return d

    bar_width = width * 0.7
    bar_height = 30
    x_start = width * 0.15
    y = height * 0.4

    # Bars
    high_w = (high / total) * bar_width if total > 0 else 0
    med_w = (medium / total) * bar_width if total > 0 else 0
    low_w = (low / total) * bar_width if total > 0 else 0

    if high_w > 0:
        d.add(Rect(x_start, y, high_w, bar_height,
                    fillColor=COLORS["danger"], strokeColor=None))
    if med_w > 0:
        d.add(Rect(x_start + high_w, y, med_w, bar_height,
                    fillColor=COLORS["warning"], strokeColor=None))
    if low_w > 0:
        d.add(Rect(x_start + high_w + med_w, y, low_w, bar_height,
                    fillColor=COLORS["success"], strokeColor=None))

    # Labels
    labels = [
        (f"High Risk: {high}", COLORS["danger"], x_start),
        (f"Medium: {medium}", COLORS["warning"], x_start + bar_width * 0.35),
        (f"Low Risk: {low}", COLORS["success"], x_start + bar_width * 0.7),
    ]
    for text, color, x in labels:
        d.add(String(x, y - 15, text, fontSize=9, fillColor=color,
                     fontName="Helvetica-Bold"))

    return d


# ---------------------------------------------------------------------------
# Styles
# ---------------------------------------------------------------------------
def get_styles():
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name="CoverTitle", fontName="Helvetica-Bold", fontSize=28,
        textColor=COLORS["primary"], alignment=TA_CENTER, spaceAfter=10
    ))
    styles.add(ParagraphStyle(
        name="CoverSubtitle", fontName="Helvetica", fontSize=14,
        textColor=COLORS["gray_text"], alignment=TA_CENTER, spaceAfter=30
    ))
    styles.add(ParagraphStyle(
        name="SectionHeader", fontName="Helvetica-Bold", fontSize=16,
        textColor=COLORS["primary"], spaceBefore=20, spaceAfter=10,
        borderWidth=0, borderPadding=5
    ))
    styles.add(ParagraphStyle(
        name="SubHeader", fontName="Helvetica-Bold", fontSize=12,
        textColor=COLORS["secondary"], spaceBefore=12, spaceAfter=6
    ))
    styles.add(ParagraphStyle(
        name="BodyText2", fontName="Helvetica", fontSize=10,
        textColor=COLORS["dark_text"], spaceBefore=4, spaceAfter=4,
        leading=14
    ))
    styles.add(ParagraphStyle(
        name="RiskHigh", fontName="Helvetica-Bold", fontSize=10,
        textColor=COLORS["danger"], spaceBefore=2, spaceAfter=2
    ))
    styles.add(ParagraphStyle(
        name="RiskMedium", fontName="Helvetica-Bold", fontSize=10,
        textColor=COLORS["warning"], spaceBefore=2, spaceAfter=2
    ))
    styles.add(ParagraphStyle(
        name="RiskLow", fontName="Helvetica-Bold", fontSize=10,
        textColor=COLORS["success"], spaceBefore=2, spaceAfter=2
    ))
    styles.add(ParagraphStyle(
        name="Disclaimer", fontName="Helvetica-Oblique", fontSize=8,
        textColor=COLORS["gray_text"], alignment=TA_CENTER, spaceBefore=10,
        spaceAfter=10
    ))
    styles.add(ParagraphStyle(
        name="Footer", fontName="Helvetica", fontSize=8,
        textColor=COLORS["gray_text"], alignment=TA_CENTER
    ))

    return styles


# ---------------------------------------------------------------------------
# PDF Builder
# ---------------------------------------------------------------------------
def build_pdf(data, output_path):
    """Build the PDF report from structured data."""
    styles = get_styles()
    doc = SimpleDocTemplate(
        output_path, pagesize=letter,
        leftMargin=0.75 * inch, rightMargin=0.75 * inch,
        topMargin=0.75 * inch, bottomMargin=0.75 * inch
    )
    story = []

    # ── Cover Page ──
    story.append(Spacer(1, 1.8 * inch))
    story.append(Paragraph("Contract Review Report", styles["CoverTitle"]))
    story.append(Spacer(1, 40))
    story.append(Paragraph(
        f"Generated {datetime.now().strftime('%B %d, %Y')}",
        styles["CoverSubtitle"]
    ))
    story.append(Spacer(1, 60))

    # Score gauge
    score = data.get("score", 0)
    gauge = create_score_gauge(score)
    story.append(gauge)
    story.append(Spacer(1, 40))

    # Grade label
    grade = data.get("grade", "N/A")
    grade_label = data.get("grade_label", "")
    story.append(Paragraph(
        f"Grade: {grade} — {grade_label}", styles["CoverSubtitle"]
    ))

    # Disclaimer
    story.append(Spacer(1, 40))
    story.append(Paragraph(
        "LEGAL DISCLAIMER: This analysis is AI-generated and does not constitute legal advice. "
        "It is intended as a starting point for review. Always consult a licensed attorney "
        "before signing contracts or relying on generated legal documents.",
        styles["Disclaimer"]
    ))

    story.append(PageBreak())

    # ── Contract Details ──
    story.append(Paragraph("Contract Details", styles["SectionHeader"]))
    story.append(HRFlowable(
        width="100%", thickness=1, color=COLORS["light_border"]
    ))

    details = data.get("details", {})
    detail_rows = [
        ["Contract Type", details.get("type", "N/A")],
        ["Parties", details.get("parties", "N/A")],
        ["Effective Date", details.get("effective_date", "N/A")],
        ["Term", details.get("term", "N/A")],
        ["Total Value", details.get("total_value", "N/A")],
        ["Governing Law", details.get("governing_law", "N/A")],
    ]
    detail_table = Table(detail_rows, colWidths=[2 * inch, 4.5 * inch])
    detail_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("TEXTCOLOR", (0, 0), (0, -1), COLORS["primary"]),
        ("TEXTCOLOR", (1, 0), (1, -1), COLORS["dark_text"]),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("LINEBELOW", (0, 0), (-1, -2), 0.5, COLORS["light_border"]),
    ]))
    story.append(detail_table)
    story.append(Spacer(1, 20))

    # ── Executive Summary ──
    story.append(Paragraph("Executive Summary", styles["SectionHeader"]))
    story.append(HRFlowable(
        width="100%", thickness=1, color=COLORS["light_border"]
    ))
    story.append(Paragraph(
        data.get("executive_summary", "No summary available."),
        styles["BodyText2"]
    ))
    story.append(Spacer(1, 20))

    # ── Risk Dashboard ──
    story.append(Paragraph("Risk Dashboard", styles["SectionHeader"]))
    story.append(HRFlowable(
        width="100%", thickness=1, color=COLORS["light_border"]
    ))

    risks = data.get("risks", {"high": 0, "medium": 0, "low": 0})
    risk_chart = create_risk_bar_chart(
        risks.get("high", 0), risks.get("medium", 0), risks.get("low", 0)
    )
    story.append(risk_chart)
    story.append(Spacer(1, 15))

    # Risk summary table
    risk_rows = [
        ["Risk Level", "Count", "Clauses"],
        ["HIGH RISK", str(risks.get("high", 0)),
         risks.get("high_clauses", "None")],
        ["MEDIUM RISK", str(risks.get("medium", 0)),
         risks.get("medium_clauses", "None")],
        ["LOW RISK", str(risks.get("low", 0)),
         risks.get("low_clauses", "None")],
    ]
    risk_table = Table(risk_rows, colWidths=[1.5 * inch, 1 * inch, 4 * inch])
    risk_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("BACKGROUND", (0, 0), (-1, 0), COLORS["primary"]),
        ("TEXTCOLOR", (0, 0), (-1, 0), COLORS["white"]),
        ("BACKGROUND", (0, 1), (-1, 1), COLORS["high_risk_bg"]),
        ("TEXTCOLOR", (0, 1), (0, 1), COLORS["danger"]),
        ("BACKGROUND", (0, 2), (-1, 2), COLORS["med_risk_bg"]),
        ("TEXTCOLOR", (0, 2), (0, 2), COLORS["warning"]),
        ("BACKGROUND", (0, 3), (-1, 3), COLORS["low_risk_bg"]),
        ("TEXTCOLOR", (0, 3), (0, 3), COLORS["success"]),
        ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("GRID", (0, 0), (-1, -1), 0.5, COLORS["light_border"]),
    ]))
    story.append(risk_table)
    story.append(Spacer(1, 20))

    # ── Clause Analysis ──
    clauses = data.get("clauses", [])
    if clauses:
        story.append(PageBreak())
        story.append(Paragraph("Clause-by-Clause Analysis", styles["SectionHeader"]))
        story.append(HRFlowable(
            width="100%", thickness=1, color=COLORS["light_border"]
        ))

        for clause in clauses:
            risk = clause.get("risk", "low")
            risk_color = {
                "high": COLORS["danger"],
                "medium": COLORS["warning"],
                "low": COLORS["success"]
            }.get(risk, COLORS["gray_text"])
            risk_emoji = {"high": "HIGH RISK", "medium": "MEDIUM RISK", "low": "LOW RISK"}.get(risk, "")
            risk_bg = {
                "high": COLORS["high_risk_bg"],
                "medium": COLORS["med_risk_bg"],
                "low": COLORS["low_risk_bg"]
            }.get(risk, COLORS["light_bg"])

            clause_block = []
            clause_block.append(Paragraph(
                f'<font color="{risk_color.hexval()}">[{risk_emoji}]</font> '
                f'<b>{clause.get("name", "Unnamed Clause")}</b> — Section {clause.get("section", "N/A")}',
                styles["SubHeader"]
            ))
            if clause.get("summary"):
                clause_block.append(Paragraph(
                    f'<b>What it says:</b> {clause["summary"]}', styles["BodyText2"]
                ))
            if clause.get("risk_explanation"):
                clause_block.append(Paragraph(
                    f'<b>Why it matters:</b> {clause["risk_explanation"]}', styles["BodyText2"]
                ))
            if clause.get("recommendation"):
                clause_block.append(Paragraph(
                    f'<b>Recommended change:</b> {clause["recommendation"]}', styles["BodyText2"]
                ))
            clause_block.append(Spacer(1, 10))
            story.append(KeepTogether(clause_block))

    # ── Negotiation Priorities ──
    priorities = data.get("negotiation_priorities", [])
    if priorities:
        story.append(Paragraph("Negotiation Priorities", styles["SectionHeader"]))
        story.append(HRFlowable(
            width="100%", thickness=1, color=COLORS["light_border"]
        ))
        for i, priority in enumerate(priorities, 1):
            story.append(Paragraph(f"<b>{i}.</b> {priority}", styles["BodyText2"]))
        story.append(Spacer(1, 20))

    # ── Missing Protections ──
    missing = data.get("missing_protections", [])
    if missing:
        story.append(Paragraph("Missing Protections", styles["SectionHeader"]))
        story.append(HRFlowable(
            width="100%", thickness=1, color=COLORS["light_border"]
        ))
        for item in missing:
            story.append(Paragraph(f"• {item}", styles["BodyText2"]))
        story.append(Spacer(1, 20))

    # ── Next Steps ──
    steps = data.get("next_steps", [])
    if steps:
        story.append(Paragraph("Recommended Next Steps", styles["SectionHeader"]))
        story.append(HRFlowable(
            width="100%", thickness=1, color=COLORS["light_border"]
        ))
        for i, step in enumerate(steps, 1):
            story.append(Paragraph(f"<b>{i}.</b> {step}", styles["BodyText2"]))

    # ── Footer Disclaimer ──
    story.append(Spacer(1, 40))
    story.append(HRFlowable(
        width="100%", thickness=0.5, color=COLORS["light_border"]
    ))
    story.append(Paragraph(
        "This report was generated by AI Legal Codex. "
        "It does not constitute legal advice. Consult a licensed attorney before signing.",
        styles["Disclaimer"]
    ))
    story.append(Paragraph(
        f"Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}",
        styles["Footer"]
    ))

    # Build
    doc.build(story)
    return output_path


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 generate_legal_pdf.py <json_data_file> [output_path]")
        print("  json_data_file: Path to JSON file with report data")
        print("  output_path: Optional output PDF path (default: CONTRACT-REVIEW-REPORT.pdf)")
        sys.exit(1)

    json_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else "CONTRACT-REVIEW-REPORT.pdf"

    with open(json_path, "r") as f:
        data = json.load(f)

    result = build_pdf(data, output_path)
    print(f"PDF generated: {result}")
