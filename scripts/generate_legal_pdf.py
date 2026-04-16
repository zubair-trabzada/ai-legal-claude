#!/usr/bin/env python3
"""
AI 法律助手 — PDF 报告生成器
使用 ReportLab 生成专业的中文合同审查 PDF 报告。
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
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
except ImportError:
    print("错误: 需要 reportlab 库。请使用以下命令安装: pip3 install reportlab")
    sys.exit(1)


# ---------------------------------------------------------------------------
# 字体设置 (支持中文)
# ---------------------------------------------------------------------------
def register_chinese_fonts():
    """注册中文字体，优先尝试系统自带字体。"""
    font_paths = [
        # Windows 路径
        "C:\\Windows\\Fonts\\simhei.ttf",
        "C:\\Windows\\Fonts\\simsun.ttc",
        # macOS 路径
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/Library/Fonts/Arial Unicode.ttf",
        # Linux 路径 (常见位置)
        "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",
        "/usr/share/fonts/wqy-zenhei/wqy-zenhei.ttc",
        # 当前目录下的字体文件
        "simhei.ttf"
    ]
    
    registered_name = "Helvetica" # 默认回退
    
    for path in font_paths:
        if os.path.exists(path):
            try:
                # 统一注册为 'ChineseFont' 方便后面调用
                pdfmetrics.registerFont(TTFont('ChineseFont', path))
                registered_name = "ChineseFont"
                break
            except:
                continue
    
    return registered_name

CHINESE_FONT = register_chinese_fonts()

# ---------------------------------------------------------------------------
# 颜色调色板
# ---------------------------------------------------------------------------
COLORS = {
    "primary": HexColor("#1a365d"),      # 深海军蓝
    "secondary": HexColor("#2d5f8a"),    # 中蓝
    "accent": HexColor("#3182ce"),       # 亮蓝
    "success": HexColor("#38a169"),      # 绿色 (低风险)
    "warning": HexColor("#d69e2e"),      # 橙黄色 (中风险)
    "danger": HexColor("#e53e3e"),       # 红色 (高风险)
    "light_bg": HexColor("#f7fafc"),     # 浅灰背景
    "dark_text": HexColor("#1a202c"),    # 深色文字
    "gray_text": HexColor("#718096"),    # 灰色文字
    "white": white,
    "black": black,
    "light_border": HexColor("#e2e8f0"), # 浅色边框
    "high_risk_bg": HexColor("#fff5f5"), # 浅红背景
    "med_risk_bg": HexColor("#fffff0"),  # 浅黄背景
    "low_risk_bg": HexColor("#f0fff4"),  # 浅绿背景
}


# ---------------------------------------------------------------------------
# 评分仪表盘
# ---------------------------------------------------------------------------
def create_score_gauge(score, size=200):
    """创建一个半圆仪表盘，显示合同安全分。"""
    d = Drawing(size, size * 0.65)
    cx, cy = size / 2, size * 0.55
    radius = size * 0.4

    # 背景圆弧段
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

    # 内圆 (白色中心)
    inner = Circle(cx, cy, radius * 0.65, fillColor=white, strokeColor=None)
    d.add(inner)

    # 分数文字
    score_str = str(int(score))
    score_text = String(cx, cy - 5, score_str,
                        fontSize=36, fillColor=COLORS["primary"],
                        textAnchor="middle", fontName=CHINESE_FONT + "-Bold" if CHINESE_FONT == "Helvetica" else CHINESE_FONT)
    d.add(score_text)

    label = String(cx, cy - 22, "/ 100",
                   fontSize=12, fillColor=COLORS["gray_text"],
                   textAnchor="middle", fontName=CHINESE_FONT)
    d.add(label)

    # 指针
    angle_deg = 180 + (score / 100) * 180
    angle_rad = math.radians(angle_deg)
    needle_len = radius * 0.55
    nx = cx + needle_len * math.cos(angle_rad)
    ny = cy + needle_len * math.sin(angle_rad)
    needle = Line(cx, cy, nx, ny, strokeColor=COLORS["primary"], strokeWidth=2.5)
    d.add(needle)

    # 中心点
    center_dot = Circle(cx, cy, 5, fillColor=COLORS["primary"], strokeColor=None)
    d.add(center_dot)

    return d


# ---------------------------------------------------------------------------
# 风险柱状图
# ---------------------------------------------------------------------------
def create_risk_bar_chart(high, medium, low, width=400, height=100):
    """创建一个水平堆叠柱状图，显示风险分布。"""
    d = Drawing(width, height)
    total = high + medium + low
    if total == 0:
        return d

    bar_width = width * 0.7
    bar_height = 30
    x_start = width * 0.15
    y = height * 0.4

    # 柱条
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

    # 标签
    labels = [
        (f"高风险: {high}", COLORS["danger"], x_start),
        (f"中风险: {medium}", COLORS["warning"], x_start + bar_width * 0.35),
        (f"低风险: {low}", COLORS["success"], x_start + bar_width * 0.7),
    ]
    for text, color, x in labels:
        d.add(String(x, y - 15, text, fontSize=9, fillColor=color,
                     fontName=CHINESE_FONT))

    return d


# ---------------------------------------------------------------------------
# 样式定义
# ---------------------------------------------------------------------------
def get_styles():
    styles = getSampleStyleSheet()

    # 更新默认字体
    for style_name in styles.byName:
        styles[style_name].fontName = CHINESE_FONT

    styles.add(ParagraphStyle(
        name="CoverTitle", fontName=CHINESE_FONT, fontSize=28,
        textColor=COLORS["primary"], alignment=TA_CENTER, spaceAfter=10
    ))
    styles.add(ParagraphStyle(
        name="CoverSubtitle", fontName=CHINESE_FONT, fontSize=14,
        textColor=COLORS["gray_text"], alignment=TA_CENTER, spaceAfter=30
    ))
    styles.add(ParagraphStyle(
        name="SectionHeader", fontName=CHINESE_FONT, fontSize=16,
        textColor=COLORS["primary"], spaceBefore=20, spaceAfter=10,
        borderWidth=0, borderPadding=5
    ))
    styles.add(ParagraphStyle(
        name="SubHeader", fontName=CHINESE_FONT, fontSize=12,
        textColor=COLORS["secondary"], spaceBefore=12, spaceAfter=6
    ))
    styles.add(ParagraphStyle(
        name="BodyText2", fontName=CHINESE_FONT, fontSize=10,
        textColor=COLORS["dark_text"], spaceBefore=4, spaceAfter=4,
        leading=14
    ))
    styles.add(ParagraphStyle(
        name="RiskHigh", fontName=CHINESE_FONT, fontSize=10,
        textColor=COLORS["danger"], spaceBefore=2, spaceAfter=2
    ))
    styles.add(ParagraphStyle(
        name="RiskMedium", fontName=CHINESE_FONT, fontSize=10,
        textColor=COLORS["warning"], spaceBefore=2, spaceAfter=2
    ))
    styles.add(ParagraphStyle(
        name="RiskLow", fontName=CHINESE_FONT, fontSize=10,
        textColor=COLORS["success"], spaceBefore=2, spaceAfter=2
    ))
    styles.add(ParagraphStyle(
        name="Disclaimer", fontName=CHINESE_FONT, fontSize=8,
        textColor=COLORS["gray_text"], alignment=TA_CENTER, spaceBefore=10,
        spaceAfter=10
    ))
    styles.add(ParagraphStyle(
        name="Footer", fontName=CHINESE_FONT, fontSize=8,
        textColor=COLORS["gray_text"], alignment=TA_CENTER
    ))

    return styles


# ---------------------------------------------------------------------------
# PDF 构建器
# ---------------------------------------------------------------------------
def build_pdf(data, output_path):
    """根据结构化数据构建 PDF 报告。"""
    styles = get_styles()
    doc = SimpleDocTemplate(
        output_path, pagesize=letter,
        leftMargin=0.75 * inch, rightMargin=0.75 * inch,
        topMargin=0.75 * inch, bottomMargin=0.75 * inch
    )
    story = []

    # ── 封面 ──
    story.append(Spacer(1, 1.8 * inch))
    story.append(Paragraph("合同审查报告", styles["CoverTitle"]))
    story.append(Spacer(1, 40))
    story.append(Paragraph(
        f"生成日期: {datetime.now().strftime('%Y年%m月%d日')}",
        styles["CoverSubtitle"]
    ))
    story.append(Spacer(1, 60))

    # 评分仪表盘
    score = data.get("score", 0)
    gauge = create_score_gauge(score)
    story.append(gauge)
    story.append(Spacer(1, 40))

    # 等级标签
    grade = data.get("grade", "N/A")
    grade_label = data.get("grade_label", "")
    story.append(Paragraph(
        f"等级: {grade} — {grade_label}", styles["CoverSubtitle"]
    ))

    # 免责声明
    story.append(Spacer(1, 40))
    story.append(Paragraph(
        "法律免责声明：本分析由 AI 生成，不构成正式法律意见。本报告仅供审查参考。在签署合同或依赖本报告之前，请务必咨询专业律师。",
        styles["Disclaimer"]
    ))

    story.append(PageBreak())

    # ── 合同详情 ──
    story.append(Paragraph("合同基本信息", styles["SectionHeader"]))
    story.append(HRFlowable(
        width="100%", thickness=1, color=COLORS["light_border"]
    ))

    details = data.get("details", {})
    detail_rows = [
        ["合同类型", details.get("type", "N/A")],
        ["当事人", details.get("parties", "N/A")],
        ["生效日期", details.get("effective_date", "N/A")],
        ["履行期限", details.get("term", "N/A")],
        ["合同总值", details.get("total_value", "N/A")],
        ["管辖法律/机构", details.get("governing_law", "N/A")],
    ]
    detail_table = Table(detail_rows, colWidths=[2 * inch, 4.5 * inch])
    detail_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), CHINESE_FONT),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("TEXTCOLOR", (0, 0), (0, -1), COLORS["primary"]),
        ("TEXTCOLOR", (1, 0), (1, -1), COLORS["dark_text"]),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("LINEBELOW", (0, 0), (-1, -2), 0.5, COLORS["light_border"]),
    ]))
    story.append(detail_table)
    story.append(Spacer(1, 20))

    # ── 执行摘要 ──
    story.append(Paragraph("执行摘要", styles["SectionHeader"]))
    story.append(HRFlowable(
        width="100%", thickness=1, color=COLORS["light_border"]
    ))
    story.append(Paragraph(
        data.get("executive_summary", "无可用摘要。"),
        styles["BodyText2"]
    ))
    story.append(Spacer(1, 20))

    # ── 风险看板 ──
    story.append(Paragraph("风险看板", styles["SectionHeader"]))
    story.append(HRFlowable(
        width="100%", thickness=1, color=COLORS["light_border"]
    ))

    risks = data.get("risks", {"high": 0, "medium": 0, "low": 0})
    risk_chart = create_risk_bar_chart(
        risks.get("high", 0), risks.get("medium", 0), risks.get("low", 0)
    )
    story.append(risk_chart)
    story.append(Spacer(1, 15))

    # 风险摘要表格
    risk_rows = [
        ["风险等级", "条款数量", "涉及条款"],
        ["🔴 高风险", str(risks.get("high", 0)),
         risks.get("high_clauses", "无")],
        ["🟡 中风险", str(risks.get("medium", 0)),
         risks.get("medium_clauses", "无")],
        ["🟢 低风险", str(risks.get("low", 0)),
         risks.get("low_clauses", "无")],
    ]
    risk_table = Table(risk_rows, colWidths=[1.5 * inch, 1 * inch, 4 * inch])
    risk_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), CHINESE_FONT),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("BACKGROUND", (0, 0), (-1, 0), COLORS["primary"]),
        ("TEXTCOLOR", (0, 0), (-1, 0), COLORS["white"]),
        ("BACKGROUND", (0, 1), (-1, 1), COLORS["high_risk_bg"]),
        ("TEXTCOLOR", (0, 1), (0, 1), COLORS["danger"]),
        ("BACKGROUND", (0, 2), (-1, 2), COLORS["med_risk_bg"]),
        ("TEXTCOLOR", (0, 2), (0, 2), COLORS["warning"]),
        ("BACKGROUND", (0, 3), (-1, 3), COLORS["low_risk_bg"]),
        ("TEXTCOLOR", (0, 3), (0, 3), COLORS["success"]),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("GRID", (0, 0), (-1, -1), 0.5, COLORS["light_border"]),
    ]))
    story.append(risk_table)
    story.append(Spacer(1, 20))

    # ── 条款分析 ──
    clauses = data.get("clauses", [])
    if clauses:
        story.append(PageBreak())
        story.append(Paragraph("逐条条款分析", styles["SectionHeader"]))
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
            risk_emoji = {"high": "🔴 高风险", "medium": "🟡 中风险", "low": "🟢 低风险"}.get(risk, "")

            clause_block = []
            clause_block.append(Paragraph(
                f'<font color="{risk_color.hexval()}">[{risk_emoji}]</font> '
                f'<b>{clause.get("name", "未命名条款")}</b> — 第 {clause.get("section", "N/A")} 节',
                styles["SubHeader"]
            ))
            if clause.get("summary"):
                clause_block.append(Paragraph(
                    f'<b>内容摘要:</b> {clause["summary"]}', styles["BodyText2"]
                ))
            if clause.get("risk_explanation"):
                clause_block.append(Paragraph(
                    f'<b>风险点:</b> {clause["risk_explanation"]}', styles["BodyText2"]
                ))
            if clause.get("recommendation"):
                clause_block.append(Paragraph(
                    f'<b>修改建议:</b> {clause["recommendation"]}', styles["BodyText2"]
                ))
            clause_block.append(Spacer(1, 10))
            story.append(KeepTogether(clause_block))

    # ── 谈判优先级 ──
    priorities = data.get("negotiation_priorities", [])
    if priorities:
        story.append(Paragraph("谈判优先级", styles["SectionHeader"]))
        story.append(HRFlowable(
            width="100%", thickness=1, color=COLORS["light_border"]
        ))
        for i, priority in enumerate(priorities, 1):
            story.append(Paragraph(f"<b>{i}.</b> {priority}", styles["BodyText2"]))
        story.append(Spacer(1, 20))

    # ── 缺失的保护性条款 ──
    missing = data.get("missing_protections", [])
    if missing:
        story.append(Paragraph("缺失的必要保障", styles["SectionHeader"]))
        story.append(HRFlowable(
            width="100%", thickness=1, color=COLORS["light_border"]
        ))
        for item in missing:
            story.append(Paragraph(f"• {item}", styles["BodyText2"]))
        story.append(Spacer(1, 20))

    # ── 后续步骤 ──
    steps = data.get("next_steps", [])
    if steps:
        story.append(Paragraph("建议后续步骤", styles["SectionHeader"]))
        story.append(HRFlowable(
            width="100%", thickness=1, color=COLORS["light_border"]
        ))
        for i, step in enumerate(steps, 1):
            story.append(Paragraph(f"<b>{i}.</b> {step}", styles["BodyText2"]))

    # ── 页脚 ──
    story.append(Spacer(1, 40))
    story.append(HRFlowable(
        width="100%", thickness=0.5, color=COLORS["light_border"]
    ))
    story.append(Paragraph(
        "本报告由 AI 法律助手生成。不构成法律意见。签署前请咨询律师。",
        styles["Disclaimer"]
    ))
    story.append(Paragraph(
        f"生成于 {datetime.now().strftime('%Y年%m月%d日 %H:%M')}",
        styles["Footer"]
    ))

    # 构建
    doc.build(story)
    return output_path


# ---------------------------------------------------------------------------
# 主程序
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 generate_legal_pdf.py <json数据文件> [输出路径]")
        print("  json数据文件: 包含报告数据的 JSON 文件路径")
        print("  输出路径: 可选的 PDF 输出路径 (默认: 合同审查报告.pdf)")
        sys.exit(1)

    json_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else "合同审查报告.pdf"

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    result = build_pdf(data, output_path)
    print(f"PDF 已生成: {result}")
