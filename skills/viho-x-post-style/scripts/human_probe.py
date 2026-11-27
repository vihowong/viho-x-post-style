#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""人工特征可测项探针（viho-x-post-style §16.5 第 1 步）。

只测机器能数的部分：句长分布、明显 AI 模板句式、AI 高频词、感叹与碎句计数。
它不是人工特征分本身——H2/H3/H4/H5/H9/H10 必须人逐项读原文打分（见 §16.4）。
探针 FAIL（模板命中、AI 高频词）即 §16 第 6/7 维 0 分，整条返工；WARN 只说明数字不好看，
仍须人读出声、打分表过关才交付。

用法：
    python3 scripts/human_probe.py posts.md
    python3 scripts/human_probe.py WA.md WB.md WC.md WD.md

输入：贴文 markdown，每条正文按段落分行；跳过标题行（# 开头）、project URL: 行、
空行。英文版同样测（句长按词数、模板按英文表述）。
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# 明显 AI 模板（§16 H6）：出现即 FAIL。中文“不是……而是”只算同一句内同时出现。
TEMPLATE_CN = ["首先", "其次", "最后", "综上所述", "总而言之", "值得注意的是",
               "让我们", "众所周知", "不难看出"]
TEMPLATE_EN = [r"\bnot\s+\w+\s+but\b", r"\bnot just\b", r"\bnot only\b",
               r"\bin conclusion\b", r"\bto sum up\b", r"\bit is worth noting\b"]
# AI 高频词（§16 H7）：出现即 FAIL。
AI_WORDS_CN = ["赋能", "抓手", "闭环", "至关重要", "深入探讨", "深度赋能", "打造生态"]
AI_WORDS_EN = ["crucial", "pivotal", "delve", "showcase", "landscape",
               "tapestry", "underscore", "meticulous"]

SENT_SPLIT = re.compile(r"[。！？；.!?;\n]+")


def split_sentences(text: str) -> list[str]:
    parts = [p.strip() for p in SENT_SPLIT.split(text) if p.strip()]
    # 英文按词数、中文按字数分别量；这里统一返回句子原文，长度另算
    return parts


def sent_len(s: str) -> int:
    # 含英文字母时按词数算，否则按字数算（空格不计）
    if re.search(r"[A-Za-z]", s):
        return len(s.split())
    return len(re.sub(r"\s+", "", s))


def probe_file(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8")
    lines = [l for l in raw.splitlines()
             if l.strip() and not l.strip().startswith("#")
             and not l.strip().lower().startswith("project url")]
    text = "\n".join(lines)
    sents = split_sentences(text)
    lens = [sent_len(s) for s in sents]
    fails: list[str] = []
    warns: list[str] = []
    passes: list[str] = []

    # H1 节奏：最长句 >= 3x 最短句，且有 <=10 短句与 >=25 长句
    if lens:
        lo, hi = min(lens), max(lens)
        has_short = any(n <= 10 for n in lens)
        has_long = any(n >= 25 for n in lens)
        ratio = hi / lo if lo else 0
        if ratio >= 3 and has_short and has_long:
            passes.append(f"H1 节奏：句长 {lo}–{hi}（{ratio:.1f}倍），有短句有长句")
        else:
            warns.append(f"H1 节奏偏平：句长 {lo}–{hi}（{ratio:.1f}倍），"
                         f"短句≤10：{'有' if has_short else '无'}、长句≥25：{'有' if has_long else '无'}"
                         f"（要最长≥3×最短，且短长兼备）")

    # H6 模板：中文逐词 grep；“不是……而是”只算同一句
    hits: list[str] = []
    for w in TEMPLATE_CN:
        n = text.count(w)
        if n:
            hits.append(f"{w}×{n}")
    not_but = sum(1 for s in sents if "不是" in s and "而是" in s)
    if not_but:
        hits.append(f"不是……而是×{not_but}")
    for pat in TEMPLATE_EN:
        n = len(re.findall(pat, text, flags=re.I))
        if n:
            hits.append(f"{pat}×{n}")
    if hits:
        fails.append("H6 明显 AI 模板命中：" + "、".join(hits) + "（§16 硬门，整条 FAIL）")
    else:
        passes.append("H6 无明显 AI 模板命中")

    # H7 AI 高频词
    ai_hits: list[str] = []
    for w in AI_WORDS_CN:
        if w in text:
            ai_hits.append(f"{w}×{text.count(w)}")
    for w in AI_WORDS_EN:
        n = len(re.findall(rf"\b{w}\b", text, flags=re.I))
        if n:
            ai_hits.append(f"{w}×{n}")
    if ai_hits:
        fails.append("H7 AI 高频词命中：" + "、".join(ai_hits) + "（§16 H7 0 分）")
    else:
        passes.append("H7 无 AI 高频词")

    # 参考数：感叹号、碎句（≤6 字／词的句子）、“我”出现次数——只作参考，不直接判分
    bangs = text.count("！") + text.count("!")
    frags = sum(1 for n in lens if n <= 6)
    wo = text.count("我") + len(re.findall(r"\bI\b", text))
    warns.append(f"参考：感叹号 {bangs} 个、碎句≤6共 {frags} 句、“我” {wo} 处"
                 f"（碎句、感叹、重复每批各≤2 次，见 §16.3）")
    return {"file": str(path), "fails": fails, "warns": warns, "passes": passes,
            "sentences": len(sents)}


def main() -> None:
    files = [Path(a) for a in sys.argv[1:]]
    if not files:
        print("用法：python3 scripts/human_probe.py posts.md [更多文件]")
        sys.exit(2)
    total_fail = 0
    for f in files:
        if not f.exists():
            print(f"[FAIL] 文件不存在：{f}")
            total_fail += 1
            continue
        r = probe_file(f)
        print("=" * 70)
        print(f"{r['file']}（{r['sentences']} 句）")
        for x in r["fails"]:
            print("[FAIL]", x)
        for x in r["warns"]:
            print("[WARN]", x)
        for x in r["passes"]:
            print("[PASS]", x)
        total_fail += len(r["fails"])
    print("=" * 70)
    print(f"结论：FAIL {total_fail}（FAIL>0 即 §16 第 6/7 维 0 分，返工）")
    sys.exit(1 if total_fail else 0)


if __name__ == "__main__":
    main()
