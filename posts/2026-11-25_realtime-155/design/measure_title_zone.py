#!/usr/bin/env python3
"""realtime-152: title-zone composite contrast.
Title occupies y=56..~174 (two 56px lines, lh 1.05).
Dark cards: top gradient rgba(8,14,18,0.88)->0 over 380px.
Light cards: white gradient 0.92 at 0%, 0.55 at 55% (209px), 0 at 380px.
Composite sampled at title mid-height (y=115) and at both line centers."""
import colorsys

def lum(hexs):
    def lin(c):
        c /= 255
        return c/12.92 if c <= 0.04045 else ((c+0.055)/1.055)**2.4
    r, g, b = (int(hexs[i:i+2], 16) for i in (1, 3, 5))
    return 0.2126*lin(r) + 0.7152*lin(g) + 0.0722*lin(b)

def contrast(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la+0.05)/(lb+0.05)

def comp(fg, bg, a):
    fr, fg_, fb = (int(fg[i:i+2], 16) for i in (1, 3, 5))
    br, bg_, bb = (int(bg[i:i+2], 16) for i in (1, 3, 5))
    r = round(a*fr + (1-a)*br); g = round(a*fg_ + (1-a)*bg_); b = round(a*fb + (1-a)*bb)
    return "#%02X%02X%02X" % (r, g, b)

def dark_alpha(y): return 0.88 * (1 - y/380)
def light_alpha(y):
    if y <= 209: return 0.92 - (0.92-0.55) * (y/209)
    return 0.55 * (1 - (y-209)/171)

CARDS = {
    "WA": ("light", "#D8CDC4", "#1A44B4"),
    "WB": ("light",  "#D9E1E7", "#AA2D3B"),
    "WC": ("light", "#DBD4CD", "#1A44B4"),
    "WD": ("light",  "#C2CCD2", "#AA2D3B"),
}
for k, (kind, bg, acc) in CARDS.items():
    print(f"-- {k} ({kind}) bg {bg} accent {acc} --")
    for y in (85, 115, 145):
        a = dark_alpha(y) if kind == "dark" else light_alpha(y)
        fg = "#080E12" if kind == "dark" else "#FFFFFF"
        zone = comp(fg, bg, a)
        print(f"   y={y}: alpha={a:.2f} zone {zone} contrast {contrast(acc, zone):.1f}:1")
