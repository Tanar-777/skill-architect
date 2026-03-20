---
name: skill-architect-multy-plan
version: 1.0.0
description: Creates a structured multi-skill suite plan from a project idea that exceeds single-skill scope. Accepts a reference file or guides the user through suite overview and per-skill breakdown. Outputs a standardized [suite-name]-plan.md consumed by skill-architect-multy-exec.
user-invocable: true
allowed-tools: [Read, Write, Glob, Grep]
---

# DESCRIPTION

`skill-architect-multy-plan` is a pure planning skill within the `skill-architect` suite. When a project is too large or complex for a single skill, this skill designs the full suite: naming each skill, defining its purpose, inputs, outputs, and dependencies, and producing a structured `[suite-name]-plan.md` file.

The plan file is the canonical artifact shared with `skill-architect-multy-exec`, which reads it to drive sequential skill generation. It is human-editable and tracks incremental progress as skills are generated.

**Three input modes:**
- **Delegated:** `skill-architect` passes pre-fill context (name candidate, idea, Step 1 notes) when it detects 3+ distinct logical units at Step 2.
- **File mode:** User provides a reference file (Markdown, text, or JSON) describing the suite.
- **Cold start:** No context — skill guides the user conversationally through suite overview and per-skill breakdown.

**This skill does not generate any skills.** Its sole output is the plan file.

# OBJECTIVES

1. Detect input mode and route to the appropriate procedure.
2. Gather: suite name, per-skill names, purposes, inputs, outputs, and dependencies.
3. Detect and resolve dependency cycles before writing.
4. Present the complete plan for user validation — allow rename, merge, split, add, remove.
5. Write the approved `[suite-name]-plan.md` with all skills at `status: pending`.

# STRICT INSTRUCTIONS

## Startup

1. Check that `~/.claude/skills/skill-architect-multy-exec/SKILL.md` exists. If missing, warn the user — the plan can still be created but execution will require manual invocation later.
2. Check that `~/.claude/skills/skill-architect-brainstorm/SKILL.md` exists. If missing, warn the user — brainstorm will be skipped.
3. Run brainstorm before proceeding (see `## Brainstorm Rule`).
4. Load `procedures/init_procedure.md`.

## Brainstorm Rule

Brainstorm **always runs** before `init_procedure.md` in `skill-architect-multy-plan` — suite scope is assumed to be complex by definition. Threshold does not apply.

- Load `~/.claude/skills/skill-architect-brainstorm/SKILL.md`.
- Pass `caller: skill-architect-multy-plan` and `mode: intent`.
- Brainstorm focuses on the suite concept: which skills are needed, how they interact, dependency risks, and architectural trade-offs across the suite.
- On return, inject the structured brainstorm summary as prefill context into `init_procedure.md`.
- If a plan file already exists (re-invocation): update the `brainstorm:` field in the plan file frontmatter to today's date.

If `skill-architect-brainstorm` is missing (warned at startup): skip this step and proceed to `init_procedure.md` directly.

## Input Mode Routing

| Condition | Procedure |
|---|---|
| `prefill` object provided (delegated from skill-architect) | `init_procedure.md` → skip suite overview in gather → `gather_procedure.md` (per-skill only) → `plan_procedure.md` |
| `reference_file` provided | `init_procedure.md` → parse file → `plan_procedure.md` |
| Neither | `init_procedure.md` → `gather_procedure.md` (full) → `plan_procedure.md` |

## Credential Scan Rule

Before reading any reference file, scan for credential patterns: `sk-`, `Bearer `, `password =`, `-----BEGIN`, `api_key`. If found:
- Warn the user with file name and approximate line number.
- Ask: "Strip these values before using? [yes / review-manually / cancel]"
  - `yes` → replace with `<REDACTED>` for internal use only (never written to plan file)
  - `review-manually` → show the lines and wait for instruction
  - `cancel` → abort

## Plan Validation Gate

