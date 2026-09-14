import re, os, urllib.parse
ROOT="/Users/samuelgodwin/Documents/2026/Parallax/Website Test — Copy"
src=open(f"{ROOT}/Landing page/files/index.html").read()
body=src[src.index('<body>'):]

def rep(s, old, new, n=1):
    assert s.count(old)==n, (old[:70], s.count(old))
    return s.replace(old, new)

def placeholder(key, w, h):
    svg=(f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {w} {h}'><rect width='100%' height='100%' fill='#d8dde4'/>"
         f"<text x='50%' y='50%' dominant-baseline='middle' text-anchor='middle' font-family='JetBrains Mono,monospace' "
         f"font-size='{max(w,h)//40}' letter-spacing='2' fill='#5b6470'>{key}</text></svg>")
    return "data:image/svg+xml," + urllib.parse.quote(svg)

b = body

# ── preloader ──
b = rep(b, "status.textContent = 'NORTHEAST INDIA'", "status.textContent = 'MUNICH'")
b = rep(b, "FINAL = 'NORTHEAST INDIA'", "FINAL = 'MUNICH'")

# ── nav ──
b = rep(b, '<span class="nav__label">Northeast India</span>', '<span class="nav__label">Munich</span>')

# ── hero ──
hero_media_old = b[b.index('      <picture>\n        <source type="image/webp" srcset="images/ne-hero-poster.webp">'):b.index('    <!-- Cursor colour-reveal')]
hero_media_new = f'''      <!-- Placeholder until Munich footage exists: slot img_muc_hero, 16:9. -->
      <img class="hero__poster" src="{placeholder('img_muc_hero · 1920×1080', 1920, 1080)}" width="1920" height="1080"
           alt="" aria-hidden="true" fetchpriority="high" decoding="async">
    </div>
'''
b = b.replace(hero_media_old, hero_media_new, 1)
b = rep(b, '<div class="slabel slabel--hero">Northeast India</div>', '<div class="slabel slabel--hero">Munich</div>')
b = rep(b, '''<h1 class="sh sh--hero" id="hero-h">We build the brands and<br>
          apps Northeast India<br>
          <em>runs</em> on.</h1>''',
'''<h1 class="sh sh--hero" id="hero-h">We build the brands and<br>
          apps Munich<br>
          <em>runs</em> on.</h1>
        <p class="hero__de" lang="de">Markensystem, Produkt-UI und Frontend &mdash; ein Studio, von der Identit&auml;t bis zum Code.</p>''')
lede_old = re.search(r'<p class="lede hero__lede">.*?</p>', b).group(0)
b = b.replace(lede_old, '<p class="lede hero__lede">Brand systems, interface design and frontend engineering &mdash; one studio, from identity to shipped code. For the startup before Series A, the Mittelstand product that was built but never designed, and the insurer whose website is now required by law to work for everyone.</p>', 1)
b = rep(b, 'mailto:projects@parallaxorg.com?subject=New%20project%20%E2%80%94%20Northeast%20India', 'mailto:projects@parallaxorg.com?subject=New%20project%20%E2%80%94%20Munich')
b = rep(b, 'href="https://www.parallaxorg.com/work.html"', 'href="/work.html"', 2)
note_old = re.search(r'<a href="#designers">Designer i[^<]*</a>', b).group(0)
b = b.replace(note_old, '<a href="#designers">Designer in Munich?</a>', 1)
b = rep(b, '<span class="hero__sn">4</span><span class="hero__sl">Studios worldwide</span>', '<span class="hero__sn">5</span><span class="hero__sl">Markets</span>')

# ── what we build lede ──
b = re.sub(r'<p class="svcs__desc">.*?</p>', '<p class="svcs__desc">Everything a product needs to leave the building, from one team &mdash; at a rate a Series-A budget can carry.</p>', b, count=1, flags=re.S)
b = rep(b, 'href="https://www.parallaxorg.com/services.html"', 'href="/services.html"')

# ── client logos: BMW first ──
logos = b[b.index('05 — CLIENT LOGOS'):b.index('06 — SECTORS BENTO')]
i = logos.index('          <!-- BMW -->'); j = logos.index('          <!-- Accenture')
bmw = logos[i:j]                       # BMW mark + its separator
assert bmw.count('logo-mark')==1 and bmw.count('logo-sep')==1
k = logos.index('          <!-- Biblica -->')
new_logos = logos[:k] + bmw + logos[k:i] + logos[j:]
b = b.replace(logos, new_logos, 1)

