# Test Cases — skill-architect-git-load

Behavioural tests. These are manual verification scenarios, not automated unit tests.

---

## TC-01 — First run, no config

**Setup:** Delete `~/.claude/git-load.config.json` and `[project]/.claude/git-load.config.json`.
**Invoke:** `/skill-architect-git-load`
**Expected:**
- Init procedure runs.
- User is asked: repo usage intent, default repo (optional), update check mode.
- Config is written to chosen scope.
- After init, standalone flow begins.

---

## TC-02 — Explicit repo argument, trust gate

**Setup:** Config exists with `use_repo: true`.
**Invoke:** `/skill-architect-git-load repo_url:https://github.com/some/repo`
**Expected:**
- Trust gate prompt appears with full URL and detected visibility.
- No `git` or network command runs before user confirms.
- After confirm, access test runs.

---

## TC-03 — Public repo trust gate not bypassed

**Setup:** Config exists. `repo_url` points to a public GitHub repo.
**Expected:**
- Trust gate still prompts — "Public repositories are not automatically safe."
- User must explicitly confirm before any download.

---

## TC-04 — Monorepo skill selection

**Setup:** Repo contains 3 skills in subdirectories.
**Expected:**
- Discovery scan finds all 3 `SKILL.md` files.
- Selection checklist shows all 3 with correct NEW / UP TO DATE / UPDATE AVAILABLE labels.
- `[all]` option available.
- Only selected skills are installed.

---

## TC-05 — Local modification conflict

**Setup:** Skill `foo` is installed locally with a manual patch. Remote has a newer version.
**Invoke:** Update for skill `foo`.
**Expected:**
- Warning shown with diff summary.
- User prompted: overwrite / backup-first / skip / cancel.
- `backup-first` creates `~/.claude/skills/foo.backup-[timestamp]/` before overwriting.

---

## TC-06 — Executable scripts warning

**Setup:** Remote skill has a `scripts/main.py` file.
**Expected:**
- Warning lists all script files before install.
- `view-first` option shows file content.
- Install only proceeds after explicit user confirmation.

---

## TC-07 — on-proof update check mode

**Setup:** Config has `update_check_mode: on-proof`. Skill has a remote update available.
**Invoke:** Triggered from `skill-architect-proofing` with `caller: proofing`.
**Expected:**
- User is asked: "Check for updates? [y/n]"
- `y` → check runs, update shown.
- `n` → git-load exits immediately, proofing continues.

---

## TC-08 — manual update check mode

**Setup:** Config has `update_check_mode: manual`. Triggered from proofing.
**Expected:**
- git-load returns immediately without prompting.
- Proofing is not interrupted.

---

## TC-09 — automatic update check mode, no update

**Setup:** Config has `update_check_mode: automatic`. Local skill is up to date.
**Invoke:** Triggered from proofing.
**Expected:**
- Silent check runs.
- No prompt shown (already up to date).
- Proofing continues uninterrupted.

---

## TC-10 — Download fallback chain

**Setup:** `git` is not installed. `gh` is not installed.
**Expected:**
- Methods 1 and 2 (git) skipped with clear error.
- Method 3 (gh) skipped.
- Method 4 (HTTP zip) attempted for GitHub URLs.
- Non-GitHub/GitLab URL → clear error "HTTP zip not supported for this type. Please install git."
