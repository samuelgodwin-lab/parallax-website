# Article draft — hub · Accessibility deadlines across all four markets

Signed off 3 Oct 2026 and **loaded into the CMS as a draft** (articles id
`682e4a55-19e5-4aff-b043-2e1730cee852`, slug `accessibility-deadlines-2026`,
category compliance, author Samuel Godwin, tags Accessibility · WCAG · ADA Title II ·
EAA · BFSG · GIGW · IS 17802 · UAE). Add a hero and publish from
`/admin/article-editor.html?id=682e4a55-19e5-4aff-b043-2e1730cee852`; live at
`/articles/accessibility-deadlines-2026`.

**Why this piece:** the four market articles (Denver, Munich, Dubai, Northeast
India) each answer one country's question. Nothing on the site answers the
question a company selling in more than one of them asks: *what is due, where,
and when?* This is that page. It links all four (it's the hub they've been
missing) and it's built to be kept current: a visible "last updated" line,
and a note to republish when a date moves. That keeps `dateModified` fresh,
and freshness is what answer engines weigh on a deadline query.

**AEO/SEO shape:** answer-first paragraph that stands alone if quoted;
question-shaped H3s matching real queries; one dated timetable; the same
standard named in every section; six FAQs → `FAQPage` schema; four internal
links + one CTA. About 1,350 words.

---

**Slug:** `/articles/accessibility-deadlines-2026`
**Title (CMS, accent marked):** Accessibility law in 2026: the *deadlines* in the US, EU, UAE and India
**Title tag (57):** Digital Accessibility Deadlines 2026: US, EU, UAE and India
**Description (153):** One standard, four timetables. The web-accessibility deadlines in the US, EU, UAE and India, what WCAG 2.1 AA requires, and what to fix first.
**Category:** Compliance · **Read time:** 6 min · **Author:** Parallax

---

## Accessibility law in 2026: the deadlines in the US, EU, UAE and India

*Four markets, four laws, one standard. If you sell digital products in more than one of them, here is the timetable on one page. We update it whenever a date moves.*

*Last updated 3 October 2026.*

**In one paragraph.** In every market we work in, the legal bar for websites and apps is the same: WCAG 2.1 Level AA. Only the dates and the enforcers differ. The **EU** has enforced it on consumer products since 28 June 2025 under the European Accessibility Act. The **US** requires it of state and local government from 26 April 2027, or 26 April 2028 for smaller entities, and Colorado already does. The **UAE** applies it to federal government services now. **India** applies it to government through GIGW 3.0 and is extending it to every company through draft rules phased over one to two years. One audit and one compliant design system cover all four.

### What are the deadlines?

| Market | Law | Who | Date | Standard |
|---|---|---|---|---|
| EU (incl. Germany) | European Accessibility Act / BFSG | Consumer sites, apps, shops, banking, ticketing | **28 June 2025** (in force) | EN 301 549 → WCAG 2.1 AA |
| Colorado | HB21-1110 | State and local government, and their vendors | **1 July 2025** (in force) | WCAG 2.1 AA |
| United States | ADA Title II web rule | Public entities serving 50,000+ | **26 April 2027** | WCAG 2.1 AA |
| United States | ADA Title II web rule | Public entities under 50,000, special districts | **26 April 2028** | WCAG 2.1 AA |
| UAE | National Digital Accessibility Policy | Federal government websites and apps | **In force** | WCAG 2.1 AA |
| India | GIGW 3.0 | Central and state government websites and apps | **In force** (STQC audit) | GIGW 3.0 / IS 17802 |
| India | Draft RPwD (Amendment) Rules 2026 | Every establishment offering digital products in India | **12–24 months after notification** (draft, July 2026) | IS 17802 → WCAG 2.1 AA |

### Is it really the same standard everywhere?

Yes, in practice. The US rule names WCAG 2.1 AA directly. The EU's EN 301 549 incorporates it for web and mobile. India's IS 17802 is modelled on EN 301 549. The UAE design system guides federal entities to it. A product that meets WCAG 2.1 AA meets the technical bar in all four markets. What changes from place to place is the paperwork around it and who can come after you.

WCAG 2.2 is not yet required anywhere on this list. Meeting it satisfies 2.1, and the next EN 301 549 revision is expected to adopt it, so it's the sensible build target.

### United States: who has to comply, and when?

ADA Title II covers state and local government: cities, counties, school districts, public universities, transit and courts. In April 2026 the Department of Justice moved its deadlines back a year but left the standard unchanged. Large entities must comply by 26 April 2027 and smaller ones by 26 April 2028. Colorado didn't wait: its own law has applied since 1 July 2025, with a $3,500 fine per violation paid to the person affected.