# ── sectors ──
sectors = [
 ('S&mdash;01 · Startups &amp; scale-ups','Shipped before the next <em>round.</em>',
  "Three and a half thousand companies started here last year. Most need a brand system, a product interface and a marketing site before Series A &mdash; and can't pay Munich agency rates for all three. We're one team for the lot.",
  ['Brand systems','Product UI','Design systems','Marketing sites'],'img_muc_s01',(1600,1067)),
 ('S&mdash;02 · Mobility &amp; industrial','Software that was built, never <em>designed.</em>',
  "Configurators, dealer portals, fleet tools, machine interfaces &mdash; the software the Mittelstand runs on was specified by engineers for engineers. We design it for the person who actually uses it, and hand back a system your own team can keep building.",
  ['Configurators','Partner &amp; fleet portals','Industrial software UI'],'img_muc_s02',(1280,1600)),
 ('S&mdash;03 · Insurance &amp; finance','Onboarding people <em>finish.</em>',
  "Europe's insurance capital sells products through flows most customers abandon. We build the onboarding, claims and advisor tools that get finished &mdash; and, since June 2025, that are accessible by law.",
  ['Onboarding &amp; claims flows','Broker portals','Advisor dashboards'],'img_muc_s03',(1600,1600)),
 ('S&mdash;04 · Real estate &amp; proptech','Inventory that sells <em>online.</em>',
  "Germany's most expensive property market still moves through PDFs and phone calls. We build the owner, tenant and management portals that replace them &mdash; the same systems we run for developers in India, built for German law and German tenants.",
  ['Inventory &amp; viewing portals','Tenant apps','Property-management UI'],'img_muc_s04',(1600,1067)),
]
sec = b[b.index('06 — SECTORS BENTO'):b.index('07 — GOVERNMENT')]
arts = re.findall(r'(<article class="sector sector--0\d reveal">.*?</article>)', sec, re.S)
assert len(arts)==4
new_sec = sec
for art,(lab,h3,bod,tags,key,(w,h)) in zip(arts,sectors):
    a = art
    a = re.sub(r'<picture>.*?</picture>', f'<img src="{placeholder(key+f" · {w}×{h}", w, h)}" width="{w}" height="{h}" alt="" loading="lazy" decoding="async">', a, flags=re.S)
    a = re.sub(r'<div class="slabel">S&mdash;0\d · [^<]*</div>', f'<div class="slabel">{lab}</div>', a)
    a = re.sub(r'<h3 class="sh sh--sub">.*?</h3>', f'<h3 class="sh sh--sub">{h3}</h3>', a, flags=re.S)
    a = re.sub(r'<p class="sector__body">.*?</p>', f'<p class="sector__body">{bod}</p>', a, flags=re.S)
    a = re.sub(r'<div class="sector__tags">.*?</div>', '<div class="sector__tags">\n'+''.join(f'              <span class="tag">{t}</span>\n' for t in tags)+'            </div>', a, flags=re.S)
    new_sec = new_sec.replace(art, a, 1)
b = b.replace(sec, new_sec, 1)

# ── government → accessibility band ──
gov = b[b.index('07 — GOVERNMENT'):b.index('08 — DESIGN HUB')]
g = gov.replace('07 — GOVERNMENT', '07 — ACCESSIBILITY (BFSG)')
g = rep(g, '<div class="slabel">Public Sector</div>', '<div class="slabel">Accessibility · <span lang="de">Barrierefreiheit</span></div>')
g = re.sub(r'<h2 class="sh" id="gov-h">.*?</h2>', '<h2 class="sh" id="gov-h">Accessible is no longer a <em>choice.</em></h2>', g, flags=re.S)
g = re.sub(r'<p class="lede gov__lede">.*?</p>',
  '<p class="lede gov__lede">Since 28 June 2025 the Barrierefreiheitsst&auml;rkungsgesetz requires every consumer website, app, shop and banking service to meet WCAG 2.1 AA. Fines run to &euro;100,000 &mdash; and a competitor can send the Abm&shy;ahnung before the regulator ever looks. We measure every page we ship against AA. We can do the same for the ones you already have.</p>\n'
  '          <p class="lede gov__lede gov__lede--de" lang="de">Seit dem 28. Juni 2025 gilt das BFSG: Websites, Apps, Shops und Banking-Dienste f&uuml;r Verbraucher m&uuml;ssen WCAG 2.1 AA erf&uuml;llen. Bu&szlig;gelder bis 100.000 &euro; &mdash; und die Abmahnung kommt oft vom Wettbewerber. Wir pr&uuml;fen jede Seite, die wir ausliefern, auf AA. Ihre bestehenden auch.</p>', g, flags=re.S)
