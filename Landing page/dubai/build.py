"""Generate /dubai/ from the live Munich page.

Munich, not the Northeast working copy, is the source: it carries every
structural edit made since the Northeast build (three-line hero, proof line,
network section, accessibility band, .mk__here, marquee fill) and the Dubai
page differs from it only in copy, images and the added pricing band.

Copy comes from 01-COPY.md. Every substitution is asserted, so a change to
munich/index.html that breaks an anchor fails loudly here rather than
shipping a half-Munich page.
"""
import re, os, shutil, urllib.parse
ROOT = "/Users/samuelgodwin/Documents/2026/Parallax/Website Test — Copy"
src = open(f"{ROOT}/munich/index.html").read()
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

def ph_img(key, w, h, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<img{c} src="{placeholder(key+f" · {w}×{h}", w, h)}" width="{w}" height="{h}" alt="" loading="lazy" decoding="async">'

b = body

# ── preloader / nav ──
b = rep(b, "status.textContent = 'MUNICH'", "status.textContent = 'DUBAI'")
b = rep(b, "FINAL = 'MUNICH'", "FINAL = 'DUBAI'")
b = rep(b, '<span class="nav__label">Munich</span>', '<span class="nav__label">Dubai</span>')

# ── hero: Samuel's Vimeo loop (Dubai_Landing, 1226928370), poster = its first frame ──
# Poster pulled from Vimeo at 1920×1080 into dubai/images/dxb-hero-poster.{jpg,webp};
# mean 229/255, so the veil stays off, as on Munich.
hero_bg = b[b.index('    <div class="hero__bg">'):b.index('    <!-- Cursor colour-reveal')]
b = b.replace(hero_bg, hero_bg.replace('muc-hero-poster', 'dxb-hero-poster').replace('1226635583', '1226928370').replace('1226927399', '1226928370').replace('title="Munich hero"', 'title="Dubai hero"'), 1)
assert '1226928370' in b and 'dxb-hero-poster.webp' in b and 'Munich' not in hero_bg.replace('title="Munich hero"', '')
b = rep(b, '<div class="slabel slabel--hero">Munich</div>', '<div class="slabel slabel--hero">Dubai</div>')
b = rep(b, 'Munich&rsquo;s next companies<br>', 'Dubai&rsquo;s next companies<br>')
b = sub1(b, r'<p class="lede hero__lede">.*?</p>',
  '<p class="lede hero__lede">Brand systems, interface design and frontend engineering &mdash; one studio, from identity to shipped code, in English and Arabic from the first screen. For the founder setting up in a free zone, the developer launching off-plan, and the DIFC firm whose onboarding now has to pass the PDPL.</p>')
b = rep(b, 'subject=New%20project%20%E2%80%94%20Munich', 'subject=New%20project%20%E2%80%94%20Dubai')
b = sub1(b, r'<p class="hero__proof">.*?</p>', '<p class="hero__proof">YVT &middot; BMW &middot; Accenture &middot; Nissan &middot; Sportradar &mdash; and two of our own already in Dubai.</p>')
b = rep(b, '<a href="#designers">Designer in Munich?</a>', '<a href="#designers">Designer in Dubai?</a>')

# ── what we build ──
b = sub1(b, r'<p class="svcs__desc">.*?</p>', '<p class="svcs__desc">Everything a product needs to leave the building, from one team &mdash; Arabic and English, at a rate a founder&rsquo;s budget can carry.</p>')

# ── client logos: YVT first, Biblica out ──
yvt_svg = open(f"{ROOT}/Projects/YVT/Identity/SVG/Logo.svg").read()
yvt_paths = re.findall(r'<path class="cls-1" d="[^"]+"/>', yvt_svg)
assert len(yvt_paths) >= 3, len(yvt_paths)
yvt = ('          <!-- YVT -->\n          <div class="logo-mark">\n'
       '            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 274.85 140.64" style="height: 24px; width: auto;" role="img" aria-label="YVT">\n'
       '              <defs><style>.logo-cls-1 {fill: #fff;}</style></defs>\n'
       '              <g>' + ''.join(p.replace('class="cls-1"', 'class="logo-cls-1"') for p in yvt_paths) + '</g>\n'
       '            </svg>\n          </div>\n  \n          <div class="logo-sep"></div>\n  \n')
logos = b[b.index('05 — CLIENT LOGOS'):b.index('06 — SECTORS BENTO')]
i = logos.index('          <!-- Biblica -->'); j = logos.index('          <!-- Accenture')
assert logos[i:j].count('logo-mark') == 1
new_logos = logos[:i] + logos[j:]                      # drop Biblica + its separator
k = new_logos.index('          <!-- BMW -->')
new_logos = new_logos[:k] + yvt + new_logos[k:]
b = b.replace(logos, new_logos, 1)
b = rep(b, '''    <!-- ============================================================
         PRICING
    ============================================================ -->

''', '')

# ── sectors ──
sectors = [
 ('S&mdash;01 · Real estate &amp; proptech', 'Sold before it&rsquo;s <em>built.</em>',
  "Two hundred and seventy thousand transactions last year, most of them off-plan &mdash; sold on a launch site, a broker's phone and a configurator. We build the launch sites, broker and buyer apps, and owner and tenant portals that carry a project from first release to handover &mdash; the same systems we run for developers in India, built for DLD and REES.",
  ['Off-plan launch sites', 'Broker &amp; buyer apps', 'Owner &amp; tenant portals', 'Property-management UI'], ('sector-realestate-1600', 'A developer&rsquo;s sales lounge in Dubai: an Emirati buyer in a kandura and a broker over a white scale model on a brass-edged plinth, warm marble and wood, towers and date palms through the glass.'), (1600, 1067)),
 ('S&mdash;02 · Hospitality &amp; tourism', 'Bookings that skip the <em>middleman.</em>',
  "Nearly twenty million visitors, 827 hotels, and most rooms sold through a channel that keeps a fifth of the rate. We build direct booking engines, guest apps and F&amp;B ordering that keep the guest &mdash; and the margin &mdash; with the property.",
  ['Direct booking engines', 'Guest apps', 'F&amp;B ordering', 'Property UI'], ('sector-hospitality-1600', 'A beachfront resort lobby in Dubai at blue hour: pointed sandstone arches lit by brass lanterns, a glowing mashrabiya screen, a guest in linen checking in at a travertine desk, the dark sea through the far arch.'), (1280, 1600)),
 ('S&mdash;03 · Fintech &amp; financial services', 'Onboarding people <em>finish.</em>',
  "Finance is Dubai's fastest-growing sector, and its products are still sold through flows most customers abandon at the document upload. We build the onboarding, KYC, payments and advisor tools that get finished &mdash; and, under the PDPL, that handle the data the way the regulator expects.",
  ['Onboarding &amp; KYC flows', 'Payments UI', 'Advisor dashboards'], ('sector-fintech-1600', 'A limestone arcade in Dubai&rsquo;s financial district at blue hour, the arches uplit under a glass roof: an Emirati advisor in a kandura and a client in a grey suit at a small marble table with a tablet, lit towers beyond.'), (1600, 1600)),
 ('S&mdash;04 · Founders &amp; trade', 'Open before the licence <em>dries.</em>',
  "Twenty-two thousand Indian businesses set up here in six months, and most needed a brand, a storefront and an ordering portal before the first customer walked in. One team for the lot, from the studio the Bengaluru founders in Dubai already know &mdash; a lead in the room by lunch.",
  ['Brand systems', 'Storefronts', 'B2B ordering portals', 'Marketing sites'], ('sector-founders-1600', 'A young founder with a tablet on the wharf of Dubai Creek at golden hour, cartons and sacks beside him, wooden dhows moored behind and the wind towers of the old town across the water.'), (1600, 1067)),
]
sec = b[b.index('06 — SECTORS BENTO'):b.index('07 — ACCESSIBILITY')]
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

# ── accessibility band → bilingual band ──
gov = b[b.index('07 — ACCESSIBILITY'):b.index('08 — THE NETWORK')]
g = sub1(gov, r'07 — ACCESSIBILITY[^\n]*', '07 — BILINGUAL &amp; ACCESSIBLE', 0)
g = rep(g, '<div class="slabel">Accessibility</div>', '<div class="slabel">Bilingual &amp; Accessible</div>')
g = sub1(g, r'<h2 class="sh" id="gov-h">.*?</h2>', '<h2 class="sh" id="gov-h">Two languages. One <em>system.</em></h2>')
g = sub1(g, r'<p class="lede gov__lede">.*?</p>',
  "<p class=\"lede gov__lede\">Every product in Dubai is two products &mdash; Arabic and English, right-to-left and left-to-right. For government it's law; for everyone else it's expected, and usually bolted on last. We design bilingual from the first screen: mirrored, not flipped, with Arabic typography done properly, every page measured against WCAG 2.1 AA, data flows that have read the PDPL, and UAE Pass where it belongs.</p>")
tiles = [
 ('Systems', 'Bilingual design systems', 'One component library, two directions. Layouts mirror rather than flip, so the Arabic product is designed, not translated.', ('bi-systems-800', 'An Emirati designer in an abaya at a monitor showing the same app interface mirrored right-to-left and left-to-right as grey blocks, warm light through a mashrabiya screen.'), (800, 600)),
 ('Type', 'Arabic typography &amp; RTL', 'Arabic faces chosen and set to sit with the Latin, numerals, dates and forms handled properly, right-to-left tested on real devices.', ('bi-type-800', 'Proof sheets of Arabic and Latin letterforms under a brass desk lamp at night, a reed pen and inkwell, the dusk city through the window behind.'), (800, 600)),
 ('Audit', 'Accessibility audits (WCAG 2.1 AA)', 'Measured page by page against the TDRA policy and the Dubai Universal Design Code, every failure specified as a fix rather than a finding.', ('bi-audit-1200', 'An Emirati man in a kandura and a colleague in a hijab testing a web application on a laptop at a pale oak desk in a warm stone-walled office.'), (1200, 1200)),
 ('Integration', 'UAE Pass &amp; Dubai Now integration', 'Sign-in, identity and government services wired the way Digital Dubai expects, on the front end your customer actually sees.', ('bi-pass-1200', 'A government customer-happiness centre in Dubai in the evening: a woman in an abaya holding her phone to a glowing self-service kiosk, a man in a kandura at a dark marble counter, a brass mashrabiya screen and deep-blue windows.'), (1200, 1200)),
 ('Data', 'PDPL-ready data flows', 'Consent, records of processing and breach paths designed into the product before the executive regulations make them a fine.', ('bi-pdpl-800', 'An Emirati man, a woman in a hijab and a man in a suit over printed system diagrams on a walnut table high in a Dubai tower, the hazy city and sea below.'), (800, 600)),
 ('Handover', 'Handover to the next vendor', 'Documentation, tokens and test evidence that let another team pick it up &mdash; a supplier requirement for most government and enterprise work.', ('bi-handover-800', 'A designer passing a bound documentation binder and a laptop across a dark table to an Emirati woman in an abaya and her colleague in the evening, a lit wall of printed screens behind, the city at dusk through the glass.'), (800, 600)),
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
d = rep(dn, '<div class="slabel">For Designers in Munich</div>', '<div class="slabel">For Designers in Dubai</div>')
d = sub1(d, r'<p class="lede dn__lede">.*?</p>',
  "<p class=\"lede dn__lede\">Two of us are already in Dubai. We're looking for more: senior designers and design leads who can sit across the table &mdash; run discovery, present the work, own the relationship &mdash; and Arabic-speaking designers who can make the Arabic side of a product as good as the English. Paid a day rate for your time, ten percent of what you bring in. No exclusivity. Three ways in.</p>")
d = sub1(d, r'<picture>.*?</picture>', pic('network-studio-1600', 1600, 700, 'Young designers of mixed backgrounds in a bright converted-warehouse studio in Dubai&rsquo;s design district: one walking through with a laptop, others at a wall of sticky notes and along a long oak table; sunlit sand-coloured buildings and palms through the glass.'))
steps = [('Lead a project', 'Discovery, workshops and presentations, in the room, in Dubai. Day rate agreed before you start.'),
         ('Bring work in', 'Introduce a company. We scope, price and close; you lead it, and take 10% of the fee.'),
         ('Localise it', 'Arabic typography, RTL layout and copy for the products we build. Paid per project, credited by name.')]
st = re.findall(r'(<h3 class="sh sh--step">.*?</h3>\s*<p class="dn__step-b">.*?</p>)', d, re.S)
assert len(st) == 3
for old, (h, p) in zip(st, steps):
    d = d.replace(old, f'<h3 class="sh sh--step">{h}</h3>\n          <p class="dn__step-b">{p}</p>', 1)
b = b.replace(dn, d, 1)

# ── where we work: Dubai is here, Munich becomes a link ──
b = rep(b, '<span class="mk__pin mk__pin--flip" style="--x:61.52%;--y:52.06%;--d:1.2s" data-tz="Asia/Dubai"><span class="mk__dot" aria-hidden="true"></span><span class="mk__pin-label">Dubai</span></span>',
           '<span class="mk__pin mk__pin--live mk__pin--here mk__pin--flip" style="--x:61.52%;--y:52.06%;--d:1.2s" data-tz="Asia/Dubai"><span class="mk__dot" aria-hidden="true"></span><span class="mk__pin-label">Dubai</span></span>')
b = rep(b, '<span class="mk__pin mk__pin--live mk__pin--here" style="--x:48.33%;--y:37.98%;--d:1.8s" data-tz="Europe/Berlin"><span class="mk__dot" aria-hidden="true"></span><span class="mk__pin-label">Munich</span></span>',
           '<a class="mk__pin mk__pin--live" style="--x:48.33%;--y:37.98%;--d:1.8s" href="/munich/" data-tz="Europe/Berlin"><span class="mk__dot" aria-hidden="true"></span><span class="mk__pin-label">Munich <span aria-hidden="true">&rarr;</span></span></a>')
b = rep(b, '''            <li class="mk__row">
              <span class="mk__cell">
                <span class="mk__name">Dubai</span>
                <span class="mk__meta"><span class="mk__time" data-tz="Asia/Dubai">--:--</span><span class="mk__soon">Soon</span></span>
              </span>
            </li>''', '''            <li class="mk__row mk__row--live mk__row--here">
              <span class="mk__cell">
                <span class="mk__name">Dubai</span>
                <span class="mk__meta"><span class="mk__time" data-tz="Asia/Dubai">--:--</span><span class="mk__here">You're here</span></span>
              </span>
            </li>''')
b = rep(b, '''            <li class="mk__row mk__row--live mk__row--here">
              <span class="mk__cell">
                <span class="mk__name">Munich</span>
                <span class="mk__meta"><span class="mk__time" data-tz="Europe/Berlin">--:--</span><span class="mk__here">You're here</span></span>
              </span>
            </li>''', '''            <li class="mk__row mk__row--live">
              <a class="mk__cell" href="/munich/">
                <span class="mk__name">Munich</span>
                <span class="mk__meta"><span class="mk__time" data-tz="Europe/Berlin">--:--</span><span class="mk__go">Visit <span aria-hidden="true">&rarr;</span></span></span>
              </a>
            </li>''')
b = sub1(b, r'<p class="lede mk__lede">.*?</p>',
  "<p class=\"lede mk__lede\">Bengaluru, Northeast India and Munich each have their own page &mdash; the work we've done there, the people, and how to reach us. Pick a market. Denver is next.</p>")

# ── pricing band, between Where we work and CTA ──
plans = [
 ('starter', '', 'Starter', 'Foundation', '<sup>AED</sup>50,000', 'from, per project',
  'Brand identity + single digital touchpoint. Ideal for early-stage companies that need to move fast without sacrificing quality.',
  ['Brand strategy workshop (half-day)', 'Logo mark + full identity system', 'Typography + colour token set', 'One digital touchpoint (landing page or app screen set)', 'Brand guidelines document (PDF + Figma)', 'Two rounds of revisions'],
  'Typical turnaround: 4&ndash;6 weeks. 50% upfront, 50% on delivery. Arabic scope priced on top.'),
 ('studio', ' plan--featured', 'Most popular', 'Studio', '<sup>AED</sup>120,000', 'from, per project',
  'Complete brand system, product UI, and build-ready design specifications. Our most requested engagement.',
  ['Everything in Foundation', 'Full product UI design (up to 40 screens)', 'Component library in Figma (design system)', 'Interaction &amp; motion specifications', 'Developer handoff package', 'Frontend build (React / Next.js)', 'Three rounds of revisions', 'Two weeks post-launch support'],
  'Typical turnaround: 8&ndash;12 weeks. 40% upfront, 40% at mid-point, 20% on delivery. Bilingual UI priced on top.'),
 ('custom', '', 'Enterprise', 'Custom', 'Let&rsquo;s talk', 'scoped to the engagement',
  'Multi-phase engagements, embedded design teams, and long-term partnerships. Scoped to your exact needs.',
  ['Multi-phase brand + product engagements', 'Embedded design team (2&ndash;4 designers)', 'Ongoing retainer or milestone-based billing', 'Direct access to the founding team', 'Priority scheduling &amp; response', 'White-label options available'],
  'We take on one or two custom engagements a quarter. Reach out early.'),
]
def plan_html(key, mod, tag, name, price, per, desc, inc, note):
    return f'''        <article class="plan{mod}" data-plan="{key}" role="button" tabindex="0" aria-haspopup="dialog" aria-controls="plans">
          <p class="plan__tag">{tag}</p>
          <h3 class="plan__name">{name}</h3>
          <p class="plan__price">{price}<small>{per}</small></p>
          <p class="plan__desc">{desc}</p>
          <p class="plan__more">{'Start a conversation' if key == 'custom' else 'View what&rsquo;s included'} <span aria-hidden="true">&nearr;</span></p>
          <div class="plan__line" aria-hidden="true"></div>
          <span class="plan__arrow" aria-hidden="true">&nearr;</span>
        </article>
'''
def pane_html(key, mod, tag, name, price, per, desc, inc, note):
    items = ''.join(f'        <li>{c}</li>\n' for c in inc)
    cta = 'Start a conversation' if key == 'custom' else ('Start a Studio project' if key == 'studio' else 'Book a discovery call')
    return f'''    <div class="prc-pane" data-plan-pane="{key}" hidden>
      <p class="net-drawer__tag">{tag}</p>
      <h2 class="net-drawer__h">{name}</h2>
      <p class="prc-pane__price">{price}<span>{per}</span></p>
      <p class="net-drawer__sub">{desc}</p>
      <hr class="net-drawer__rule">
      <p class="net-drawer__label">What&rsquo;s included</p>
      <ul class="prc-pane__list">
{items}      </ul>
      <hr class="net-drawer__rule">
      <p class="net-drawer__note">{note}</p>
      <a class="net-drawer__btn" href="#cta">{cta} <span aria-hidden="true">&nearr;</span></a>
    </div>
'''
pricing = '''  <!-- ============================================================
       10 — PRICING
       Dubai publishes prices, so the tiers sit on the page in AED: the
       main site's euro tiers at ~4.30 AED/EUR, rounded down to the 10k
       (01-COPY.md §10, option A). Inclusions are the main site's lists.
       ============================================================ -->
  <section class="pricing invert" id="pricing" aria-labelledby="pricing-h">
    <div class="w">
      <div class="pricing__head reveal">
        <div class="slabel">Pricing</div>
        <h2 class="sh" id="pricing-h">Transparent pricing. No <em>surprises.</em></h2>
        <p class="lede pricing__lede">Dubai publishes its prices. So do we &mdash; three ways to work with us, in dirhams, with what&rsquo;s included on one page.</p>
      </div>
      <div class="pricing__plans stagger">
''' + ''.join(plan_html(*p) for p in plans) + '''      </div>
    </div>
  </section>

'''
cta_marker = '  <!-- ============================================================\n       10 — CTA'
b = rep(b, cta_marker, pricing + cta_marker.replace('10 — CTA', '11 — CTA'))
b = rep(b, '     11 — FOOTER', '     12 — FOOTER')

# ── CTA ──
b = sub1(b, r'<p class="lede cta__lede">.*?</p>',
  "<p class=\"lede cta__lede\">We start by questioning the brief. One call &mdash; or a WhatsApp thread &mdash; a lot of questions, no deck. Someone from the studio can be in a room in Dubai within the week. If we're not the right studio for it, we'll say so and point you at someone who is.</p>")
b = rep(b, '<a class="btn btn-g" href="/#pricing">See pricing</a>', '<a class="btn btn-g" href="#pricing">See pricing</a>')

# ── footer ──
b = rep(b, '<span class="footer__v">Munich &middot; Bavaria &middot; DACH</span>', '<span class="footer__v">Dubai &middot; UAE &middot; GCC</span>')

# ── drawer: Dubai variant ──
b = rep(b, '<p class="net-drawer__tag">For Designers in Munich</p>', '<p class="net-drawer__tag">For Designers in Dubai</p>')
b = rep(b, 'and a Munich lead who runs the room. That could be you.', 'and a Dubai lead who runs the room. That could be you.')
b = rep(b, 'Configurators, onboarding flows, brand systems, portals. Work you led, with a client who&rsquo;ll say so.',
           'Launch sites, booking engines, onboarding flows, brand systems. Work you led, with a client who&rsquo;ll say so.')
b = rep(b, 'When we open a Munich role, the network hears first.', 'When we open a Dubai role, the network hears first.')
b = rep(b, '09:00 in Munich is 12:30 in Bengaluru.', '09:00 in Dubai is 10:30 in Bengaluru.')
b = rep(b, '<strong>One conversation</strong><span>Thirty minutes with the founder, in German or English</span>', '<strong>One conversation</strong><span>Thirty minutes with the founder, on a call or over WhatsApp</span>')
b = rep(b, '<span class="net-chip">German-speaking</span>', '<span class="net-chip">Arabic-speaking, for localisation</span>')
b = rep(b, '<span class="net-chip">In or near Munich</span>', '<span class="net-chip">In Dubai or the Northern Emirates</span>')
b = rep(b, "We're starting with one or two leads in Munich, not a roster.", "Two of us are already in Dubai; we're adding leads and Arabic-speaking designers, not a roster.")
b = rep(b, 'placeholder="Munich, Augsburg, remote in Bavaria&hellip;"', 'placeholder="Dubai, Sharjah, Abu Dhabi&hellip;"')
b = rep(b, '<option>Design leadership</option>', '<option>Design leadership</option>\n            <option>Arabic localisation</option>')
b = rep(b, '<input type="hidden" name="market" value="Munich">', '<input type="hidden" name="market" value="Dubai">')

assert 'Munich' not in re.sub(r'<a class="mk__pin[^>]*>.*?</a>|<li class="mk__row mk__row--live">\s*<a class="mk__cell" href="/munich/">.*?</li>|mk__lede.*?</p>', '', b, flags=re.S), \
    [m.start() for m in re.finditer('Munich', b)]
assert 'German' not in b and 'BFSG' not in b and 'Bavaria' not in b

# ── plan drawer: network-drawer shell, one static pane per plan ──
plan_drawer = '''
<!-- ============================================================
     PLAN DRAWER
     Same shell as the network drawer; the pricing cards open it with the
     matching pane shown (main.js initPricing). Static so the inclusions
     are crawlable; under .no-js all three panes render inline here.
     ============================================================ -->
<div class="net-scrim" id="prc-scrim" hidden></div>
<aside class="net-drawer" id="plans" role="dialog" aria-modal="true" aria-label="Plan details" aria-hidden="true">
  <div class="net-drawer__top">
    <button class="net-drawer__close" id="prc-close" type="button" aria-label="Close">&#x2715;</button>
  </div>
  <div class="net-drawer__body">
''' + ''.join(pane_html(*p) for p in plans) + '''  </div>
</aside>
'''
b = rep(b, '<script src="main.js', plan_drawer + '\n<script src="main.js')

# ── cache-bust: Dubai has its own series ──
b = re.sub(r'\?v=\d+', '?v=2', b)

head = '''<!doctype html>
<html lang="en" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" type="image/png" href="/images/Favicon.png">
<link rel="apple-touch-icon" href="/images/Favicon.png">
<title>Parallax — Brand, Product &amp; Frontend Studio for Dubai</title>
<meta name="description" content="Parallax builds the brands and apps Dubai runs on. Brand systems, interface design and frontend engineering — one studio, from identity to shipped code. Bilingual and PDPL-ready by default.">
<!-- Pre-launch: not indexed until the page is signed off. Remove with the sitemap entry. -->
<meta name="robots" content="noindex, nofollow">
<link rel="canonical" href="https://www.parallaxorg.com/dubai/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Parallax">
<meta property="og:locale" content="en_AE">
<meta property="og:url" content="https://www.parallaxorg.com/dubai/">
<meta property="og:title" content="Parallax — Brand, Product &amp; Frontend Studio for Dubai">
<meta property="og:description" content="Parallax builds the brands and apps Dubai runs on. Brand systems, interface design and frontend engineering — one studio, from identity to shipped code.">
<meta property="og:image" content="https://www.parallaxorg.com/dubai/images/dxb-hero-poster.jpg">
<meta property="og:image:width" content="1920">
<meta property="og:image:height" content="1080">
<meta property="og:image:alt" content="Parallax — brand systems and apps for Dubai">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Parallax — Brand, Product &amp; Frontend Studio for Dubai">
<meta name="twitter:description" content="Parallax builds the brands and apps Dubai runs on. Brand systems, interface design and frontend engineering — one studio, from identity to shipped code.">
<meta name="twitter:image" content="https://www.parallaxorg.com/dubai/images/dxb-hero-poster.jpg">
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "ProfessionalService",
  "name": "Parallax",
  "url": "https://www.parallaxorg.com/dubai/",
  "logo": "https://www.parallaxorg.com/images/Favicon.png",
  "parentOrganization": { "@type": "Organization", "name": "Parallax", "url": "https://www.parallaxorg.com/" },
  "sameAs": ["https://www.parallaxorg.com/", "https://www.linkedin.com/company/parallaxorg", "https://www.instagram.com/parallaxdsign/"],
  "description": "Parallax builds the brands and apps Dubai runs on. Brand systems, interface design and frontend engineering — one studio, from identity to shipped code.",
  "email": "projects@parallaxorg.com",
  "areaServed": [{ "@type": "City", "name": "Dubai" }, { "@type": "Country", "name": "United Arab Emirates" }],
  "availableLanguage": ["en", "ar"],
  "priceRange": "AED 50,000 – 120,000+",
  "knowsAbout": ["Brand Systems","Interface Design","Frontend Engineering","Design Systems","Bilingual Arabic–English Design","Accessibility (WCAG 2.1 AA)","Digital Strategy","Motion & Interaction"]
}
</script>
<script>document.documentElement.classList.replace('no-js','js');</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,200..800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="tokens.css?v=2">
<link rel="stylesheet" href="styles.css?v=2">
</head>
'''
out = f"{ROOT}/dubai"
os.makedirs(f"{out}/images", exist_ok=True)
open(f"{out}/index.html", "w").write(head + b)
for f in ("styles.css", "tokens.css", "main.js"):
    shutil.copy(f"{ROOT}/Landing page/files/{f}", f"{out}/{f}")
shutil.copy(f"{ROOT}/munich/images/world-map.svg", f"{out}/images/world-map.svg")
print("dubai/index.html written", len(head + b) // 1024, "KB")
