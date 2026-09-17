"""Generate /denver/ from the live Dubai page.

Dubai, not Munich, is the source: it is the freshest structure and already
carries the pricing band and plan drawer that Denver also publishes. Denver
differs from it in copy, images, currency, the band (accessibility and
compliance replaces bilingual) and the hero loop.

Copy comes from 01-COPY.md (signed off 17 Sep 2026). Every substitution is
asserted, so a change to dubai/index.html that breaks an anchor fails loudly
here rather than shipping a half-Dubai page.
"""
import re, os, shutil, urllib.parse
ROOT = "/Users/samuelgodwin/Documents/2026/Parallax/Website Test — Copy"
src = open(f"{ROOT}/dubai/index.html").read()
body = src[src.index('<body>'):]

def rep(s, old, new, n=1):
    assert s.count(old) == n, (old[:70], s.count(old))
    return s.replace(old, new)

def sub1(s, pattern, new, flags=re.S):
    m = re.search(pattern, s, flags)
    assert m, pattern[:70]
    return s[:m.start()] + new + s[m.end():]

def placeholder(key, w, h):
    svg = (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {w} {h}'><rect width='100%' height='100%' fill='#d8dde4'/>"
           f"<text x='50%' y='50%' dominant-baseline='middle' text-anchor='middle' font-family='JetBrains Mono,monospace' "
           f"font-size='{max(w,h)//40}' letter-spacing='2' fill='#5b6470'>{key}</text></svg>")
    return "data:image/svg+xml," + urllib.parse.quote(svg)

def pic(name, w, h, alt):
    return (f'<picture>\n                <source type="image/webp" srcset="images/{name}.webp">\n'
            f'                <img src="images/{name}.jpg" width="{w}" height="{h}"\n'
            f'                     alt="{alt}"\n                     loading="lazy" decoding="async">\n              </picture>')

b = body

# ── preloader / nav ──
b = rep(b, "status.textContent = 'DUBAI'", "status.textContent = 'DENVER'")
b = rep(b, "FINAL = 'DUBAI'", "FINAL = 'DENVER'")
b = rep(b, '<span class="nav__label">Dubai</span>', '<span class="nav__label">Denver</span>')

# ── hero: Samuel's Vimeo loop (Denver_Final, 1227702653, 23 s — fourth cut of
# 17 Sep, after 1227691546, 1227693782 and 1227698154), poster = its first frame ──
# Poster pulled from Vimeo's oEmbed thumbnail at 1920×1080 into
# denver/images/den-hero-poster.{jpg,webp}. Mean 231/255, text column 234:
# light enough for the type to run straight over it, no veil, as on Munich
# and Dubai. main.js pins the player to 1080p.
hero_bg = b[b.index('    <div class="hero__bg">'):b.index('    <!-- Cursor colour-reveal')]
new_bg = hero_bg.replace('dxb-hero-poster', 'den-hero-poster').replace('1226928370', '1227702653').replace('title="Dubai hero"', 'title="Denver hero"')
# Dubai's source carries the poster comment twice; keep one.
dup = """      <!-- Poster is the video's own first frame, pulled from Vimeo. It holds the
           frame while the player boots and is all that shows under reduced motion. -->
"""
assert new_bg.count(dup) == 2
new_bg = new_bg.replace(dup, '', 1)
b = b.replace(hero_bg, new_bg, 1)
assert '1227702653' in b and 'den-hero-poster.webp' in b and 'Dubai' not in new_bg
b = rep(b, '<div class="slabel slabel--hero">Dubai</div>', '<div class="slabel slabel--hero">Denver</div>')
b = rep(b, 'Dubai&rsquo;s next companies<br>', 'Denver&rsquo;s next companies<br>')
b = sub1(b, r'<p class="lede hero__lede">.*?</p>',
  '<p class="lede hero__lede">Brand systems, interface design and frontend engineering &mdash; one studio, from identity to shipped code, on your clock: briefed at five, built overnight, waiting at eight. For the startup that left the coast and the brand that lives on taste.</p>')
b = rep(b, 'subject=New%20project%20%E2%80%94%20Dubai', 'subject=New%20project%20%E2%80%94%20Denver')
b = sub1(b, r'<p class="hero__proof">.*?</p>', '<p class="hero__proof">BMW &middot; Accenture &middot; Nissan &middot; Sportradar &mdash; and a studio that works while Denver sleeps.</p>')
b = rep(b, '<a href="#designers">Designer in Dubai?</a>', '<a href="#designers">Designer in Denver?</a>')

