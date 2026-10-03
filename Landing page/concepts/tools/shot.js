// node shot.js <html> <out.png> <w> <h> <scale>
const { chromium } = require('playwright');
(async () => {
  const [html, out, w, h, sc] = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: +w, height: +h }, deviceScaleFactor: +sc });
  await p.goto('file://' + html); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(400);
  await p.screenshot({ path: out }); await b.close(); console.log('shot', out);
})();
