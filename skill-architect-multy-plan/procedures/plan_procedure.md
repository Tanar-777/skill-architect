# Plan Procedure — Synthesize, Validate, and Write

## Purpose
Assemble gathered or parsed data into a structured plan, validate with the user, and write the approved plan file.

---

## Step 1 — Dependency Order

Sort skills by dependency graph (topological sort):
- Skills with no dependencies first.
- Then skills depending on them, in order.

If a circular dependency is detected:
> "Circular dependency detected: [skill-a] → [skill-b] → [skill-a]
> Please resolve this before I can build the plan."
Wait for user to reassign or remove a dependency. Re-check until acyclic.

---

## Step 2 — Generate Context Fields

For each skill, compose the `context` field (two sentences):
1. **Suite context:** "[Suite name] is [suite_overview condensed to one sentence]."
2. **Skill idea:** "This specific skill [skill purpose in one sentence]."

Example:
> "This skill is part of the `data-pipeline` suite — a toolkit to ingest, validate, transform and export structured data. This specific skill reads CSV/JSON files from a given path and normalizes them into a standard dataset format."

Display each generated context to the user and allow edits before finalizing the plan.

---

## Step 3 — Complexity Estimation

For each skill, estimate complexity based on declared inputs/outputs and purpose:
- **Simple:** pure agent instructions, no scripts, no external APIs
- **Moderate:** 1–2 scripts, standard I/O
- **Complex:** multiple scripts, external APIs, sub-procedures, or Agent delegation

---

## Step 3 — Build ASCII Skill Tree

Render the dependency tree using ASCII:
```
[suite-name]
├── [suite-name]-[skill-a]     — [one-line purpose]
│   └── [suite-name]-[skill-b] — [one-line purpose]  (depends on skill-a)
└── [suite-name]-[skill-c]     — [one-line purpose]
```

---

## Step 4 — Assemble Plan Document

Build the full plan Markdown (YAML frontmatter + body) using the format defined in SKILL.md under `## Plan File Format`.

Set in YAML:
- `status: draft` (not yet approved)
- All skills: `status: pending`, `generated_at: ~`
- `plan_version: 1.0` (or incremented version if in revision mode)
- `created` and `last_updated`: today's date

---

## Step 5 — Present Plan for Validation

Display the complete plan to the user.

> "Here is the multi-skill plan for **[suite-name]** ([N] skills).
>
> You can:
> - **rename** a skill → 'rename [old] to [new]'
> - **merge** two skills → 'merge [a] and [b] into [new-name]'
> - **split** a skill → 'split [name] into [name-a] and [name-b]'
> - **add** a skill → describe it
> - **remove** a skill → 'remove [name]'
> - **reorder** → give the new generation sequence
> - **approve** → type 'yes' or 'approved'"

Apply any requested changes and re-display the updated plan. Repeat until explicit approval.

---

## Step 6 — Write Plan File

After approval:
1. Set `status: approved` in YAML frontmatter.
2. Set `last_updated` to today's date.
3. Determine output path: `[output_path]/[suite-name]-plan.md` (default: `./`).
4. Write the file using the Write tool.
5. Confirm to the user:
   > "Plan written to [path] ([N] skills, plan_version [X]).
   > Run `/skill-architect-multy-exec plan_file=[path]` when ready to generate skills."