# ── what we build ──
b = sub1(b, r'<p class="svcs__desc">.*?</p>', '<p class="svcs__desc">Everything a product needs to leave the building, from one team &mdash; coast-quality work at a price a Denver round can carry.</p>')

# ── client logos: YVT stays on Dubai; BMW leads ──
logos = b[b.index('05 — CLIENT LOGOS'):b.index('06 — SECTORS BENTO')]
i = logos.index('          <!-- YVT -->'); j = logos.index('          <!-- BMW -->')
assert logos[i:j].count('logo-mark') == 1 and logos[i:j].count('logo-sep') == 1
b = b.replace(logos, logos[:i] + logos[j:], 1)

# ── sectors: bright / dark / dark / bright (two-scene rule) ──
sectors = [
 ('S&mdash;01 · Startups &amp; scale-ups', 'Ready before the <em>round.</em>',
  "Fourteen hundred startups, and the ones that matter came here from the coast for cost and talent. They need a brand system, a product interface and a marketing site that look like they never left &mdash; before the next round, not after it. We build all three as one system, from a studio that prices like Denver and ships like San Francisco.",
  ['Brand systems', 'Product UI', 'Design systems', 'Marketing sites'],
  ('sector-startups-1600', 'A founding team of three in fleece and flannel around a long timber table in a converted red-brick RiNo loft, hard midday sun through tall factory windows, laptops and a wall of printed app screens, the Front Range on the horizon through the glass.'), (1600, 1067)),
 ('S&mdash;02 · Aerospace, energy &amp; industrial', 'Tools that match the <em>hardware.</em>',
  "Twenty-three billion dollars of federal contracts and a renewable cluster, running on internal software built by engineers for engineers and never once designed. We build the dashboards, partner portals and configurators that make a control room feel like a product &mdash; and the design system that keeps the next one consistent.",
  ['Internal tools &amp; dashboards', 'Partner portals', 'Configurators', 'Industrial software UI'],
  ('sector-aerospace-1600', 'An engineer in a flannel shirt at a glowing console in a mission-operations room at blue hour, a wall of telemetry dashboards, a satellite bus on a stand behind her and alpenglow on the mountains through the window.'), (1280, 1600)),
 ('S&mdash;03 · Outdoor &amp; consumer brands', 'Taste is the <em>spec.</em>',
  "Thirty-seven billion dollars of outdoor spending, and the brands that earn it are judged on how they look before what they sell. We build the storefronts, product configurators and brand systems where the craft has to show &mdash; for the brands that make Denver Denver, and the long tail behind them in Boulder and RiNo.",
  ['Brand systems', 'Storefronts', 'Product configurators', 'Brand sites'],
  ('sector-outdoor-1600', 'A customer in a down jacket weighing a pack in a flagship outdoor store at blue hour, timber and blackened-steel shelving under warm pendant lamps, an assistant at a concrete counter, the lit city and the mountain silhouette through the glass front.'), (1600, 1600)),
 ('S&mdash;04 · Real estate &amp; proptech', 'Inventory that <em>moves.</em>',
  "A five-seventy-five median, a hundred and twenty days of condo supply, and buyers who read the HOA line before the floor plan. A buyer's market needs product that sells, not a PDF. We build the inventory, viewing and owner portals that move units &mdash; the same systems we run for developers in India and Dubai, built for a Colorado closing.",
  ['Inventory &amp; viewing portals', 'Owner &amp; HOA portals', 'Property-management UI', 'Broker tools'],
  ('sector-realestate-1600', 'A young couple touring an empty new-build loft in LoDo with a broker holding a tablet, hard morning light down exposed brick and steel beams, Union Station&rsquo;s clock tower and the mountains through the tall windows.'), (1600, 1067)),
]
sec = b[b.index('06 — SECTORS BENTO'):b.index('07 — BILINGUAL')]
arts = re.findall(r'(<article class="sector sector--0\d reveal">.*?</article>)', sec, re.S)
assert len(arts) == 4
new_sec = sec
for art, (lab, h3, bod, tags, (img, alt), (w, h)) in zip(arts, sectors):
    a = art
    a = sub1(a, r'<picture>.*?</picture>', pic(img, w, h, alt))
    a = sub1(a, r'<div class="slabel">S&mdash;0\d · [^<]*</div>', f'<div class="slabel">{lab}</div>')
    a = sub1(a, r'<h3 class="sh sh--sub">.*?</h3>', f'<h3 class="sh sh--sub">{h3}</h3>')
    a = sub1(a, r'<p class="sector__body">.*?</p>', f'<p class="sector__body">{bod}</p>')
    a = sub1(a, r'<div class="sector__tags">.*?</div>', '<div class="sector__tags">\n' + ''.join(f'              <span class="tag">{t}</span>\n' for t in tags) + '            </div>')
    new_sec = new_sec.replace(art, a, 1)
