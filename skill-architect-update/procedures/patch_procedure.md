# Patch Procedure — skill-architect-update

Targeted fix: bug correction, typo, small wording change, or missing metadata. Affects ≤ 2 files. No schema changes. No README update required.

## Step 1 — Read current skill state

- Read `[skill_path]/SKILL.md` — note current version.
- If `version:` field absent → insert `version: 1.0.0` before proceeding.

## Step 2 — Intake change request

Ask: "What needs to be patched? Describe the issue."

## Step 3 — Identify scope

- Read the affected file(s).
- Confirm the change touches ≤ 2 files and requires no schema or README changes.
- If scope is larger: warn the user and suggest upgrading to `minor`. Ask: "Upgrade to minor? [yes/no]"
  - `yes` → load `procedures/minor_procedure.md`.
  - `no` → proceed as patch, noting the limited scope.

## Step 4 — Propose edit

- Display the exact proposed change(s) for each affected file (before/after diff style).
- Ask: "Apply this patch? [yes/no]"

## Step 5 — Apply and version bump

If confirmed:
- Apply edits using Edit tool.
- Bump PATCH version in SKILL.md frontmatter (e.g., `1.0.0` → `1.0.1`).
- Append to CHANGELOG.md (create if absent):
  ```
  ## [X.Y.Z] — YYYY-MM-DD
  ### Fixed
  - <description of change>
  ```

## Step 6 — Delegate to skill-architect-proofing

- Verify `~/.claude/skills/skill-architect-proofing/SKILL.md` exists. If not: warn and skip.
- Run skill-architect-proofing (Branch 1) with `skill_path`.
- Display the result.

## Step 7 — Offer further upgrade

```
Patch applied. Any further upgrade needed?
(patch)  Another patch
(minor)  New feature or section
(major)  Architectural rewrite
(done)   Exit
```

Route accordingly or exit.
