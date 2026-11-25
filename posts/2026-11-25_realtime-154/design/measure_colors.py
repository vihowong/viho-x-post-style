#!/usr/bin/env python3
"""realtime-151 pairing check: accent HSV, dH/dV vs bg mean (120x68),
contrast vs bg mean and vs shaded title zone (top gradient 0.88 dark).
Accent candidates are the 23 unused colors from realtime-150 pairings.md."""
import colorsys

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

BG = {"WA": ("#052B40", 200.9, 0.25), "WB": ("#CAC9C7", 36.3, 0.79),
      "WC": ("#2C3F4E", 206.5, 0.31), "WD": ("#1F394D", 206.4, 0.30)}
UNUSED = ["#015267", "#017084", "#11325B", "#152674", "#1A44B4", "#2D2D2B",
          "#494136", "#5C614D", "#A8703F", "#AA2D3B", "#B45228", "#B78D77",
          "#C9A99D", "#D7CAD1", "#DAC339", "#F2F9F2", "#F4B609", "#F8D49F",
          "#F8D72B", "#F9F6E5", "#FAC75E", "#FEFDF8", "#FFC207"]

print("== unused colors HSV ==")
for c in UNUSED:
    h, s, v = hsv(c)
    print(f"{c}: H={h:6.1f} S={s:.2f} V={v:.2f} lum={lum(c):.3f}")

print("\n== chosen accents vs bg ==")
CHOSEN = {"WA": "#F9F6E5", "WB": "#152674", "WC": "#D7CAD1", "WD": "#C9A99D"}
for k, acc in CHOSEN.items():
    bghex, bh, bv = BG[k]
    h, s, v = hsv(acc)
    print(f"{k}: accent {acc} H={h:.1f} S={s:.2f} V={v:.2f} | bg H={bh} V={bv} | "
          f"dH={dh(h, bh):.1f} (>=100) dV={abs(v-bv):.2f} (>=0.30) | "
          f"contrast vs bg mean {contrast(acc, bghex):.1f}:1 (>=3.0)")

print("\n== accent hue intervals (smaller arc) ==")
accs = {k: hsv(v)[0] for k, v in CHOSEN.items()}
keys = list(accs)
for i in range(len(keys)):
    for j in range(i+1, len(keys)):
        print(f"{keys[i]}-{keys[j]}: {dh(accs[keys[i]], accs[keys[j]]):.1f} deg")

print("\n== caption #EAF2F0 vs dark bg means ==")
for k in ("WA", "WC", "WD"):
    print(f"{k}: {contrast('#EAF2F0', BG[k][0]):.1f}:1")
print(f"WB caption uses accent #152674 vs bg mean: {contrast('#152674', BG['WB'][0]):.1f}:1")
