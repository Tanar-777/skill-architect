# skill-architect-makeinto

Converts an existing file or code repository into a fully structured Claude Code skill.

## Usage

```
/skill-architect-makeinto
```

Then provide the path to your file or directory when prompted, or pass arguments directly:

```
/skill-architect-makeinto input_path="./my_script.py"
/skill-architect-makeinto input_path="./src/" mode="multi"
/skill-architect-makeinto input_path="./utils.py" skill_name="my-utils"
```

## Parameters

| Parameter | Required | Default | Description |
|---|---|---|---|
| `input_path` | yes | — | Path to file or directory |
| `mode` | no | `auto` | `auto` / `single` / `multi` |
| `skill_name` | no | inferred | Override the generated skill name |
| `output_dir` | no | `~/.claude/skills/` | Override output location |

## Modes

### Mode A — Single
Triggered when input is **1 file** or contains **1 dominant logical unit** (auto-detected, or forced with `mode=single`).

Flow:
1. Reads the file
2. Infers name, description, inputs, outputs
3. Proposes SKILL.md + schema.json + README + test stub
4. Waits for approval → writes files
5. Runs `skill-architect-proofing`

### Mode B — Multi
Triggered when input is a **directory** or contains **3+ distinct logical units** (auto-detected, or forced with `mode=multi`).

Flow:
1. Scans directory, groups files by responsibility
2. Proposes a skill tree: parent skill + N sub-skills
3. **Pauses for user verification** (rename, merge, split, reject)
4. After approval: generates parent skill, then each sub-skill sequentially
5. Runs `skill-architect-proofing` on each

### Too-Big Escalation → skill-architect-multy

When Mode B is triggered **and** scope exceeds thresholds (`file_count > 5` or `unit_count > 10`), you are offered a choice:

- **inline** — proceed with the standard interactive multi flow inside this skill
- **multy** — delegate to `skill-architect-multy-plan` (generates a plan file) + `skill-architect-multy-exec` (batch-executes it)

Requires both `skill-architect-multy-plan` and `skill-architect-multy-exec` to be installed. Falls back to inline if either is missing.

## Output Structure

### Mode A
```
~/.claude/skills/[skill-name]/
├── SKILL.md
├── schema.json
├── README.md
└── tests/
    └── test_[skill-name].py
```

### Mode B
```
~/.claude/skills/[parent]/          ← orchestrator skill
~/.claude/skills/[parent]-[unit-a]/ ← sub-skill A
~/.claude/skills/[parent]-[unit-b]/ ← sub-skill B
...
```

## Scripts

- `scripts/scan_repo.py` — walks a directory, filters non-source files, returns file metadata
- `scripts/infer_skill.py` — parses a source file, extracts functions/classes/docstrings/I/O

## File Filtering

Automatically ignored during repo scan:
- Directories: `.git`, `node_modules`, `__pycache__`, `dist`, `build`, `venv`
- Extensions: `.lock`, `.log`, `.png`, `.jpg`, `.env`, `.bin`, `.exe`, `.zip`

## Integration

Part of the `skill-architect` family. Uses:
- `skill-architect-proofing` — quality gate after each generation
- Follows the same SKILL.md structure conventions as `skill-architect`