b = b.replace(sec, new_sec, 1)

# ── bilingual band → accessibility & compliance band ──
gov = b[b.index('07 — BILINGUAL'):b.index('08 — THE NETWORK')]
g = sub1(gov, r'07 — BILINGUAL[^\n]*', '07 — ACCESSIBLE &amp; COMPLIANT', 0)
g = rep(g, '<div class="slabel">Bilingual &amp; Accessible</div>', '<div class="slabel">Accessible &amp; Compliant</div>')
g = sub1(g, r'<h2 class="sh" id="gov-h">.*?</h2>', '<h2 class="sh" id="gov-h">Accessible is the <em>law</em> here.</h2>')
g = sub1(g, r'<p class="lede gov__lede">.*?</p>',
  '<p class="lede gov__lede">Colorado got there first. HB21-1110 has required every public platform to meet WCAG 2.1 AA since July 2025, at $3,500 a violation; the ADA Title II web rule follows in April 2027, the Privacy Act governs the data and SB 26-189 the AI. Product sold to the public sector has to pass. We measure every page we ship against AA &mdash; and can do the same for yours.</p>')
tiles = [  # bright / dark / bright / dark / bright / dark
 ('Audit', 'Accessibility audits (WCAG 2.1 AA)', 'Measured page by page against Title II and HB21-1110, every failure specified as a fix rather than a finding.',
  ('ac-audit-800', 'A woman with headphones and a refreshable braille display testing a web app at a desk by a tall sunlit window, exposed brick and a low Denver skyline outside.'), (800, 600)),
 ('Fix', 'Remediation', 'Contrast, focus, structure, forms and motion brought to AA inside your existing codebase, without a redesign.',
  ('ac-remediation-800', 'Two engineers pairing at a monitor of grey interface blocks with focus rings highlighted, at dusk in a brick loft, alpenglow on the Front Range through the window.'), (800, 600)),
 ('Systems', 'Accessible design systems', 'Tokens and components that pass by default, so the next feature your team ships is compliant before anyone checks.',
  ('ac-systems-1200', 'A designer in a flannel shirt at a wide monitor showing a grid of grey interface components, hard midday light across a concrete and timber studio, the mountains beyond the window.'), (1200, 1200)),
 ('Privacy', 'Privacy by design (CPA)', 'Consent, opt-outs and data-protection assessments designed into the product the way the Colorado Privacy Act reads them, not bolted on by a banner.',
  ('ac-privacy-1200', 'Three people over printed data-flow diagrams at a dark walnut table high in a downtown Denver tower at blue hour, the city lights and the dark mountain line below.'), (1200, 1200)),
 ('AI', 'AI disclosure &amp; consent flows (SB 26-189)', 'Notice, disclosure and impact-assessment flows for the high-risk AI features you&rsquo;ll ship in 2027, designed in before the law is live.',
  ('ac-ai-800', 'A product team sketching a consent flow on a whiteboard against a red-brick wall, hard morning sun through a steel-framed window, coffee and laptops on a plywood table.'), (800, 600)),
 ('Handover', 'Compliance handover', 'Documentation, VPAT-style conformance reports and test evidence that let a procurement office, or the next vendor, pick it up.',
  ('ac-handover-800', 'A designer passing a bound documentation binder and a laptop across a table to two city officials in the evening, a wall of printed screens behind, the lit capitol dome through the window at dusk.'), (800, 600)),
]
tl = re.findall(r'(<article class="gov__tile[^"]*">.*?</article>)', g, re.S)
assert len(tl) == 6, len(tl)
for art, (tag, head, desc, (img, alt), (w, h)) in zip(tl, tiles):
    a = art
    a = sub1(a, r'<picture>.*?</picture>', pic(img, w, h, alt))
    a = sub1(a, r'<p class="gov__tile-tag">.*?</p>', f'<p class="gov__tile-tag">{tag}</p>')
    a = sub1(a, r'<h3 class="gov__tile-head">.*?</h3>', f'<h3 class="gov__tile-head">{head}</h3>')
    a = sub1(a, r'<p class="gov__tile-desc">.*?</p>', f'<p class="gov__tile-desc">{desc}</p>')
    g = g.replace(art, a, 1)