Private companies are reached two ways. A vendor's product becomes the government's product once the public uses it, so the requirement flows down through contracts and RFPs. Businesses open to the public face Title III lawsuits, which number in the thousands every year. → [ADA Title II in Colorado: the deadlines and what to fix first](/articles/ada-title-ii-colorado)

### European Union: what has changed since June 2025?

The European Accessibility Act has applied since 28 June 2025 to consumer e-commerce, banking, transport ticketing, telecoms and e-books. Each member state sets its own penalties. They range from a few thousand euros in some countries to €100,000 in Germany and up to €1 million in Spain, and Italy can fine a share of turnover. Enforcement so far has been complaint-led and corrective first: a barrier is reported, an order to fix it follows, and fines come if the fix doesn't. Micro-enterprises that only provide services are exempt. Pure B2B products are out of scope.

In Germany, competitors can also send an *Abmahnung* (a formal warning letter) before any authority acts. → [BFSG in Munich: who it covers, what it costs, and what to fix first](/articles/bfsg-munich)

### UAE: what applies in Dubai?

Accessibility obligations in the UAE sit with government. The Cabinet-adopted National Digital Accessibility Policy and the TDRA's UAE Design System guide federal websites and apps to WCAG 2.1 AA, and Dubai entities work under the Dubai Universal Design Code. Anything built for a government client inherits that bar, and in practice it must be bilingual: Arabic and English, right-to-left and left-to-right.

