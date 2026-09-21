"""SEO/AEO layer for the market pages (pass 1, 21 Sep 2026).

Idempotent: strips anything it added before, then re-injects. Run after a
market's build.py (both call it), or on its own:

    python3 "Landing page/seo.py" [northeast-india|munich|dubai|denver|all]

Per market it:
  1. inserts the FAQ accordion (from that market's 04-FAQ.md) before the CTA;
  2. replaces the page's single ProfessionalService JSON-LD with a @graph —
     Organization (by @id), WebPage with dateModified, the ProfessionalService
     linked to the Organization and carrying Offers where prices are
     published, BreadcrumbList, FAQPage;
  3. bumps nothing else — cache keys for styles.css/main.js are bumped by
     hand when those files change.
Also writes /llms.txt from the same data.
"""
import re, json, sys, os, datetime, html, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://www.parallaxorg.com"
ORG_ID = f"{SITE}/#organization"
TODAY = datetime.date.today().isoformat()

MARKETS = {
  'northeast-india': dict(name='Northeast India', faq='files/04-FAQ.md', published='2026-09-12', prices=None,
                          region='Assam, Meghalaya, Manipur, Mizoram, Nagaland, Tripura, Arunachal Pradesh, Sikkim',
                          one_line='Brand systems, app design and frontend engineering for the companies and state governments of Northeast India.'),
  'munich':          dict(name='Munich', faq='munich/04-FAQ.md', published='2026-09-14', prices=('EUR', 12000, 28000),
                          one_line="Brand systems, product UI and frontend engineering for Munich's startups, mobility, insurance and property companies — WCAG 2.1 AA and BFSG-ready."),
  'dubai':           dict(name='Dubai', faq='dubai/04-FAQ.md', published='2026-09-15', prices=('AED', 50000, 120000),
                          one_line="Bilingual Arabic–English brand systems, product UI and frontend engineering for Dubai's developers, hospitality groups, fintechs and founders — PDPL-ready."),
  'denver':          dict(name='Denver', faq='denver/04-FAQ.md', published='2026-09-17', prices=('USD', 15000, 35000),
                          one_line="Brand systems, product UI and frontend engineering for Denver's startups, aerospace and outdoor brands — briefed at five, built overnight; ADA Title II and WCAG 2.1 AA by default."),
}

FAQ_START = '  <!-- ============================================================\n       FAQ (SEO/AEO)'
FAQ_END   = '  <!-- /FAQ -->\n'

def parse_faq(path):
    s = open(path).read()
    pairs = re.findall(r'^\*\*(.+?)\*\*\n(.+?)(?=\n\n|\Z)', s, re.M | re.S)
    pairs = [(q.strip(), ' '.join(a.split())) for q, a in pairs]
    assert len(pairs) == 6, (path, len(pairs))
    return pairs

def h(t):  # html-escape prose the way the pages do it
    return (t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
             .replace('—', '&mdash;').replace('’', '&rsquo;').replace('–', '&ndash;'))

def faq_html(pairs, market):
    rows = []
    for i, (q, a) in enumerate(pairs, 1):
        rows.append(f'''        <div class="faq__item">
          <span class="faq__n">{i:02d}</span>
          <div>
            <h3 class="faq__q"><button class="faq__btn" type="button" aria-expanded="false" aria-controls="faq-a{i}">{h(q)}</button></h3>
            <div class="faq__shell"><div class="faq__inner" id="faq-a{i}">
              <p class="faq__a">{h(a)}</p>
            </div></div>
          </div>
          <span class="faq__toggle" aria-hidden="true">+</span>
        </div>
''')
    return f'''{FAQ_START}
       Six questions in the market's own words, one open at a time. Copy in
       Landing page/{market["faq"]}; injected by Landing page/seo.py, which
       also emits the FAQPage schema. Edit the .md and re-run, not this.
       ============================================================ -->
  <section class="section section--surface faq" id="faq" aria-labelledby="faq-h">
    <div class="w">
      <div class="faq__wrap">
        <div class="faq__left reveal">
          <p class="slabel">Questions</p>
          <h2 class="sh" id="faq-h">Straight answers,<br>before the <em>call.</em></h2>
          <p class="faq__desc">The six things people in {h(market["name"])} ask before they write to us. If yours isn&rsquo;t here, ask it.</p>
        </div>
        <div class="faq__list stagger">
{''.join(rows)}        </div>
      </div>
    </div>
  </section>
{FAQ_END}'''

