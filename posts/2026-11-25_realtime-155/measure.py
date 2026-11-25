#!/usr/bin/env python3
"""Measure realtime-154 posts.md (NEW STYLE, 2026-11-25 overhaul):
zh chars (target 130-160, never >170), en words (target 60-70),
? counts, paragraphs (golden line + question each count as one paragraph).
Extra: counts '不是' (not-X-but-Y family, max 1 per batch) and digits
(numbers appear only when the number itself is the topic point)."""
import re, sys

path = sys.argv[1] if len(sys.argv) > 1 else "posts.md"
text = open(path, encoding="utf-8").read()
text = "\n" + text  # so the first ## header splits like the rest
sections = re.split(r"\n## (W[ABCD]) · ", text)[1:]
for i in range(0, len(sections), 2):
    code = sections[i]
    body = sections[i + 1]
    body = body.split("\n- 来源：")[0]
    lines = [ln for ln in body.split("\n") if ln.strip() and not ln.strip().startswith("https://github.com/")]
    lines = lines[1:]  # drop header remainder line
    zh_lines, en_lines = [], []
    seen_en = False
    for ln in lines:
        if not seen_en and not re.search(r"[\u4e00-\u9fff]", ln):
            seen_en = True
        (en_lines if seen_en else zh_lines).append(ln)
    zh = "".join(zh_lines)
    en = " ".join(en_lines)
    print(f"{code}: zh={len(zh)} (target 130-160, max 170) | en_words={len(en.split())} (target 60-70) | "
          f"zh_paras={len(zh_lines)} | en_paras={len(en_lines)} | "
          f"zh_?={zh.count('？') + zh.count('?')} | en_?={en.count('?')} | "
          f"zh_!={zh.count('！')} | en_!={en.count('!')} | "
          f"zh_不是={zh.count('不是')} | en_not_X_but_Y={en.count(', not ')} | digits={len(re.findall(r'[0-9]', zh + en))}")
    for pat in ["★", "stars", "star ", "fork"]:
        if pat.lower() in (zh + en).lower():
            print(f"   !! contains {pat!r}")
