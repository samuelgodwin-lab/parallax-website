# Parallax Brand System v3.0

One system for the Parallax identity, the marketing site (parallaxorg.com) and the
products we ship (Project Tracker). Shared foundations first, then how they apply on
web and in product. September 2026. Confidential.

---

## 1. Identity

Premium brand and digital design agency. We build brand systems and digital
environments for enterprises, founders and market leaders.

- **Position:** the agency you hire when "good enough" design is costing you customers,
  credibility or clarity. We don't redesign — we rearchitect.
- **Principle:** precision over decoration, logic over assumption. Design is architecture,
  not decoration.
- **Clients:** BMW, Biblica, Sportradar, Vestas, Nissan, Accenture.

**Wordmark:** "Parallax" in Bricolage Grotesque 800, `letter-spacing: -0.045em`.
The full stop is part of the mark and is always set in the accent. Never remove it,
recolour it, distort the mark, or place it on busy backgrounds.

---

## 2. Colour

Light-first. White grounds, black text, one blue accent. All values in OKLCH.

### Foundation

| Token | Value | Notes |
|---|---|---|
| `--bg` | `oklch(1 0 0)` | #ffffff |
| `--surface` | `oklch(0.98 0.001 0)` | |
| `--surface-raised` | `oklch(0.96 0.001 0)` | |
| `--text` | `oklch(0 0 0)` | 21:1 |
| `--text-2` | `oklch(0.40 0.005 0)` | 9.20:1 |
| `--text-3` | `oklch(0.51 0.005 0)` | 5.75:1 — holds on every surface |
| `--border` | `oklch(0 0 0 / 0.15)` | |
| `--border-strong` | `oklch(0 0 0 / 0.30)` | |
| `--success` | `#15803d` | |
| `--danger` | `#dc2626` | |

### Accent — Parallax Blue, one value

| Token | Value | Contrast |
|---|---|---|
| `--accent` | `oklch(0.53 0.18 249)` → `#006dcd` | 5.16:1 white · 4.87:1 surface · 4.58:1 raised |
| `--accent-hover` | `oklch(0.47 0.18 249)` | 6.64:1 — hover/press |
| `--accent-display` | `oklch(0.60 0.18 249)` → `#0083e5` | 3.90:1 — **24px+ only**, never small text |
| `--accent-on-dark` | `oklch(0.70 0.14 249)` → `#50a4f1` | 7.67:1 on near-black |
| `--accent-muted` | `oklch(0.60 0.18 249 / 0.14)` | tint backgrounds |
| `--accent-soft` | `oklch(0.60 0.18 249 / 0.06)` | subtle fills |

**Accent lightness moves with the ground.** Lighter on dark, darker on light. `--accent`
is 0.53 and not 0.55 because 0.55 passes on pure white but drops to 4.4993:1 on
`--surface`, which is where most section labels actually sit. On near-black, 0.53 manages
only ~4.26:1 while `--accent-on-dark` reaches 7.67:1 — dark sections re-point the token.

**Rules:** accent is a signal — labels, section markers, links, CTAs, hover states.
Never a large background fill. Never a third hue. Check contrast against the *darkest
surface a colour lands on*, not against white. Never draw a label's text and its
background tint from the same value — that caps contrast near 4:1; darken the text ~15%.

---

## 3. Typography

Two typefaces. Never a third.

- **Bricolage Grotesque** (200–800, variable) — display, headings, body, UI.
  Tracking −0.052em display, −0.03em body.
- **JetBrains Mono** (400/500/600) — buttons, labels, tags, CTAs, metadata, code.
  Uppercase, 9–11px, tracking 0.08–0.20em.

Headings are always left-aligned (centred only for pull quotes). One accent word per
heading, marked `*asterisks*` in CMS fields, rendered as `<em>` — prefer the last or
most important noun. Product headings take no accent word.

---

## 4. Spacing, motion, geometry

Spacing is a 4px scale: `--s1` 4 · `--s2` 8 · `--s3` 12 · `--s4` 16 · `--s6` 24 ·
`--s8` 32 · `--s12` 48 · `--s16` 64 · `--s24` 96 (section padding).

Motion is architectural, never decorative. `--ease-out: cubic-bezier(0.23, 1, 0.32, 1)`
for entrances and hover; `--ease-inout: cubic-bezier(0.77, 0, 0.175, 1)` for state
changes and layout shifts. Micro 130–160ms · standard 280–420ms · cinematic 560–700ms.
Scroll reveal is opacity 0→1 plus translateY(12px→0), staggered 55ms per child.
**No bounce or spring easings.**

Geometry: `--radius: 0` on everything structural — tiles, cards, inputs, buttons, bento
cells. `--radius-pill: 999px` for **status badges only**. `--radius-full: 50%` for status
dots and avatars only.

---

## 5. Web (marketing)

