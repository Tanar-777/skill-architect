# skill-architect

> 6-step protocol to design, critique, and generate a complete Claude Code skill from scratch.

## Description

`skill-architect` is a Claude Code skill that acts as an Expert Software Architect. It guides you through a structured, validated 6-step process to transform any task idea into a robust, modular, and well-structured Claude Code skill.

## Usage

```
/skill-architect
```

No arguments required. The skill idea is provided conversationally at Step 1.

## Process

| Step | Name | Description |
|------|------|-------------|
| 1 | Definition, Critique & Research | Skill idea intake, research, trade-off analysis, naming |
| 2 | Tooling & Architecture | Components, scripts, config, sub-skills |
| 3 | Storage & Data Strategy | Input/output formats, file handling |
| 4 | Skill File Structure | Folder layout and SKILL.md section outline |
| 5 | Dry Run & Logic Verification | Step-by-step simulation + script draft |
| 6 | Final Critique & Generation | Security review + file generation |

Each step ends with a mandatory pause — the agent waits for explicit user validation before continuing.

## Output

All generated skills are written to:

```
~/.claude/skills/[skill-name]/
├── SKILL.md         ← YAML frontmatter + agent instructions
├── schema.json      ← I/O parameter definitions (if needed)
├── scripts/         ← Isolated Python scripts
└── tests/           ← Unit tests
```

After Step 6, `skill-architect-proofing` is automatically invoked on the output directory.

## Rules

- All skill files are written in English.
- Generated code must be modular, independently testable, and follow single-responsibility principle.
- Step 6 output is never generated unless all previous steps are explicitly validated.
- If a skill with the same name already exists at Step 1, `skill-architect-git-load` is triggered in `check` mode before proceeding.

## Related Skills

- [`skill-architect-proofing`](../skill-architect-proofing/) — quality gate, automatically invoked after generation
- [`skill-architect-update`](../skill-architect-update/) — update and maintain existing skills
- [`skill-architect-git-load`](../skill-architect-git-load/) — load/update skills from a remote repository
- [`skill-architect-git-upload`](../skill-architect-git-upload/) — upload skills to a remote repository
