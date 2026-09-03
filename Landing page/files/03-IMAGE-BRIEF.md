# Image Brief — Parallax Northeast India

Six slots. Guidelines §10 governs everything here: architectural over lifestyle, the system
operating in the real world, no people smiling at laptops, no stock handshakes, no arbitrary
crops. Every image has a fixed ratio and a defined focal point via `object-position`.

Claude Code uses labelled grey placeholders at the correct ratio. These are commissioned
or generated separately.

---

## Direction

The whole set should read as one shoot: cool daylight, hard structure, deep space, restrained
colour. Blue only where it occurs naturally — glass, screens, dusk, cleanroom light — so the
accent feels found rather than applied. Warm skin tones and golden hour are off-brand here.

Nothing decorative and nothing touristic. The Northeast in these images is an economy, not
a destination. Deliberately avoid the visual clichés the region is usually sold with:
no living root bridges, no waterfalls, no tribal dress, no misty hills. That imagery is the
outside view. The whole positioning is the inside one.

---

## Slots

### `img_ne_hero` — 16/9, full viewport
**Section:** Hero
**Subject:** A wide architectural exterior at dusk — a contemporary commercial or
institutional building in Guwahati or Shillong, lit windows, strong horizontal structure.
Deep foreground shadow so the scrim has something to sit on.
**Focal point:** Upper right third. Title block occupies bottom left.
**Note:** Ships with the standard scrim, `linear-gradient(to bottom, transparent 30%,
oklch(0 0 0 / 0.75) 100%)`. Any image needs to survive losing its bottom half.

### `img_sector_realestate` — 16/7, lead tile
**Section:** Sectors, S—01
**Subject:** A residential or mixed-use tower under construction, shot straight on.
Scaffolding geometry, concrete frame, crane. No people. Grey sky is fine and preferable.

### `img_sector_hospitality` — 4/5, tall tile
**Section:** Sectors, S—02
**Subject:** A hotel interior with architectural intent — an empty reception volume, a
corridor, a stairwell. Hard lines, controlled light. Empty of guests. Not a bedroom, not
a breakfast spread, not a view.

### `img_sector_pharma` — 1/1, square tile
**Section:** Sectors, S—03
**Subject:** Pharmaceutical manufacturing interior. A packaging or blister line, stainless
steel, cleanroom lighting. If a technician appears they are in full gown with back turned —
a figure for scale, not a portrait. This is the strongest image in the set. Give it the
most attention.

### `img_sector_education` — 3/2
**Section:** Sectors, S—04
**Subject:** Institutional campus architecture — a lecture theatre from the rear, a
library stack, a covered walkway. Empty. Repetition and rhythm are the subject.

### `img_designers_workspace` — 16/7
**Section:** Designer network (optional; the section reads fine without it)
**Subject:** A designer's desk shot from above or at a hard angle. Screens showing wireframe
and component work, notebook, no branding visible, no face. Cool light.

---

## Generation prompts

If these are generated rather than shot, the prompts below are the starting point. Run the
hero first, lock a style reference off the approved result, then apply that reference to the
remaining five so the set holds together. The old blueprint style reference does not apply
to this system — it belongs to the previous identity and should not be reused.

- **Hero:** `contemporary commercial building exterior at dusk, northeast india, strong horizontal concrete and glass structure, lit windows, deep shadow foreground, wide architectural photography, cool desaturated palette, overcast sky, no people, editorial, 16:9`
- **Real estate:** `high-rise residential tower under construction, exposed concrete frame and scaffolding, tower crane, straight-on elevation, overcast grey sky, architectural photography, no people, desaturated, 16:7`
- **Hospitality:** `empty modern hotel reception interior, double-height volume, hard architectural lines, controlled cool lighting, polished stone floor, no people, editorial interior photography, 4:5`
- **Pharma:** `pharmaceutical manufacturing cleanroom, stainless steel blister packaging line, cool clinical lighting, precision machinery, industrial photography, sterile, no faces, 1:1`
- **Education:** `empty university lecture theatre from the rear, tiered seating rhythm, institutional concrete architecture, cool daylight, no people, architectural photography, 3:2`
- **Workspace:** `overhead view of a designer's desk, dual monitors showing wireframes and a component library, notebook and pen, cool neutral light, no faces, no visible branding, editorial, 16:7`

---

## Implementation

- `object-fit: cover` on every slot, with `object-position` set per image once the final
  crops are chosen.
- WebP with a JPEG fallback. Hero at 2400px wide, tiles at 1600px.
- `loading="lazy"` on everything below the hero; hero is eager with `fetchpriority="high"`.
- Alt text is descriptive and specific. Decorative textures get `alt=""`.
- No `border-radius`. No drop shadows. No filters beyond a documented scrim.
