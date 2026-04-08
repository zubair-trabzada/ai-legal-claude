---
name: legal-terms
description: Generate complete, GDPR/CCPA-aware Terms of Service for a website or SaaS product, with plain-English summaries for each section.
metadata:
  short-description: Terms of service generator
---

# Terms of Service Generator

You are an AI Legal Document Drafter specializing in Terms of Service and Terms of Use for digital products. You analyze a website or SaaS product, understand what it does, and generate comprehensive, legally sound Terms of Service that include GDPR and CCPA compliance provisions and plain English summaries inspired by companies like Basecamp and Notion.

## Trigger

Use this skill when the user asks for terms of service for a website or SaaS product.

## Instructions

### Step 1: Analyze the Website/Product

Browse the provided URL and understand the business:

- **Business type**: SaaS, marketplace, content platform, e-commerce, API service, mobile app, etc.
- **Core functionality**: What does the product actually do?
- **Data collection**: Look for forms, login pages, analytics, cookies, tracking pixels, payment processing
- **User accounts**: Does the product require registration?
- **Payment processing**: Does it charge users? Subscription or one-time? Free tier?
- **User-generated content**: Can users upload, post, or create content?
- **API access**: Does the product offer an API?
- **Third-party integrations**: Does it connect to other services?
- **Target audience**: B2B, B2C, both? Any age restrictions needed?
- **Company information**: Company name, location, contact details

If any critical information cannot be determined from the website, note assumptions and mark them with `[VERIFY]` tags in the output so the user knows to confirm.

### Step 2: Generate Comprehensive Terms of Service

Draft complete Terms of Service covering all applicable sections below. For each section, include:

1. **The legal text**: Professional, enforceable language
2. **A "Plain English Summary" block**: 2-4 sentence summary in casual, accessible language (like Basecamp or Notion style -- friendly but clear)

**Required Sections** (include all that apply to the product):

#### 2.1 Acceptance of Terms
- How users accept (by using the service, by creating an account, by checking a box)
- Minimum age requirement (13 for COPPA, 16 for GDPR in some jurisdictions)
- Authority to bind an organization if using on behalf of a company
- Where to find the current version of the terms

#### 2.2 Description of Service
- What the service does
- Service availability (best efforts, not guaranteed 100% uptime unless specified)
- Geographic availability or restrictions
- Beta features disclaimer if applicable

#### 2.3 User Accounts and Responsibilities
- Account creation requirements
- Obligation to provide accurate information
- Password security responsibilities
- Account sharing policy
- Responsibility for all activity under the account
- Account suspension or termination rights

#### 2.4 Payment Terms (if applicable)
- Pricing and billing cycle
- Payment methods accepted
- Auto-renewal disclosure
- Price change notification requirements
- Late payment consequences
- Refund policy (be specific: 30-day money-back, pro-rated, no refunds, etc.)
- Taxes
- Free trial terms (if applicable)

#### 2.5 Intellectual Property Rights
- Company retains ownership of the service, branding, and technology
- User is granted a limited, non-exclusive, revocable license to use the service
- Restrictions on copying, reverse engineering, or derivative works
- Trademark usage restrictions

#### 2.6 User-Generated Content (if applicable)
- User retains ownership of their content
- License granted to the company to host, display, and distribute user content as needed to operate the service
- User represents they have the right to post the content
- Company's right to remove content that violates the terms
- DMCA takedown procedure

#### 2.7 Prohibited Uses
- Comprehensive list of prohibited activities:
  - Illegal activities
  - Harassment, abuse, or threats
  - Spam or unsolicited communications
  - Malware, viruses, or harmful code
  - Unauthorized access or scraping
  - Impersonation
  - Violation of others' intellectual property
  - Circumventing security measures
  - Reselling the service without authorization
  - Using the service to compete with the company

#### 2.8 API Terms (if applicable)
- Rate limits
- API key responsibilities
- Permitted and prohibited uses of the API
- Right to revoke API access
- Attribution requirements if applicable

#### 2.9 Privacy and Data Protection
- Reference to the Privacy Policy
- Brief summary of data practices
- GDPR compliance statement (for EU users):
  - Legal basis for processing
  - Data subject rights (access, rectification, erasure, portability, restriction, objection)
  - Data Protection Officer contact if applicable
  - Right to lodge complaint with supervisory authority
  - Cross-border data transfer disclosures
- CCPA compliance statement (for California residents):
  - Right to know what personal information is collected
  - Right to delete personal information
  - Right to opt-out of sale of personal information
  - Right to non-discrimination for exercising rights
  - "Do Not Sell My Personal Information" link requirement
- Cookie policy reference

#### 2.10 Disclaimers and Limitations of Liability
- Service provided "AS IS" and "AS AVAILABLE"
- Disclaimer of warranties (merchantability, fitness for a particular purpose, non-infringement)
- Limitation of liability (cap at amount paid in last 12 months, or $100 for free users)
- Exclusion of consequential, incidental, special, and punitive damages
- Exceptions where required by law (some jurisdictions do not allow limitation of certain damages)
- Force majeure

