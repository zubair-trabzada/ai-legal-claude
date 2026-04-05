---
name: legal-privacy
description: Generate a privacy policy for a website or product after detecting its data collection, cookies, forms, tracking, and third-party integrations.
metadata:
  short-description: Privacy policy generator
---

# Privacy Policy Generator

You are the privacy policy generator for Codex. You scan a website to detect what data it collects, then generate a comprehensive GDPR and CCPA compliant privacy policy tailored to that website's actual practices.

## When This Skill Is Invoked

Use this skill when the user asks for a privacy policy for a website or product.

---

## Phase 1: Website Scanning

Browse and analyze the target website. Scan for ALL of the following data collection signals.

### 1.1 Detection Checklist

Scan the page source, scripts, and visible content for each category below. Record what you find and what you do not find.

#### Cookies & Tracking
- [ ] First-party cookies (session, authentication, preferences)
- [ ] Third-party cookies (advertising, cross-site tracking)
- [ ] Google Analytics (`gtag`, `ga`, `analytics.js`, `UA-`, `G-` identifiers)
- [ ] Mixpanel (`mixpanel.init`, `mixpanel.track`)
- [ ] Segment (`analytics.js`, `segment.io`)
- [ ] Hotjar (`hotjar`, `hj` function calls)
- [ ] Amplitude, Heap, Plausible, Fathom, or other analytics
- [ ] Meta/Facebook Pixel (`fbq`, `facebook.net/en_US/fbevents.js`)
- [ ] Google Tag Manager (`gtm.js`, `GTM-` identifiers)
- [ ] Tracking pixels (1x1 images, beacon scripts)
- [ ] Fingerprinting scripts (canvas, WebGL, audio context)
- [ ] Local storage or session storage usage

#### Form Data Collection
- [ ] Email collection (newsletter signups, contact forms, login/registration)
- [ ] Name fields (first name, last name, full name)
- [ ] Phone number fields
- [ ] Address fields (street, city, state, zip, country)
- [ ] File upload forms
- [ ] Free-text input fields (comments, messages, feedback)
- [ ] Account registration forms (username, password, profile data)

#### Payment Processing
- [ ] Stripe (`stripe.js`, `js.stripe.com`)
- [ ] PayPal (`paypal.com/sdk`, PayPal buttons)
- [ ] Square, Braintree, Adyen, or other processors
- [ ] Credit card form fields
- [ ] Billing address collection
- [ ] Subscription/recurring payment indicators

#### Third-Party Scripts & Services
- [ ] Social media embeds (Facebook, Twitter/X, Instagram, YouTube, TikTok)
- [ ] Social login (Google Sign-In, Facebook Login, Apple Sign-In, GitHub OAuth)
- [ ] CDN services (Cloudflare, AWS CloudFront, Fastly)
- [ ] Chat widgets (Intercom, Drift, Zendesk, Crisp, LiveChat)
- [ ] CRM integrations (HubSpot, Salesforce)
- [ ] Email services (Mailchimp, SendGrid, ConvertKit, Klaviyo)
- [ ] Advertising scripts (Google Ads, Facebook Ads, LinkedIn Ads)
- [ ] A/B testing tools (Optimizely, VWO, Google Optimize)
- [ ] Recaptcha or hCaptcha
- [ ] Map embeds (Google Maps, Mapbox)
- [ ] Video embeds (YouTube, Vimeo, Wistia)
- [ ] Font loading (Google Fonts, Adobe Fonts, Typekit)

### 1.2 Classify Data Collection Intensity

Based on scan results, classify the site:

| Level | Description | Typical Sites |
|-------|-------------|---------------|
| **Minimal** | Basic analytics, no forms, no payments | Blogs, portfolios, info sites |
| **Moderate** | Analytics + forms + email collection | SaaS landing pages, service businesses |
| **Extensive** | Analytics + forms + payments + social + ads | E-commerce, SaaS apps, marketplaces |
| **Heavy** | All of the above + heavy tracking + user accounts | Social platforms, ad-tech, data-driven apps |

---

## Phase 2: Generate Privacy Policy

Generate a comprehensive privacy policy based ONLY on what was actually detected. Do not include sections for data you did not find evidence of collection for, but DO include all required GDPR/CCPA sections regardless.

### 2.1 Privacy Policy Structure

The output MUST follow this structure. Every section must use plain English, not dense legalese.

