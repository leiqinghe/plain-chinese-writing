# 中文流水写作

**一个给 AI agent 用的中文写作技能：把"一眼是 AI 写的"稿子，改成正序、流水、有人味的陈述。**

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](./scripts/check.py)

---

## 它解决什么问题

AI 写的中文，毛病很少出在词汇，多在句法。常见四种：

**靠语法制造悬念。**
「变大、加料还能降价，通常只有一个原因：它被打了。」
答案被藏在冒号后面，读者被牵着走，却不知道走去哪。

**用标签句当段落开头。**
「硅谷支持他。」「这个价位很尴尬。」
没有动作，只有判断，读起来像小标题掉进了正文。

**丢主语，堆名词。**
「换代的主要变化在尺寸和底盘。」
谁改的？什么时候改的？句子没说。

**用中立口吻装作客观。**
「补得是否到位，要看销量。」
这不是作者在说话，是研报在说话。

这四条加在一起，就是"AI 味"。

---

## 六条规则

| 规则 | 一句话 |
|---|---|
| 正序 | 句首放施动者，动词落地 |
| 流水 | 一段一个信息单元，说完就完 |
| 并列 | 对比要同口径并排放 |
| 第一人称 | 只放评价位，不放在事实里 |
| 不悬念 | 不藏答案、不打拍子、不拟人、不升华 |
| 敢示弱 | "我心里没底"比断言更像人 |

完整规则见 [`references/style-rules.md`](references/style-rules.md)，
20 条禁用句式见 [`references/banned-patterns.md`](references/banned-patterns.md)。

---

## 改稿三步

```
一、去悬念    删揭晓结构、孤立短句、拟人化、升华
二、去名词化  把"X 的 Y"拆成"把 Y 怎么样"
三、补第一人称 中立评价换成"我的反应"
```

三遍分开过，不要混着改。混着改的结果通常是：悬念没了，句子还是没主语。

详见 [`references/rewrite-path.md`](references/rewrite-path.md)。

---

## 前后对照

**改前**

> 一台车同时做到变大、加料、降价，通常只有一个原因：它被打了。

**改后**

> 变大、加料还能降价，原因在销量上。星愿去年卖了 46.58 万辆，海鸥 31.1 万辆。

更多对照见 [`examples/before-after.md`](examples/before-after.md)。

---

## 安装

技能本体是几个 markdown 文件，任何能读文件的 agent 都能用。

```bash
git clone https://github.com/leiqinghe/plain-chinese-writing.git
```

**OpenCode**

```bash
cp -R plain-chinese-writing ~/.agents/skills/plain-chinese-writing
```

**Claude Code / Codex**

```bash
mkdir -p ~/.claude/skills
ln -s "$PWD/plain-chinese-writing" ~/.claude/skills/plain-chinese-writing
```

**Cursor / Copilot**

把 `references/banned-patterns.md` 的内容放进 `.cursor/rules/writing-style.mdc`
或 `.github/copilot-instructions.md` 即可。

> 软链的好处是只有一份真源，更新规则后所有工具同时生效。

---

## 自检脚本

```bash
python3 scripts/check.py 你的稿子.md
```

输出：

```
你的稿子.md
  1668 字 / 48 句 / 24 段
  ✓ 平均句长             33.8     目标 28–36
  ✓ 句长变异系数           0.41     目标 0.4–0.5
  ✗ 长句(≥50字)占比       0.167    目标 0.08–0.16
  ✓ 平均段长             69.5     目标 60–90
  ✓ 名词化密度/千字         0.60     目标 0–1.0
  ✓ 数字密度/千字          46.2     目标 25–90
    短句(≤8字)占比      2.1%
    短段(≤40字)占比     25.0%
  禁用句式: 未命中
```

也支持整个目录，或 `--json` 输出。

指标不是判据，是提示。数字达标但读着别扭，还是得改。

---

## 指标为什么是这几个

**句长变异系数（CV）** 是"有没有节奏"的代理量。
全是 25 字的句子，CV 约 0.35，读起来发木；全是一个短句打一个长句，CV 冲到 0.6，读起来像在表演。
实测下来 0.40–0.50 最像人说话。

**名词化密度** 是"报告腔"的代理量。
"轴距的增加"是名词，"把轴距加长"是动作。前者密了，文章就开始像文件。

**数字密度** 管的是另一个极端：全是数据、没有判断，就成了配置表朗读。

详见 [`references/calibration.md`](references/calibration.md) 的实测数据。

---

## 目录结构

```
plain-chinese-writing/
├── SKILL.md                    技能入口
├── references/
│   ├── style-rules.md          写作规则
│   ├── banned-patterns.md      20 条禁用句式
│   ├── rewrite-path.md         改稿三步
│   └── calibration.md          实测数据
├── scripts/
│   └── check.py                文稿体检（纯标准库）
└── examples/
    ├── before-after.md         前后对照
    ├── haiou.md                车型评测示例
    ├── blg.md                  赛事快讯示例
    └── ai-manju.md             行业观察示例
```

---

## 适合谁

- 用 AI 写公众号、评测、行业观察，但不想让人一眼看出来
- 想让 AI 的初稿更像"自己写的"
- 做内容审核，需要一套能落地的判断标准

## 不适合谁

- 需要绕开 AI 检测器的场景（这个项目不承诺，也不以此为目标）
- 学术论文、法律文书（有各自的体例，别用这套）
- 需要煽动情绪的宣传稿

---

## 参与

规则不是定死的。你在自己稿子里发现的、这套清单没覆盖的 AI 腔，欢迎提 PR。

提 PR 时请附一条对照：改前一句、改后一句、为什么。

详见 [`CONTRIBUTING.md`](CONTRIBUTING.md)。

## 许可

MIT