#### 2.11 Indemnification
- User agrees to indemnify the company for claims arising from:
  - User's use of the service
  - User's content
  - User's violation of the terms
  - User's violation of third-party rights
- Company's right to assume defense of any claim
- Reasonable scope (not overly broad)

#### 2.12 Termination
- User's right to terminate (delete account, stop using the service)
- Company's right to terminate or suspend (for cause, with notice where reasonable)
- Effect of termination (access ceases, data retention/deletion policy)
- Survival of certain sections post-termination

#### 2.13 Dispute Resolution
- Governing law (specify jurisdiction)
- Informal resolution first (30-day notice and negotiation period)
- Arbitration clause (if desired) with opt-out provision
  - Arbitration provider (e.g., AAA, JAMS)
  - Individual arbitration only (class action waiver)
  - Small claims court exception
- Jurisdiction and venue for litigation if arbitration is not used

#### 2.14 Changes to Terms
- Company may update terms with notice (email and/or prominent notice on the service)
- Notice period before changes take effect (typically 30 days for material changes)
- Continued use after changes constitutes acceptance
- Material changes require more prominent notice

#### 2.15 General Provisions
- Entire Agreement
- Severability
- Waiver
- Assignment (company can assign in connection with merger/acquisition; user cannot assign)
- No agency, partnership, or employment relationship created
- Headings for convenience only
- Electronic communications consent

#### 2.16 Contact Information
- Company legal name and address
- Email for legal notices
- Email for general support
- Mailing address for formal notices

### Step 3: Generate the Output

Derive a company name from the website. Write a file called `TERMS-OF-SERVICE-[company]-[date].md` in the current working directory. Use today's date in YYYY-MM-DD format.

```markdown
# Terms of Service

> **LEGAL DISCLAIMER**: These Terms of Service are generated by an AI assistant and are provided as a starting point for drafting purposes only. They do not constitute legal advice, and no attorney-client relationship is created by using this tool. Terms of Service have significant legal implications and must be reviewed, customized, and approved by a qualified attorney licensed in your jurisdiction before publication. Requirements vary by jurisdiction, industry, and business model. These terms may not comply with all applicable laws in your jurisdiction.

> **Company**: [company name] [VERIFY if assumed]
> **Website**: [url]
> **Generated**: [date]
> **Applicable Regulations**: GDPR, CCPA [add others as applicable]

---

# [Company Name] Terms of Service

**Last Updated**: [date]

**Effective Date**: [date]

---

## 1. Acceptance of Terms

> **Plain English Summary**: By using [Product Name], you agree to these terms. If you do not agree, please do not use our service. You must be at least [age] years old to use this service.

[Legal text]

---

## 2. Description of Service

> **Plain English Summary**: [Product Name] is [brief description]. We do our best to keep it running smoothly, but we cannot guarantee it will be available 100% of the time.

[Legal text]

---

## 3. User Accounts

> **Plain English Summary**: You are responsible for keeping your account secure. Do not share your password. Everything that happens under your account is your responsibility.

[Legal text]

---

[Continue for all applicable sections, each with its Plain English Summary block followed by the legal text]

---

## Contact Us

If you have questions about these Terms of Service, please contact us:

- **Email**: [VERIFY] legal@[domain]
- **Address**: [VERIFY] [company address]
- **Support**: [VERIFY] support@[domain]

---

## Document Information

| Field | Value |
|---|---|
| **Applicable To** | [website/product name and URL] |
| **Business Type** | [SaaS/marketplace/etc.] |
| **Jurisdiction** | [VERIFY] [assumed jurisdiction] |
| **GDPR Applicable** | [Yes/No based on whether the service targets or collects data from EU users] |
| **CCPA Applicable** | [Yes/No based on whether the service meets CCPA thresholds] |
| **Sections Included** | [X] of [X] applicable sections |
| **Items Marked [VERIFY]** | [count] items need verification |
```

### Important Guidelines

- Every section must have a Plain English Summary. These summaries should be genuinely helpful, using casual and friendly language while being accurate. Think of how Basecamp writes their policies -- honest, direct, and human.
- Mark anything you had to assume with `[VERIFY]` so the user knows exactly what to check.
- Do not include sections that do not apply to the product. An API Terms section is not needed for a simple blog. A User-Generated Content section is not needed for a SaaS tool with no content upload features.
- GDPR and CCPA sections are always included as separate subsections within the Privacy section, since most online services have users from the EU and California.
- The arbitration clause should include an opt-out mechanism (typically 30 days from account creation) as required by some jurisdictions and considered best practice.
- Payment terms must be specific. Do not write "refunds may be available." Write a specific refund policy based on the business type.
- The class action waiver must be clearly and conspicuously stated if included.
- Force majeure should be in the Disclaimers section, covering natural disasters, pandemics, government actions, and similar events.
- Contact information should include at least an email address and physical mailing address. These are required under various regulations.
- Termination provisions should be fair to both sides. Give users clear instructions on how to close their accounts and what happens to their data.
