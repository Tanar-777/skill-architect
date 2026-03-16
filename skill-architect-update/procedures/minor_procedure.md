# Minor Procedure — skill-architect-update

New feature, new section, or backward-compatible enhancement. May update schema.json and README.md. No breaking changes to existing I/O or behavior.

## Step 1 — Read current skill state

- Read `[skill_path]/SKILL.md`, `schema.json` (if exists), `README.md` (if exists).
- Note current version. If `version:` field absent → insert `version: 1.0.0` before proceeding.

## Step 2 — Intake change request

Ask: "What needs to be added or improved? Describe the enhancement."

## Step 3 — Identify scope and check compatibility

- Determine which files are affected: SKILL.md, schema.json, README.md, procedure files.
- Confirm the change is backward-compatible (no removal of existing parameters, sections, or behaviors).
- If breaking changes are detected: warn the user and suggest upgrading to `major`. Ask: "Upgrade to major? [yes/no]"
  - `yes` → load `procedures/major_procedure.md`.
  - `no` → proceed as minor, documenting the constraint.

## Step 4 — Propose changes

- Display the exact proposed change(s) for each affected file (before/after diff style).
- For README.md: show which sections will be updated or created.
- For schema.json: show new/modified parameters clearly.
- Ask: "Apply these changes? [yes / no / select]"
  - `yes` → apply all.
  - `no` → cancel.
  - `select` → user picks which changes to apply individually.

## Step 5 — Apply and version bump

For each confirmed change:
- Apply edits using Edit tool (existing files) or Write tool (new files).
- Bump MINOR version in SKILL.md frontmatter (e.g., `1.0.1` → `1.1.0`).
- Update README.md affected sections (create README.md if absent).
- Append to CHANGELOG.md (create if absent):
  ```
  ## [X.Y.Z] — YYYY-MM-DD
  ### Added / Changed
  - <description of change>
  ```

## Step 6 — Delegate to skill-architect-proofing

- Verify `~/.claude/skills/skill-architect-proofing/SKILL.md` exists. If not: warn and skip.
- Run skill-architect-proofing (Branch 1) with `skill_path`.
- Display the result.

## Step 7 — Offer further upgrade

```
Minor update applied. Any further upgrade needed?
(patch)  Bug fix or small correction
(minor)  Another enhancement
(major)  Architectural rewrite
(done)   Exit
```

Route accordingly, or on `done` → proceed to git upload offer:

```
Would you like to publish this skill to Git now?
  (yes)  Invoke skill-architect-git-upload
  (no)   Exit
```
- `yes` → invoke `skill-architect-git-upload` with `skill_name` and `caller: skill-architect-update`.
- `no`  → exit.
