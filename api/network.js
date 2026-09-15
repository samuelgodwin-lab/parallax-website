/* Designer network application — the "Join the network" drawer on
   /northeast-india/. Same delivery path as api/contact.js (Resend), its own
   handler because the fields, validation and subject line are different.
   Requires RESEND_API_KEY. Optional: CONTACT_TO_EMAIL, CONTACT_FROM_EMAIL. */

const TO_EMAIL   = process.env.CONTACT_TO_EMAIL   || 'projects@parallaxorg.com';
const FROM_EMAIL = process.env.CONTACT_FROM_EMAIL || 'Parallax Website <website@parallaxorg.com>';

const RE_MAIL = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const DISCIPLINES = ['Brand', 'UI / Product', 'Frontend', 'Motion', 'Design leadership', 'More than one'];
const MARKETS = ['Northeast India', 'Munich', 'Dubai'];

function esc(str) {
  return String(str || '')
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}
function clip(str, max) {
  const s = String(str || '').trim();
  return s.length > max ? s.slice(0, max) : s;
}
/* Accept "behance.net/x" as well as a full URL; refuse anything that isn't http(s). */
function normaliseUrl(raw) {
  let s = clip(raw, 300);
  if (!s) return '';
  if (!/^https?:\/\//i.test(s)) s = 'https://' + s;
  try {
    const u = new URL(s);
    if (!/^https?:$/.test(u.protocol) || !u.hostname.includes('.')) return '';
    return u.href;
  } catch (_) { return ''; }
}

module.exports = async (req, res) => {
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return res.status(405).json({ error: 'Method not allowed.' });
  }

  let body = req.body;
  if (typeof body === 'string') {
    try { body = JSON.parse(body); } catch (_) { body = {}; }
  }
  body = body || {};

  /* Honeypot — bots fill hidden fields, humans don't. Pretend success. */
  if (clip(body.website, 200)) return res.status(200).json({ ok: true });

  const name       = clip(body.name, 120);
  const email      = clip(body.email, 200);
  const city       = clip(body.city, 120);
  const discipline = DISCIPLINES.includes(body.discipline) ? body.discipline : '';
  const portfolio  = normaliseUrl(body.portfolio);
  const note       = clip(body.note, 1000);
  const market     = MARKETS.includes(body.market) ? body.market : 'Northeast India';

  if (!name || !RE_MAIL.test(email) || !city || !discipline || !portfolio) {
    return res.status(400).json({ error: 'Please complete all required fields.' });
  }

  if (!process.env.RESEND_API_KEY) {
    console.error('Network form: RESEND_API_KEY is not set — application not delivered.', { name, email });
    return res.status(500).json({ error: 'Email delivery is not configured.' });
  }

  const rows = [
    ['Name', name],
    ['Email', email],
    ['City', city],
    ['Discipline', discipline],
    ['Portfolio', `<a href="${esc(portfolio)}">${esc(portfolio)}</a>`],
  ].map(([k, v]) => `<tr><td style="padding:4px 16px 4px 0;color:#666">${esc(k)}</td><td style="padding:4px 0"><strong>${k === 'Portfolio' ? v : esc(v)}</strong></td></tr>`).join('');

  const html =
    `<h2 style="margin:0 0 16px;font:600 18px system-ui,sans-serif">Designer network application — ${esc(market)}</h2>` +
    `<table style="font:14px system-ui,sans-serif;border-collapse:collapse">${rows}</table>` +
    (note
      ? `<h3 style="margin:24px 0 8px;font:600 14px system-ui,sans-serif">What they want to do more of</h3>` +
        `<p style="font:14px/1.6 system-ui,sans-serif;white-space:pre-wrap;margin:0">${esc(note)}</p>`
      : '');

  const text =
    `Designer network application — ${market}\n\n` +
    `Name: ${name}\nEmail: ${email}\nCity: ${city}\nDiscipline: ${discipline}\nPortfolio: ${portfolio}\n` +
    (note ? `\nWhat they want to do more of:\n${note}\n` : '');

  try {
    const send = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${process.env.RESEND_API_KEY}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        from: FROM_EMAIL,
        to: [TO_EMAIL],
        reply_to: email,
        subject: `Network application (${market}) — ${name} (${city}, ${discipline})`,
        html,
        text,
      }),
    });

    if (!send.ok) {
      const detail = await send.text();
      console.error('Network form: Resend rejected the message.', send.status, detail);
      return res.status(502).json({ error: 'Could not send your application right now.' });
    }
    return res.status(200).json({ ok: true });
  } catch (err) {
    console.error('Network form: send failed.', err);
    return res.status(502).json({ error: 'Could not send your application right now.' });
  }
};
