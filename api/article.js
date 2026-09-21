/* Server-rendered article page.
   /articles/<slug>  (and the legacy /article.html?slug=…, which 301s here)
   are rewritten to this function. It reads the row from Supabase and returns
   article-template.html with the real <title>/description/canonical/og, an
   Article + BreadcrumbList JSON-LD, and the article itself already in the
   DOM — so crawlers that don't run JavaScript (GPTBot, ClaudeBot,
   PerplexityBot) see the piece, not an empty shell. The page's own script
   picks the row up from window.__ARTICLE__ instead of fetching it.
   Same pattern as api/project.js; the template is renamed so the rewrite
   fires (Vercel resolves static files before rewrites). */
const fs   = require('fs');
const path = require('path');

const SUPABASE_URL  = 'https://oveiewvqykwoliuyaiey.supabase.co';
const SUPABASE_ANON = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im92ZWlld3ZxeWt3b2xpdXlhaWV5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzc1NDMyMDIsImV4cCI6MjA5MzExOTIwMn0.Lz48hdUsqp3PX8jLGEJTc_5pVDn_gMjxEbhmpGdosbA';
const SITE = 'https://www.parallaxorg.com';
const CAT  = { brand: 'Brand Identity', interface: 'Interface Design', engineering: 'Engineering', process: 'Process', opinion: 'Opinion', compliance: 'Compliance' };

