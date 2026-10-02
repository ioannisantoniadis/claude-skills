# claude-skills

Personal collection of [Claude Code](https://claude.com/claude-code) skills and plugins —
reusable, well-scoped agent instructions for tasks that come up often enough to be worth
packaging instead of re-explaining every time.

This repo is itself a Claude Code plugin marketplace, so any skill here can be installed
directly:

```
/plugin marketplace add ioannisantoniadis/claude-skills
/plugin install <skill-name>@claude-skills
```

## Skills

| Skill | What it does |
|---|---|
| [`interview-prep-repo`](plugins/interview-prep-repo/) | Scaffolds a tailored, research-backed interview-prep repo (topics, cram brief, rehearsable prompts, real-source notes, optional runnable code) for an upcoming job interview. |
| [`algorithm-visualizer`](plugins/algorithm-visualizer/) | Adds a new algorithm to an existing Streamlit + Plotly algorithm-visualizer portfolio repo, matching its from-scratch NumPy + step-by-step visualization convention. |
| [`ai-topic-note`](plugins/ai-topic-note/) | Adds a new topic (or extends an existing one) to an existing personal AI/ML knowledge-base repo, deciding the right granularity and updating only the index files that apply. |
| [`white-paper`](plugins/white-paper/) | Turns a rough idea into a researched, well-argued white paper (verbatim seed, evidence against, structured template, review and revision). |
| [`skeptical-review`](plugins/skeptical-review/) | Referee-style critique of papers, proposals and plans: verified citations, anchored rubrics, hard fails, ranked issues, decisions for the author. |
| [`learning-repo`](plugins/learning-repo/) | Two skills sharing one rubric: `learning-repo-build` builds or upgrades a learning repo (technical book, notes, demos) from primary sources and real computation; `learning-repo-audit` scores one against the rubric and writes a severity-ranked report. |

## Structure

Each skill lives in its own plugin under `plugins/<name>/`, following Claude Code's
standard layout:

```
plugins/<name>/
├── .claude-plugin/
│   └── plugin.json          # plugin metadata
├── skills/<name>/
│   ├── SKILL.md              # frontmatter (name, description) + instructions
│   ├── references/           # detail loaded on demand, not in the main context window
│   └── assets/                # files copied into generated output, not read as instructions
└── README.md
```

`SKILL.md` stays lean (instructions an agent needs every time it triggers); anything
situational or reference-heavy lives in `references/` and gets read only when the skill's
own instructions point there. This progressive-disclosure split is what keeps a skill both
thorough and cheap to load.

## License

MIT — see [LICENSE](LICENSE).
