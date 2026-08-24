const fs   = require('fs');
const path = require('path');

const SUPABASE_URL  = 'https://oveiewvqykwoliuyaiey.supabase.co';
const SUPABASE_ANON = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im92ZWlld3ZxeWt3b2xpdXlhaWV5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzc1NDMyMDIsImV4cCI6MjA5MzExOTIwMn0.Lz48hdUsqp3PX8jLGEJTc_5pVDn_gMjxEbhmpGdosbA';

function esc(str) {
  return (str || '').replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

module.exports = async (req, res) => {
  const html = fs.readFileSync(path.join(process.cwd(), 'project-template.html'), 'utf8');
  const id   = req.query.id;

  if (!id) {
    res.setHeader('Content-Type', 'text/html; charset=utf-8');
    return res.end(html);
  }

  try {
    const apiRes = await fetch(
      `${SUPABASE_URL}/rest/v1/case_studies?id=eq.${encodeURIComponent(id)}&select=client,title,overview,img_hero&limit=1`,
      { headers: { apikey: SUPABASE_ANON, Authorization: `Bearer ${SUPABASE_ANON}` } }
    );
    const rows = await apiRes.json();
    const p    = rows[0];

    if (!p) {
      res.setHeader('Content-Type', 'text/html; charset=utf-8');
      return res.end(html);
    }

    const siteUrl     = 'https://www.parallaxorg.com';
    const pageUrl     = `${siteUrl}/project.html?id=${encodeURIComponent(id)}`;
    const titleStr    = esc(`${p.client || p.title} — ${p.title} | Parallax`);
    const descStr     = esc((p.overview || 'A project by Parallax Digital Craft Studio.').slice(0, 160));
    const imageStr    = esc(p.img_hero || '');

    const ogTags = [
      `  <title>${titleStr}</title>`,
      `  <meta property="og:type" content="website">`,
      `  <meta property="og:site_name" content="Parallax">`,
      `  <meta property="og:title" content="${titleStr}">`,
      `  <meta property="og:description" content="${descStr}">`,
      imageStr ? `  <meta property="og:image" content="${imageStr}">` : '',
      `  <link rel="canonical" href="${pageUrl}">`,
      `  <meta property="og:url" content="${pageUrl}">`,
      `  <meta name="twitter:card" content="summary_large_image">`,
      `  <meta name="twitter:title" content="${titleStr}">`,
      `  <meta name="twitter:description" content="${descStr}">`,
      imageStr ? `  <meta name="twitter:image" content="${imageStr}">` : '',
    ].filter(Boolean).join('\n');

    const modified = html
      .replace(/<title>[\s\S]*?<\/title>/gi, '')
      .replace(/<link rel="canonical"[^>]*>/gi, '')
      .replace(/<meta (?:property="og:[^"]*"|name="twitter:[^"]*")[^>]*>/gi, '')
      .replace('</head>', ogTags + '\n</head>');

    res.setHeader('Content-Type', 'text/html; charset=utf-8');
    res.end(modified);
  } catch (_) {
    res.setHeader('Content-Type', 'text/html; charset=utf-8');
    res.end(html);
  }
};