const esc = s => (s == null ? '' : String(s)).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
/* The CMS convention: *word* is the accent word in a title. */
const plain     = s => (s || '').replace(/\*([^*]+)\*/g, '$1');
const accentify = s => (s ? esc(s).replace(/\*([^*]+)\*/g, '<span class="text-accent">$1</span>') : '');
const fmtDate   = iso => (iso ? new Date(iso).toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' }) : '');
const slugId    = t => t.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');

function bodyHtml(body) {
  if (!body) return '';
  /* Quill saves HTML; the page's own mdToHtml handles the older markdown rows
     in the browser, so those are left for the client. */
  if (!/^\s*<[a-zA-Z]/.test(body)) return '';
  let html = body.replace(/\*([^*<>\n]+)\*/g, '<span class="text-accent">$1</span>');
  /* Heading ids for the TOC and deep links, as the client does. */
  html = html.replace(/<(h2|h3)(?![^>]*\bid=)([^>]*)>([\s\S]*?)<\/\1>/g, (m, tag, attrs, inner) => {
    const id = slugId(inner.replace(/<[^>]+>/g, ''));
    return id ? `<${tag} id="${id}"${attrs}>${inner}</${tag}>` : m;
  });
  return html;
}

function fill(html, a) {
  const title   = plain(a.title) || 'Article';
  const url     = `${SITE}/articles/${encodeURIComponent(a.slug)}`;
  const desc    = (a.excerpt || '').replace(/\s+/g, ' ').trim().slice(0, 160);
  const image   = a.hero_image_url || `${SITE}/images/og-default.png`;
  const cat     = CAT[a.category] || a.category || '';
  const date    = a.date || a.created_at;
  const readMin = typeof a.read_time === 'number' ? `${a.read_time} min read` : (a.read_time || '');

  const head = [
    `  <title>${esc(title)} — Parallax</title>`,
    `  <meta name="description" content="${esc(desc)}">`,
    `  <link rel="canonical" href="${url}">`,
    `  <meta property="og:type" content="article">`,
    `  <meta property="og:site_name" content="Parallax">`,
    `  <meta property="og:locale" content="en_US">`,
    `  <meta property="og:url" content="${url}">`,
    `  <meta property="og:title" content="${esc(title)}">`,
    `  <meta property="og:description" content="${esc(desc)}">`,
    `  <meta property="og:image" content="${esc(image)}">`,
    date ? `  <meta property="article:published_time" content="${esc(new Date(date).toISOString())}">` : '',
    `  <meta name="twitter:card" content="summary_large_image">`,
    `  <meta name="twitter:title" content="${esc(title)}">`,
    `  <meta name="twitter:description" content="${esc(desc)}">`,
    `  <meta name="twitter:image" content="${esc(image)}">`,
  ].filter(Boolean).join('\n');

  const ld = {
    '@context': 'https://schema.org',
    '@graph': [
      { '@type': 'Article', '@id': `${url}#article`, headline: title, description: desc, image: [image],
        datePublished: date ? new Date(date).toISOString() : undefined,
        dateModified: a.updated_at ? new Date(a.updated_at).toISOString() : undefined,
        author: a.author ? { '@type': 'Person', name: a.author } : { '@type': 'Organization', '@id': `${SITE}/#organization` },
        publisher: { '@type': 'Organization', '@id': `${SITE}/#organization`, name: 'Parallax', logo: { '@type': 'ImageObject', url: `${SITE}/images/Favicon.png` } },
        mainEntityOfPage: { '@type': 'WebPage', '@id': url },
        articleSection: cat || undefined, keywords: (a.tags || []).join(', ') || undefined, inLanguage: 'en' },
      { '@type': 'BreadcrumbList', '@id': `${url}#breadcrumb`, itemListElement: [
        { '@type': 'ListItem', position: 1, name: 'Parallax', item: `${SITE}/` },
        { '@type': 'ListItem', position: 2, name: 'Journal', item: `${SITE}/articles.html` },
        { '@type': 'ListItem', position: 3, name: title, item: url } ] },
    ],
  };
  const ldTag = `  <script type="application/ld+json">\n${JSON.stringify(ld, null, 1)}\n  </script>`;
  const data  = `  <script>window.__ARTICLE__ = ${JSON.stringify(a).replace(/</g, '\\u003c')};</script>`;

  let out = html
    .replace(/<title>[\s\S]*?<\/title>/gi, '')
    .replace(/<meta name="description"[^>]*>/i, '')
    .replace(/<link rel="canonical"[^>]*>/i, '')
    .replace(/<meta (?:property="og:[^"]*"|name="twitter:[^"]*")[^>]*>/gi, '')
    .replace('</head>', `${head}\n${ldTag}\n${data}\n</head>`);

  /* The visible article, rendered the way the page script renders it. */
  const body = bodyHtml(a.body);
  out = out
    .replace(/(<[^>]*class="[^"]*post-crumb__current[^"]*"[^>]*>)[\s\S]*?(<\/[a-z]+>)/i, `$1${accentify(a.title)}$2`)
    .replace(/(<[^>]*class="[^"]*post-cat[^"]*"[^>]*>)[\s\S]*?(<\/[a-z]+>)/i, `$1${esc(cat)}$2`)
    .replace(/(<h1[^>]*class="[^"]*post-title[^"]*"[^>]*>)[\s\S]*?(<\/h1>)/i, `$1${accentify(a.title)}$2`)
    .replace(/(<[^>]*class="[^"]*post-meta__name[^"]*"[^>]*>)[\s\S]*?(<\/[a-z]+>)/i, `$1${esc(a.author || 'Parallax Studio')}$2`)
    .replace(/(<[^>]*class="[^"]*post-meta__role[^"]*"[^>]*>)[\s\S]*?(<\/[a-z]+>)/i, `$1$2`);
  const metaItems = [`<strong>${esc(fmtDate(date))}</strong>`, `<strong>${esc(readMin)}</strong>`, esc(cat)];
  let i = 0;
  out = out.replace(/(<div class="post-meta__item">)[\s\S]*?(<\/div>)/g, (m, o, c) => (i < 3 ? `${o}${metaItems[i++]}${c}` : m));
  if (a.hero_image_url) {
    out = out.replace(/(<figure[^>]*class="[^"]*post-hero-img[^"]*"[^>]*>)[\s\S]*?(<\/figure>)/i,
      `$1<img src="${esc(a.hero_image_url)}" alt="${esc(title)}" style="width:100%;display:block;max-height:600px;object-fit:cover;">$2`);
  }
  if (body) out = out.replace(/(<article[^>]*id="post-body"[^>]*>)[\s\S]*?(<\/article>)/i, `$1\n${body}\n$2`);
  /* third breadcrumb link is the category */
  out = out.replace(/(<a href="\/articles\.html">)[^<]*(<\/a>\s*<span class="post-crumb__sep post-crumb__sep--title">)/, `$1${esc(cat)}$2`);
  if (a.tags && a.tags.length) {
    out = out.replace(/(<div class="post-tags">)[\s\S]*?(<\/div>)/,
      `$1<span class="post-tags__label">Tags</span>${a.tags.map(t => `<a href="/articles.html" class="post-tag">${esc(t)}</a>`).join('')}$2`);
  }
  return out;
}

module.exports = async (req, res) => {
  const html = fs.readFileSync(path.join(process.cwd(), 'article-template.html'), 'utf8');
  const { slug, id } = req.query;
  res.setHeader('Content-Type', 'text/html; charset=utf-8');

  /* Admin preview (?id=) keeps the client path: it reads localStorage. */
  if (!slug) {
    if (!id) res.setHeader('X-Robots-Tag', 'noindex');
    return res.end(html);
  }
  /* Legacy query URL → clean URL, permanently. */
  if ((req.url || '').startsWith('/article.html')) {
    res.statusCode = 301;
    res.setHeader('Location', `/articles/${encodeURIComponent(slug)}`);
    return res.end();
  }

  try {
    const r = await fetch(
      `${SUPABASE_URL}/rest/v1/articles?slug=eq.${encodeURIComponent(slug)}&status=eq.published&select=*&limit=1`,
      { headers: { apikey: SUPABASE_ANON, Authorization: `Bearer ${SUPABASE_ANON}` } }
    );
    const rows = await r.json();
    const a = Array.isArray(rows) ? rows[0] : null;
    if (!a) {
      res.statusCode = 404;
      res.setHeader('X-Robots-Tag', 'noindex');
      return res.end(html.replace('</head>', '  <meta name="robots" content="noindex">\n</head>'));
    }
    res.setHeader('Cache-Control', 'public, max-age=0, s-maxage=300, stale-while-revalidate=3600');
    res.end(fill(html, a));
  } catch (_) {
    res.end(html);
  }
};