1400px max width, fluid padding `clamp(24px, 5vw, 80px)`, 96px section padding.

Patterns: full-viewport hero with left-aligned title at the bottom; 4-column meta band;
2-column overview (heading left, body right); 12-column asymmetric bento; dark statistics
band; identity bento.

Buttons are uppercase mono, 0.11em tracking, sharp corners. Primary is dark fill with
white text; ghost is outlined. Both hover to a 3px offset accent box-shadow with
`translate(-1.5px, -1.5px)`; active is `scale(0.97)`.

Section label ("slabel"): mono, 10px, 0.20em tracking, uppercase, accent, preceded by a
22px accent rule. Always precedes a section heading.

Imagery is architectural, not lifestyle — the system operating in the real world, not
people smiling at laptops. Defined bento ratios (16/7 lead, 7/5, 1/1, 4/5, 3/2), never
arbitrary crops. Hero images always carry a scrim:
`linear-gradient(to bottom, transparent 30%, rgba(0,0,0,0.75) 100%)`.

---

## 6. Product (application UI)

Denser than web: 13px body, 10px mono labels, 8–12px control padding, 12px 24px rows.

### Surfaces

| Token | Value | Use |
|---|---|---|
| `--bg-primary` | `oklch(1 0 0)` | app canvas |
| `--bg-secondary` | `oklch(0.985 0.001 0)` | sidebar, panels, modals |
| `--bg-tertiary` | `oklch(0.97 0.001 0)` | inputs, chips, cards |
| `--bg-hover` | `oklch(0.96 0.001 0)` | row and nav hover |
| `--bg-elevated` | `oklch(0.955 0.001 0)` | raised cards |
| `--bg-active` | `oklch(0.93 0.001 0)` | pressed/selected |
| `--border-subtle` | `oklch(0 0 0 / 0.08)` | row separators |

Elevation is a surface step plus a border, never a shadow. Hover lifts a row *toward*
white, never darkens it. Shadows only where something genuinely floats — modals,
drawers, popovers. No dark panels inside the app; the whole product is light.

### Status

Seven states, each ~5:1 on white. Status is the one permitted pill and the one place
colour carries meaning — so every badge pairs its colour with a dot **and** a written
label. Colour is never the only signal.

| Status | Value | On white |
|---|---|---|
| Planning | `#7c3aed` | 5.70:1 |
| Active | `#0f766e` | 5.47:1 |
| In Review | `#b45309` | 5.02:1 |
| On Hold | `#c2410c` | 5.18:1 |
| Completed | `#15803d` | 5.02:1 |
| Paid | `#a16207` | 4.92:1 |
| Cancelled | `#dc2626` | 4.83:1 |

Badge: `border-radius: 999px`, padding `3px 12px`, JetBrains Mono 10px / 0.08em /
uppercase, 7px solid dot, background at 10% tint. When a badge sits on a card rather
than on white, darken the *label* ~15% and leave the tint at the original colour.

Identity colours (avatars), assigned by hashing the name so they stay stable — all hold
4.6:1+ under white initials: `#4f46e5` `#7c3aed` `#9333ea` `#db2777` `#e11d48` `#c2410c`
`#a16207` `#15803d` `#0f766e` `#0e7490` `#1d4ed8` `#1e40af`.

Product rules: money, dates, counts and IDs in JetBrains Mono (tabular). Accent for
derived and interactive values only, not every number. Row hover reveals actions. One
accent action per view. Circles only for status dots and avatars.

---

## 7. Voice

Direct, authoritative, specific. Lead with the point; no throat-clearing. Reference real
outcomes and numbers. Think Stripe or Figma blog, not generic Medium.

**Write like this:** "We engineer brand systems that perform under pressure." ·
"Fix the governance and the drift disappears." · "We don't redesign. We rearchitect."

**Never:** "We're passionate about creating beautiful experiences." · "Our innovative
solutions leverage cutting-edge methodologies." · "We'll make your brand pop!"

---

## 8. Build notes

**Always:** use tokens, never hardcoded values. OKLCH for all colour. `font-synthesis:
none`. `clamp()` for fluid type. Left-aligned headings. `-webkit-font-smoothing:
antialiased`. Verify contrast against the darkest surface a colour lands on. Define every
token a module references — an undefined `var()` silently falls back and can ship the
wrong theme.

**Never:** border-radius on structural elements. A third typeface. Bounce or spring
easing. Centred hero or section headings. Hardcoded hex. Accent as a large background
fill. `var()` inside an SVG `stroke`/`fill` attribute — presentation attributes don't
resolve custom properties; use `currentColor` or a literal. Building a colour by
string-concatenating an alpha suffix onto a token.

**Web/product parity:** identical palette, typefaces, easing, zero radius, left-aligned
headings. Different only in density. Product adds surfaces and status on top of the
foundation; it never redefines it. A second accent hue for product is never the answer.