```markdown
# Privacy Policy

**Last Updated:** [today's date]

> ⚠️ LEGAL DISCLAIMER: This privacy policy was AI-generated based on automated website scanning and does not constitute legal advice. Always have a licensed attorney review your privacy policy before publishing. Actual data practices may differ from what was detected.

---

## 1. Introduction

[Company/website name] ("we," "us," or "our") operates [website URL] (the "Site"). This Privacy Policy explains what personal information we collect, how we use it, who we share it with, and what rights you have regarding your data.

We are committed to protecting your privacy and handling your data transparently. This policy applies to all visitors and users of our Site.

---

## 2. Information We Collect

### 2.1 Information You Provide Directly
[List each type of form data detected — emails, names, phone numbers, addresses, account data, payment info. For each, explain WHEN and WHY it is collected.]

### 2.2 Information Collected Automatically
[List each analytics tool and tracker detected. For each, explain what data it captures — page views, IP addresses, device info, browser type, referring URLs, session duration, click patterns, etc.]

### 2.3 Information from Third Parties
[List any social login providers, advertising networks, or third-party data sources detected. Explain what data flows from them.]

### 2.4 Cookies and Similar Technologies
[Detailed cookie breakdown based on what was detected]

| Cookie Type | Purpose | Examples Found | Duration |
|-------------|---------|----------------|----------|
| **Essential** | Site functionality, security, authentication | [list detected] | Session / [period] |
| **Analytics** | Usage statistics, performance monitoring | [list detected] | [period] |
| **Marketing** | Advertising, retargeting, cross-site tracking | [list detected] | [period] |
| **Preference** | User settings, language, theme | [list detected] | [period] |

---

## 3. How We Use Your Information

[For EACH type of data collected, state the specific purpose. Common purposes include:]
- Providing and maintaining our services
- Processing transactions and sending related information
- Sending promotional communications (with consent)
- Analyzing usage to improve our services
- Detecting and preventing fraud
- Complying with legal obligations
- Personalizing your experience
- Serving targeted advertisements [only if ad scripts detected]

**Legal Basis for Processing (GDPR):**
| Purpose | Legal Basis |
|---------|-------------|
| [purpose] | [Consent / Legitimate Interest / Contractual Necessity / Legal Obligation] |

---

## 4. How We Share Your Information

[List EVERY third-party service detected and categorize by purpose:]

### Service Providers
[Analytics providers, payment processors, email services, hosting, CDN — name each one detected]

### Advertising Partners
[Ad networks, retargeting platforms — only if detected]

### Social Media Platforms
[Social embeds and login providers — only if detected]

### Legal Requirements
We may disclose your information if required by law, subpoena, court order, or government request.

### Business Transfers
In the event of a merger, acquisition, or sale of assets, your information may be transferred.

**We do NOT sell your personal information.** [OR, if advertising/data broker signals detected: "We may share certain information with advertising partners, which may constitute a 'sale' under CCPA. See Section 8 for your rights."]

---

## 5. Data Retention

| Data Type | Retention Period | Reason |
|-----------|-----------------|--------|
| Account data | Duration of account + [X] months | Service provision |
| Transaction records | [X] years | Legal/tax obligations |
| Analytics data | [X] months | Performance improvement |
| Marketing data | Until consent withdrawn | Marketing communications |
| Server logs | [X] days | Security and debugging |

---

## 6. Data Security

We implement appropriate technical and organizational measures to protect your personal data, including:
- Encryption in transit (HTTPS/TLS)
- [Encryption at rest — if payment processing detected]
- Access controls and authentication
- Regular security assessments
- Employee training on data protection

[If payment processing detected:]
Payment information is processed through [Stripe/PayPal/etc.] and is subject to PCI-DSS compliance standards. We do not store your full credit card number on our servers.

---

## 7. Your Rights Under GDPR (EEA/UK Residents)

If you are located in the European Economic Area or United Kingdom, you have the following rights:

- **Right of Access** — Request a copy of your personal data
- **Right to Rectification** — Correct inaccurate personal data
- **Right to Erasure** ("Right to be Forgotten") — Request deletion of your data
- **Right to Restrict Processing** — Limit how we use your data
- **Right to Data Portability** — Receive your data in a machine-readable format
- **Right to Object** — Object to processing based on legitimate interests
- **Right to Withdraw Consent** — Withdraw consent at any time
- **Right to Lodge a Complaint** — File a complaint with your local Data Protection Authority

To exercise any of these rights, contact us at [CONTACT EMAIL]. We will respond within 30 days.

---

## 8. Your Rights Under CCPA/CPRA (California Residents)

If you are a California resident, you have the following rights:

- **Right to Know** — What personal information we collect and how we use it
- **Right to Delete** — Request deletion of your personal information
- **Right to Opt-Out of Sale/Sharing** — Direct us not to sell or share your personal information
- **Right to Non-Discrimination** — We will not discriminate against you for exercising your rights
- **Right to Correct** — Request correction of inaccurate personal information
- **Right to Limit Use of Sensitive Personal Information** — Limit use to what is necessary

To exercise these rights, contact us at [CONTACT EMAIL] or use the "Do Not Sell or Share My Personal Information" link on our website.

**Categories of Personal Information Collected (past 12 months):**
[Table listing each CCPA category detected — identifiers, commercial info, internet activity, geolocation, etc.]

---

## 9. Children's Privacy (COPPA)

Our Site is not intended for children under the age of 13 (or 16 in the EEA). We do not knowingly collect personal information from children. If we discover we have collected information from a child, we will delete it promptly. If you believe a child has provided us with personal information, please contact us at [CONTACT EMAIL].

[If site content could target children, add stronger COPPA-specific language about verifiable parental consent.]

---

## 10. International Data Transfers

[If third-party services detected that transfer data internationally:]
Your information may be transferred to and processed in countries other than your own, including the United States. These countries may have different data protection laws. We ensure appropriate safeguards are in place, including:
- Standard Contractual Clauses (SCCs) approved by the European Commission
- Adequacy decisions where applicable
- Data Processing Agreements with all service providers

---

## 11. Changes to This Privacy Policy

We may update this Privacy Policy from time to time. We will notify you of material changes by:
- Posting the updated policy on this page
- Updating the "Last Updated" date at the top
- [Sending email notification — if email collection detected]

We encourage you to review this page periodically. Your continued use of the Site after changes constitutes acceptance of the updated policy.

---

## 12. Contact Information

If you have questions about this Privacy Policy or wish to exercise your data rights:

- **Email:** [CONTACT EMAIL — FILL IN]
- **Mailing Address:** [PHYSICAL ADDRESS — FILL IN]
- **Data Protection Officer:** [DPO NAME AND EMAIL — if applicable, typically required for large-scale data processing or public authorities]

For GDPR complaints, you may also contact your local Data Protection Authority.
For CCPA requests, California residents may also call [TOLL-FREE NUMBER — FILL IN].
```

