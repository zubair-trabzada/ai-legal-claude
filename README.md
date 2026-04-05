<p align="center">
  <img src="assets/banner.svg" alt="AI Legal Assistant for Codex" width="900"/>
</p>

<p align="center">
  <strong>AI-powered contract review and legal document generation.</strong> Review contracts, flag risks,<br/>
  generate NDAs, check compliance, negotiate terms, and produce client-ready PDF reports — all from Codex.
</p>

<p align="center">
  Every contract has hidden risks. This tool finds them in 60 seconds.
</p>

<p align="center">
  <strong>Install once, then ask Codex to review contracts in plain English.</strong>
</p>

---

## Why This Matters

| Metric | Value |
|--------|-------|
| Average legal review cost | $300–$500/hour |
| Basic contract review | $1,500–$3,000 |
| Freelancers who don't read contracts | 82% |
| Cost of one bad clause | $10,000+ |
| Small businesses without legal review | 67% |
| Time to review with this tool | Under 60 seconds |

---

## Quick Start

```bash
curl -fsSL https://raw.githubusercontent.com/pa4uslf/ai-legal-codex/main/install.sh | bash
```

这会把全部 skill 安装到 `~/.codex/skills`，并把完整审查用的分析框架安装到 `~/.codex/agents`。

也可以本地安装：

```bash
./install.sh
```

安装后，重启 Codex 即可生效。

如果你需要导出 PDF 报告，再额外安装：

```bash
pip3 install reportlab
```

---

## How To Use In Codex

你可以直接自然语言触发：

```text
Review ./msa.pdf and tell me the top 3 legal risks.
Generate a mutual NDA between Acme and Beta for partnership talks.
Audit https://example.com for GDPR and CCPA compliance gaps.
```

推荐工作流：

1. 先让 Codex 完整审查合同并输出风险摘要
2. 再让 Codex 生成可直接回发的修改语言
3. 最后让 Codex 把最新分析导出成正式 PDF

---

## All 14 Capabilities

### Contract Analysis
| What To Ask Codex | What It Does |
|---------|-------------|
| “Review this contract and give me a full risk report.” | **Flagship** — Full contract review across 5 legal analysis lenses. Returns a Contract Safety Score, clause-by-clause analysis, and prioritized recommendations. |
| “Analyze the risk level of every clause in this contract.” | Deep risk analysis with severity scoring for every clause. Estimates financial exposure. |
| “Compare these two contract versions and tell me what changed.” | Side-by-side comparison of two contract versions. Flags additions, removals, and dangerous changes. |
| “Translate this contract into plain English.” | Translates every clause from legalese into plain English anyone can understand. |
| “Draft negotiation language for the risky clauses in this contract.” | Generates specific counter-proposals with replacement language for every unfavorable clause. |
| “Tell me what protections are missing from this contract.” | Finds protections that SHOULD be in the contract but aren't. |

### Document Generation
| What To Ask Codex | What It Does |
|---------|-------------|
| “Generate a mutual NDA for these two parties.” | Generates a custom NDA — mutual, one-way, employee, or vendor. |
| “Generate terms of service for this website: [url].” | Generates terms of service based on what the website actually does. GDPR/CCPA compliant. |
| “Generate a privacy policy for this website: [url].” | Generates a privacy policy by scanning what data the site collects. |
| “Draft a freelancer agreement / MSA / SOW / partnership agreement.” | Generates business agreements — freelancer contracts, partnerships, SOWs, MSAs, and more. |
| “Review this contract from the freelancer’s perspective.” | Specialized review from the freelancer's perspective. Flags common contractor traps. |

### Compliance & Reporting
| What To Ask Codex | What It Does |
|---------|-------------|
| “Audit this website for compliance gaps: [url].” | Compliance gap analysis — GDPR, CCPA, ADA, PCI-DSS, CAN-SPAM, SOC 2. |
| “Turn the latest legal analysis into a PDF report.” | Professional PDF report with score gauges, risk charts, and prioritized actions. |

---

## What You Get

- `Contract Safety Score`：快速判断一份合同是否值得继续推进
- `Clause-by-Clause Analysis`：逐条解释条款含义、风险和修改建议
- `Missing Protections`：指出合同缺失的关键保护条款
- `Negotiation Priorities`：给出最值得优先谈判的修改项
- `PDF Report`：生成适合交付给客户或团队的正式版报告

---

## The Flagship: Full Contract Review

The most powerful workflow. Ask Codex to review any contract and get:

1. **Contract Safety Score** (0-100) with letter grade
2. **Risk Dashboard** — high/medium/low risk clause counts
3. **Clause-by-Clause Analysis** — every clause scored, explained in plain English, with specific fix recommendations
4. **Missing Protections** — what should be there but isn't
5. **Obligations Timeline** — every deadline and consequence mapped
6. **Compliance Flags** — regulatory issues flagged
7. **Negotiation Priorities** — ranked list of what to change first
8. **Next Steps** — actionable checklist

