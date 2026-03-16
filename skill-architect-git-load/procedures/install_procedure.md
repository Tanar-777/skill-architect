# Install Procedure — skill-architect-git-load

Copies selected skills from the temp directory to `~/.claude/skills/`.
Handles all conflict cases with warn + ask permission before any write.

---

## For each skill in SELECTED_SKILLS:

### Step 1 — Check for executable scripts

Scan the skill's source directory for any files in `scripts/`:
```bash
find [temp_dir]/[skill_path]/scripts/ -type f
```

If any files are found:
```
⚠️  This skill contains executable scripts:
    - scripts/main.py
    - scripts/helper.py
    (... full list)

    Review these files before installing. Scripts are not run automatically,
    but they will be present on your machine.

Proceed with installation? [yes / view-first / skip-this-skill / cancel-all]
```

- `view-first` → display each script's content using Read, then re-prompt.
- `skip-this-skill` → remove from SELECTED_SKILLS, continue to next.

---

### Step 2 — Check for local modifications

If `~/.claude/skills/[skill_name]/` already exists:

Check for any differences between local and remote:
```bash
diff -rq [temp_dir]/[skill_path]/ ~/.claude/skills/[skill_name]/ --exclude=".git"
```

If differences found:
```
⚠️  Local skill '[skill_name]' has modifications that will be overwritten:

    [diff summary — changed files listed]

    Your local version: [local_version]
    Remote version:     [remote_version]

Proceed? [yes / backup-first / skip-this-skill / cancel-all]
```

- `backup-first` → copy current local skill to `~/.claude/skills/[skill_name].backup-[timestamp]/`, then overwrite.

---

### Step 3 — Check for name collision (different skill)

If `~/.claude/skills/[skill_name]/` exists but appears to be a different skill
(different `name:` field in SKILL.md frontmatter):
```
⚠️  A skill named '[skill_name]' already exists locally but appears to be different
    from the remote skill.

    Local  name: [local_name_field]
    Remote name: [remote_name_field]

    Options:
    [overwrite]            Replace the local skill entirely
    [install-as-new]       Install remote as '~/.claude/skills/[skill_name]-remote/'
    [skip-this-skill]      Skip this skill
    [cancel-all]           Cancel all remaining installs
```

---

### Step 4 — Check for dependency skills

Scan the source `SKILL.md` for any sub-skill references (lines matching `~/.claude/skills/` or skill name patterns in the STRICT INSTRUCTIONS section).

For each detected dependency not present locally:
```
ℹ️  Skill '[skill_name]' references sub-skill '[dep_name]' which is not installed.

Install '[dep_name]' as well?
  [yes]    Run skill-architect-git-load for '[dep_name]' after this install
  [no]     Skip — install manually later
```

Queue any `yes` dependencies for a subsequent git-load run.

---

### Step 5 — Final install confirmation

Display a summary for all skills about to be written:
```
Install summary:
  ✅ skill-name-1   NEW         → ~/.claude/skills/skill-name-1/
  ✅ skill-name-2   UPDATE      → ~/.claude/skills/skill-name-2/  (backup: yes)
  ⏭️  skill-name-3   SKIPPED

Proceed with install? [yes / cancel]
```

---

### Step 6 — Write files

For each confirmed skill:
1. If backup requested: `cp -r ~/.claude/skills/[name]/ ~/.claude/skills/[name].backup-[timestamp]/`
2. Copy skill files from `[temp_dir]/[skill_path]/` to `~/.claude/skills/[name]/` using Bash.
3. Verify the install: check `~/.claude/skills/[name]/SKILL.md` exists.

---

### Step 7 — Cleanup

Delete `TEMP_DIR`:
```bash
rm -rf [temp_dir]
```

---

### Step 8 — Install report

```
Install complete:

  ✅ skill-name-1   v2.1.0   installed at ~/.claude/skills/skill-name-1/
  ✅ skill-name-2   v3.0.0   updated  at ~/.claude/skills/skill-name-2/  (backup saved)
  ⏭️  skill-name-3            skipped

Pending dependency installs:
  → Run /skill-architect-git-load skill_name:dep-skill to install 'dep-skill'
```

If any queued dependency installs exist, offer to run them now:
```
Run dependency installs now? [yes / later]
```
- `yes` → invoke `skill-architect-git-load` for each queued dependency in order.
