# Article draft — /munich/ · BFSG (Barrierefreiheitsstärkungsgesetz)

Signed off 21 Sep 2026 and **loaded into the CMS as a draft** (articles id `ccbb0ba4-9035-45af-b073-1ee673a5e53c`, slug `bfsg-munich`, category compliance, tags Munich · Germany · BFSG · Accessibility). Review, add a hero and publish from `/admin/article-editor.html?id=ccbb0ba4-9035-45af-b073-1ee673a5e53c`; it goes live at `/articles/bfsg-munich`. On publish: re-run `Landing page/seo.py`, deploy, and add the band button on /munich/ (hand-edit — Munich has no live build script). Same shape as the Denver Title II piece:
opens with the answer, question-shaped headings, exact dates and numbers,
a "what to fix first" list, six FAQs. English, for the English `/munich/`
page; a German version can follow with `/de/munich/`. About 1,450 words.
Goes into the CMS as a draft (category Compliance, tags Munich · Germany ·
BFSG · Accessibility) when you say "article works".

---

**Slug:** `/articles/bfsg-munich`
**Title (CMS, accent marked):** BFSG in Munich: who it *covers*, what it costs, and what to fix first
**Title tag (58):** BFSG Explained: Who It Covers, Fines, and What to Fix First
**Description (152):** Germany's Barrierefreiheitsstärkungsgesetz has applied since 28 June 2025: WCAG 2.1 AA for consumer sites, apps and shops, fines to €100,000. What to fix first.
**Category:** Compliance · **Read time:** 7 min · **Author:** Parallax

---

## BFSG in Munich: who it covers, what it costs, and what to fix first

*The grace period is over. Since January the market-surveillance office has been working through complaints, the first Abmahnungen have arrived, and the standard is the same one everyone else uses.*

**In one paragraph.** The Barrierefreiheitsstärkungsgesetz (BFSG) has required consumer-facing websites, apps, online shops, banking services, ticketing and e-books in Germany to be accessible since 28 June 2025. The technical bar is EN 301 549, which for web and mobile means WCAG 2.1 Level AA. Micro-enterprises providing services — fewer than ten staff *and* at most €2 million turnover — are exempt; everyone else selling to consumers is not. Fines run to €100,000, the market-surveillance office can order a service withdrawn, and competitors can send an Abmahnung before any authority looks.

### Who does the BFSG apply to?

The BFSG is Germany's implementation of the European Accessibility Act. It applies to products and services offered to consumers, and the list is concrete:

- **E-commerce** — any website or app through which a consumer can conclude a contract: shops, bookings, subscriptions, sign-ups with payment.
- **Consumer banking** — online banking, payment and account services, identification flows.
- **Passenger transport** — websites, apps, ticketing and real-time information for air, bus, rail and waterborne services (urban and regional transport are partly exempt).
- **Telecommunications** and the customer portals around them.
- **E-books** and the software that reads them.
- **Hardware with a consumer interface** — computers, phones, self-service terminals, ticket and payment machines.

For Munich that reads as a map of the local economy. A mobility start-up's app, a carmaker's subscription and charging services, an insurer selling policies online, a proptech letting tenants sign digitally, a hotel taking direct bookings — each is a consumer contract concluded through an interface, and each is in scope.

Two things are *not* covered. Pure B2B products, where no consumer is a party, fall outside the law. And micro-enterprises that only provide services (under ten employees and no more than €2 million in annual turnover or balance-sheet total — both conditions at once) are exempt; a micro-enterprise that *makes* a product is not.

Public bodies are a different regime: Bavarian authorities have been bound by BayBITV since 2019, and federal ones by BITV 2.0. The BFSG is about the private sector.

### What does "accessible" mean under the BFSG?

The law delegates the technical standard to a regulation (BFSGV), which points at EN 301 549 — the European standard that, for websites and mobile apps, incorporates WCAG 2.1 Level AA. In practice that is the same list a Colorado city or a Dubai ministry is measured against, and the same short list of failures accounts for most of the risk:

- **Contrast** of 4.5:1 for text and 3:1 for large text and interface components. Light grey on white fails; so do most brand colours at small sizes.
- **Keyboard** — everything reachable and operable without a mouse, in a sensible order, with a visible focus indicator.
- **Names and labels** — every field labelled, every button and link saying what it does, every image described or marked decorative.
- **Structure** — headings in order, landmarks, one `h1`, tables with headers; the skeleton a screen reader navigates.
- **Forms and errors** — errors announced and explained in text, with a way to correct them; time limits extendable.
- **Motion** — nothing that flashes; autoplay that can be paused.
- **Documents** — PDFs tagged and readable, or the content provided as HTML.
- **Mobile** — content that reflows to 320px, touch targets large enough, orientation not locked.

The BFSG adds obligations the WCAG list does not: a published **accessibility statement** (Erklärung zur Barrierefreiheit) describing how the service meets the requirements, kept current, in the terms or on the site; an accessible way for users to report barriers; and, if a company claims the requirements would be a disproportionate burden, a documented assessment it can show the authority.

### What are the deadlines?

| Obligation | Date |
|---|---|
| BFSG in force — new products and services must comply | **28 June 2025** — already passed |
| Market surveillance (MLBF, Magdeburg) actively handling complaints and sampling | **since January 2026** |
| Service contracts concluded before 28 June 2025 may run unchanged | until **27 June 2030** |
| Self-service terminals placed in service before the date | up to 15 years, latest **2040** |

The transition rules are narrower than they sound. A subscription a customer signed in 2024 may continue on the old interface until 2030, but the shop that sells the *next* subscription has had to comply since June 2025, and a relaunch resets the clock.

