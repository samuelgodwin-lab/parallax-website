# Copy v2 — Parallax Northeast India

Repositioned from market analysis to offer. Supersedes `02-COPY.md`, which is left
untouched as the record of v1.

**Provenance is marked on every slot:**
`[KEPT]` verbatim from v1 · `[EDITED]` v1 line, reworked · `[NEW]` written for v2, needs your approval

Voice reference: Brand Guidelines §07. Asterisks mark the accent word → `<em>`.

---

## What changed structurally

| v1 | v2 |
|---|---|
| 04 — The gap (market analysis) | **Cut** |
| 05 — Statistics band (dark, full-bleed) | **Retired.** Numbers moved into the hero foot, as on live |
| 08 — Services (seventh in reading order) | **Moved to 05** — the offer now lands right after proof |
| 06 — Sectors diagnose what's broken | Sectors state **what we build** |
| 09 — Referral scheme | **Design hub** — culture, network, projects |
| — | **New 04 — client strip**, slim and light, mirroring the live logos-strip |

Nine sections becomes eight. Reading order is now
hero → clients → services → sectors → government → hub → CTA.

---

## 02 — Hero

**Slabel:** `NORTHEAST INDIA` — [KEPT]

**H1:** [EDITED — v3]
We build the brands and apps Northeast India *runs* on.

> v1 was `Most software here was never designed. It was just built.` — a diagnosis of the
> reader's market. v2 stated the offer instead. v3 names both artefacts — brands and apps —
> in nine words against v2's ten, one clause instead of two. "Brands" first, matching the
> service order.

**Lede:** [EDITED — v3]
Brand systems, interface design and frontend engineering — one studio, from identity to
shipped code. For property platforms, booking engines, distributor portals and student
records.

> Names the three lead services in service order, then states the differentiator: one studio
> covering identity through shipped code. `Precision over decoration. Logic over assumption.`
> is cut from the hero — good voice, but studio-inward at the point of conversion. The sector
> list is v1 verbatim.

