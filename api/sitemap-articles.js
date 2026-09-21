/* /sitemap-articles.xml — every published article at its clean URL.
   sitemap.xml is a sitemap index pointing here and at sitemap-pages.xml. */
const SUPABASE_URL  = 'https://oveiewvqykwoliuyaiey.supabase.co';
const SUPABASE_ANON = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im92ZWlld3ZxeWt3b2xpdXlhaWV5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzc1NDMyMDIsImV4cCI6MjA5MzExOTIwMn0.Lz48hdUsqp3PX8jLGEJTc_5pVDn_gMjxEbhmpGdosbA';
const SITE = 'https://www.parallaxorg.com';

module.exports = async (req, res) => {
  res.setHeader('Content-Type', 'application/xml; charset=utf-8');
  res.setHeader('Cache-Control', 'public, max-age=0, s-maxage=600, stale-while-revalidate=3600');
  let rows = [];
  try {
    const r = await fetch(`${SUPABASE_URL}/rest/v1/articles?status=eq.published&select=slug,updated_at,created_at,date&order=created_at.desc`,
      { headers: { apikey: SUPABASE_ANON, Authorization: `Bearer ${SUPABASE_ANON}` } });
    rows = await r.json();
    if (!Array.isArray(rows)) rows = [];
  } catch (_) {}
  const urls = rows.filter(a => a.slug).map(a => {
    const mod = (a.updated_at || a.date || a.created_at || '').slice(0, 10);
    return `  <url>\n    <loc>${SITE}/articles/${encodeURIComponent(a.slug)}</loc>\n${mod ? `    <lastmod>${mod}</lastmod>\n` : ''}    <priority>0.7</priority>\n  </url>`;
  }).join('\n');
  res.end(`<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${urls}\n</urlset>\n`);
};