### How It Works

```text
Review my-contract.pdf and produce a full legal risk report with a contract safety score.
```

Codex 版会默认按 5 个分析视角完成完整审查；如果你的宿主环境明确允许并行子代理，也可以把这 5 个视角并行执行：

| Analysis Lens | Role | Weight |
|-------|------|--------|
| Clause Analyst | Identifies and categorizes every clause | 20% |
| Risk Assessor | Scores each clause for risk | 25% |
| Compliance Checker | Flags regulatory issues | 20% |
| Terms Mapper | Maps obligations, deadlines, and triggers | 15% |
| Recommendations Engine | Generates specific fixes | 20% |

Results are aggregated into a unified report with a single Contract Safety Score.

---

## Codex-Friendly Design

这个仓库已经专门适配 Codex：

- 所有 skills 都补齐了 Codex frontmatter
- 安装目标统一为 `~/.codex/skills`
- PDF 脚本和模板会随 `legal-report-pdf` 一起安装
- 完整合同审查默认按 5 个分析视角运行，不强依赖并行子代理
- README 默认使用自然语言触发示例，不依赖 slash command 约定

---

## Use Cases

### For Freelancers & Agencies
- Review client contracts before signing
- Generate NDAs for new client engagements
- Create statements of work with proper protections
- Offer contract review as a paid service ($500-$1,500 per review)

### For Small Businesses
- Review vendor and supplier contracts
- Generate privacy policies and terms of service
- Run compliance audits on your website
- Understand what you're actually agreeing to

### For AI Automation Agencies
- Add contract review to your service offering
- Generate professional PDF reports for clients
- Offer monthly legal document management retainers
- Pair with the AI Marketing Suite and AI Sales Team

---

## Project Structure

```text
ai-legal-codex/
├── legal/
│   └── SKILL.md                    # Main orchestrator (command router)
├── skills/
│   ├── legal-review/SKILL.md       # Full contract review (5 review lenses)
│   ├── legal-risks/SKILL.md        # Deep risk analysis
│   ├── legal-compare/SKILL.md      # Contract comparison
│   ├── legal-plain/SKILL.md        # Plain English translation
│   ├── legal-negotiate/SKILL.md    # Counter-proposal generator
│   ├── legal-missing/SKILL.md      # Missing protections finder
│   ├── legal-nda/SKILL.md          # NDA generator
│   ├── legal-terms/SKILL.md        # Terms of service generator
│   ├── legal-privacy/SKILL.md      # Privacy policy generator
│   ├── legal-agreement/SKILL.md    # Business agreement generator
│   ├── legal-compliance/SKILL.md   # Compliance gap analysis
│   ├── legal-freelancer/SKILL.md   # Freelancer contract review
│   └── legal-report-pdf/SKILL.md   # PDF report generator
├── agents/
│   ├── legal-clauses.md            # Clause analysis framework
│   ├── legal-risks.md              # Risk assessment framework
│   ├── legal-compliance.md         # Compliance check framework
│   ├── legal-terms.md              # Terms & obligations framework
│   └── legal-recommendations.md    # Recommendations framework
├── scripts/
│   └── generate_legal_pdf.py       # PDF generation (ReportLab)
├── templates/
│   └── contract-review-template.md # Report template
├── install.sh                      # One-line installer
├── uninstall.sh                    # Clean uninstaller
└── README.md
```

---

## Requirements

- **Codex**
- **Python 3.8+** (for PDF generation only)
- **reportlab** — `pip3 install reportlab` (for PDF generation only)

---

## Uninstall

```bash
curl -fsSL https://raw.githubusercontent.com/pa4uslf/ai-legal-codex/main/uninstall.sh | bash
```

Or run locally:

```bash
./uninstall.sh
```

---

## Disclaimer

This tool is for educational and informational purposes only. It does **not** provide legal advice and should **not** be used as a substitute for consultation with a licensed attorney. Always have a qualified lawyer review any contract before signing.

Do not rely on AI-generated output as your final legal position in employment, fundraising, M&A, privacy, regulatory, or other high-stakes matters.

---

<p align="center">
  <strong>Part of the Codex Skills Series</strong><br>
  <a href="https://github.com/zubair-trabzada/ai-marketing-claude">AI Marketing Suite</a> ·
  <a href="https://github.com/zubair-trabzada/ai-sales-team-claude">AI Sales Team</a> ·
  <strong>AI Legal Assistant</strong>
</p>

<p align="center">
  <a href="https://www.skool.com/aiworkshop">🎓 Learn How to Sell Codex Services to Real Businesses</a>
</p>
