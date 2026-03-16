# Select Skills Procedure — skill-architect-git-upload

Determines which skill(s) to upload based on calling context.
Runs at the start of the full flow, before repo resolution.

---

## Branch A — Called from skill-architect (`caller: skill-architect`)

`skill_name` is pre-set by the caller. No selection prompt needed.

1. Verify `~/.claude/skills/[skill_name]/SKILL.md` exists.
2. Display:
   ```
   Uploading skill: [skill_name]
   Source: ~/.claude/skills/[skill_name]/
   ```
3. Return `SELECTED_SKILLS = [skill_name]` to caller.

If `skill_name` is not set or directory doesn't exist → warn and exit:
```
⚠️  skill-architect-git-upload was called by skill-architect but skill_name is missing or not found.
    Cannot proceed.
```

---

## Branch B — Standalone (`caller: standalone` or no caller)

### Step 1 — Scan local skills

Use Glob to find all `~/.claude/skills/*/SKILL.md`.

For each skill, read frontmatter to extract:
- `name`
- `version`
- `description` (first line only)

### Step 2 — Present selection checklist

```
Local skills available for upload:

  [ ] skill-architect           v4.0.0   6-step protocol to design Claude Code skills
  [ ] skill-architect-git-load  v1.0.1   Load skills from a remote Git repository
  [ ] skill-architect-git-upload v1.0.0  Upload skills to a remote Git repository
  [ ] skill-architect-proofing  v...     Quality gate for Claude Code skills
  [ ] skill-architect-update    v...     Guided update workflow for skills
  (... full list)

  [all]    Select all
  [none]   Deselect all

Select skills to upload, then confirm:
```

At least one skill must be selected to continue.

### Step 3 — Confirm selection

```
Selected for upload:
  - [skill_name_1]  v[version]
  - [skill_name_2]  v[version]

Proceed? [yes / change / cancel]
```

- `change` → return to Step 2.
- `yes` → return `SELECTED_SKILLS` list to caller.

---

## Per-skill flow

For each skill in `SELECTED_SKILLS`, the caller runs the full procedure chain independently:
1. `resolve_repo_procedure.md`
2. `branch_procedure.md`
3. `sync_check_procedure.md`
4. `upload_procedure.md`

Each skill is handled in sequence. If one skill fails or is cancelled, the remaining skills in the list are offered:
```
Upload of '[skill_name]' cancelled/failed.
Continue with remaining skills? [yes / no]
```
