# Changelog — skill-architect-git-load

## [1.0.1] — 2026-03-16
### Changed
- Config file renamed from `~/.claude/git-load.config.json` to `~/.claude/skill-git.config.json` — shared with `skill-architect-git-upload` as single source of truth for git settings
- Updated all references in `SKILL.md`, `procedures/init_procedure.md`, `procedures/resolve_repo_procedure.md`

## [1.0.0] — 2026-03-16
### Added
- Initial release
- `SKILL.md` with full routing logic, trust gate rule, warn+ask permission model, config resolution
- `schema.json` — parameters: `mode`, `repo_url`, `skill_name`, `caller`
- `procedures/init_procedure.md` — first-run setup: repo intent, default repo, update check mode, config scope selection
- `procedures/resolve_repo_procedure.md` — 5-level priority chain: arg → skill-memory → project config → global config → prompt; save offer after manual entry
- `procedures/trust_gate_procedure.md` — hard gate: trusted_sources cache, visibility detection, explicit confirmation required for ALL repos (public not auto-trusted), access test, optional trust save
- `procedures/discover_skills_procedure.md` — repo structure classification, SKILL.md scan, version comparison, selection checklist with NEW / UP TO DATE / UPDATE AVAILABLE / LOCAL AHEAD labels
- `procedures/download_procedure.md` — priority chain: git sparse-checkout → git clone → gh CLI → HTTP zip; auth error handling, full fallback messaging
- `procedures/install_procedure.md` — scripts warning, local modification diff, name collision handling, dependency detection, backup-before-overwrite, cleanup, install report
- `tests/test_skill.md` — 10 behavioural test cases covering init, trust gate, monorepo selection, conflict, scripts, update check modes, download fallback
- `README.md` — usage, modes, parameters, init flow, trust gate explanation, integration points
