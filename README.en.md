# Plain Chinese Writing

**A writing skill for AI agents that turns "obviously AI-generated" Chinese prose into plain, sequential, human-sounding statements.**

Most Chinese text written by LLMs fails on syntax rather than vocabulary. It builds tension with grammar instead of with information:

- **Withholding the answer** behind a colon: "There is only one reason it got bigger, packed more in, and got cheaper: it got hit."
- **Label sentences as paragraphs**: "Silicon Valley supports him." No action, just a verdict.
- **Dropping the subject**: "The main change of the generation lies in size and chassis." Who changed it?
- **Analyst neutrality**: "Whether the fix is adequate depends on sales." That is a research report, not a person.

Put those four together and readers can tell a machine wrote it.

## Six rules

| Rule | In one line |
|---|---|
| Sequential | Subject first, real verbs, no nominalization |
| Plain flow | One idea per paragraph, no padding, no transitions |
| Parallel comparison | Same dimensions, same units, side by side |
| First person | Only in evaluative positions, never in facts |
| No suspense | No hidden answers, no punchline fragments, no personification, no uplift |
| Admit uncertainty | "I'm not sure" reads more human than a verdict |

## Three-pass rewrite

1. **Remove suspense** — hidden answers, standalone fragments, personification, uplift.
2. **Remove nominalization** — turn "the increase of X" into "made X longer".
3. **Add first-person judgment** — replace neutral evaluation with your own reaction.

## Check your draft

```bash
python3 scripts/check.py your-article.md
```

The script reports sentence length, length variance (CV), paragraph length, nominalization density, digit density, and banned patterns. Targets are in `references/calibration.md`.

## Install

```bash
cp -R plain-chinese-writing ~/.agents/skills/plain-chinese-writing   # OpenCode
ln -s "$PWD/plain-chinese-writing" ~/.claude/skills/plain-chinese-writing  # Claude Code / Codex
```

Any agent that can read files will work. The whole skill is Markdown plus one standard-library Python script.

## What this is not

- It does not promise to beat AI detectors.
- It does not add fake personal anecdotes to sound human.
- It does not replace fact-checking.

## License

MIT
