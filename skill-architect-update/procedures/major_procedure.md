# Major Procedure — skill-architect-update

Architectural rewrite or breaking change. Full review against skill-architect standards. May rewrite SKILL.md structure, schema, and README entirely. Introduces a MAJOR version bump.

## Step 1 — Read full current skill state

- Read all files in `[skill_path]/`:
  - `SKILL.md`, `schema.json`, `README.md` (if present)
  - All `procedures/*.md` (if present)
  - All `scripts/*.py` (if present) — read for context, not for rewriting here
- Note current version. If `version:` field absent → insert `version: 1.0.0` before proceeding.
- Read `proofing-report.md` if available — use as baseline quality context.

## Step 2 — Intake change request

Ask: "Describe the architectural change or breaking update needed."

## Step 3 — Full review against skill-architect standards

Evaluate the current skill against these mandatory criteria:

**SKILL.md structure:**
- Frontmatter: `name`, `description`, `version`, `user-invocable`, `allowed-tools`
- Mandatory sections: `# DESCRIPTION`, `# OBJECTIVES`, `# STRICT INSTRUCTIONS`, `# AVAILABLE TOOLS`, `# EXPECTED FORMAT (I/O)`

**schema.json:** Present if skill has I/O parameters. Parameters correctly typed and described.

**README.md:** Present and covers usage, modes, I/O, and examples.

**Breaking changes in the requested update:**
- Removed or renamed parameters
- Changed behavior of existing modes
- Incompatible SKILL.md restructuring

Present a full gap analysis to the user:
```
Gap Analysis:
✅ / ❌  <criterion>  — <finding>
```

## Step 4 — Propose rewrite plan

- Draft the complete set of changes needed (file by file).
- Clearly mark what is REMOVED, CHANGED, and ADDED.
- Ask: "Proceed with this rewrite plan? [yes/no]"

## Step 5 — Apply rewrite

If confirmed:
- Rewrite SKILL.md using Write tool (full replacement — read current first).
- Rewrite schema.json if I/O contract changes.
- Full README.md rewrite following skill-architect standards (create if absent).
- Bump MAJOR version (e.g., `1.1.0` → `2.0.0`).
- Append to CHANGELOG.md (create if absent):
  ```
  ## [X.0.0] — YYYY-MM-DD
  ### Breaking Changes
  - <description of breaking change>
  ### Added / Changed / Removed
  - <description>
  ```

## Step 6 — Delegate to skill-architect-proofing

- Verify `~/.claude/skills/skill-architect-proofing/SKILL.md` exists. If not: warn and skip.
- Run skill-architect-proofing (Branch 1) with `skill_path`.
- Display the full result.
- If ❌ failures remain after the rewrite: surface them and ask:
  "Failures remain. Apply immediate patch fixes? [yes/no]"
  - `yes` → load `procedures/patch_procedure.md` with the current `skill_path`.
  - `no` → proceed to Step 7.

## Step 7 — Final summary and git upload offer

Display:
- New version
- Files modified or created
- Proofing badge status (✅ ready / ⚠️ warnings / ❌ failures)
- "Major update complete."

Then ask:
```
Would you like to publish this skill to Git now?
  (yes)  Invoke skill-architect-git-upload
  (no)   Exit
```
- `yes` → invoke `skill-architect-git-upload` with `skill_name` and `caller: skill-architect-update`.
- `no`  → exit.