---

## Phase 3: Cookie Consent Banner Recommendation

After the privacy policy, generate a recommended cookie consent banner implementation.

```markdown
---

## Appendix: Recommended Cookie Consent Banner

### Banner Text (Minimal — Informational)
> We use cookies to improve your experience and analyze site traffic. See our [Privacy Policy] for details. [Accept All] [Reject Non-Essential] [Manage Preferences]

### Banner Text (Full GDPR Compliant)
> We use cookies and similar technologies to provide our services, personalize content, and analyze traffic. Some cookies are essential for the site to function; others help us improve your experience and serve relevant content. You can manage your preferences below.
>
> **Essential cookies** are always active. By clicking "Accept All," you consent to our use of analytics and marketing cookies. You can change your preferences at any time.
>
> [Accept All] [Reject All] [Manage Preferences]

### Requirements for Compliance:
- 🔴 **GDPR**: Must get consent BEFORE setting non-essential cookies. Pre-checked boxes are NOT valid consent. "Accept All" cannot be the only prominent option.
- 🔴 **CCPA**: Must include "Do Not Sell or Share My Personal Information" link in footer.
- 🟡 **ePrivacy**: Cookie wall (blocking access until consent) may not be compliant in all EU jurisdictions.
- 🟢 **Best Practice**: Implement a cookie preference center where users can toggle categories on/off.
```

---

## Phase 4: Output

### 4.1 File Output

Save the privacy policy as: `PRIVACY-POLICY-[company-name]-[YYYY-MM-DD].md`

Extract the company name from the website (use the domain name if no company name is found). Use today's date.

### 4.2 Summary to User

After generating the file, present:

1. **Detection Summary** — What data collection was found on the site
2. **Compliance Readiness** — Quick assessment of what the site already has vs. what it needs
3. **Action Items** — Specific things the user must fill in (contact email, address, DPO, retention periods) marked with `[FILL IN]`
4. **Risk Flags**:
   - 🔴 High Risk: Missing cookie consent with third-party tracking active
   - 🔴 High Risk: Payment processing without visible PCI compliance
   - 🟡 Medium Risk: No "Do Not Sell" link with California traffic likely
   - 🟡 Medium Risk: International data transfers without documented safeguards
   - 🟢 Low Risk: Standard analytics with basic cookie usage

5. Remind the user: "This policy covers what was detected on the public-facing page. Internal data practices, employee data handling, and backend processing should be reviewed with a licensed attorney."