**Buttons:** [EDITED — v3]
`Start a project` (primary → #cta) · `See the work` (ghost → parallaxorg.com/work.html)

> Both hero buttons are now client-facing. The designer route was a conversion leak in the
> hero — the secondary action sent a prospective client into a recruitment section.

**Note line:** [NEW — v3]
One call, a lot of questions, no deck. · *Designer in the region?* (→ #designers)

> Friction-reducer borrowed from the section 09 lede, and it carries the designer route so
> nothing is lost by reclaiming the second button.

**Hero stats** — [MOVED from the retired statistics band, values [KEPT]]
`100+` Projects shipped · `3M+` Users reached · `15+` Years in practice · `4` Studios worldwide

> Sits in the hero foot at the live site's own scale, with the `+` in accent — live `.hero__sn`
> / `.hero__sn-plus` / `.hero__sl`. Credibility now lands in the first screen instead of the fifth section.

---

## Meta band — [REMOVED — v3]  *(was 03)*

The four-cell band under the hero is cut. `Region` and `Practice` were already said, better,
in the hero slabel and lede; `Sectors` is the whole of section 05; `Studio` was the only cell
carrying anything new, and it now lives in the footer.

> The `.meta-band` component itself stays in `components.html` and in `styles.css` — it is a
> library component, not a landing-page-only one.

---

## 03 — Services marquee — [NEW — v3]

Lifted verbatim from parallaxorg.com, where it occupies the identical slot: an accent band
straight after the hero. Six items, printed twice in the track, translating -50% over 28s.

`Brand Systems · Interface Design · Frontend Engineering · Design Systems ·
Digital Strategy · Motion & Interaction`

> Treatment is the live one verbatim; the **names are this page's**, in section 04's order.
> The live marquee reads Brand Identity · Interface Design · Motion Engineering · Frontend
> Architecture · Design Systems · Creative Direction — four of those conflict with the
> service rows two sections below, so the marquee was aligned to the page rather than the
> other way round. **If parallaxorg.com is ever renamed to match, this is the line to
> revisit.**

---

## 04 — Services  *(moved up from 08 — this is the offer)*

**Slabel:** `WHAT WE BUILD` — [EDITED, was `WHAT WE DO`]

**H2:** Six disciplines. One *standard.* — [KEPT] *(also the live site's exact heading)*

**Lede:** [EDITED — v3]
Brand systems, UX, UI and the frontend engineering that ships them. We take a product from
identity to shipped code, and hand back something your team can run without us.

> Added because the section previously opened straight into the list. This is the line that
> says explicitly what we build. v3 opens on brand systems and runs the arc from identity —
> not research — to shipped code.

**The six rows — bodies all [KEPT] verbatim from v1; order [EDITED — v3]:**

| # | Title | Body |
|---|---|---|
| 01 | Brand Systems | Identity, voice and design language built as a complete system. Not how you look, but how you hold together across every surface. |
| 02 | Interface Design | Screens that think. Every state, every edge case, every micro-interaction resolved before a line of code is written. |
| 03 | Frontend Engineering | We write production code. React, Next.js, TypeScript — built for performance, built for teams, built to last past the handoff. |
| 04 | Design Systems | Components, tokens and governance your team runs without calling us. The system is the deliverable, not the screens. |
| 05 | Digital Strategy | We map the distance between where your product is and where it needs to be — research, positioning, architecture — then build the roadmap to close it. |
| 06 | Motion & Interaction | The gap between software that works and software people trust is how it moves. Choreographed with precision timing and physics-based motion. |

Rows 1–3 keep the accent treatment. The order now runs the sequence a client buys in —
identity, then screens, then shipped code — with the supporting disciplines behind it.

---

## 05 — Client logos — [REPLACED — v3]  *(was 03, text-only)*

The live `.logos-strip` copied verbatim — accent ground, five inline SVG marks at 72%
opacity, hairline separators — and moved to sit after the services section.

**Label:** `SELECTED CLIENTS` — [EDITED from the live `MUCH MORE`]

> On parallaxorg.com this strip follows testimonials, where "Much More" reads as *more
> clients*. Here it follows the services section, where it would read as *more services*.

**Marks:** Biblica · BMW · **Accenture** · Nissan · Sportradar

> The live source comments the third mark `<!-- Vestas -->`, but the SVG it wraps is the
> **Accenture** wordmark. v2 of this doc dropped Accenture on the belief it "appears nowhere
> on parallaxorg.com" — that was wrong; it was reading the mislabelled comment. Vestas is not
> among the logo marks at all, only in the mobile name list below. **Confirmed kept**: the
> mark is already public on the live site, so it carries no clearance the live site doesn't.

**Mobile (<768px):** the marks are replaced by the live name-marquee —
Strato · Suka · Sopra · Vestas · YVT · Re'flekt · BMW · BuildDeli · Sinnerschrader · Sportradar

> Ten names, seven of which appear nowhere else on this page.

---

## 06 — Sectors

**Slabel:** `WHERE WE WORK` — [EDITED, was `WHERE THE WORK IS`]

**H2:** [NEW]
The software we build, by *sector.*

> v1 was `Four sectors already running software they never designed.` — diagnosis again.

Every tile now ends in a **We build** block naming the concrete software, replacing the
market-sizing figures. Headlines are outcome-led rather than problem-led.

### S—01 · Real estate — [KEPT slabel]

**H3:** [NEW] Inventory that sells *online.*
**Body:** [EDITED — v4] High-value inventory still moves through PDF brochures, shared spreadsheets and message threads. We build the portal that replaces all three — browsable stock, live availability, partner-level pricing, and a payment flow that closes without a single phone call.

> Six words longer than v3, to bring this tile's body to three lines so it ends level
> with S—02 beside it. `partner-level pricing` earns its place — it is the feature behind
> the `Channel partner portals` tag already in this tile.
**We build:** `Inventory dashboards` · `Channel partner portals` · `Booking & payment flows` — [KEPT]

### S—02 · Hospitality — [KEPT slabel]

**H3:** [NEW] Direct bookings that keep your *margin.*
**Body:** [EDITED] Aggregators take a fifth of every booking because the property's own flow is unusable. We build a direct engine that guests finish — and a management interface your front desk can actually run.
**We build:** `Direct booking engines` · `Property management UI` · `Guest apps` — [EDITED]

### S—03 · Pharma — [KEPT slabel]

**H3:** [NEW] Compliance systems people can *use.*
**Body:** [EDITED — v4] Sikkim runs one of the country's densest manufacturing clusters on batch records and distributor systems built for an audit rather than a person. We build what the floor and field actually use.

> Cut from four lines to three so this tile ends level with S—04. The tag row was the
> other half of that mismatch — three tags overflowed the narrower span-5 tile by ~2px
> and wrapped; `.tag` padding was tightened to `--s2` / `0.10em` to fit them on one row.
**We build:** `Compliance dashboards` · `Distributor portals` · `Field-force apps` — [KEPT]

### S—04 · Education — [KEPT slabel]

**H3:** [NEW] Admissions students don't *fight.*
**Body:** [EDITED] Admissions, records and learning systems carry the highest volume and the highest friction of any software in the region. We build the portals and dashboards that carry ten thousand students without a helpdesk queue.
**We build:** `Admissions portals` · `Student dashboards` · `Learning platforms` — [KEPT]

---

## 07 — Government

Unchanged — already offer-led and tight. — [KEPT]

**Slabel:** `PUBLIC SECTOR`
**H2:** Citizens don't get to choose another *portal.*
**Lede:** Which is precisely why public software should be held to a higher standard than
private, not a lower one. We work with state departments, boards and missions on the systems
citizens are required to use, and we hand back a design system the next vendor can build on.
**Capability tiles:** `Citizen service portals` · `Tourism & permit systems` · `Scheme & benefit tracking` · `Internal dashboards` · `Accessibility audits` · `Design system handover`

---

## 08 — Design hub

Rebuilt to your brief: the hub is the long-term position, the project pipeline is how it
scales now, and joining the team is a real route. The transactional
"you bring the lead / we convert it" framing is gone.

**Slabel:** `FOR DESIGNERS IN THE REGION` — [KEPT]

**H2:** [NEW]
We're building a design hub in the *Northeast.*

> v1 was `We remove pitching, pricing and paperwork. You get to design.` — that described a
> service arrangement. This states the ambition.

**Lede:** [EDITED]
Talent is not the constraint in the Northeast. Access is. We're building the network, the
standard and the body of work that keeps designers here — on real products, paid properly,
credited publicly. Three ways in.

> First two sentences are v1 verbatim.

**Three routes — all [NEW], replacing v1's STEP 01/02/03:**

| Route | Title | Body |
|---|---|---|
| 01 | Join a project | Staffed on live client work at an agreed rate, alongside our team. Reviewed, credited, paid on delivery. |
| 02 | Bring work in | Introduce a business that needs design. We take scoping, proposal, pricing, contract and collection. If it closes, you are on the project team. |
| 03 | Build the standard | Portfolio reviews, mentorship and published work — so the bar is set here rather than imported from Bangalore. |

**Terms row:** `No exclusivity` · `No joining fee` · `Paid for work, not for leads` · `Publicly credited` — [KEPT]

**Button:** `Join the network` — [KEPT]

---

## 09 — CTA

Unchanged — already offer-led. — [KEPT]

**Slabel:** `NEXT`
**H2:** Tell us what you're *building.*
**Lede:** We start by questioning the brief. One call, a lot of questions, no deck. If we're
not the right studio for it, we'll say so and point you at someone who is.
**Buttons:** `projects@parallaxorg.com` (primary, mailto) · `See the work` (ghost → work.html)

---

## 10 — Footer — [EDITED — v3]

Left: wordmark · `© 2026 Parallax Studio` — [KEPT]

Right, now two labelled rows:

| Key | Value | |
|---|---|---|
| Studios | Bengaluru · Munich · Dubai · Denver | [MOVED from the retired meta band] |
| Region | Assam · Meghalaya · Nagaland · Manipur · Mizoram · Tripura · Arunachal · Sikkim | [KEPT, now labelled] |

> The region list was previously unlabelled. With a second place-list beside it the label
> became necessary — otherwise the two read as one run-on list of locations.

---

## Resolved

- **Client list** — settled against what is already published on parallaxorg.com.
  Five names, Accenture dropped. See section 04.
- **Pricing** — not used on this page. Closed; the page links to no pricing tier.
- **Statistics placement** — numbers moved into the hero foot, matching live.

- **Local presence** — closed. No regional address, and none is claimed: the hub heading
  reads "We're *building* a design hub in the Northeast", which states intent, and the only
  location claim on the page is the meta band's Bengaluru · Munich · Dubai · Denver.
  No copy change required.

## Still open

Nothing.
