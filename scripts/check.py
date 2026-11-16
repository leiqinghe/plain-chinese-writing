#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""plain-chinese-writing: 中文文稿体检

用法:
    python3 scripts/check.py article.md
    python3 scripts/check.py articles/          # 目录下所有 md/txt
    python3 scripts/check.py article.md --json  # 机器可读

只依赖标准库，Python 3.8+。
"""

import argparse
import glob
import json
import os
import re
import statistics
import sys

CJK = r"\u4e00-\u9fff"

# 指标阈值：低于/高于都算不合格
TARGET = {
    "avg_sentence_len": (28, 36),
    "sentence_cv": (0.40, 0.50),
    "long_sentence_ratio": (0.08, 0.16),
    "avg_para_len": (60, 90),
    "noun_phrase_density": (0, 1.0),
    "digit_density": (25, 90),
}

BANNED = [
    ("揭晓结构", r"(?:只有|只)一个原因\s*[:：]|答案很简单\s*[:：]|说穿了\s*[:：]"),
    ("不是A而是B", r"不是[^。！？\n]{2,30}而是"),
    ("万能总结", r"综上所述|总的来说|由此可见|不难发现|值得(?:一提|注意)的是"),
    ("行业黑话", r"赋能|抓手|闭环|心智|生态位|护城河|底层逻辑"),
    ("抒情副词", r"令人唏嘘|不禁|竟然|偏偏|恰恰|无疑"),
    ("升华结尾", r"未来可期|拭目以待|写在最后|让我们一起"),
    ("套话过渡", r"与此同时|此外|换句话说|说白了"),
    ("感叹号", r"[！!]"),
]

SENT_END = re.compile(r"[。！？!?\n]+")


def split_sentences(text):
    parts = SENT_END.split(text)
    return [p.strip() for p in parts if len(p.strip()) >= 2]


def split_paragraphs(text):
    parts = re.split(r"\n\s*\n", text)
    return [p.strip() for p in parts if p.strip()]


def non_space_len(s):
    return len(re.sub(r"\s", "", s))


def analyze(text):
    # 去掉 markdown 标题符号和引用符号，避免污染句长
    clean = re.sub(r"^#{1,6}\s*", "", text, flags=re.M)
    clean = re.sub(r"^>\s?", "", clean, flags=re.M)
    clean = re.sub(r"`{1,3}", "", clean)

    sents = split_sentences(clean)
    paras = split_paragraphs(clean)
    total = max(non_space_len(clean), 1)

    lens = [non_space_len(s) for s in sents]
    avg_len = statistics.mean(lens) if lens else 0
    cv = (statistics.pstdev(lens) / avg_len) if avg_len else 0

    short8 = sum(1 for x in lens if x <= 8) / len(lens) if lens else 0
    long50 = sum(1 for x in lens if x >= 50) / len(lens) if lens else 0

    plens = [non_space_len(p) for p in paras]
    avg_para = statistics.mean(plens) if plens else 0
    short_para = sum(1 for x in plens if x <= 40) / len(plens) if plens else 0

    # 名词化/书面腔的近似信号
    noun_patterns = [
        r"的(?:增加|提升|优化|变化|下放|取消|实现|推进|增长|下降|调整|升级|改善|转型|布局)",
        r"[%s]{2}(?:性|化|度)的" % CJK,
        r"(?:进行|实现|开展|完成)[%s]{2}" % CJK,
        r"在[%s]{2,6}方面" % CJK,
        r"从[%s]{2,6}看" % CJK,
    ]
    noun_hits = sum(len(re.findall(p, clean)) for p in noun_patterns)

    digits = re.findall(r"\d+(?:\.\d+)?", clean)
    quotes = len(re.findall(r"[“”「」]", clean))

    hits = []
    for name, pattern in BANNED:
        found = re.findall(pattern, clean)
        if found:
            hits.append({"type": name, "count": len(found),
                         "samples": list(dict.fromkeys(found))[:3]})

    return {
        "chars": total,
        "sentences": len(sents),
        "avg_sentence_len": round(avg_len, 1),
        "sentence_cv": round(cv, 2),
        "short_sentence_ratio": round(short8, 3),
        "long_sentence_ratio": round(long50, 3),
        "paragraphs": len(paras),
        "avg_para_len": round(avg_para, 1),
        "short_para_ratio": round(short_para, 3),
        "noun_phrase_density": round(noun_hits / total * 1000, 2),
        "digit_density": round(len(digits) / total * 1000, 1),
        "quote_pairs": quotes,
        "banned": hits,
    }


def check(result):
    rows = []
    for key, (lo, hi) in TARGET.items():
        val = result[key]
        ok = lo <= val <= hi
        rows.append((key, val, lo, hi, ok))
    return rows


NAMES = {
    "avg_sentence_len": "平均句长",
    "sentence_cv": "句长变异系数",
    "long_sentence_ratio": "长句(≥50字)占比",
    "avg_para_len": "平均段长",
    "noun_phrase_density": "名词化密度/千字",
    "digit_density": "数字密度/千字",
}


def report(path, result):
    print(f"\n{path}")
    print(f"  {result['chars']} 字 / {result['sentences']} 句 / {result['paragraphs']} 段")
    for key, val, lo, hi, ok in check(result):
        mark = "✓" if ok else "✗"
        print(f"  {mark} {NAMES[key]:<16} {val:<8} 目标 {lo}–{hi}")
    print(f"    {'短句(≤8字)占比':<14} {result['short_sentence_ratio']:.1%}")
    print(f"    {'短段(≤40字)占比':<14} {result['short_para_ratio']:.1%}")
    if result["banned"]:
        print("  禁用句式:")
        for h in result["banned"]:
            print(f"    · {h['type']} ×{h['count']}  例：{h['samples'][0][:24]}")
    else:
        print("  禁用句式: 未命中")


def collect(paths):
    files = []
    for p in paths:
        if os.path.isdir(p):
            for ext in ("md", "txt"):
                files.extend(sorted(glob.glob(os.path.join(p, f"*.{ext}"))))
        else:
            files.append(p)
    return files


def main():
    ap = argparse.ArgumentParser(description="中文文稿体检")
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    files = collect(args.paths)
    if not files:
        print("没找到文件", file=sys.stderr)
        return 1

    all_results = []
    for f in files:
        with open(f, encoding="utf-8") as fh:
            result = analyze(fh.read())
        all_results.append({"file": f, **result})
        if not args.json:
            report(f, result)

    if args.json:
        print(json.dumps(all_results, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