b = b.replace(gov, g, 1)

# ── network ──
dn = b[b.index('08 — THE NETWORK'):b.index('09 — WHERE WE WORK')]
d = rep(dn, '<div class="slabel">For Designers in Dubai</div>', '<div class="slabel">For Designers in Denver</div>')
d = sub1(d, r'<p class="lede dn__lede">.*?</p>',
  "<p class=\"lede dn__lede\">The lead in the room is the whole model here: you run the day in Mountain time, the studio builds overnight. We're looking for the first &mdash; senior designers and design leads who can own the relationship, with a delivery team behind them. A day rate for your time, ten percent of what you bring in. Three ways in.</p>")
d = sub1(d, r'<picture>.*?</picture>', pic('network-studio-1600', 1600, 700, 'A mixed young design team in a bright converted-warehouse studio in RiNo: one walking through with a laptop, others at a wall of sticky notes and along a long timber table; hard sunlight, red brick and a mural across the street through the tall windows.'))
steps = [('Lead a project', 'Discovery, workshops and presentations, in the room, in Denver or Boulder. Day rate agreed before you start.'),
         ('Bring work in', 'Introduce a company. We scope, price and close; you lead it, and take 10% of the fee.'),
         ('Set the standard', 'Portfolio reviews for the network, a presence at AIGA Colorado and Startup Week, published work with your name on it.')]
st = re.findall(r'(<h3 class="sh sh--step">.*?</h3>\s*<p class="dn__step-b">.*?</p>)', d, re.S)
assert len(st) == 3
for old, (h, p) in zip(st, steps):
    d = d.replace(old, f'<h3 class="sh sh--step">{h}</h3>\n          <p class="dn__step-b">{p}</p>', 1)
b = b.replace(dn, d, 1)

# ── where we work: Denver is here; Dubai becomes a link (source is the launched Dubai page, Denver live everywhere) ──
b = rep(b, '<a class="mk__pin mk__pin--live" style="--x:19.61%;--y:40.75%;--d:0.6s" href="/denver/" data-tz="America/Denver"><span class="mk__dot" aria-hidden="true"></span><span class="mk__pin-label">Denver <span aria-hidden="true">&rarr;</span></span></a>',
           '<span class="mk__pin mk__pin--live mk__pin--here" style="--x:19.61%;--y:40.75%;--d:0.6s" data-tz="America/Denver"><span class="mk__dot" aria-hidden="true"></span><span class="mk__pin-label">Denver</span></span>')
b = rep(b, '<span class="mk__pin mk__pin--live mk__pin--here mk__pin--flip" style="--x:61.52%;--y:52.06%;--d:1.2s" data-tz="Asia/Dubai"><span class="mk__dot" aria-hidden="true"></span><span class="mk__pin-label">Dubai</span></span>',
           '<a class="mk__pin mk__pin--live mk__pin--flip" style="--x:61.52%;--y:52.06%;--d:1.2s" href="/dubai/" data-tz="Asia/Dubai"><span class="mk__dot" aria-hidden="true"></span><span class="mk__pin-label">Dubai <span aria-hidden="true">&rarr;</span></span></a>')
b = rep(b, '''            <li class="mk__row mk__row--live">
              <a class="mk__cell" href="/denver/">
                <span class="mk__name">Denver</span>
                <span class="mk__meta"><span class="mk__time" data-tz="America/Denver">--:--</span><span class="mk__go">Visit <span aria-hidden="true">&rarr;</span></span></span>
              </a>
            </li>''', '''            <li class="mk__row mk__row--live mk__row--here">
              <span class="mk__cell">
                <span class="mk__name">Denver</span>
                <span class="mk__meta"><span class="mk__time" data-tz="America/Denver">--:--</span><span class="mk__here">You're here</span></span>
              </span>
            </li>''')
