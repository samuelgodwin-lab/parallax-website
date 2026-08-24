/* Contact form handler — delivers "Work With Us" enquiries to the studio inbox.
   Requires RESEND_API_KEY in the Vercel project env.
   Optional: CONTACT_TO_EMAIL, CONTACT_FROM_EMAIL. */

const TO_EMAIL   = process.env.CONTACT_TO_EMAIL   || 'projects@parallaxorg.com';
const FROM_EMAIL = process.env.CONTACT_FROM_EMAIL || 'Parallax Website <website@parallaxorg.com>';

const RE_MAIL = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

function esc(str) {
  return String(str || '')
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function clip(str, max) {
  const s = String(str || '').trim();
  return s.length > max ? s.slice(0, max) : s;
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

  const name    = clip(body.name, 120);
  const company = clip(body.company, 160);
  const email   = clip(body.email, 200);
  const service = clip(body.service, 80);
  const message = clip(body.message, 5000);

  if (!name || !RE_MAIL.test(email) || message.length < 10) {
    return res.status(400).json({ error: 'Please complete all required fields.' });
  }

  if (!process.env.RESEND_API_KEY) {
    console.error('Contact form: RESEND_API_KEY is not set — enquiry not delivered.', { name, email });
    return res.status(500).json({ error: 'Email delivery is not configured.' });
  }

  const rows = [
    ['Name', name],
    ['Company', company || '—'],
    ['Email', email],
    ['Service', service || '—'],
  ].map(([k, v]) => `<tr><td style="padding:4px 16px 4px 0;color:#666">${esc(k)}</td><td style="padding:4px 0"><strong>${esc(v)}</strong></td></tr>`).join('');

  const html =
    `<h2 style="margin:0 0 16px;font:600 18px system-ui,sans-serif">New enquiry from parallaxorg.com</h2>` +
    `<table style="font:14px system-ui,sans-serif;border-collapse:collapse">${rows}</table>` +
    `<h3 style="margin:24px 0 8px;font:600 14px system-ui,sans-serif">Project brief</h3>` +
    `<p style="font:14px/1.6 system-ui,sans-serif;white-space:pre-wrap;margin:0">${esc(message)}</p>`;

  const text =
    `New enquiry from parallaxorg.com\n\n` +
    `Name: ${name}\nCompany: ${company || '-'}\nEmail: ${email}\nService: ${service || '-'}\n\n` +
    `Project brief:\n${message}\n`;

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
        subject: `New enquiry — ${name}${company ? ` (${company})` : ''}`,
        html,
        text,
      }),
    });

    if (!send.ok) {
      const detail = await send.text();
      console.error('Contact form: Resend rejected the message.', send.status, detail);
      return res.status(502).json({ error: 'Could not send your message right now.' });
    }

    return res.status(200).json({ ok: true });
  } catch (err) {
    console.error('Contact form: send failed.', err);
    return res.status(502).json({ error: 'Could not send your message right now.' });
  }
};