### What does non-compliance cost?

Three exposures, in the order they usually arrive.

1. **An Abmahnung.** Because the BFSG's requirements are market-conduct rules, a competitor or a recognised consumer or disability association can send a formal warning under competition law, with a cease-and-desist declaration and its legal costs attached. Lawyers argue about how many of these will hold up; none of them argue that they have stopped arriving.
2. **The market-surveillance office.** The Marktüberwachungsstelle der Länder für die Barrierefreiheit (MLBF) in Magdeburg has been operating since January 2026, mainly on complaints, with risk-based sampling of high-reach sites. It can demand documentation, order corrections, and ultimately require a service to be withdrawn.
3. **Fines.** Up to €100,000 for the serious breaches, €10,000 for the procedural ones — a missing statement, a missing feedback route.

The quieter cost is commercial. Procurement teams at banks, insurers and transport operators now ask their vendors for an accessibility conformance report, and a consumer product that cannot produce one is a harder sale in 2026 than it was in 2024.

### What should a Munich company do first?

1. **Establish whether you're in scope.** Consumers, a contract, an interface — if all three, you are. Check the micro-enterprise thresholds honestly; both conditions must hold.
2. **Measure before you plan.** An audit against WCAG 2.1 AA, screen by screen, with every failure written as a fix. Automated scanners catch roughly a third of the criteria; the rest needs a person with a keyboard and a screen reader.
3. **Fix the paths a consumer depends on.** Checkout, registration, login, payment, the contact form. A compliant homepage with an inaccessible checkout is where the complaint comes from.
4. **Fix the system, not the page.** Contrast, focus, labels and structure belong in the design tokens and the component library, so the next feature passes by default.
5. **Publish the statement and the feedback route.** The Erklärung zur Barrierefreiheit is the first thing an authority or a warning letter asks for, and the easiest thing to have.
6. **Re-check as you ship.** Compliance is a state, not an event. Quarterly re-tests as content and code change.

### Where Parallax fits

Parallax measures every page it ships against WCAG 2.1 AA and does the same for products that already exist: audits, remediation inside your codebase without a redesign, accessible design systems, the Erklärung zur Barrierefreiheit and the test evidence behind it. The Munich practice runs in your working hours — 09:00 in Munich is 12:30 in Bengaluru — with the studio continuing after you log off. If you sell to consumers in Germany, [start with the brief](https://www.parallaxorg.com/munich/#cta).

### Questions people ask

**Does the BFSG apply to a B2B SaaS company?**
Not if no consumer is ever a party to the contract. The moment the product is sold to private individuals — a freelancer plan bought by a person, a consumer tier, an app in the public app stores that people pay for — the consumer parts are in scope.

**My start-up has eight people. Are we exempt?**
Only if you provide services rather than products, *and* your annual turnover or balance-sheet total is at most €2 million. Cross either threshold and the exemption ends with the next financial year. Investors and enterprise customers increasingly ask anyway.

**Is WCAG 2.2 required?**
No. EN 301 549 currently references WCAG 2.1 Level AA. Meeting 2.2 AA satisfies it and adds a handful of criteria — focus visibility, target size, dragging alternatives — that are worth doing; the standard is expected to move to 2.2 in its next revision.

**What has to be in the accessibility statement?**
Which requirements the service meets and how, the parts that don't yet comply and why, a contact route for barriers, and the date it was last reviewed. It lives in the terms and conditions or on the site, and it has to stay current after every significant change.

**Can a competitor really send an Abmahnung for accessibility?**
Yes. Competition law lets competitors and recognised associations act on breaches of market-conduct rules, and the BFSG's requirements are widely treated as such. Some of the first letters have been contested as opportunistic; being compliant is cheaper than finding out which kind you received.

**How long does remediation take?**
An audit of a typical consumer product takes two to three weeks. Remediation depends on what it finds: contrast, labels and focus are usually fixed inside a design system in weeks; legacy checkout flows and document backlogs take longer. Starting now leaves time before the market-surveillance office's next sample; the statement can be published the same week.

---

*Sources: [BFSG — Gesetzestext](https://bfsg-gesetz.de/) · [IHK München — Barrierefreiheitsstärkungsgesetz](https://www.ihk-muenchen.de/ratgeber/recht/werbung-fairer-wettbewerb/barrierefreiheitsstaerkungsgesetz/) · [activeMind.legal — BFSG guide](https://www.activemind.legal/de/guides/bfsg/) · [accessgo — Strafen und Sanktionen](https://www.accessgo.de/wissen/barrierefreiheitsstaerkungsgesetz-strafen-folgen-bei-verstoessen/) · [EN 301 549 / WCAG 2.1](https://www.w3.org/TR/WCAG21/)*

---

## Notes for sign-off

1. **Insurance.** The EAA lists consumer *banking* services, not insurance. Insurers are caught through e-commerce (selling and servicing policies online), which is how the piece frames it — say if you'd rather name Allianz-style insurers more directly; I kept it generic.
2. **Hedged figures.** "Roughly a third" of WCAG criteria catchable by scanners (Deque, ~30% of criteria); the "€10,000 for procedural breaches" tier is from the fine schedule in §37 BFSG as summarised by the IHK and legal guides. Cut either if you'd rather.
3. **German version.** This is the English piece for `/munich/`. If the German page goes ahead, the German article should be written fresh, not translated — the search phrases (*Barrierefreiheitserklärung Pflicht*, *BFSG Abmahnung*, *barrierefreie Website Agentur München*) are different queries.
4. **Hero image.** You'll want one in the editor before publishing, as with Denver.
