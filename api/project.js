/* Server-renders a project page.

   /project.html?id=<uuid>   — client projects (existing links)
   /work/<slug>              — concept projects (vercel.json rewrite → ?slug=)

   Fills project-template.html with the real <title>/description/canonical/og,
   a CreativeWork + Breadcrumb graph, and a visually hidden copy of the page's
   text inside #app so crawlers that don't run JS (GPTBot, ClaudeBot,
   PerplexityBot) read the same words a visitor sees. The template's render
   replaces #app on load, and it picks the row up from window.__PROJECT__
   instead of fetching it again. */
const fs   = require('fs');
const path = require('path');

const SUPABASE_URL  = 'https://oveiewvqykwoliuyaiey.supabase.co';
const SUPABASE_ANON = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im92ZWlld3ZxeWt3b2xpdXlhaWV5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzc1NDMyMDIsImV4cCI6MjA5MzExOTIwMn0.Lz48hdUsqp3PX8jLGEJTc_5pVDn_gMjxEbhmpGdosbA';
const SITE = 'https://www.parallaxorg.com';

const esc   = s => (s == null ? '' : String(s)).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const plain = s => (s || '').replace(/\*([^*]+)\*/g, '$1');
const isConcept = p => /^concept-/.test(p.slug || '');

function send(res, html, status = 200) {
  res.statusCode = status;
  res.setHeader('Content-Type', 'text/html; charset=utf-8');
  res.end(html);
}

function ssrBody(p) {
  const stats = [1, 2, 3, 4, 5].map(i => [p[`stat${i}_value`], p[`stat${i}_label`]]).filter(s => s[0]);
  const outs  = [1, 2, 3, 4].map(i => [p[`outcome${i}_title`], p[`outcome${i}_description`]]).filter(o => o[0]);
  const services = Array.isArray(p.services) ? p.services.join(' · ') : (p.services || '');
  return `
    <article class="ssr-project" style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;">
      <p>${esc(p.client)}</p>
      <h1>${esc(plain(p.title))}</h1>
      <p>${esc(p.industry)} · ${esc(services)} · ${esc(p.year)}</p>
      ${p.overview ? `<h2>${esc(plain(p.overview_heading))}</h2><p>${esc(p.overview)}</p>` : ''}
      ${p.challenge_body ? `<h2>${esc(plain(p.challenge_heading))}</h2><p>${esc(p.challenge_body)}</p>` : ''}
      ${stats.length ? `<h2>${esc(plain(p.heading_stats))}</h2>${p.stats_description ? `<p>${esc(plain(p.stats_description))}</p>` : ''}<ul>${stats.map(s => `<li>${esc(s[0])} ${esc(s[1])}</li>`).join('')}</ul>` : ''}
      ${outs.length ? `<h2>${esc(plain(p.heading_outcomes))}</h2><ul>${outs.map(o => `<li>${esc(o[0])}: ${esc(o[1])}</li>`).join('')}</ul>` : ''}
    </article>`;
}

module.exports = async (req, res) => {
  const html = fs.readFileSync(path.join(process.cwd(), 'project-template.html'), 'utf8');
  const { id, slug } = req.query;
  if (!id && !slug) return send(res, html);

  try {
    const filter = slug ? `slug=eq.${encodeURIComponent(slug)}` : `id=eq.${encodeURIComponent(id)}`;
    const apiRes = await fetch(
      `${SUPABASE_URL}/rest/v1/case_studies?${filter}&status=eq.published&select=*&limit=1`,
      { headers: { apikey: SUPABASE_ANON, Authorization: `Bearer ${SUPABASE_ANON}` } }
    );
    const p = (await apiRes.json())[0];
    if (!p) return send(res, slug ? html.replace('</head>', '  <meta name="robots" content="noindex">\n</head>') : html, slug ? 404 : 200);

    const concept = isConcept(p);
    const url   = concept ? `${SITE}/work/${p.slug}` : `${SITE}/project.html?id=${encodeURIComponent(p.id)}`;
    const title = p.seo_title || `${p.client || p.title} — ${plain(p.title)} | Parallax`;
    const desc  = (p.seo_description || p.overview || 'A project by Parallax Digital Craft Studio.').replace(/\s+/g, ' ').trim().slice(0, 160);
    const image = p.img_hero || `${SITE}/images/og-default.png`;

    const head = [
      `  <title>${esc(title)}</title>`,
      `  <meta name="description" content="${esc(desc)}">`,
      `  <link rel="canonical" href="${url}">`,
      `  <meta property="og:type" content="website">`,
      `  <meta property="og:site_name" content="Parallax">`,
      `  <meta property="og:url" content="${url}">`,
      `  <meta property="og:title" content="${esc(title)}">`,
      `  <meta property="og:description" content="${esc(desc)}">`,
      `  <meta property="og:image" content="${esc(image)}">`,
      `  <meta name="twitter:card" content="summary_large_image">`,
      `  <meta name="twitter:title" content="${esc(title)}">`,
      `  <meta name="twitter:description" content="${esc(desc)}">`,
      `  <meta name="twitter:image" content="${esc(image)}">`,
    ].join('\n');

    const work = {
      '@type': 'CreativeWork', '@id': `${url}#work`, name: plain(p.title), headline: plain(p.title),
      description: desc, image: [image], url, inLanguage: 'en',
      genre: concept ? 'Concept project' : 'Case study',
      about: p.industry || undefined,
      keywords: Array.isArray(p.services) ? p.services.join(', ') : undefined,
      creator: { '@type': 'Organization', '@id': `${SITE}/#organization`, name: 'Parallax' },
      dateModified: p.updated_at || undefined,
      ...(p.market ? { spatialCoverage: { '@type': 'Place', name: p.market } } : {}),
      ...(concept ? { creativeWorkStatus: 'Concept' } : {}),
    };
    const ld = { '@context': 'https://schema.org', '@graph': [
      work,
      { '@type': 'BreadcrumbList', '@id': `${url}#breadcrumb`, itemListElement: [
        { '@type': 'ListItem', position: 1, name: 'Parallax', item: `${SITE}/` },
        { '@type': 'ListItem', position: 2, name: 'Work', item: `${SITE}/work.html` },
        { '@type': 'ListItem', position: 3, name: plain(p.title), item: url } ] },
    ] };
    const ldTag = `  <script type="application/ld+json">\n${JSON.stringify(ld, null, 1)}\n  </script>`;
    const data  = `  <script>window.__PROJECT__ = ${JSON.stringify(p).replace(/</g, '\\u003c')};</script>`;

    const out = html
      .replace(/<title>[\s\S]*?<\/title>/gi, '')
      .replace(/<meta name="description"[^>]*>/i, '')
      .replace(/<link rel="canonical"[^>]*>/gi, '')
      .replace(/<meta (?:property="og:[^"]*"|name="twitter:[^"]*")[^>]*>/gi, '')
      .replace('</head>', `${head}\n${ldTag}\n${data}\n</head>`)
      .replace(/(<div id="app">)/, `$1${ssrBody(p)}`);

    res.setHeader('Cache-Control', 'public, s-maxage=300, stale-while-revalidate=86400');
    send(res, out);
  } catch (_) {
    send(res, html);
  }
};