tiles = [
 ('Audit','Accessibility audits','WCAG 2.1 AA measured page by page, with every failure specified as a fix rather than a finding.','img_muc_a01',(800,600)),
 ('Fix','Remediation','Contrast, focus, structure, forms and motion brought to AA inside your existing codebase, without a redesign.','img_muc_a02',(800,600)),
 ('System','Accessible design systems','Tokens and components that pass by default, so the next feature your team ships is compliant before anyone checks.','img_muc_a03',(1200,1200)),
 ('Handover','Compliance handover','The documentation, the Barrierefreiheitserkl&auml;rung and the test evidence a Marktüberwachung or an Abmahnung will ask for.','img_muc_a04',(1200,1200)),
 ('Documents','Accessible documents &amp; PDFs','Tagged, navigable, readable by a screen reader &mdash; the contracts, statements and brochures the law counts as part of the service.','img_muc_a05',(800,600)),
 ('Ongoing','Ongoing monitoring','Quarterly re-checks as content and code change, so you stay compliant rather than having been compliant once.','img_muc_a06',(800,600)),
]
tl = re.findall(r'(<article class="gov__tile[^"]*">.*?</article>)', g, re.S)
assert len(tl)==6, len(tl)
for art,(tag,head,desc,key,(w,h)) in zip(tl,tiles):
    a = art
    a = re.sub(r'<picture>.*?</picture>', f'<img src="{placeholder(key+f" · {w}×{h}", w, h)}" width="{w}" height="{h}" alt="" loading="lazy" decoding="async">', a, flags=re.S)
    a = re.sub(r'<p class="gov__tile-tag">.*?</p>', f'<p class="gov__tile-tag">{tag}</p>', a)
    a = re.sub(r'<h3 class="gov__tile-head">.*?</h3>', f'<h3 class="gov__tile-head">{head}</h3>', a)
    a = re.sub(r'<p class="gov__tile-desc">.*?</p>', f'<p class="gov__tile-desc">{desc}</p>', a, flags=re.S)
    g = g.replace(art, a, 1)
b = b.replace(gov, g, 1)

# ── design hub → network ──
dn = b[b.index('08 — DESIGN HUB'):b.index('09 — WHERE WE WORK')]
d = dn.replace('08 — DESIGN HUB', '08 — THE NETWORK')
d = rep(d, '<div class="slabel">For Designers in the Region</div>', '<div class="slabel">For Designers in Munich</div>')
d = re.sub(r'<h2 class="sh" id="dn-h">.*?</h2>', '<h2 class="sh" id="dn-h">Lead it here. We\'ll <em>build it.</em></h2>', d, flags=re.S)
d = re.sub(r'<p class="lede dn__lede">.*?</p>', "<p class=\"lede dn__lede\">We're looking for the first: German-speaking senior designers and design leads who can sit across the table in Munich &mdash; run discovery, present the work, own the relationship &mdash; with a studio team delivering behind them. Paid a day rate for your time, ten percent of what you bring in. No exclusivity. Three ways in.</p>", d, flags=re.S)
d = re.sub(r'<picture>.*?</picture>', f'<img src="{placeholder("img_muc_network · 1600×700", 1600, 700)}" width="1600" height="700" alt="" loading="lazy" decoding="async">', d, count=1, flags=re.S)
steps = [('Lead a project','Discovery, workshops and presentations, in German, in the room. Day rate agreed before you start.'),
         ('Bring work in','Introduce a company. We scope, price and close; you lead it, and take 10% of the fee.'),
         ('Set the standard','Portfolio reviews for the network, a presence at MCBW and Friends of Figma, published work with your name on it.')]
st = re.findall(r'(<h3 class="sh sh--step">.*?</h3>\s*<p class="dn__step-b">.*?</p>)', d, re.S)
assert len(st)==3
for old,(h,p) in zip(st,steps):
    d = d.replace(old, f'<h3 class="sh sh--step">{h}</h3>\n          <p class="dn__step-b">{p}</p>', 1)
d = rep(d, '<span class="dn__term">No joining fee</span>', '<span class="dn__term">Day rate, not commission</span>')
d = rep(d, '<span class="dn__term">Paid for work, not for leads</span>', '<span class="dn__term">10% on work you bring</span>')
b = b.replace(dn, d, 1)

# ── where we work: Munich is here, Bengaluru and NE are links ──
b = rep(b, '<span class="mk__pin" style="--x:48.33%;--y:37.98%;--d:1.8s" data-tz="Europe/Berlin"><span class="mk__dot" aria-hidden="true"></span><span class="mk__pin-label">Munich</span></span>',
           '<span class="mk__pin mk__pin--live mk__pin--here" style="--x:48.33%;--y:37.98%;--d:1.8s" data-tz="Europe/Berlin"><span class="mk__dot" aria-hidden="true"></span><span class="mk__pin-label">Munich</span></span>')
