# Changelog — skill-architect-git-upload

## [1.0.0] — 2026-03-16
### Added
- Initial release
- `SKILL.md` — routing logic, git_enabled gate, upload repo resolution, branch safety rule, sync check rule, commit rule, warn+ask permission model
- `schema.json` — parameters: `mode`, `repo_url`, `skill_name`, `caller`
- `procedures/init_procedure.md` — first-run setup: git_enabled gate, default repo, branch mode, commit message style, update check mode, config scope selection
- `procedures/resolve_repo_procedure.md` — 5-level upload repo resolution: arg → skill upload override → skill load repo (symmetry fallback) → global default → prompt; load≠upload info warning
- `procedures/branch_procedure.md` — fetch remote state, branch selection, `⛔` double confirmation for main/master (typed input required), new branch creation
- `procedures/sync_check_procedure.md` — LOCAL_AHEAD / NEW_BRANCH / REMOTE_AHEAD / DIVERGED / UP_TO_DATE states; pull-first and force-with-lease options; typed confirmation for destructive actions
- `procedures/select_skills_procedure.md` — Branch A (skill-architect caller, single skill) and Branch B (standalone checklist, multi-skill with per-failure continue prompt)
- `procedures/upload_procedure.md` — repo structure detection, credential file skip warning, auto-generated commit message from CHANGELOG + version, `auto-with-edit` review, git add/commit/push, `--force-with-lease`, cleanup, upload report, config update with last_uploaded metadata
- `tests/test_skill.md` — 12 behavioural test cases covering init, git_enabled gate, main branch double-confirm, load≠upload warning, remote-ahead, diverged force-push, auto commit, credential detection, skill-architect caller, multi-skill standalone, UP_TO_DATE
- `tests/test_skill.py` — structural placeholder
- `README.md` — usage, modes, parameters, shared config shape, upload resolution order, branch safety, sync check states, commit flow, selection behavior