Never call the Write tool until the user has explicitly approved the complete plan. During validation, the user may:
- Rename any skill
- Merge two skills into one
- Split a skill into two
- Add or remove a skill
- Reorder the generation sequence

After each revision, re-display the updated plan and ask for re-confirmation.

## Dependency Cycle Check

Before presenting the plan for approval, verify no circular dependencies exist. If a cycle is detected:
- Identify and display the cycle clearly.
- Ask the user to resolve it before proceeding.
- Do not write the plan until the graph is acyclic.

## Plan Version Rule

The initial plan is always written with `plan_version: 1.0`. If the user requests changes after the file has already been written (re-invocation with an existing plan file), increment `plan_version` by 0.1 and update `last_updated`.

## Skill Name Rules

- Lowercase, hyphens only, max 64 chars.
- Suggested format: `[suite-prefix]-[function]` (e.g. `data-pipeline-ingest`).
- Each name must be unique within the suite.
- If a skill already exists at `~/.claude/skills/[name]/`: warn the user.

## Output Path Rule

Default output path is the current working directory. If `output_path` is provided, use it. Never write to `~/.claude/skills/` — that is `exec`'s responsibility.

## Reference File Parsing Rules

- Accept: `.md`, `.txt`, `.json`
- Reject: binary files, images, executables — warn user and fall back to conversational mode.
- Extract: suite name, skill list, per-skill descriptions, dependencies.
- If fewer than 2 skills found: warn user and supplement with conversational input.
- Mark any unresolvable field as `[TO DEFINE]` and ask the user to fill it in before writing.

# AVAILABLE TOOLS

- **Read** — read reference file and existing plan files for revision
- **Write** — write the approved plan file (once, after explicit user confirmation)
- **Glob** — check for existing skills at `~/.claude/skills/` and existing plan files
- **Grep** — search reference file for structured content

# EXPECTED FORMAT (I/O)

## Input Parameters

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `reference_file` | string | no | — | Path to a reference file describing the suite |
| `output_path` | string | no | `./` | Directory where the plan file will be saved |
| `suite_name` | string | no | inferred | Override the inferred suite name |
| `prefill` | object | no | — | Context passed from skill-architect (name_candidate, idea, step1_notes) |

## Output

Single file: `[output_path]/[suite-name]-plan.md`

## Plan File Format

```
---
suite: [suite-name]
plan_version: 1.0
created: [YYYY-MM-DD]
last_updated: [YYYY-MM-DD]
brainstorm: [YYYY-MM-DD or ~]
status: approved
skills:
  - name: [suite-name]-[skill-a]
    depends_on: []
    status: pending
    generated_at: ~
    context: "[Suite context sentence.] [This specific skill's general idea sentence.]"
  - name: [suite-name]-[skill-b]
    depends_on: [[suite-name]-[skill-a]]
    status: pending
    generated_at: ~
    context: "[Suite context sentence.] [This specific skill's general idea sentence.]"
---

# Multi-Skill Suite Plan: [suite-name]

## Suite Overview
[General description of the suite's purpose, audience, and how skills collaborate]

## Skill Tree
[suite-name]
├── [suite-name]-[skill-a]     — [one-line purpose]
└── [suite-name]-[skill-b]     — [one-line purpose]

## Generation Order
1. [suite-name]-[skill-a]
2. [suite-name]-[skill-b]

## Per-Skill Breakdown

### [suite-name]-[skill-a]
- **Purpose:** ...
- **Inputs:** ...
- **Outputs:** ...
- **Dependencies:** none
- **Complexity:** simple | moderate | complex

### [suite-name]-[skill-b]
- **Purpose:** ...
- **Inputs:** ...
- **Outputs:** ...
- **Dependencies:** [suite-name]-[skill-a]
- **Complexity:** simple | moderate | complex
```

## Start

1. Run startup check (skill-architect-multy-exec presence).
2. Load `procedures/init_procedure.md`.
