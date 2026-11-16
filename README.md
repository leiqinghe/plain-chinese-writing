# 中文流水写作

给 AI agent 用的中文写作技能。装上之后，agent 写中文会按一套固定规则来。附一个脚本，能把稿子里几项"AI 味"指标测出来。

## 规则

| | |
|---|---|
| 正序 | 句首放做事的人或物，动词用加了、换了、砍了 |
| 流水 | 一段说一件事，不铺垫、不总结、不做过场 |
| 并列 | 对比同维度、同口径并排放 |
| 第一人称 | 只在评价的位置出现 |
| 不悬念 | 不藏答案，不让数字单独成段，不拟人，不升华 |
| 敢示弱 | 没底、犹豫、没想清楚，照实写 |

完整版在 [`references/style-rules.md`](references/style-rules.md)。

## 例子

改前：

> 变大、加料还能降价，通常只有一个原因：它被打了。

改后：

> 变大、加料还能降价，原因在销量上。星愿去年卖了 46.58 万辆，海鸥 31.1 万辆。

另外三组在 [`examples/before-after.md`](examples/before-after.md)。

## 改稿

1. 删掉冒号后给答案的句子、单独成段的数字、拟人化的动词、结尾的升华。
2. 把"……的+名词"改成"把……怎么样"。
3. 中立评价换成"我的反应"。

## 安装

```bash
cp -R plain-chinese-writing ~/.agents/skills/plain-chinese-writing          # OpenCode
ln -s "$PWD/plain-chinese-writing" ~/.claude/skills/plain-chinese-writing    # Claude Code / Codex
```

任何能读文件的 agent 都能用。Cursor 和 Copilot 把 `references/banned-patterns.md` 的内容放进 `.cursor/rules/` 或 `.github/copilot-instructions.md`。

## 体检

```bash
python3 scripts/check.py 你的稿子.md
```

```
  1668 字 / 48 句 / 24 段
  ✓ 平均句长             33.8     目标 28–36
  ✓ 句长变异系数           0.41     目标 0.4–0.5
  ✗ 长句(≥50字)占比       0.167    目标 0.08–0.16
  ✓ 名词化密度/千字         0.60     目标 0–1.0
  禁用句式: 未命中
```

支持目录和 `--json`。指标给文章正文用，文档类只看禁用句式那一栏。

## 文件

```
SKILL.md            技能入口
references/         规则、20 条禁用句式、改稿三步、实测数据
scripts/check.py    纯标准库
examples/           四份示例稿
```

## 许可

MIT
