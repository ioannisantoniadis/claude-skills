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