b = rep(b, '''            <li class="mk__row mk__row--live mk__row--here">
              <span class="mk__cell">
                <span class="mk__name">Dubai</span>
                <span class="mk__meta"><span class="mk__time" data-tz="Asia/Dubai">--:--</span><span class="mk__here">You're here</span></span>
              </span>
            </li>''', '''            <li class="mk__row mk__row--live">
              <a class="mk__cell" href="/dubai/">
                <span class="mk__name">Dubai</span>
                <span class="mk__meta"><span class="mk__time" data-tz="Asia/Dubai">--:--</span><span class="mk__go">Visit <span aria-hidden="true">&rarr;</span></span></span>
              </a>
            </li>''')
b = sub1(b, r'<p class="lede mk__lede">.*?</p>',
  "<p class=\"lede mk__lede\">Bengaluru, Northeast India, Munich and Dubai each have their own page &mdash; the work we've done there, the people, and how to reach us. Pick a market.</p>")

# ── pricing: USD, market-set (01-COPY.md §10) ──
b = rep(b, '''       Dubai publishes prices, so the tiers sit on the page in AED: the
       main site's euro tiers at ~4.30 AED/EUR, rounded down to the 10k
       (01-COPY.md §10, option A). Inclusions are the main site's lists.''',
'''       Denver publishes prices, so the tiers sit on the page in USD, set
       from the Denver agency check (01-COPY.md §10): at the floor of the
       local range for Foundation, a third under it for Studio, and within
       10% of the euro tiers. Inclusions are the main site's lists.''')
b = sub1(b, r'<p class="lede pricing__lede">.*?</p>', '<p class="lede pricing__lede">Denver publishes its prices. So do we &mdash; three ways to work with us, in dollars, with what&rsquo;s included on one page.</p>')
b = rep(b, '<sup>AED</sup>50,000', '<sup>$</sup>15,000', 2)
b = rep(b, '<sup>AED</sup>120,000', '<sup>$</sup>35,000', 2)
b = rep(b, ' Arabic scope priced on top.', '')
b = rep(b, ' Bilingual UI priced on top.', '')

# ── CTA ──
b = sub1(b, r'<p class="lede cta__lede">.*?</p>',
  "<p class=\"lede cta__lede\">We start by questioning the brief. One call &mdash; or a WhatsApp thread &mdash; a lot of questions, no deck. Brief us in your afternoon and the first answer is in your inbox the next morning. If we're not the right studio for it, we'll say so and point you at someone who is.</p>")

# ── footer ──
b = rep(b, '<span class="footer__v">Dubai &middot; UAE &middot; GCC</span>', '<span class="footer__v">Denver &middot; Colorado &middot; Mountain West</span>')

# ── drawer: Denver variant ──
b = rep(b, '<p class="net-drawer__tag">For Designers in Dubai</p>', '<p class="net-drawer__tag">For Designers in Denver</p>')
b = rep(b, 'and a Dubai lead who runs the room. That could be you.', 'and a Denver lead who runs the room. That could be you.')
b = rep(b, 'Launch sites, booking engines, onboarding flows, brand systems. Work you led, with a client who&rsquo;ll say so.',
           'Brand systems, product UI, storefronts, owner portals. Work you led, with a client who&rsquo;ll say so.')
b = rep(b, 'When we open a Dubai role, the network hears first.', 'When we open a Denver role, the network hears first.')
b = rep(b, 'Figma seats, our design system and libraries, and a team in your working hours &mdash; 09:00 in Dubai is 10:30 in Bengaluru.',
           'Figma seats, our design system and libraries, and a team that works while you sleep: brief at five, it&rsquo;s waiting at eight. 09:00 in Denver is 20:30 in Bengaluru.')
b = rep(b, '<span class="net-chip">Arabic-speaking, for localisation</span>', '')
b = rep(b, '<span class="net-chip">In Dubai or the Northern Emirates</span>', '<span class="net-chip">In Denver, Boulder or the Front Range</span>')
b = rep(b, "Two of us are already in Dubai; we're adding leads and Arabic-speaking designers, not a roster. Small on purpose &mdash; whoever joins first shapes how it works.",
           "Nobody from the studio is in Denver yet &mdash; you'd be the first, and the first lead shapes how it works. Leads, not a roster. Small on purpose.")
b = rep(b, 'placeholder="Dubai, Sharjah, Abu Dhabi&hellip;"', 'placeholder="Denver, Boulder, Fort Collins&hellip;"')
b = rep(b, '\n            <option>Arabic localisation</option>', '')
b = rep(b, '<input type="hidden" name="market" value="Dubai">', '<input type="hidden" name="market" value="Denver">')

