# Test Cases — skill-architect-git-upload

Behavioural tests. Manual verification scenarios.

---

## TC-01 — First run, no config

**Setup:** No `~/.claude/skill-git.config.json` exists.
**Invoke:** `/skill-architect-git-upload`
**Expected:**
- Init procedure runs.
- User asked: git_enabled, default repo, branch mode, commit message mode, update check mode.
- Config written to chosen scope.
- Full upload flow begins after init.

---

## TC-02 — git_enabled: false — standalone

**Setup:** Config exists with `git_enabled: false`.
**Invoke:** `/skill-architect-git-upload`
**Expected:**
- Warning displayed: "Git features are disabled."
- No further action. Exits gracefully.

---

## TC-03 — git_enabled: false — called from skill-architect

**Setup:** Config exists with `git_enabled: false`.
**Invoke:** Called internally by skill-architect with `caller: skill-architect`.
**Expected:**
- Returns silently. No output. skill-architect continues normally.

---

## TC-04 — Push to main — double confirmation

**Setup:** User selects `main` as target branch.
**Expected:**
- First `⛔` warning displayed.
- Second confirmation requires typing `push to main` exactly.
- Anything else → reverts to new branch proposal.

---

## TC-05 — Upload repo ≠ load repo warning

**Setup:** `skill_repos["my-skill"].load_repo` = repo-A, `upload_repo` = repo-B.
**Expected:**
- ℹ️ info note shown: "upload repo differs from load repo".
- Non-blocking — user can proceed normally.

---

## TC-06 — Remote ahead conflict

**Setup:** Remote branch has 2 commits local doesn't have.
**Expected:**
- Warning shown with commit count.
- Options: pull-first / force-push / abort.
- `force-push` requires explicit second confirmation.

---

## TC-07 — Diverged state — force push

**Setup:** Local and remote both have changes the other doesn't.
**Expected:**
- Diverged warning with conflicting files listed.
- `force-push` requires typing `force push` exactly.
- `--force-with-lease` used (not `--force`).

---

## TC-08 — Auto-generated commit message

**Setup:** Skill has `CHANGELOG.md` with a `## [1.2.0]` entry.
**Expected:**
- Commit message: `chore: update [skill-name] to v1.2.0\n\n[CHANGELOG entry]`
- If `commit_message_mode: auto-with-edit` → shown for review before commit.

---

## TC-09 — Credential file detection

**Setup:** Skill directory contains a `.env` file.
**Expected:**
- Warning: "Skipping '.env' — potential credentials file."
- User asked: skip / upload anyway.
- `.env` never included in `git add` without explicit confirmation.

---

## TC-10 — Called from skill-architect, single skill

**Setup:** skill-architect finishes generating `my-new-skill`.
**Invoke:** skill-architect calls git-upload with `caller: skill-architect`, `skill_name: my-new-skill`.
**Expected:**
- No selection checklist shown.
- Proceeds directly to repo resolution for `my-new-skill`.
- Upload completes for that skill only.

---

## TC-11 — Standalone, multiple skills selected

**Setup:** 3 local skills exist. User selects 2 of them.
**Expected:**
- Each skill processed in sequence.
- If one fails: "Continue with remaining? [yes/no]" shown.
- Final report shows one line per skill with status.

---

## TC-12 — UP_TO_DATE state

**Setup:** Local skill is identical to remote.
**Expected:**
- "Already in sync" message shown.
- User asked: "Push anyway? [yes / no]"
- `no` → exits cleanly for that skill.
