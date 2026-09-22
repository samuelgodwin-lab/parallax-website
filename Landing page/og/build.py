"""Share cards (og:image, 1200×630) for the market pages, on the main site's
og-default.png system: white ground, blue rule + mono slabel, the wordmark,
the page's line, a footer rule with the market list (current market in blue)
and the domain. Output: <market>/images/og-<slug>.png. Fonts from ~/Library/Fonts."""
import os, sys
from PIL import Image, ImageDraw, ImageFont
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
F = os.path.expanduser('~/Library/Fonts')
BLUE, INK, MUTE, RULE = '#006dcd', '#0a0a0a', '#3a3a3a', '#d9d9d9'
W, H = 1200, 630

CARDS = {
 'northeast-india': ('BRAND & APP DESIGN AGENCY · NORTHEAST INDIA', ['The brands and apps', 'Northeast India runs on.'], 'NORTHEAST INDIA'),
 'munich':          ('DESIGN AGENCY IN MUNICH',  ['The brands and apps', "Munich’s next companies run on."], 'MUNICH'),
 'dubai':           ('DESIGN AGENCY IN DUBAI',   ['The brands and apps', "Dubai’s next companies run on."], 'DUBAI'),
 'denver':          ('DESIGN AGENCY IN DENVER',  ['The brands and apps', "Denver’s next companies run on."], 'DENVER'),
}
MARKETS = ['BENGALURU', 'NORTHEAST INDIA', 'MUNICH', 'DUBAI', 'DENVER']

def font(name, size): return ImageFont.truetype(f'{F}/{name}', size)

def card(slug):
    label, lines, here = CARDS[slug]
    im = Image.new('RGB', (W, H), 'white'); d = ImageDraw.Draw(im)
    x = 96
    # slabel
    d.line([(x, 152), (x + 56, 152)], fill=BLUE, width=3)
    d.text((x + 76, 141), label, font=font('JetBrainsMono-Medium.ttf', 20), fill=BLUE, spacing=0)
    # wordmark
    fw = font('BricolageGrotesque-ExtraBold.ttf', 128)
    d.text((x - 6, 200), 'Parallax', font=fw, fill=INK)
    wdt = d.textlength('Parallax', font=fw)
    d.text((x - 6 + wdt, 200), '.', font=fw, fill=BLUE)
    # line
    fl = font('BricolageGrotesque-SemiBold.ttf', 40)
    y = 372
    for ln in lines:
        d.text((x, y), ln, font=fl, fill=MUTE); y += 48
    # footer
    d.line([(x, 512), (W - x, 512)], fill=RULE, width=1)
    fm = font('JetBrainsMono-Medium.ttf', 20); fx = x
    for m in MARKETS:
        d.text((fx, 546), m, font=fm, fill=(BLUE if m == here else INK))
        fx += d.textlength(m, font=fm) + 40
    dom = 'parallaxorg.com'; d.text((W - x - d.textlength(dom, font=fm), 546), dom, font=fm, fill='#8a8a8a')
    out = f'{ROOT}/{slug}/images/og-{slug}.png'
    im.save(out, optimize=True); print(out)

for s in (sys.argv[1:] or CARDS): card(s)
