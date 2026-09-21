# Article draft — /denver/ · ADA Title II & Colorado HB21-1110

Draft for sign-off, 21 Sep 2026. **Loaded into the CMS as a draft the same day** (articles id `8ebff43a-2542-4994-9a54-6d614dab1c58`, slug `ada-title-ii-colorado`, category compliance, tags Denver · Colorado · Accessibility · ADA Title II). Review and publish from `/admin/article-editor.html?id=8ebff43a-2542-4994-9a54-6d614dab1c58`; it goes live at `/articles/ada-title-ii-colorado`. Written to be the answer an AI or a search
engine quotes when a Colorado city clerk, a school district IT lead or a
SaaS founder selling to them asks "when is the Title II deadline" — so it
opens with the answer, uses question-shaped headings, gives exact dates in a
table, and ends with an FAQ that becomes `FAQPage` schema. About 1,400 words.

**Container:** the journal CMS, now server-rendered at `/articles/<slug>` (commit `b82ae29`), so crawlers get the full article.

---

**Slug:** `/denver/ada-title-ii-colorado/`
**Title tag (59):** ADA Title II in Colorado: Deadlines, Standard, First Fixes
**Description (154):** The DOJ's Title II web rule lands 26 April 2027 for most Colorado entities; HB21-1110 already applies. What WCAG 2.1 AA means and what to fix first.
**Category:** Accessibility · **Read time:** 7 min · **Author:** Parallax

---

## ADA Title II in Colorado: the deadlines, the standard, and what to fix first

*Colorado got there before Washington. The state's own accessibility law has applied since July 2025, the federal web rule lands in April 2027, and both measure the same thing.*

**In one paragraph.** Every state and local government website, app and digital document in Colorado has to meet WCAG 2.1 Level AA. Colorado's HB21-1110 has required this since 1 July 2025, with a $3,500 statutory fine per violation payable to the person it fails. The federal ADA Title II web rule adds a second, national deadline: 26 April 2027 for entities serving 50,000 people or more, 26 April 2028 for smaller ones and special districts. Anyone who sells software to those entities inherits the requirement.

### Who does this apply to?

Title II of the Americans with Disabilities Act covers state and local government: cities, counties, school districts, public universities, transit agencies, courts, libraries and special districts. In April 2024 the Department of Justice published a rule that, for the first time, set a technical standard for their web content and mobile apps. Until then "accessible" was argued case by case; now it has a definition.

Colorado's HB21-1110 covers the same public bodies at state level and reaches further into what counts: not only websites but the "digital products" a government offers — apps, kiosks, online forms, PDFs and the software it buys from vendors. The Governor's Office of Information Technology (OIT) sets the standard, and it chose the same one: WCAG 2.1 AA.

The private-sector consequence is the one most people miss. A vendor's product becomes the government's digital product the moment it is offered to the public. If your onboarding flow, payments portal or scheduling tool is used by a Colorado city, its accessibility is now a term of the contract, and increasingly a question in the RFP.

### When are the deadlines?

| Law | Who | Deadline | Standard |
|---|---|---|---|
| Colorado HB21-1110 (with HB24-1454) | State agencies, local governments, school districts | **1 July 2025** — already passed | WCAG 2.1 AA (OIT rules) |
| ADA Title II web rule | Public entities serving **50,000+** | **26 April 2027** | WCAG 2.1 AA |
| ADA Title II web rule | Public entities under 50,000, and all special districts | **26 April 2028** | WCAG 2.1 AA |

The federal dates moved once. The 2024 rule set April 2026 and April 2027; on 20 April 2026 the DOJ issued an interim final rule pushing each by a year, citing the cost of remediation and the limits of automated tools. The technical standard did not change, and neither did the litigation risk in the meantime: Title II has always required effective communication, and the rule only defines what that means online.

Colorado did not wait. HB21-1110 originally required compliance by July 2024; HB24-1454 gave entities that could show "good-faith efforts" — a published progress report, updated quarterly, and a visible way for the public to report barriers — until 1 July 2025. That grace period has ended. A Colorado entity is either compliant or exposed, and the exposure is a private right of action.

### What does non-compliance cost?

Under HB21-1110, a person who cannot use a government digital product can bring a claim under the Colorado Anti-Discrimination Act. The remedies are a court order to fix it, actual damages, and **a statutory fine of $3,500 per violation, paid to the person affected** — per instance, not per lawsuit. A form that fails for a screen-reader user, a PDF without tags, a video without captions: each is a violation.

Under Title II, the DOJ can investigate and enforce, and individuals can sue. The larger, quieter cost is procurement: state and local entities are now writing WCAG 2.1 AA into contracts, asking for a VPAT or an Accessibility Conformance Report, and dropping vendors who cannot produce one.

### What does WCAG 2.1 Level AA actually require?

WCAG is a list of 50 testable criteria at Level A and AA. In practice, the failures that account for most of the risk are a short list:

