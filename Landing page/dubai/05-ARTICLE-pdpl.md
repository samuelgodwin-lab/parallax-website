# Article draft — /dubai/ · PDPL, the free-zone laws, and designing for both

Signed off 21 Sep 2026 and **loaded into the CMS as a draft** (articles id `2b905302-373d-4b88-acff-2a6e98c970d9`, slug `pdpl-dubai`, category compliance, tags Dubai · UAE · PDPL · Privacy · Accessibility). Add a hero and publish from `/admin/article-editor.html?id=2b905302-373d-4b88-acff-2a6e98c970d9`; live at `/articles/pdpl-dubai`. On publish: band button via `build.py` (Dubai builds from Munich; add after the gov lede), seo.py, deploy. Denver/Munich shape. English. About
1,450 words. Goes into the CMS as a draft (category Compliance, tags
Dubai · UAE · PDPL · Privacy · Accessibility) on "article works".

The honest framing, which is also the useful one: the federal PDPL has
been law since January 2022 but its Executive Regulations — the part that
sets the fines and the breach clock — were still unpublished as of
mid-2026 (Chambers, DLA Piper). Meanwhile the DIFC and ADGM laws are fully
enforced and fined. So the piece says: if you're in a free zone the teeth
are already there; if you're onshore, the regulations start a six-month
clock the day they land, and the flows take longer than that to redesign.

---

**Slug:** `/articles/pdpl-dubai`
**Title (CMS, accent marked):** PDPL in Dubai: what's law *now*, what's waiting on the regulations, and what to design in
**Title tag (57):** UAE PDPL Explained: What Applies Now and What to Design In
**Description (153):** The UAE's PDPL has been law since 2022; its fines wait on Executive Regulations, while DIFC and ADGM already enforce theirs. What to design in before the clock starts.
**Category:** Compliance · **Read time:** 7 min · **Author:** Parallax

---

## PDPL in Dubai: what's law now, what's waiting on the regulations, and what to design in

*Three data-protection regimes share one city. One of them has fined companies for years, one is about to, and every product that onboards a customer in Dubai has to be built for all three.*

**In one paragraph.** The UAE's federal Personal Data Protection Law (Federal Decree-Law 45 of 2021) has applied since 2 January 2022 to any organisation processing the personal data of people in the UAE. Its Executive Regulations — which set the fines, the breach-notification deadline and the detail — had still not been published by mid-2026; when they are, companies get six months to comply. The DIFC and ADGM free zones run their own data-protection laws, modelled on the GDPR, with commissioners who already audit and fine. The practical answer for a product team is the same under all three: consent that is specific and withdrawable, records of what is processed and why, a working path for access and deletion requests, and a breach procedure — designed into the product, not bolted on by a banner.

### Which law applies to my company in Dubai?

It depends on where the entity sits, and many groups sit in more than one place.

- **Onshore UAE and the non-financial free zones** (Dubai Internet City, Dubai Media City, JAFZA, DMCC, the mainland): the federal **PDPL**, supervised by the UAE Data Office.
- **DIFC**: the **DIFC Data Protection Law (DIFC Law No. 5 of 2020)** and its regulations, enforced by the DIFC Commissioner of Data Protection.
- **ADGM**: the **ADGM Data Protection Regulations 2021**, enforced by the ADGM Office of Data Protection.

The federal law also carves out sectors with their own rules — health data under the ICT-in-health law, banking and credit data under the Central Bank's rules, and government data — and applies to companies outside the UAE that process the data of people inside it. A fintech with a DIFC licence, an onshore operating company and customers across the Emirates answers to two regulators for the same customer record.

### What does the PDPL actually require?

The federal law reads like a lighter GDPR, and its obligations are already in force even though the penalty schedule is not:

- **A lawful basis, and by default it is consent** — clear, specific, given by a positive act, recorded, and as easy to withdraw as it was to give. Pre-ticked boxes and bundled consent fail.
- **Transparency** — a privacy notice that says what is collected, why, for how long, with whom it is shared and where it goes.
- **Rights** — access, correction, deletion, restriction, objection to marketing and profiling, and portability, each with a route that works in the product.
- **Data minimisation and retention** — collect what the purpose needs, keep it only as long as the purpose lasts.
- **Security and breach notification** — appropriate technical measures, and notification to the Data Office and, where there is a risk to the person, to the person; the deadline is set by the Executive Regulations.
- **Records of processing**, and a **data-protection impact assessment** for high-risk processing such as profiling, large-scale sensitive data or new technologies.
- **A data protection officer** where processing is high-risk, large-scale or systematic.
- **Cross-border transfers** only to countries with adequate protection or under contractual safeguards — which matters for every product hosted outside the UAE.

The DIFC and ADGM laws ask for the same things with more precision: named lawful bases beyond consent, a 72-hour breach clock, mandatory DPO registration for many firms, annual assessments, and published fine schedules. The DIFC Commissioner has issued fines and directions since 2020; the ADGM regulations carry maxima in the tens of millions of dollars.

### What are the deadlines?

| Regime | Status |
|---|---|
| Federal PDPL | In force since **2 January 2022**. Executive Regulations **not yet published** as of mid-2026 |
| Federal PDPL — once the regulations issue | **Six months** to comply, then the penalty schedule applies |
| DIFC Data Protection Law | In force since **1 July 2020**; enforced and fined |
| ADGM Data Protection Regulations | In force since **14 February 2021**; enforced and fined |

The six-month window is the trap. Redesigning consent, the privacy notice, the rights flows and the breach procedure across a live product takes longer than six months for most companies — which is why the Data Office's guidance over the last two years has been to comply with the law as written rather than wait for the regulations.

