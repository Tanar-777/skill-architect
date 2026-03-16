---
name: skill-architect-makeinto
version: 1.2.0
description: Analyzes an existing file or code repository and converts it into a fully structured Claude Code skill — generating SKILL.md, schema.json, README.md, and test stubs by inferring the code's purpose, inputs, outputs, and behavior. Supports two modes: single (1 file/function → 1 skill) and multi (multiple files/functions → parent skill + sub-skills).
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent
---

# DESCRIPTION

`skill-architect-makeinto` converts existing code into a Claude Code skill. Given a file path or repository directory, it analyzes the code, infers intent, detects scope, and generates a complete, proofing-compliant skill directory following the `skill-architect` family structure.

**Two modes based on scope:**
- **Mode A — Single:** 1 file or 1 dominant logical unit → generates 1 skill directly
- **Mode B — Multi:** multiple files or 3+ distinct logical units → proposes a skill tree (parent + sub-skills), verifies with user, then generates sequentially

Reuses `skill-architect-proofing` as the quality gate after every generated skill.

# OBJECTIVES

1. Detect scope automatically (or respect user-provided mode).
2. Infer skill name, description, inputs, outputs, and behavior from source code.
3. In Mode A: generate a single compliant skill and proof it.
4. In Mode B: propose a named skill tree plan, pause for user verification, then generate parent + each sub-skill in order, proofing each.
5. Never write files before user approval.
6. Reuse `skill-architect` conventions and delegate proofing to `skill-architect-proofing`.

# STRICT INSTRUCTIONS

## Startup Checks

1. Verify `~/.claude/skills/skill-architect-proofing/SKILL.md` exists. If missing, warn the user — proofing step will be skipped.
2. Read `procedures/scope_procedure.md` to begin.

## Routing Table

| `mode` param | Action |
|---|---|
| `auto` (default) | Load `procedures/scope_procedure.md` to detect A vs B |
| `single` | Skip scope detection → load `procedures/single_procedure.md` directly |
| `multi` | Skip scope detection → load `procedures/multi_procedure.md` directly |

## Input Validation

- Resolve `input_path` to an absolute path before any operation.
- If path does not exist: stop and inform the user.
- If path is a file: treat as single-file input.
- If path is a directory: run `scripts/scan_repo.py` to enumerate relevant files.

## No-Write-Before-Approval Rule

Display all proposed file contents to the user before writing anything. Only write after explicit confirmation ("yes", "go", "proceed", or equivalent).

## Skill Name Rules

- Lowercase, hyphens only, max 64 chars.
- If `skill_name` is provided by the user: use it verbatim (after slug validation).
- If not provided: infer from file/directory name and dominant purpose.
- If `~/.claude/skills/[name]/` already exists: warn user and ask to overwrite or rename.

## Mode B — Plan-Before-Write Rule

In multi mode, always present the full skill tree plan in Markdown before generating any file. Wait for explicit user approval. User may rename, merge, split, or reject sub-skills at this stage.

## Too-Big Detection & Multy Escalation

When scope detection resolves to **Mode B (multi)** and any of the following thresholds are exceeded:

| Metric | Threshold |
|---|---|
| `file_count` | > 5 |
| `unit_count` | > 10 |
| `sub_skill_count` (proposed) | > 5 |

Offer to delegate to the `skill-architect-multy` pipeline instead of processing inline:

```
⚠️  Large scope detected: [N files / N units]
This exceeds the inline multi threshold. Two options:

  (inline)  Continue here — interactive step-by-step generation
  (multy)   Delegate to skill-architect-multy — plan-first, then batch-exec

Which approach? [inline / multy]
```

- `inline` → continue with `procedures/multi_procedure.md` as normal
- `multy` → invoke `skill-architect-multy-plan` with the analyzed input, then chain to `skill-architect-multy-exec`

**Availability check:** Before offering `multy`, verify that `~/.claude/skills/skill-architect-multy-plan/SKILL.md` AND `~/.claude/skills/skill-architect-multy-exec/SKILL.md` both exist. If either is missing: warn the user and fall back to `inline` automatically.

## File Filter List (repo scan)

Ignore: `.git/`, `node_modules/`, `__pycache__/`, `dist/`, `build/`, `venv/`, `.venv/`
Ignore extensions: `.lock`, `.log`, `.png`, `.jpg`, `.jpeg`, `.gif`, `.svg`, `.ico`, `.bin`, `.exe`, `.whl`, `.zip`, `.tar`, `.env`, `.DS_Store`

## Source Code Credential Scan

Before generating any skill file from source code, scan all source files for credential patterns (API keys, tokens, passwords, private keys, inline secrets — e.g. `sk-`, `Bearer `, `password =`, `-----BEGIN`). If found: warn the user, list the affected files and approximate line numbers, and ask:
```
⚠️  Possible credentials detected in source files:
    [file] line ~[N]: [pattern label]

Strip these values before generating? [yes / review-manually / cancel]
```
- `yes` → replace credential values with `"<REDACTED>"` placeholder in the generated skill output only (never modify the original source).
- `review-manually` → show the user the exact lines and wait for their instruction.
- `cancel` → abort generation.

Never copy credential values into generated SKILL.md, scripts, or tests.

## Proofing Delegation

After generating each skill (parent or sub-skill), invoke `skill-architect-proofing` by loading its SKILL.md and passing `skill_path` directly (Branch 1). Never reimplement proofing logic here.

## Script Execution

Run Python scripts via Bash: `python ~/.claude/skills/skill-architect-makeinto/scripts/scan_repo.py [path]`

# AVAILABLE TOOLS

- **Read** — read source files for analysis
- **Glob** — discover files in a directory, verify output structure
- **Grep** — search for function/class definitions, docstrings, imports
- **Bash** — run `scan_repo.py`, `infer_skill.py`, and delegate to `skill-architect-proofing`
- **Write** — generate skill files after user approval
- **Edit** — patch generated files if needed
- **Agent** — delegate sub-skill generation in Mode B for parallelism if approved

# EXPECTED FORMAT (I/O)

## Input Parameters

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `input_path` | string | yes | — | Path to file or directory to convert |
| `mode` | `auto`\|`single`\|`multi` | no | `auto` | Force a specific mode |
| `skill_name` | string | no | inferred | Override the inferred skill name |
| `output_dir` | string | no | `~/.claude/skills/` | Override output root directory |

## Output (Mode A — Single)

```
~/.claude/skills/[skill-name]/
├── SKILL.md
├── schema.json
├── README.md
└── tests/
    └── test_[skill-name].py
```

## Output (Mode B — Multi)

```
~/.claude/skills/[parent-name]/
├── SKILL.md
├── schema.json
├── README.md
└── tests/
    └── test_[parent-name].py

~/.claude/skills/[parent-name]-[unit-a]/
├── SKILL.md
├── schema.json
├── README.md
└── tests/
    └── test_[unit-a].py

~/.claude/skills/[parent-name]-[unit-b]/
...
```

## Start

1. Run startup checks (proofing sub-skill presence).
2. Validate `input_path`.
3. Load `procedures/scope_procedure.md` (or route directly if mode is explicit).
