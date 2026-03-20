# skill-architect-brainstorm

Pre-design brainstorm agent for the `skill-architect` suite. Facilitates a structured deep discussion of intent, scope, trade-offs, and edge cases **before** any skill design or multi-skill planning begins.

Part of the `skill-architect` suite — independently invocable.

---

## When to Use

| Situation | Use brainstorm? |
|---|---|
| You pass `-brainstorm` as an argument | Always |
| `skill-architect-update` is in `major` mode | Always |
| `skill-architect` detects 2+ major edge cases or 3+ important trade-offs | Agent offers it |
| `skill-architect-multy-plan` is invoked (any mode) | Always |
| All other cases | Never (not triggered by default) |

---

## Modes

### Intent mode
Explores what you want to achieve before any design begins. Covers purpose, scope, constraints, trade-offs, edge cases, and alternative approaches.

Called from:
- `skill-architect` (Step 0 or agent-estimated complexity)
- `skill-architect-update` (major mode — focuses on the intent of the change)
- `skill-architect-multy-plan` (always, before planning begins)

### Standalone mode
Discusses the current state of an existing skill. Reads the skill's `SKILL.md`, summarizes it, and explores gaps, limitations, and potential directions.

Triggered by: providing `skill_path` without a `caller`.

Conclusions can be passed directly to `skill-architect-update`.

---

## Usage

```
/skill-architect-brainstorm
/skill-architect-brainstorm skill_path=~/.claude/skills/my-skill
/skill-architect-brainstorm keep_file=true
```

---

## Brainstorm Protocol (6 Blocks)

| Block | Topic | Pause? |
|---|---|---|
| 1 | Intent or Current State | Yes |
| 2 | Scope & Constraints | Yes |
| 3 | Trade-offs (architectural implications) | Yes |
| 4 | Edge Cases (architectural implications) | Yes |
| 5 | Alternative Approaches | Yes |
| 6 | Summary & Conclusions | No (writes output) |

The agent writes progress to a `.md` file after each block to prevent context loss.

---

## Trigger Thresholds

- **Major trade-off:** affects data strategy, skill modularity, integration points, output format, or caller compatibility.
- **Major edge case:** could materially change the skill's architecture, data strategy, or integration points.
- **Agent-estimated trigger:** fires if 2+ major edge cases OR 3+ major trade-offs are identified at Step 1/2 of `skill-architect`.

---

## Output

| Output | Description |
|---|---|
| Inline summary | Structured context passed to the calling skill |
| `brainstorm-[skill-name]-[YYYY-MM-DD].md` | Written progressively during session; deleted at end unless `keep_file: true` |
| `brainstorm: YYYY-MM-DD` | Added to target `SKILL.md` frontmatter (or plan file) |

---

## File & Git Rules

- The result `.md` file is written to the **current working directory**.
- The file is **deleted at session end** unless the user explicitly keeps it (`keep_file: true` or confirmed via prompt).
- The result file is **never committed to git** and excluded from `skill-architect-git-upload` exports.
- The **skill itself** (`SKILL.md`, `schema.json`, etc.) is fully git-shareable (`git-shareable: true`).

---

## Parameters

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `mode` | string | no | auto-detected | `intent` or `standalone` |
| `skill_path` | string | no | — | Path to existing skill (triggers standalone mode) |
| `caller` | string | no | — | Calling skill name (triggers intent mode) |
| `keep_file` | boolean | no | false | Keep the brainstorm `.md` file after the session |

---

## Session Flag

If a `brainstorm-*.md` file already exists for the skill in the current directory, the agent will detect it and ask:
> "Resume, start fresh, or use existing output as-is? [resume / fresh / use-as-is]"

This prevents accidental re-runs within the same session.
