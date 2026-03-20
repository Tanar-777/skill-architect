---
name: skill-architect-brainstorm
description: Pre-design brainstorm agent for the skill-architect suite. Facilitates structured deep discussion of intent, scope, trade-offs, and edge cases before skill design or multi-skill planning begins. Supports intent mode (called from skill-architect or skill-architect-update major) and standalone mode (discussing an existing skill's current state).
version: 1.0.0
user-invocable: true
git-shareable: true
allowed-tools: [Read, Write, Glob, Grep]
---

# DESCRIPTION

`skill-architect-brainstorm` is a pre-design discussion agent within the `skill-architect` suite. Its role is to facilitate a structured, deep conversation about a skill project **before** any design, planning, or code generation begins.

It operates in two modes:

- **Intent mode** — explores what the user wants to achieve: purpose, scope, constraints, complexity, trade-offs, and edge cases. Called from `skill-architect` (Step 0 or agent-estimated complexity trigger) or `skill-architect-update` (major upgrade — focuses on the intent of the change, not the existing skill).
- **Standalone mode** — discusses the current state of an existing skill: what it does, gaps, limitations, and potential directions. Called directly with a `skill_path` parameter. Conclusions can be passed to `skill-architect-update`.

**Output:** a structured brainstorm summary written progressively to `brainstorm-[skill-name]-[YYYY-MM-DD].md` in the current working directory. After the session, the summary is passed as context to the calling skill. The file is deleted at session end unless the user explicitly asks to keep it.

> **Note on git sharing:** The skill itself is shareable. The `brainstorm-*.md` result file must never be committed to git or included in `skill-architect-git-upload` exports.

# OBJECTIVES

1. Identify and articulate the user's intent or the current state of a skill clearly.
2. Surface major trade-offs with consequent architectural implications (threshold: 3+ important trade-offs).
3. Identify major edge cases with consequent architectural implications (threshold: 2+ major edge cases).
4. Propose alternative approaches and critique each.
5. Produce a structured summary passable as context to `skill-architect`, `skill-architect-update`, or `skill-architect-multy-plan`.
6. Write the summary progressively to a `.md` file to prevent context loss.
7. Update the `brainstorm:` frontmatter field in the target skill's `SKILL.md` (or plan file) upon completion.

# STRICT INSTRUCTIONS

## Mode Detection

| Condition | Mode |
|---|---|
| `skill_path` provided, no `caller` | Standalone — discuss current state of the existing skill |
| `caller` provided (skill-architect / skill-architect-update / skill-architect-multy-plan) | Intent — discuss what the user wants to achieve |
| `-brainstorm` argument only, no `skill_path` | Intent — ask user for the skill idea to brainstorm |

## Session Flag Rule

At startup, check for an existing `brainstorm-*.md` file in the current working directory matching the current skill name. If found:
- Inform the user: "A brainstorm session already exists for this skill ([filename])."
- Ask: "Resume, start fresh, or use existing output as-is? [resume / fresh / use-as-is]"
- Do NOT run a new session without explicit user confirmation.

## Brainstorm Protocol

Run the following blocks in order, writing progress to the `.md` file after each block. Pause after each block for user input before continuing.

### Block 1 — Intent or Current State

**Intent mode:** Ask the user to describe what they want to achieve. What problem does this skill solve? Who uses it? What does success look like? If called from `skill-architect-update` (major), focus on: what is the intended change and why — not the existing skill's design.

**Standalone mode:** Read `[skill_path]/SKILL.md`. Summarize current purpose, scope, and behavior. Ask: "What is unclear, missing, or worth questioning about this skill?"

> **STOP — Write Block 1 output to `.md` file. Wait for user input.**

### Block 2 — Scope & Constraints

- What is explicitly in scope?
- What is explicitly out of scope?
- Are there time, token, or integration constraints?
- Dependencies on external tools, APIs, or other skills?
- What should this skill never do?

> **STOP — Write Block 2 output to `.md` file. Wait for user input.**

### Block 3 — Trade-offs

Present and discuss trade-offs with architectural implications. For each trade-off:
- Name it clearly
- Describe both sides
- State the architectural consequence of each choice
- Ask the user to choose or defer

A trade-off qualifies as **major** if it affects: data strategy, skill modularity, integration points, output format, or caller compatibility.

Flag explicitly if 3 or more major trade-offs are identified.

> **STOP — Write Block 3 output to `.md` file. Wait for user input.**

### Block 4 — Edge Cases

Enumerate potential edge cases. For each:
- Describe the scenario
- Describe the consequence if unhandled
- Propose a handling strategy

An edge case qualifies as **major** if it could materially change the skill's architecture, data strategy, or integration points.

Flag explicitly if 2 or more major edge cases are identified.

> **STOP — Write Block 4 output to `.md` file. Wait for user input.**

### Block 5 — Alternative Approaches

Propose 1–3 alternative design directions. For each:
- One-line description
- Key advantage
- Key risk or limitation

Ask: "Does any of these change your intent? [yes / no / partial]"

> **STOP — Write Block 5 output to `.md` file. Wait for user input.**

### Block 6 — Summary & Conclusions

Synthesize all findings into a structured summary using this format:

```
## Brainstorm Summary — [skill-name] — [YYYY-MM-DD]

### Intent
[1–3 sentences]

### Scope
- In scope: ...
- Out of scope: ...
- Constraints: ...

### Trade-offs (Major)
1. [name] — chosen direction: [choice]
2. ...

### Edge Cases (Major)
1. [scenario] — handling: [strategy]
2. ...

### Alternative Approaches Considered
- [approach] — rejected/deferred because: [reason]

### Conclusions & Recommendations
[Actionable summary to pass as context to the calling skill]
```

> **Write Block 6 output to `.md` file.**

## No-Findings Rule

If Block 3 yields fewer than 3 major trade-offs AND Block 4 yields fewer than 2 major edge cases:
- Do NOT write the `.md` file.
- Still update the `brainstorm:` frontmatter field if a `skill_path` is applicable.
- Inform the user: "No major trade-offs or edge cases found. Brainstorm complete — proceeding."
- Pass the brief summary as inline context to the caller.

## File Storage Rule

- Write progressively to `brainstorm-[skill-name]-[YYYY-MM-DD].md` in the current working directory — after each block, not only at the end.
- At session end, ask: "Keep the brainstorm file? [yes / no]"
  - `yes` → retain the file.
  - `no` → delete the file after passing the summary to the caller.
- The result file must never be committed to git or included in `skill-architect-git-upload` exports.

## Frontmatter Update Rule

After the session concludes (regardless of findings):
- If `skill_path` is provided: update the `brainstorm:` field in `[skill_path]/SKILL.md` frontmatter to today's date.
- If called from `skill-architect-multy-plan`: update `brainstorm:` in the plan file frontmatter.
- If no `skill_path` and pure intent mode (no existing skill yet): skip frontmatter update.

## Output Passing Rule

After the session, pass the structured summary as context to the calling skill:
- Called from `skill-architect` → inject as prefill context into Step 1.
- Called from `skill-architect-update` → inject as context into the major procedure.
- Called from `skill-architect-multy-plan` → inject as prefill context into `init_procedure.md`.
- Standalone → present conclusions and ask: "Pass these conclusions to skill-architect-update? [yes / no]"

## Security Rule

Never write API keys, tokens, passwords, or personal config paths into the brainstorm `.md` file. If the user shares credentials during the session, omit them from the file and warn: "Credential omitted from brainstorm file."

# AVAILABLE TOOLS

- **Read** — read existing `SKILL.md` in standalone mode; read existing brainstorm files on resume
- **Write** — write and update brainstorm `.md` file progressively during session; update `brainstorm:` frontmatter field
- **Glob** — detect existing brainstorm files for session flag check
- **Grep** — search existing skill files for context in standalone mode

# EXPECTED FORMAT (I/O)

## Input Parameters

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `mode` | string | no | auto-detected | `intent` or `standalone` |
| `skill_path` | string | no | — | Path to an existing skill directory (triggers standalone mode) |
| `caller` | string | no | — | Calling skill name (`skill-architect`, `skill-architect-update`, `skill-architect-multy-plan`) |
| `keep_file` | boolean | no | false | If true, do not delete brainstorm `.md` after session |

## Output

- **Inline:** structured brainstorm summary passed as context to the calling skill
- **File (if findings):** `brainstorm-[skill-name]-[YYYY-MM-DD].md` in current working directory — deleted at session end unless `keep_file: true`
- **Frontmatter:** `brainstorm: YYYY-MM-DD` updated in target `SKILL.md` or plan file

## Start

1. Detect mode from parameters.
2. Run session flag check (Glob for existing `brainstorm-*.md` files).
3. Begin Block 1.
