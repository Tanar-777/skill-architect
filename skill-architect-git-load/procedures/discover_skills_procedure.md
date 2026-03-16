# Discover Skills Procedure — skill-architect-git-load

Scans the repository for installable skills and presents a selection checklist.
Runs after the trust gate passes.

---

## Step 1 — Determine repo structure type

The repo must already be cloned to a temp directory by `download_procedure.md` for this scan.
However, for `check` mode (no write), use `git ls-tree` or sparse listing instead.

Scan for `SKILL.md` files:

```bash
# If cloned locally:
find [temp_dir] -name "SKILL.md" -not -path "*/.git/*"

# If using git ls-tree (remote, check mode):
git ls-tree -r --name-only HEAD | grep "SKILL.md"
```

Collect all paths. Classify the repo structure:

| Pattern found | Structure type |
|--------------|---------------|
| `SKILL.md` at root | `root-is-skill` — single skill |
| `[name]/SKILL.md` at depth 1 | `flat-monorepo` — skills in subdirs |
| `skills/[name]/SKILL.md` | `skills-folder` — skills under `/skills/` |
| Mixed or deeper nesting | `unstructured` — present all found paths |

---

## Step 2 — Extract skill metadata

For each `SKILL.md` found, read its frontmatter to extract:
- `name` — skill name
- `description` — one-line description
- `version` — remote version

If frontmatter is malformed or missing, flag with `⚠️ no metadata`.

---

## Step 3 — Compare with local state

For each discovered skill, check `~/.claude/skills/[name]/SKILL.md`:

| State | Label |
|-------|-------|
| Not installed locally | `NEW` |
| Same version | `UP TO DATE` |
| Remote newer | `UPDATE AVAILABLE (local: x.x.x → remote: y.y.y)` |
| Local newer than remote | `⚠️ LOCAL AHEAD (local: y.y.y > remote: x.x.x)` |
| Local exists, no version field | `⚠️ LOCAL VERSION UNKNOWN` |

---

## Step 4 — Present selection checklist

```
Skills found in [RESOLVED_REPO]:

  [ ] skill-name-1     v2.1.0   NEW              Brief description
  [ ] skill-name-2     v1.0.0   UP TO DATE       Brief description
  [x] skill-name-3     v3.0.0   UPDATE AVAILABLE (local: 2.1.0 → remote: 3.0.0)
  [ ] skill-name-4     v1.2.0   ⚠️ LOCAL AHEAD   Brief description
  [ ] skill-name-5     ⚠️ no metadata

  [all]    Select all
  [none]   Deselect all

Select skills to install/update, then confirm:
```

- User selects one or more skills (or "all").
- At least one must be selected to continue.
- If `skill_name` was pre-specified in the invocation, pre-select it.

---

## Step 5 — Handle LOCAL AHEAD warnings

For any selected skill where local version is ahead of remote:
```
⚠️  Warning: [skill-name] — your local version (y.y.y) is NEWER than the remote (x.x.x).
    Installing the remote version will DOWNGRADE this skill.

Proceed with downgrade? [yes / skip-this-skill / cancel-all]
```

---

## Step 6 — Return selection

Return `SELECTED_SKILLS` list (array of `{ name, remote_path, remote_version, local_state }`) to caller.

If `check` mode → return list with comparison data, do not proceed to download/install.
If `pull` or `standalone` mode → hand off to `install_procedure.md`.
