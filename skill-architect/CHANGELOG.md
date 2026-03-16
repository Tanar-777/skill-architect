# Changelog — skill-architect

## [5.0.0] — 2026-03-16
### Breaking Changes
- Sub-skill count increased to 4 — startup check now requires `skill-architect-git-upload`
- `skill-architect-git-load` config migrated from `git-load.config.json` to shared `skill-git.config.json`
### Added
- `skill-architect-git-upload` sub-skill — uploads local skills to remote Git repositories with shared config, branch safety (main/master double-confirm), sync check, auto commit message, and push
- Git upload post-generation offer in workflow — after skill creation, user can upload directly
### Changed
- SKILL.md: 4 sub-skills registered; startup check updated; README updated

## [4.0.0] — 2026-03-16
### Breaking Changes
- Sub-skill count increased from 2 to 3 — startup check now requires `skill-architect-git-load` in addition to proofing and update
- Step 1 protocol now pauses and triggers `skill-architect-git-load` (check mode) when a skill with the same name already exists locally
### Added
- `skill-architect-git-load` sub-skill — loads/updates skills from remote Git repositories with trust gate, repo resolution, skill discovery, download fallback chain, and conflict handling
- Git Load Integration rule in SKILL.md — defines Step 1 behavior when existing skill is detected
- `Bash` added to `allowed-tools` to support git-load check mode calls at Step 1
### Changed
- SKILL.md description updated to reference three sub-skills
- README.md stale `skill-proofing` / `skill-update` references replaced with `skill-architect-proofing` / `skill-architect-update` / `skill-architect-git-load`

## [3.0.0] — 2026-03-16
### Breaking Changes
- `skill-proofing` references replaced by `skill-architect-proofing` throughout
- `skill-update` references replaced by `skill-architect-update` throughout
### Added
- `skill-architect-proofing/` sub-skill — independently invocable, canonical proofing tool
- `skill-architect-update/` sub-skill — independently invocable, canonical update tool
- `procedures/workflow_procedure.md` — full post-generation lifecycle orchestration:
  Phase 1 initial proofing → Phase 2 update loop → Phase 3 user validation →
  Phase 4 ultimate proofing → Phase 5 post-completion offer
### Changed
- SKILL.md rewritten to reference sub-skills and describe orchestration model
- `process.md` Step 6 post-generation block updated to delegate to workflow_procedure.md

## [2.0.0] — 2026-03-16
### Breaking Changes
- SKILL.md fully restructured to comply with mandatory section standard (`# DESCRIPTION`, `# OBJECTIVES`, `# STRICT INSTRUCTIONS`, `# AVAILABLE TOOLS`, `# EXPECTED FORMAT (I/O)`)
### Added
- Pre-generation checklist in `# STRICT INSTRUCTIONS` — enforces proofing compliance before any file is written
- Post-generation proofing hard gate — skill not declared complete until skill-proofing passes or warnings explicitly accepted
- `process.md` Step 6 updated with pre-generation checklist step and proofing gate with fix loop

## [1.0.0] — 2026-03-16
### Fixed
- Added `version: 1.0.0` to SKILL.md frontmatter
- Added `allowed-tools` declaration to SKILL.md frontmatter
- Created `schema.json` (no required parameters — conversational input)
- Created `tests/test_skill.md` with 5 behavioural test cases
- Created `README.md` with usage, process table, and output structure