- **Contrast.** Text needs 4.5:1 against its background (3:1 for large text). Light grey on white, and most brand accents at small sizes, fail.
- **Keyboard.** Everything a mouse can do, a keyboard can do, in a sensible order, with a visible focus ring.
- **Names and labels.** Every form field has a label; every button and link says what it does; every image has alt text that says what it shows, or is marked decorative.
- **Structure.** Headings in order, landmarks (header, nav, main, footer), one `h1`, tables with headers. This is what a screen reader navigates by.
- **Motion and time.** Nothing flashes, autoplay can be paused, and time limits can be extended.
- **Errors.** Form errors are announced, described in text, and tell the user how to fix them.
- **Documents.** PDFs are tagged, have a reading order and real text, or the content is provided as HTML instead.
- **Mobile.** Content reflows to 320px without horizontal scrolling; touch targets are large enough; orientation is not locked.

The Title II rule carves out narrow exceptions — archived content, pre-existing documents not in current use, third-party content you don't control, individualised password-protected documents, and social-media posts from before the deadline. None of them cover the forms, portals and apps people actually use.

### What should a Colorado entity, or its vendor, do first?

1. **Measure before you plan.** An audit against WCAG 2.1 AA, page by page, with every failure written as a fix rather than a finding. Automated scanners catch roughly a third of the criteria; the rest needs a person with a keyboard and a screen reader.
2. **Fix the paths people depend on.** Payment, permits, enrolment, benefits, contact. A compliant homepage with a broken application form is a violation where it matters most.
3. **Fix the system, not the page.** Contrast, focus, labels and structure belong in the design tokens and components. Once the component library passes, the next feature passes without anyone checking.
4. **Deal with documents.** Tag the PDFs that are still in use; replace the ones that can be HTML; archive the rest properly so the exception applies.
5. **Publish the evidence.** An accessibility statement, a way to report barriers, and — for vendors — an ACR/VPAT that a procurement office can file. Under HB21-1110 the statement and the reporting route are part of what "good faith" meant, and they remain the first thing a plaintiff's lawyer looks for.
6. **Re-check as you ship.** Compliance is a state, not an event. Quarterly re-tests as content and code change.

### Where Parallax fits

Parallax measures every page it ships against WCAG 2.1 AA and does the same for products that already exist: audits, remediation inside your codebase without a redesign, accessible design systems, and the conformance documentation a procurement office asks for. The Denver practice is built for Colorado's timetable — briefed in your afternoon, worked overnight, waiting the next morning. If you sell to the public sector in Colorado, or are the public sector, [start with the brief](https://www.parallaxorg.com/denver/#cta).

### Questions people ask

**Does ADA Title II apply to private companies?**
Not directly. Title II covers state and local government. But a private vendor's product becomes the government's digital product when it is offered to the public through a government service, so the requirement flows down through contracts. Private businesses open to the public are covered separately by Title III, where web-accessibility lawsuits run to several thousand a year in federal courts.

**What is the Title II deadline for Colorado cities?**
26 April 2027 for cities, counties and districts serving 50,000 or more people; 26 April 2028 for those under 50,000 and for all special districts. Colorado's own law, HB21-1110, already applies to all of them since 1 July 2025.

**Is WCAG 2.2 required?**
No. Both the DOJ rule and Colorado OIT specify WCAG 2.1 Level AA. Meeting 2.2 AA satisfies 2.1 AA and adds a handful of criteria, mostly about focus visibility and touch targets, that are worth doing anyway.

**Do PDFs and documents count?**
Yes, if they are in current use. Tagged PDFs with a reading order and real text pass; scanned images and untagged exports do not. Documents that were posted before the deadline and are not used for current services fall under the archived-content exception.

**Is an accessibility overlay enough?**
No. Overlays and widgets change the presentation in the browser but do not fix the underlying code, and neither the DOJ rule nor OIT accepts them as conformance. Several Title III lawsuits have been filed against sites that use them.

**How long does remediation take?**
An audit of a typical government or SaaS product takes two to three weeks. Remediation depends on what it finds: contrast, labels and focus can usually be fixed inside a design system in weeks; document backlogs and legacy forms take longer. Starting in 2026 leaves room before April 2027; starting in 2027 does not.

---

*Sources: [ADA.gov — Title II web rule](https://www.ada.gov/resources/web-rule-first-steps/) · [DOJ extension, April 2026 (UPCEA)](https://upcea.edu/doj-extends-accessibility-deadline-to-april-2027-policy-matters-april-2026/) · [Colorado OIT — HB21-1110 FAQ](https://oit.colorado.gov/standards-policies-guides/guide-to-accessible-web-services/faq-hb21-1110-colorado-laws-for-persons) · [Level Access — HB21-1110](https://www.levelaccess.com/blog/hb-21-1110-colorado-accessibility-law/) · [W3C — WCAG 2.1](https://www.w3.org/TR/WCAG21/)*

---

## Notes
- The deadline table became three dated lines in the CMS body (the editor has no tables).
- Two hedged figures: automated scanners catching "roughly a third" of WCAG criteria (Deque: ~57% of issues, ~30% of criteria) and "several thousand a year" Title III web suits (UsableNet, ~4,000 in 2024). Cut them in the editor if unwanted.
- No hero image set — pick one in the editor before publishing.
- On publish: re-run `Landing page/seo.py` and deploy so llms.txt lists it under Denver; the Denver band then gets its "Read the Colorado timetable" link.