m = re.search(r'(<li class="mk__row)(">\s*<span class="mk__cell">\s*<span class="mk__name">Munich</span>\s*<span class="mk__meta"><span class="mk__time" data-tz="Europe/Berlin">--:--</span>)<span class="mk__soon">Soon</span>', b)
assert m
b = b.replace(m.group(0), m.group(1)+' mk__row--live mk__row--here'+m.group(2)+'<span class="mk__here">You\'re here</span>', 1)
b = rep(b, 'Bengaluru and Northeast India each have their own page &mdash; the work we\'ve done there, the people, and how to reach us. Pick a market. Denver, Dubai and Munich are next.',
           'Bengaluru and Northeast India each have their own page &mdash; the work we\'ve done there, the people, and how to reach us. Pick a market. Denver and Dubai are next.')

# ── CTA ──
cta_old = re.search(r'<p class="lede cta__lede">.*?</p>', b, re.S).group(0)
b = b.replace(cta_old, "<p class=\"lede cta__lede\">We start by questioning the brief. One call, a lot of questions, no deck &mdash; in English or German. If we're not the right studio for it, we'll say so and point you at someone who is.</p>", 1)
b = rep(b, '<a class="btn btn-g" href="/work.html">See the work</a>\n        </div>\n      </div>', '<a class="btn btn-g" href="/#pricing">See pricing</a>\n        </div>\n      </div>')

# ── drawer: Munich variant ──
b = rep(b, "The work you'd move for.<span>Without moving.</span>", "The studio behind you.<span>The room in front.</span>")
b = re.sub(r'<p class="net-drawer__sub">.*?</p>', '<p class="net-drawer__sub">A delivery team of designers and engineers &mdash; and a Munich lead who runs the room. That could be you.</p>', b, count=1, flags=re.S)
b = rep(b, "<div class=\"net-acc__h\">Paid properly</div>", "<div class=\"net-acc__h\">A day rate, paid on time</div>")
b = rep(b, "Rate agreed in writing before you start. Invoiced on delivery, paid within 15 days. No exposure, no &ldquo;let&rsquo;s see how it goes.&rdquo;",
           "Agreed in writing before you start. Invoiced on delivery, paid within 15 days. Your rate, not a commission.")
b = rep(b, "<div class=\"net-acc__h\">Your name on the work</div>", "<div class=\"net-acc__h\">Your name on the work</div>")
b = rep(b, "<div class=\"net-acc__h\">A senior on every deliverable</div>", "<div class=\"net-acc__h\">A full team behind you</div>")
b = rep(b, "Nothing goes to a client without a lead reviewing it with you. That&rsquo;s the fastest way anyone gets better.",
           "Brand, product and frontend, delivered by the studio while you own the relationship. You present it; we make sure it&rsquo;s worth presenting.")
b = rep(b, "<div class=\"net-acc__h\">Real products in your portfolio</div>", "<div class=\"net-acc__h\">Real products in your portfolio</div>")
b = rep(b, "Government platforms, booking engines, brand systems. Not spec work, not Dribbble shots.", "Configurators, onboarding flows, brand systems, portals. Work you led, with a client who&rsquo;ll say so.")
b = rep(b, "<div class=\"net-acc__h\">A finder&rsquo;s share when you bring work in</div>", "<div class=\"net-acc__h\">10% of what you bring in</div>")
b = rep(b, "Introduce a client, we scope and close it. You&rsquo;re on the team, and you&rsquo;re paid 10% of the project fee.",
           "Introduce a company, we scope, price and close it. You lead the project, and you&rsquo;re paid 10% of the fee on top of your days.")