The deadline that worries product teams in Dubai is about privacy rather than accessibility. The federal PDPL, plus separate regimes in DIFC and ADGM, govern the same consent and onboarding screens. → [PDPL in Dubai: what's law now and what to design in](/articles/pdpl-dubai)

### India: is digital accessibility mandatory now?

For government, yes. GIGW 3.0 has 88 mandatory checkpoints and an STQC audit before a site is certified. For everyone else it's coming. In November 2024 the Supreme Court (*Rajive Raturi v Union of India*) struck down the "recommendatory" status of the old rules. Draft amendment rules published in July 2026 make IS 17802 mandatory for every establishment offering digital products to people in India, phased by turnover over twelve to twenty-four months from the date they are notified. The rules were still a draft at the time of writing. The direction is settled; only the dates aren't. → [Accessibility in Northeast India: the guidelines just became the law](/articles/accessibility-northeast-india)

### If you sell in more than one market, what do you fix first?

1. **Audit once, against WCAG 2.1 AA.** Go screen by screen and write every failure as a fix. Automated scanners catch roughly a third of the criteria; the rest needs a person with a keyboard and a screen reader.
2. **Fix the paths people depend on.** Checkout, sign-up, login, payment, applications, contact. A compliant homepage with an inaccessible form is where complaints come from.
3. **Fix the system, not the page.** Put contrast, focus states, labels, language markup and structure into the design tokens and components. Then every market, and every new feature, passes by default.
4. **Add the local paperwork.** Publish an accessibility statement and a way to report barriers (EU, India). Prepare a conformance report or VPAT for procurement (US, and India's draft rules). Do a bilingual pass (UAE) and declare each language in the markup (India).
5. **Re-check as you ship.** Compliance is a state you maintain, not a one-off event. Re-test quarterly as content and code change.

### Where Parallax fits

Parallax measures every screen it ships against WCAG 2.1 AA, from studios that work in your hours in Denver, Munich, Dubai and the Northeast. We do the same for products that already exist: audits, remediation inside your codebase without a redesign, accessible design systems, and the statements and conformance reports each market asks for. If you have a deadline on this page, [start with the brief](/#contact).

### Questions people ask

**Which accessibility standard applies in the US, EU, UAE and India?**
WCAG 2.1 Level AA, directly or through a national standard: the DOJ rule in the US, EN 301 549 in the EU, IS 17802 in India, and the UAE Design System for federal government.

**When is the ADA Title II deadline?**
26 April 2027 for state and local governments serving 50,000 or more people. 26 April 2028 for smaller ones and special districts. The DOJ pushed both back a year in April 2026 without changing the standard.

**Is the European Accessibility Act being enforced?**
Yes, since 28 June 2025. Enforcement runs through national authorities, mostly on complaints, with corrective orders first and fines for failing to fix. Penalties vary by country.

**Is accessibility mandatory for private companies in India?**
Not yet in final form. Government sites must meet GIGW 3.0 today. The draft RPwD (Amendment) Rules 2026 would require IS 17802 from every establishment, with deadlines of one to two years by turnover from the date the rules are notified.

**Is WCAG 2.2 required anywhere?**
Not yet. Every regime here references WCAG 2.1 AA. Building to 2.2 satisfies 2.1 and anticipates the next revision of EN 301 549.

**Does one audit cover all four markets?**
For the technical standard, yes. Each market then adds its own documents: an accessibility statement, a conformance report or VPAT, bilingual content, or a GIGW certificate. These are written from the same audit evidence.

---

*Sources: [ADA.gov — Title II web rule](https://www.ada.gov/resources/web-rule-first-steps/) · [Mondaq — DOJ extends Title II deadlines by one year](https://www.mondaq.com/unitedstates/media-entertainment-law/1782220/doj-extends-ada-title-ii-digital-accessibility-deadlines-by-one-year) · [Colorado OIT — HB21-1110 FAQ](https://oit.colorado.gov/standards-policies-guides/guide-to-accessible-web-services/faq-hb21-1110-colorado-laws-for-persons) · [Level Access — EAA compliance in 2026](https://www.levelaccess.com/blog/eaa-compliance-in-2026-how-enforcement-has-evolved-and-what-to-expect-next/) · [Clym — EAA fines by country](https://www.clym.io/blog/european-accessibility-act-fines-by-country) · [UAE Design System — Accessibility](https://designsystem.gov.ae/guidelines/accessibility) · [WAM — TDRA and the National Digital Accessibility Policy](https://www.wam.ae/en/article/b30lt44-tdra-supports-implementation-national-digital) · [GIGW 3.0](https://guidelines.india.gov.in/introduction/) · [Mondaq — Draft RPwD (Amendment) Rules 2026](https://www.mondaq.com/india/compliance/1824050/the-new-accessibility-conformance-regime-key-takeaways-from-the-draft-rpwd-amendment-rules-2026) · [W3C — WCAG 2.1](https://www.w3.org/TR/WCAG21/)*

---

## Notes for sign-off

1. **India.** As of today (3 Oct) I can't find the amendment rules notified as final; every source still calls them the July draft. The piece says "draft" throughout. If they're notified, the India row and FAQ flip to real dates. That's exactly the kind of update the "last updated" line is for.
2. **UAE PDPL.** A few compliance-vendor sites now claim the Executive Regulations were issued in 2026, but they cite a decision number that doesn't check out, and the law-firm sources still say pending. I've kept PDPL to one line here and made no claim about its status. Worth asking anyone in Dubai, because it affects the Dubai article too.
3. **EU fines.** Germany's €100,000 is from the BFSG itself. The Spain €1M and Italy turnover figures come from compliance-vendor summaries (Clym, AllAccessible); I've phrased them as ranges, not citations. Cut them if you'd rather.
4. **The table.** The CMS editor has no tables, so it becomes seven dated lines, as with Denver.
5. **CTA** points at `/#contact` (checked: the anchor exists on the home page).
6. **Hero image.** One suggestion: a single interface frame in four languages/scripts (English, German, Arabic, Assamese). Add it in the editor before publishing.
7. **On publish:** run seo.py (it lists tagged articles in llms.txt), deploy, and consider adding a "See all four deadlines" link from each market article back to this one, so the hub and the four pieces link both ways.

---

## LinkedIn post (Samuel, personal profile)

Post natively, with no link in the body. Put the article link in the first
comment. A PDF carousel of the timetable would outperform text alone if
you want to make one.

```
Same rule. Four countries. Four different deadlines.

We work across Denver, Munich, Dubai and Northeast India, and I keep getting asked the same question in four accents: "when do we actually have to be accessible?"

So here's the timetable on one page:

🇪🇺 EU: 28 June 2025. Already enforced. Consumer apps, shops, banking, ticketing.
🇺🇸 Colorado: 1 July 2025. Already enforced. $3,500 per violation, paid to the person it fails.
🇺🇸 US public sector: 26 April 2027 (large) and 26 April 2028 (small). Pushed back a year in April. The standard didn't move.
🇦🇪 UAE: government services, now.
🇮🇳 India: government now (GIGW 3.0). Everyone else 12–24 months after the new rules are notified.

The part nobody tells you: it's the same standard everywhere. WCAG 2.1 AA.

Which means you don't need four compliance projects. You need one audit and one design system where contrast, focus, labels and structure are built into the components, so every screen passes by default.

Then each market adds its own paperwork on top. A statement here, a conformance report there.

The companies I see struggling aren't the ones who started late. They're the ones fixing it page by page.

Full timetable, and what to fix first, in the comments. We'll keep it updated as dates move.

#Accessibility #WCAG #ProductDesign #EAA #ADA
```

**First comment:** `Here's the full breakdown, with sources: https://www.parallaxorg.com/articles/accessibility-deadlines-2026?utm_source=linkedin&utm_medium=social&utm_campaign=accessibility-deadlines`

(The UTM tag only labels the traffic in analytics; the page's canonical tag stays clean, so it costs nothing in SEO.)
