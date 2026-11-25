#!/usr/bin/env python3
"""realtime-152: measure mean HSV of the 4 card backgrounds (120x68 downscale),
then check every unused accent color against each bg (dH>=100, dV>=0.30,
contrast>=3.0 vs bg mean)."""
import colorsys
from PIL import Image

def hsv(hexs):
    r, g, b = (int(hexs[i:i+2], 16)/255 for i in (1, 3, 5))
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    return h*360, s, v

def lum(hexs):
    def lin(c):
        c /= 255
        return c/12.92 if c <= 0.04045 else ((c+0.055)/1.055)**2.4
    r, g, b = (int(hexs[i:i+2], 16) for i in (1, 3, 5))
    return 0.2126*lin(r) + 0.7152*lin(g) + 0.0722*lin(b)

def contrast(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la+0.05)/(lb+0.05)

def dh(h1, h2):
    return abs(h1-h2) if abs(h1-h2) <= 180 else 360-abs(h1-h2)

def bg_mean(path):
    im = Image.open(path).convert("RGB").resize((120, 68))
    px = list(im.getdata())
    n = len(px)
    r = sum(p[0] for p in px)/n
    g = sum(p[1] for p in px)/n
    b = sum(p[2] for p in px)/n
    hexs = "#%02X%02X%02X" % (round(r), round(g), round(b))
    h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
    return hexs, h*360, s, v

BGS = {
    "WA": "../bg/media-generation-bg-wa-prompts-0-99670c8c-f612-49c5-ab47-79d89ad57a47.webp",
    "WB": "../bg/media-generation-bg-wb-teardown-0-8b476872-c043-41a6-b7af-98329022c91e.webp",
    "WC": "../bg/media-generation-bg-wc-landing-0-19ede4c6-fdc9-4119-b6d0-830c170017be.webp",
    "WD": "../bg/media-generation-bg-wd-prmerge-0-d041c94b-bea9-44b3-bdad-775fd012779e.webp",
}
# realtime-155: remaining pool after 154 = 7 colors; non-yellow 2 (#1A44B4, #AA2D3B),
# yellow 5 excluded as title colors (collide with brand-yellow tick).
UNUSED = ["#1A44B4", "#AA2D3B"]
# yellow family excluded as title colors (collide with brand-yellow tick):
# #DAC339 #F4B609 #F8D72B #FFC207 #FAC75E

print("== bg means (120x68) ==")
BG = {}
for k, p in BGS.items():
    hexs, h, s, v = bg_mean(p)
    BG[k] = (hexs, h, v)
    print(f"{k}: mean {hexs} H={h:.1f} S={s:.2f} V={v:.2f}")

print("\n== unused accents vs each bg (PASS = dH>=100 and dV>=0.30 and contrast>=3.0) ==")
for k, (bghex, bh, bv) in BG.items():
    print(f"-- {k} bg {bghex} H={bh:.1f} V={bv:.2f} --")
    for c in UNUSED:
        h, s, v = hsv(c)
        ok = dh(h, bh) >= 100 and abs(v-bv) >= 0.30 and contrast(c, bghex) >= 3.0
        print(f"  {c}: H={h:6.1f} V={v:.2f} dH={dh(h,bh):6.1f} dV={abs(v-bv):.2f} "
              f"contrast={contrast(c,bghex):5.1f}:1 {'PASS' if ok else 'fail'}")
