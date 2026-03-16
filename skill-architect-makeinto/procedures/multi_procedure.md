# Multi Procedure — skill-architect-makeinto (Mode B)

Generates a parent skill + N sub-skills from multiple files or multiple logical units.

## Step 1 — Analyze all source files

For each file returned by `scan_repo.py`:
- Run `infer_procedure.md` to extract metadata (name, description, functions, classes, I/O)
- Group files by responsibility using function/class names and docstrings as signals

## Step 2 — Build skill tree plan

Propose a parent skill name (from directory name or dominant theme) and one sub-skill per logical group.

Present the plan as Markdown:

```
Proposed skill tree for: [input_path]

Parent skill: [parent-name]
  Description: [orchestrator description — delegates to sub-skills]

Sub-skills:
  1. [parent-name]-[unit-a]
     Source: [file.py]
     Functions: [func1, func2]
     Description: [inferred description]

  2. [parent-name]-[unit-b]
     Source: [file.py]
     Functions: [func3]
     Description: [inferred description]

  ...

Total: 1 parent + N sub-skills
```

## Step 3 — PAUSE: User verification

Ask:
```
Does this skill tree match your intent?
You can:
  - Approve as-is            → type "yes"
  - Rename a skill           → type "rename [N] [new-name]"
  - Merge two sub-skills     → type "merge [N] [M]"
  - Split a sub-skill        → type "split [N]"
  - Remove a sub-skill       → type "remove [N]"
  - Start over               → type "restart"
  - Cancel                   → type "cancel"
```

Loop until user types "yes" or "cancel". Re-present the updated plan after each modification.

## Step 4 — Generate parent skill

Using `single_procedure.md` logic, draft the parent skill:
- SKILL.md describes the orchestrator role and lists sub-skills
- schema.json accepts routing parameters
- README.md includes sub-skill tree diagram
- tests/test_[parent].py placeholder

Present and confirm (same yes/edit/cancel flow as single_procedure.md Step 3).
Write parent skill files.

## Step 5 — Generate sub-skills sequentially

For each sub-skill in the approved plan (in order):
1. Load `procedures/single_procedure.md` with the sub-skill's source file and inferred metadata
2. Present drafts
3. Confirm with user
4. Write files
5. Run `skill-architect-proofing` on that sub-skill before moving to the next

Report progress after each:
```
[2/4] Sub-skill 'parent-unit-b' generated and proofed. ✓
```

## Step 6 — Final proof of parent skill

Run `skill-architect-proofing` on the parent skill directory.

## Step 7 — Summary

Print final summary:
```
Generation complete.
  Parent:     ~/.claude/skills/[parent-name]/       ✓
  Sub-skill 1: ~/.claude/skills/[parent-name]-[a]/  ✓
  Sub-skill 2: ~/.claude/skills/[parent-name]-[b]/  ✓
  ...

All skills proofed. Run /skill-architect-makeinto again to convert more code.
```