b = rep(b, "When we hire, we hire from the network first.", "When we open a Munich role, the network hears first.")
b = rep(b, "<div class=\"net-acc__h\">Studio tools while you&rsquo;re on</div>", "<div class=\"net-acc__h\">Studio tools while you&rsquo;re on</div>")
b = rep(b, "Figma seats, our design system and libraries, for the length of the project.", "Figma seats, our design system and libraries, and a team in your working hours &mdash; 09:00 in Munich is 12:30 in Bengaluru.")
b = rep(b, "<strong>Show us the work</strong><span>A portfolio link and three pieces you&rsquo;d defend</span>", "<strong>Show us the work</strong><span>A portfolio link and three projects you led</span>")
b = rep(b, "<strong>One conversation</strong><span>Thirty minutes with a lead</span>", "<strong>One conversation</strong><span>Thirty minutes with the founder, in German or English</span>")
b = rep(b, "<strong>You&rsquo;re on the roster</strong><span>First project inside ninety days, or an honest why not</span>", "<strong>You&rsquo;re on the roster</strong><span>First engagement inside ninety days, or an honest why not</span>")
chips_old = re.search(r'(<p class="net-drawer__label">Who it&rsquo;s for</p>\s*<div class="net-drawer__chips">).*?(</div>)', b, re.S)
b = b.replace(chips_old.group(0), chips_old.group(1)+'\n        <span class="net-chip">Brand</span><span class="net-chip">Product</span><span class="net-chip">Design leadership</span>\n        <span class="net-chip">German-speaking</span><span class="net-chip">5+ years, or a portfolio that argues otherwise</span>\n        <span class="net-chip">In or near Munich</span>\n      '+chips_old.group(2), 1)
b = rep(b, "We add five to eight designers a quarter. Small on purpose &mdash; everyone on the roster gets work.", "We're starting with one or two leads in Munich, not a roster. Small on purpose &mdash; whoever joins first shapes how it works.")
b = rep(b, 'placeholder="Guwahati, Shillong, Imphal&hellip;"', 'placeholder="Munich, Augsburg, remote in Bavaria&hellip;"')
b = rep(b, '<option>UI / Product</option>\n            <option>Frontend</option>\n            <option>Motion</option>\n            <option>More than one</option>',
           '<option>UI / Product</option>\n            <option>Frontend</option>\n            <option>Motion</option>\n            <option>Design leadership</option>\n            <option>More than one</option>')
b = rep(b, '<label class="net-form__lbl" for="nf-note">What do you want to do more of? <span>optional</span></label>', '<label class="net-form__lbl" for="nf-note">What do you want to lead? <span>optional</span></label>')
b = rep(b, '<form class="net-form" id="net-form" action="/api/network" method="post" novalidate>', '<form class="net-form" id="net-form" action="/api/network" method="post" novalidate data-market="Munich">')

# ── cache-bust: Munich has its own series ──
b = re.sub(r'\?v=\d+', '?v=1', b)

head = '''<!doctype html>
<html lang="en" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" type="image/png" href="/images/Favicon.png">
<link rel="apple-touch-icon" href="/images/Favicon.png">
<title>Parallax — Brand, Product &amp; Frontend Studio for Munich</title>
<meta name="description" content="Parallax builds the brands and apps Munich runs on. Brand systems, interface design and frontend engineering — one studio, from identity to shipped code. BFSG-ready by default.">
<!-- Pre-launch: not indexed until the page is signed off. Remove with the sitemap entry. -->
<meta name="robots" content="noindex, nofollow">
<link rel="canonical" href="https://www.parallaxorg.com/munich/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Parallax">
<meta property="og:locale" content="en_DE">
<meta property="og:url" content="https://www.parallaxorg.com/munich/">
<meta property="og:title" content="Parallax — Brand, Product &amp; Frontend Studio for Munich">
<meta property="og:description" content="Parallax builds the brands and apps Munich runs on. Brand systems, interface design and frontend engineering — one studio, from identity to shipped code.">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Parallax — Brand, Product &amp; Frontend Studio for Munich">
<meta name="twitter:description" content="Parallax builds the brands and apps Munich runs on. Brand systems, interface design and frontend engineering — one studio, from identity to shipped code.">
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "ProfessionalService",
  "name": "Parallax",
  "url": "https://www.parallaxorg.com/munich/",
  "logo": "https://www.parallaxorg.com/images/Favicon.png",
  "parentOrganization": { "@type": "Organization", "name": "Parallax", "url": "https://www.parallaxorg.com/" },
  "sameAs": ["https://www.parallaxorg.com/", "https://www.linkedin.com/company/parallaxorg", "https://www.instagram.com/parallaxdsign/"],
  "description": "Parallax builds the brands and apps Munich runs on. Brand systems, interface design and frontend engineering — one studio, from identity to shipped code.",
  "email": "projects@parallaxorg.com",
  "areaServed": [{ "@type": "City", "name": "Munich" }, { "@type": "State", "name": "Bavaria" }],
  "availableLanguage": ["en", "de"],
  "knowsAbout": ["Brand Systems","Interface Design","Frontend Engineering","Design Systems","Accessibility (BFSG / WCAG 2.1 AA)","Digital Strategy","Motion & Interaction"]
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
os.makedirs(f"{ROOT}/munich/images", exist_ok=True)
open(f"{ROOT}/munich/index.html","w").write(head+b)
print("munich/index.html written", len(head+b)//1024, "KB")
