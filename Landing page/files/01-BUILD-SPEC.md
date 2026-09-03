# Build Spec — Parallax Northeast India

Single page. Nine sections. All copy lives in `02-COPY.md`; this file defines structure only.

---

## Shared components

Build these first and show a component sheet before any section work.

### `.slabel` — section label
Mono, 10px, `0.20em` tracking, uppercase, colour `--text-3`. A 22px horizontal accent rule
sits before the text with `--s3` gap. Always immediately precedes a section heading.
Never appears alone.

### Heading with accent word
Every heading contains exactly one `<em>`, rendered in `--accent`, not italic
(`font-style: normal`). Always the last or most impactful word. Display tracking
`-0.052em`, body tracking `-0.03em`. Left-aligned, no exceptions.

### `.btn` — two variants
- `.btn--primary`: solid `--text` fill, `--bg` text.
- `.btn--ghost`: 1px `--border-strong` outline, transparent fill. On hover, a 3px offset
  box-shadow in `--accent` (`box-shadow: 3px 3px 0 var(--accent)`) and the border goes
  to `--accent`.
- Both: JetBrains Mono, uppercase, `0.11em` tracking, `border-radius: 0`,
  padding `var(--s4) var(--s8)`, transition `var(--dur-micro) var(--ease-out)`.

### `.meta-band` — 4-column metadata strip
Full-width, 1px top and bottom border. Each cell: mono label in `--text-3` above a
Bricolage value in `--text`. Collapses to 2 columns below 768px, 1 column below 480px.

### `.reveal` / `.stagger` — scroll reveal
`opacity: 0 → 1` plus `translateY(12px → 0)`, `var(--dur-standard) var(--ease-out)`.
`.stagger` children offset 55ms each. IntersectionObserver, unobserve after firing.
Disabled entirely under `prefers-reduced-motion`.

### Grid texture
48px CSS grid, 3–5% opacity. Used only on the hero and the statistics band. Not on
light sections.

---

## Layout rules

- Container: `max-width: var(--w-max)`, padding `0 var(--w-padding)`.
- Section vertical padding: `var(--section-pad)` top and bottom.
- Section dividers: 1px `--border` top rule, full-bleed.
- Fluid type via `clamp()` throughout. No fixed breakpoints for copy.

---

## Sections

### 01 — Nav
Sticky, 1px bottom border, `--bg` at 85% with `backdrop-filter: blur(12px)`.
Left: `Parallax.` wordmark, Bricolage 800, `letter-spacing: -0.045em`, full stop in
`--accent`. Right: mono `NORTHEAST INDIA` label and a `.btn--ghost` reading
`Start a project`. Below 768px the button stays, the label drops.

### 02 — Hero
Full viewport (`100svh`), title block anchored bottom-left. Background: `img_ne_hero`
with the standard scrim `linear-gradient(to bottom, transparent 30%, oklch(0 0 0 / 0.75) 100%)`.
Text is white over the scrim regardless of the light palette elsewhere — wrap in `.invert`.

Order: `.slabel` → `h1` → lede paragraph (max 52ch) → button pair.
Hero entrance uses `--dur-cinematic`.

### 03 — Meta band
Immediately under the hero, no section padding above. Four cells. See copy file.

### 04 — The gap
2-column: `.slabel` + `h2` on the left (5 cols), body copy on the right (6 cols, offset 1).
Stacks below 880px. Body max 46ch.

### 05 — Statistics band
`.invert`, full-bleed dark, 48px grid texture at 4%. Four large numbers in Bricolage 800,
`clamp(40px, 6vw, 88px)`, tracking `-0.04em`. Mono caption beneath each in `--text-3`.
Below the numbers, a single centred-in-container row of client wordmarks in mono,
`--text-2`, separated by an accent `·`. This is the only place client names appear.

### 06 — Sectors bento
Four sectors, 12-column asymmetric grid — not four equal cards.

```
┌─────────────────────────┬───────────────┐
│  S-01 Real estate       │  S-02         │
│  span 7 · img 16/7      │  Hospitality  │
│                         │  span 5 · 4/5 │
├───────────────┬─────────┴───────────────┤
│  S-03 Pharma  │  S-04 Education         │
│  span 5 · 1/1 │  span 7 · 3/2           │
└───────────────┴─────────────────────────┘
```

Each tile: image slot at the stated ratio → `.slabel` with sector code (S—01 etc.) →
`h3` → body paragraph → mono capability tags (1px `--border`, no radius) → a datum block
separated by a 1px dashed top rule, with the figure in `--accent` Bricolage 800.

Tiles have a 1px `--border` and `--accent-soft` background on hover. Gap: `var(--s3)`.
Two columns below 1024px, one column below 640px.

### 07 — Government
`--surface` background. 2-column: `.slabel` + `h2` + lede on the left, a 2×3 grid of
capability tiles on the right. Each tile is mono text with a 1px `--border`, `--s6` padding.
No imagery.

### 08 — Services
Full-width list, six rows, 1px `--border` between each. Row grid:
`60px | 1fr | 1.45fr` — mono index, `h3`, body paragraph.
Rows 1–3 (Interface Design, Design Systems, Frontend Engineering) get the accent treatment:
`h3` in `--accent` and a 2px `--accent` left border that appears on hover with a
`padding-left` shift of `var(--s3)`. Rows 4–6 are plain.
Stacks to a single column below 880px.

### 09 — Designer network
`--surface-raised` background. `.slabel` → `h2` → lede → three-step grid.
Steps sit in a 1px `--border` container with 1px internal dividers, `--bg` fill,
no gaps — a single ruled block, not three floating cards.
Each step: mono `STEP 01` in `--accent` → `h4` → body.
Below the steps, a row of four mono terms in 1px `--accent` outlined boxes.
Then a single `.btn--primary`.

### 10 — CTA
`--bg`. Left-aligned like everything else. `.slabel` → large `h2` → lede →
button pair (`projects@parallaxorg.com` primary, `See the work` ghost linking to
`https://www.parallaxorg.com/work.html`).

### 11 — Footer
1px top border, `var(--s8)` padding. Left: `Parallax.` wordmark and copyright.
Right: mono list of the eight states. Below 640px, stack left-aligned.

---

## Do not

- Introduce a third typeface.
- Add `border-radius` to any tile, button, image, or input.
- Centre any heading.
- Use `--accent` as a large background fill. It appears on labels, one word per heading,
  figures, hover states, and CTA borders only.
- Add bounce, spring, or overshoot easing.
- Source or generate images. Use labelled placeholders.
