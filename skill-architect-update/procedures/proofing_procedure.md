# Proofing Procedure — skill-architect-update

Default mode. Runs skill-architect-proofing, surfaces issues, suggests and implements fixes with user validation, then offers further upgrade.

## Step 1 — Check skill-architect-proofing availability

- Verify `~/.claude/skills/skill-architect-proofing/SKILL.md` exists.
- If not found: warn the user ("skill-architect-proofing not installed — proofing steps will be skipped"), then jump to Step 6.

## Step 2 — Read current skill state

- Read `[skill_path]/SKILL.md` — note name, version (or absence), allowed-tools.
- If `proofing-report.md` exists in `skill_path`: read it and display the last report date as context.

## Step 3 — Run skill-architect-proofing

- Delegate to skill-architect-proofing passing `skill_path` directly (Branch 1 — no discovery needed).
- Display the full ❌/⚠️/ℹ️/✅ report.

## Step 4 — Surface issues and suggest fixes

- If all ✅ (no issues): inform user and skip to Step 6.
- For each ❌ and ⚠️: propose a concrete fix:
  - Edits to existing files → show exact proposed change.
  - Missing files → show proposed content to create (README.md, CHANGELOG.md, schema.json).

## Step 5 — Validate and implement

- Present all proposed fixes as a numbered list.
- Ask: "Implement these fixes? [yes / no / select]"
  - `yes` → apply all fixes.
  - `no` → skip all, go to Step 6.
  - `select` → user picks which fixes to apply individually (by number).
- For each fix applied:
  - Use Edit for existing files, Write for new files.
  - If `version:` field absent in SKILL.md frontmatter → insert `version: 1.0.0` first.
  - Determine version bump:
    - Only missing structural files created (README.md, CHANGELOG.md, schema.json) → PATCH bump.
    - Substantive content added or behavior changed → propose MINOR bump, ask user to confirm.
  - Append to CHANGELOG.md (create if absent):
    ```
    ## [X.Y.Z] — YYYY-MM-DD
    ### Fixed
    - <description of fix>
    ```
- Re-run skill-architect-proofing after all fixes are applied.
- Display the updated report.

**Re-proof cycle guard:** If the user selects `re-proof` more than 3 times in a row without progress (same failures), stop and warn: "Same issues persist after 3 re-proof cycles. Consider a patch or minor update to address these manually."

## Step 6 — Offer further upgrade

```
Update complete. Any further upgrade needed?
(patch)    Bug fix or small correction
(minor)    New feature or section, backward-compatible
(major)    Architectural rewrite
(re-proof) Run proofing again
(done)     Exit
```

- `patch`    → load `procedures/patch_procedure.md`
- `minor`    → load `procedures/minor_procedure.md`
- `major`    → load `procedures/major_procedure.md`
- `re-proof` → return to Step 3 (increment re-proof counter)
- `done`     → proceed to git upload offer:

```
Would you like to publish this skill to Git now?
  (yes)  Invoke skill-architect-git-upload
  (no)   Exit
```
- `yes` → invoke `skill-architect-git-upload` with `skill_name` and `caller: skill-architect-update`.
- `no`  → exit.
