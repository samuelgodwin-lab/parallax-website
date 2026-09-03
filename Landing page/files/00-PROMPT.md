# Instruction for Claude Code

Paste this as your first message, with this folder open.

---

Build a single-page landing site for Parallax targeting Northeast India.

Read these files first, in order, and treat them as authoritative:

1. `01-BUILD-SPEC.md` — section-by-section structure, components, layout rules
2. `02-COPY.md` — final copy for every slot. Use it verbatim. Do not rewrite it.
3. `03-IMAGE-BRIEF.md` — image slots, aspect ratios, art direction
4. `tokens.css` — the design tokens. Import it. Never hardcode a colour or spacing value.
5. `BRAND-GUIDELINES.html` — the full Parallax brand system v2.0. This overrides anything
   that conflicts with it.

Build as a static site: `index.html`, `styles.css`, `main.js`. No framework, no build step,
no dependencies beyond Google Fonts. It has to drop into the existing parallaxorg.com
structure without a toolchain.

Hard constraints, in priority order:

- Every colour and spacing value comes from a token. No hex literals in `styles.css`.
- Two typefaces only: Bricolage Grotesque and JetBrains Mono.
- `border-radius: 0` on every structural element. Pills are allowed on status badges only.
- All headings left-aligned. Never centred.
- One accent word per heading, wrapped in `<em>`. See `02-COPY.md` for which word.
- `prefers-reduced-motion` fully respected. No bounce or spring easing anywhere.
- Responsive to 360px. Visible keyboard focus on every interactive element.
- Lighthouse accessibility 95+.

Work in this order and stop for review after each phase:

**Phase 1** — Scaffold, tokens, fonts, and the shared components (`.slabel`, `.btn`,
`.meta-band`, `.reveal`). Show me a component sheet before building any sections.
**Phase 2** — Hero, meta band, and the gap section.
**Phase 3** — Sectors bento, government band, services list.
**Phase 4** — Designer network, CTA, footer.
**Phase 5** — Scroll reveal, motion pass, responsive pass, accessibility audit.

Use grey placeholder blocks with the correct aspect ratio and the slot key printed on them
for every image. Do not source or generate images — they are being commissioned separately.