def strip(s):
    if FAQ_START in s:
        i = s.index(FAQ_START); j = s.index(FAQ_END) + len(FAQ_END)
        s = s[:i] + s[j:]
    return s

def graph(slug, m, existing, pairs):
    url = f"{SITE}/{slug}/"
    svc = dict(existing)
    svc['@id'] = f"{url}#service"
    svc.pop('@context', None)
    svc['parentOrganization'] = {"@id": ORG_ID}
    svc['mainEntityOfPage'] = {"@id": f"{url}#webpage"}
    if m['prices']:
        cur, a, b = m['prices']
        # Munich doesn't publish on its own page; its offers point at the main site's euro tiers.
        price_url = f"{url}#pricing" if slug in ('dubai', 'denver') else f"{SITE}/#pricing"
        svc['makesOffer'] = [
          {"@type": "Offer", "name": "Foundation", "description": "Brand identity plus one digital touchpoint.",
           "priceSpecification": {"@type": "PriceSpecification", "price": a, "priceCurrency": cur, "minPrice": a, "valueAddedTaxIncluded": False},
           "areaServed": svc.get('areaServed'), "url": price_url, "seller": {"@id": ORG_ID}},
          {"@type": "Offer", "name": "Studio", "description": "Complete brand system, product UI and build-ready specifications, with the frontend build.",
           "priceSpecification": {"@type": "PriceSpecification", "price": b, "priceCurrency": cur, "minPrice": b, "valueAddedTaxIncluded": False},
           "areaServed": svc.get('areaServed'), "url": price_url, "seller": {"@id": ORG_ID}},
        ]
    g = {
      "@context": "https://schema.org",
      "@graph": [
        {"@type": "Organization", "@id": ORG_ID, "name": "Parallax", "url": f"{SITE}/",
         "logo": f"{SITE}/images/Favicon.png",
         "sameAs": ["https://www.linkedin.com/company/parallaxorg", "https://www.instagram.com/parallaxdsign/"]},
        {"@type": "WebPage", "@id": f"{url}#webpage", "url": url, "name": existing.get('name', 'Parallax') + f" — {m['name']}",
         "isPartOf": {"@type": "WebSite", "@id": f"{SITE}/#website", "url": f"{SITE}/", "name": "Parallax"},
         "about": {"@id": f"{url}#service"}, "inLanguage": "en",
         "datePublished": m['published'], "dateModified": TODAY},
        svc,
        {"@type": "BreadcrumbList", "@id": f"{url}#breadcrumb", "itemListElement": [
          {"@type": "ListItem", "position": 1, "name": "Parallax", "item": f"{SITE}/"},
          {"@type": "ListItem", "position": 2, "name": m['name'], "item": url}]},
        {"@type": "FAQPage", "@id": f"{url}#faq", "mainEntity": [
          {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in pairs]},
      ]
    }
    return json.dumps(g, indent=2, ensure_ascii=False)

def inject(slug):
    m = MARKETS[slug]
    path = f"{ROOT}/{slug}/index.html"
    s = strip(open(path).read())
    pairs = parse_faq(f"{ROOT}/Landing page/{m['faq']}")
    # schema
    mm = re.search(r'<script type="application/ld\+json">\n(.*?)\n</script>', s, re.S)
    assert mm, slug
    j = json.loads(mm.group(1))
    if '@graph' in j:   # already ours: recover the service node
        j = next(n for n in j['@graph'] if n.get('@type') == 'ProfessionalService')
        for k in ('@id', 'mainEntityOfPage', 'makesOffer'): j.pop(k, None)
    s = s[:mm.start(1)] + graph(slug, m, j, pairs) + s[mm.end(1):]
    # FAQ before the CTA
    cta = re.search(r'  <!-- =+\n\s+1\d — CTA', s)
    assert cta, slug
    s = s[:cta.start()] + faq_html(pairs, m) + s[cta.start():]
    open(path, 'w').write(s)
    print(slug, 'ok —', len(pairs), 'questions')

def articles_for(name):
    """Published CMS articles tagged with the market name, for llms.txt."""
    import urllib.request, urllib.parse
    q = urllib.parse.quote('{"' + name + '"}')
    url = ("https://oveiewvqykwoliuyaiey.supabase.co/rest/v1/articles?status=eq.published&select=slug,title,excerpt"
           f"&tags=cs.{q}&order=created_at.desc")
    anon = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im92ZWlld3ZxeWt3b2xpdXlhaWV5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzc1NDMyMDIsImV4cCI6MjA5MzExOTIwMn0.Lz48hdUsqp3PX8jLGEJTc_5pVDn_gMjxEbhmpGdosbA"
    try:
        req = urllib.request.Request(url, headers={"apikey": anon, "Authorization": "Bearer " + anon})
        return json.load(urllib.request.urlopen(req, timeout=10))
    except Exception:
        return []

def llms():
    lines = ["# Parallax", "",
      "> Parallax is a brand, product and frontend design studio in Bengaluru, India, working with companies in Bengaluru, Northeast India, Munich, Dubai and Denver. One team from identity to shipped code: brand systems, interface design, frontend engineering, design systems, digital strategy, motion.",
      "", "Contact: projects@parallaxorg.com · https://www.linkedin.com/company/parallaxorg", "",
      "## Markets", ""]
    for slug, m in MARKETS.items():
      line = f"- [{m['name']}]({SITE}/{slug}/): {m['one_line']}"
      if m['prices']:
        cur, a, b = m['prices']
        line += f" Published prices: Foundation from {cur} {a:,}, Studio from {cur} {b:,}."
      lines.append(line)
    lines += ["", "## Main site", "",
      f"- [Home]({SITE}/): the studio, work and euro pricing (Foundation from EUR 12,000, Studio from EUR 28,000).",
      f"- [Services]({SITE}/services.html)", f"- [Work]({SITE}/work.html)", f"- [About]({SITE}/about.html)", f"- [Articles]({SITE}/articles.html)",
      f"- [Sitemap]({SITE}/sitemap.xml)", "",
      "## Questions each market page answers", ""]
    for slug, m in MARKETS.items():
      pairs = parse_faq(f"{ROOT}/Landing page/{m['faq']}")
      lines.append(f"### {m['name']} ({SITE}/{slug}/)")
      for q, a in pairs:
        lines.append(f"- **{q}** {a}")
      for art in articles_for(m['name']):
        t = re.sub(r'\*([^*]+)\*', r'\1', art.get('title') or '')
        lines.append(f"- Article: [{t}]({SITE}/articles/{art['slug']}) — {' '.join((art.get('excerpt') or '').split())}")
      lines.append("")
    lines += ["## Journal", "", f"All articles: {SITE}/articles.html · sitemap {SITE}/sitemap-articles.xml", ""]
    lines.append(f"Last updated {TODAY}.")
    open(f"{ROOT}/llms.txt", 'w').write('\n'.join(lines) + '\n')
    print('llms.txt ok')

if __name__ == '__main__':
    which = sys.argv[1] if len(sys.argv) > 1 else 'all'
    for slug in (MARKETS if which == 'all' else [which]):
        inject(slug)
    llms()