# Dubai may only survive as the map pin, the map row, the map lede and S–04's
# "developers in India and Dubai".
leftover = re.sub(r'<a class="mk__pin[^>]*>.*?</a>|<li class="mk__row mk__row--live">\s*<a class="mk__cell" href="/dubai/">.*?</li>|mk__lede.*?</p>|developers in India and Dubai', '', b, flags=re.S)
assert 'Dubai' not in leftover and 'DUBAI' not in leftover, [leftover[m.start()-60:m.start()+20] for m in re.finditer('Dubai|DUBAI', leftover)]
for bad in ('AED', 'Arabic', 'PDPL', 'UAE', 'dxb-', 'Emirat', 'bilingual', 'Bilingual', 'dirham'):
    assert bad not in b, bad

# ── cache-bust: Denver has its own series ──
b = re.sub(r'\?v=\d+', '?v=1', b)
b = rep(b, 'main.js?v=1', 'main.js?v=2')   # bumped 17 Sep with the setQuality pin

head = '''<!doctype html>
<html lang="en" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" type="image/png" href="/images/Favicon.png">
<link rel="apple-touch-icon" href="/images/Favicon.png">
<title>Design Agency in Denver — Brand, Product &amp; Web | Parallax</title>
<meta name="description" content="Brand systems, product UI and frontend engineering for Denver's next companies — briefed at five, built overnight, ADA Title II and WCAG 2.1 AA by default.">
<link rel="canonical" href="https://www.parallaxorg.com/denver/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Parallax">
<meta property="og:locale" content="en_US">
<meta property="og:url" content="https://www.parallaxorg.com/denver/">
<meta property="og:title" content="Design Agency in Denver — Brand, Product &amp; Web | Parallax">
<meta property="og:description" content="Brand systems, product UI and frontend engineering for Denver's next companies — briefed at five, built overnight, ADA Title II and WCAG 2.1 AA by default.">
<meta property="og:image" content="https://www.parallaxorg.com/denver/images/den-hero-poster.jpg">
<meta property="og:image:width" content="1920">
<meta property="og:image:height" content="1080">
<meta property="og:image:alt" content="Parallax — brand systems and apps for Denver">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Design Agency in Denver — Brand, Product &amp; Web | Parallax">
<meta name="twitter:description" content="Brand systems, product UI and frontend engineering for Denver's next companies — briefed at five, built overnight, ADA Title II and WCAG 2.1 AA by default.">
<meta name="twitter:image" content="https://www.parallaxorg.com/denver/images/den-hero-poster.jpg">
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "ProfessionalService",
  "name": "Parallax",
  "url": "https://www.parallaxorg.com/denver/",
  "logo": "https://www.parallaxorg.com/images/Favicon.png",
  "parentOrganization": { "@type": "Organization", "name": "Parallax", "url": "https://www.parallaxorg.com/" },
  "sameAs": ["https://www.parallaxorg.com/", "https://www.linkedin.com/company/parallaxorg", "https://www.instagram.com/parallaxdsign/"],
  "description": "Parallax builds the brands and apps Denver runs on. Brand systems, interface design and frontend engineering — one studio, from identity to shipped code.",
  "email": "projects@parallaxorg.com",
  "areaServed": [{ "@type": "City", "name": "Denver" }, { "@type": "State", "name": "Colorado" }, { "@type": "Country", "name": "United States" }],
  "availableLanguage": ["en"],
  "priceRange": "USD 15,000 – 35,000+",
  "knowsAbout": ["Brand Systems","Interface Design","Frontend Engineering","Design Systems","Accessibility (WCAG 2.1 AA)","ADA Title II Compliance","Digital Strategy","Motion & Interaction"]
}
</script>
<script>document.documentElement.classList.replace('no-js','js');</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,200..800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="tokens.css?v=1">
<link rel="stylesheet" href="styles.css?v=1">
</head>
'''
out = f"{ROOT}/denver"
os.makedirs(f"{out}/images", exist_ok=True)
open(f"{out}/index.html", "w").write(head + b)
for f in ("styles.css", "tokens.css", "main.js"):
    shutil.copy(f"{ROOT}/Landing page/files/{f}", f"{out}/{f}")
shutil.copy(f"{ROOT}/dubai/images/world-map.svg", f"{out}/images/world-map.svg")
print("denver/index.html written", len(head + b) // 1024, "KB")