### What does non-compliance cost?

Under the federal law, administrative fines are to be set by Cabinet decision alongside the regulations; until then the exposure is regulatory direction, reputational, and contractual — banks, government entities and larger customers now write PDPL compliance into supplier terms. In the free zones the costs are current: the DIFC Commissioner publishes its enforcement actions, and the ADGM regime allows fines large enough to matter to any firm licensed there.

The quieter cost is the one product teams feel first: an onboarding flow that cannot show a regulator where consent was recorded, or a support desk that cannot delete a customer's data within the statutory window, fails the audit that a bank or a government tender now runs before signing.

### What should a product team in Dubai design in?

1. **Map the data before the flows.** What is collected at each step, why, where it is stored, who it is shared with, where it crosses a border. This is the record of processing, and every other decision follows from it.
2. **Design consent as a screen, not a checkbox.** Purpose by purpose, in plain Arabic and English, recorded with a timestamp, and withdrawable from inside the account without a support ticket.
3. **Build the rights into the product.** Download my data, correct it, delete my account, stop marketing — as features with a service-level, not as an email address in the privacy policy.
4. **Minimise by default.** Remove the fields the purpose doesn't need; set retention in the schema, not in a policy document.
5. **Write the breach runbook now.** Who is told, in what order, within what time — and test it before the regulations set the clock at 72 hours, which is where the free zones already are.
6. **Design bilingual, and accessible, at the same time.** In Dubai the privacy notice, the consent screen and the rights flows are two products — Arabic and English, right-to-left and left-to-right — and for anything sold to government they also have to meet WCAG 2.1 AA under the TDRA's digital-accessibility policy and the Dubai Universal Design Code. Doing the three together is one design pass; doing them separately is three.

### Where Parallax fits

Parallax designs consent, records of processing and breach paths into the product before the regulations make them a fine, and builds the whole thing bilingual from the first screen — mirrored, not flipped, Arabic typography set properly, every page measured against WCAG 2.1 AA. Two of the studio are already in Dubai; 09:00 in Dubai is 10:30 in Bengaluru, so the working day overlaps. If your onboarding has to pass the PDPL, a DIFC audit or a government tender, [start with the brief](https://www.parallaxorg.com/dubai/#cta).

### Questions people ask

**Does the PDPL apply if my company is outside the UAE?**
Yes, if you process the personal data of people in the UAE — a booking site in London selling Dubai hotel rooms to UAE residents, an app in Bengaluru with Emirati users. The free-zone laws similarly reach controllers established there regardless of where the processing happens.

**Is the PDPL enforced yet?**
The law is in force and the Data Office issues guidance and directions, but the fine schedule and the detailed procedures sit in Executive Regulations that had not been published by mid-2026. When they are, there is a six-month transition. In DIFC and ADGM, enforcement — including fines — has been running since 2020 and 2021.

**Is the PDPL the same as the GDPR?**
Close enough that a GDPR-compliant product is most of the way there, with differences that matter: consent is the default lawful basis under the PDPL, legitimate interest is narrower, the DPO and impact-assessment triggers differ, and cross-border transfers need a UAE-specific basis. The DIFC and ADGM laws are closer to the GDPR still.

**Do I need a Data Protection Officer in Dubai?**
Under the federal law, if your processing is high-risk, large-scale or involves systematic monitoring or sensitive data. In DIFC, most firms doing high-risk processing must appoint and register one. Either way the role can be outsourced.

**What has to be bilingual?**
Anything a consumer or a government user reads to make a decision: the privacy notice, the consent screens, the rights requests and their confirmations. For government-facing products it is a requirement; for everyone else it is the difference between a consent that stands up and one that a regulator reads as uninformed.

**How long does this take to design in?**
A data map and gap assessment of a typical product takes two to three weeks. Consent, notice and rights flows are then a design-system change plus a build — usually six to ten weeks for the customer-facing surfaces. That is inside the six-month window only if the work starts before the regulations do.

---

*Sources: [UAE Government — Data protection laws](https://u.ae/en/about-the-uae/digital-uae/data/data-protection-laws) · [Chambers — Data Protection & Privacy 2026, UAE](https://practiceguides.chambers.com/practice-guides/data-protection-privacy-2026/uae/trends-and-developments) · [DLA Piper — Data protection laws of the world, UAE](https://www.dlapiperdataprotection.com/countries/uae-general/law.html) · [DIFC — Data Protection Law 2020](https://www.difc.com/business/laws-and-regulations/data-protection) · [ADGM — Data Protection Regulations 2021](https://www.adgm.com/operating-in-adgm/office-of-data-protection) · [TDRA — Digital accessibility policy](https://tdra.gov.ae/en/about/tdra-sectors/information-and-egovernment-sector/digital-accessibility)*

---

## Notes for sign-off

1. **The regulations.** The whole piece turns on the Executive Regulations being unpublished. Two law-firm sources say so as of mid-2026; a handful of commercial compliance sites claim they were issued this year but cite Cabinet decisions that can't be found on official portals. I've written "not yet published as of mid-2026" and, in the FAQ, "when they are". If you know otherwise from anyone in Dubai, tell me and the piece flips to "published — the clock is running".
2. **ADGM fines** are described as "tens of millions of dollars" rather than a number; the published maximum is USD 28 million but I'd rather not anchor on it without the regulation in front of me.
3. **Sector carve-outs** (health, banking, government) are stated at the level the law states them; a DIFC bank reading this will know its own rules.
4. **"Two of the studio are already in Dubai"** matches the Dubai page's claim; adjust if that has changed.
5. **Hero image** in the editor before publishing.
