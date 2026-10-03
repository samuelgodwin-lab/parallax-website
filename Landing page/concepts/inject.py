"""Inject each market's concept section into its landing page.

The section sits between the sectors bento (06) and the compliance band (07),
delimited by <!-- CONCEPT --> … <!-- /CONCEPT --> so re-running is idempotent
and survives the build.py chain (Munich → Dubai → Denver each copy the previous
page: a copied block is simply replaced with this market's own).

Copy is signed off in 01-COPY.md. The full piece lives in the CMS
(case_studies, slug concept-*) and renders at /work/<slug>.

    python3 "Landing page/concepts/inject.py"            # every live concept
    python3 "Landing page/concepts/inject.py" dubai      # one market
"""
import re, sys, html
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

CONCEPTS = {
    'dubai': dict(
        slug='concept-off-plan-dubai', img='off-plan-dubai',
        label='Concept &mdash; Off-plan real estate',
        h2='From launch to keys, <em>in one app.</em>',
        lede="Most of Dubai&rsquo;s 270,000 sales last year were off-plan: bought from a launch site, a broker&rsquo;s phone and a payment plan in a PDF, then followed for three years by email. We designed what the buyer should have instead.",
        alt="Concept screen on a laptop: live inventory for an unbranded Dubai tower, floor 24 selected, unit 2404 with its price, payment plan and a reserve button.",
        pairs=[
            ("Units chosen from a PDF floor plan", "Live inventory: pick the floor, the view, the unit"),
            ("Payment milestones in email reminders", "Every instalment, receipt and escrow payment in one schedule"),
            ("Construction progress by rumour", "Monthly site updates against the handover date"),
        ]),
    'munich': dict(
        slug='concept-insurance-munich', img='insurance-munich',
        label='Concept &mdash; Insurance',
        h2='An insurance flow people <em>finish.</em>',
        lede="Munich is Europe&rsquo;s insurance capital, and its products are still sold through forms most customers abandon. Since June 2025 those forms must also be accessible by law. We designed an onboarding and claims flow that does both.",
        alt="Concept screen on a laptop: an unbranded home-contents quote asking one question at a time, with a suggested sum insured and a live monthly price beside it.",
        pairs=[
            ("Forty fields on one page", "One question at a time, with answers filled in for you"),
            ("A policy delivered as a PDF", "The policy as a page you can read, search and share"),
            ("Claims by phone and post", "A claim filed from your phone in minutes, photos included"),
        ]),
}

def section(c):
    pairs = '\n'.join(f'''          <li class="concept__pair">
            <span class="concept__n">0{i}</span>
            <p class="concept__was"><span class="concept__k">Today</span>{was}</p>
            <p class="concept__now">{now}</p>
          </li>''' for i, (was, now) in enumerate(c['pairs'], 1))
    base = f"/images/concepts/{c['img']}"
    return f'''<!-- CONCEPT -->
  <!-- ============================================================
       06b — CONCEPT (Landing page/concepts/inject.py — don't hand-edit)
       ============================================================ -->
  <section class="section concept" aria-labelledby="concept-h">
    <div class="w">
      <div class="concept__head reveal">
        <div>
          <div class="slabel">{c['label']}</div>
          <h2 class="sh" id="concept-h">{c['h2']}</h2>
        </div>
        <div class="concept__aside">
          <p class="lede">{c['lede']}</p>
          <a class="btn btn-p" href="/work/{c['slug']}">See the concept</a>
        </div>
      </div>
      <a class="concept__media reveal" href="/work/{c['slug']}" tabindex="-1" aria-hidden="true">
        <picture>
          <source type="image/webp" srcset="{base}/desktop-2400.webp?v=2">
          <img src="{base}/desktop-2400.jpg?v=2" width="2400" height="1600" alt="{html.escape(c['alt'])}" loading="lazy" decoding="async">
        </picture>
        <span class="concept__flag">Concept</span>
      </a>
      <ul class="concept__pairs stagger">
{pairs}
      </ul>
      <p class="concept__note">An unbranded concept. Outcomes on the full page are design targets, not client results.</p>
    </div>
  </section>
  <!-- /CONCEPT -->
'''


def inject(market):
    path = ROOT / market / 'index.html'
    s = path.read_text()
    s = re.sub(r'<!-- CONCEPT -->[\s\S]*?<!-- /CONCEPT -->\n', '', s)
    band = re.search(r'  <!-- =+\n\s+07 — ', s)
    assert band, f'{market}: no 07 band anchor'
    s = s[:band.start()] + '  ' + section(CONCEPTS[market]) + '\n' + s[band.start():]
    path.write_text(s)
    print(market, 'concept ok')


if __name__ == '__main__':
    for m in (sys.argv[1:] or CONCEPTS):
        inject(m)
