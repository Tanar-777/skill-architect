# skill-architect-proofing

> Quality gate for Claude Code skills. Sub-skill of skill-architect, also independently invocable.

## Description

`skill-architect-proofing` audits a skill directory against a strict checklist and produces a structured ❌/⚠️/ℹ️/✅ report with actionable fix suggestions. It writes `proofing-report.md` to the skill directory.

It is the canonical proofing tool for the skill-architect ecosystem and replaces the legacy `skill-proofing` skill.

## Usage

```
/skill-architect-proofing                        ← interactive discovery
/skill-architect-proofing skill-name             ← proof by name
/skill-architect-proofing skill_path=/full/path  ← proof by path (Branch 1)
```

## Checklist Categories

| Category | Checks |
|---|---|
| VERSIONING | `version:` field in frontmatter |
| TOOL_SCOPE | `allowed-tools:` in frontmatter |
| SECTIONS | All 5 mandatory `#` sections present |
| STRUCTURE | `schema.json`, `tests/test_*.py`, `README.md` |
| CREDENTIALS | API keys, tokens, private keys, passwords |
| SENSITIVE_PATH | ~/.ssh, ~/.aws, /etc/passwd, ~/.env |
| UNSAFE_BASH | rm -rf, curl\|bash, eval, sudo, os.system |

## Output

- Console: full report with ❌/⚠️/ℹ️/✅ per item
- Disk: `proofing-report.md` with embeddable badge block

## Badge colors

- `brightgreen` — all 7 categories passed
- `yellow` — warnings only
- `red` — hard failures present

## Note on proofing.py false positives

`scripts/proofing.py` contains the regex patterns it scans for (credentials, unsafe bash, etc.).
The proofing script will flag itself when run against this skill directory. This is expected — the patterns are present as scanner definitions, not as actual security issues.

## Related Skills

- [`skill-architect`](../skill-architect/) — parent orchestrator
- [`skill-architect-update`](../skill-architect-update/) — update workflow
