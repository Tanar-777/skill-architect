# skill-architect-tester

> Execute and test written code in real time — runs pytest and scripts, reports results.

## Description

`skill-architect-tester` is a Claude Code skill that runs the actual Python code inside any skill directory and reports results in real time. It complements `skill-architect-proofing` (which checks structure and documentation) by executing tests and scripts — catching runtime errors, import failures, and assertion bugs that static analysis cannot detect.

## Usage

```
/skill-architect-tester
```

Or with arguments:

```
/skill-architect-tester skill_name=my-skill
/skill-architect-tester skill_path=~/.claude/skills/my-skill run_scripts=true
```

## What it runs

| Target | Command | Default |
|--------|---------|---------|
| `tests/test_*.py` | `python -m pytest tests/ -v --tb=short` | Always (if files exist) |
| `scripts/*.py` | `python scripts/[file].py` | Only if `run_scripts: true` |

## Output

Writes `code-test-report.md` in the skill directory:

```
~/.claude/skills/[skill-name]/
└── code-test-report.md   ← pass/fail summary, output excerpts, diagnostics, badge
```

## Badges

| Badge | Meaning |
|-------|---------|
| ✅ All tests passed | All pytest tests passed, no errors |
| ⚠️ Warnings | Tests passed but scripts skipped, or minor issues |
| ❌ Tests failed | One or more pytest failures or errors |

## Safety

- Scripts are **not** run by default (`run_scripts` defaults to `false`) — they may have side effects.
- A security gate scans for `os.system`, `eval`, `exec`, and unsafe file writes before running any script.
- Never crashes — always writes a `code-test-report.md`, even if documenting what could not be run.

## Graceful fallbacks

- Python not in PATH → report notes it, no crash.
- pytest not installed → report notes `pip install pytest` is needed.
- No `tests/` or `scripts/` found → report notes "no runnable code found."

## Related Skills

- [`skill-architect`](../skill-architect/) — parent skill, calls tester automatically in workflow Phase 1.5
- [`skill-architect-proofing`](../skill-architect-proofing/) — structural quality gate, runs before tester in the workflow
- [`skill-architect-update`](../skill-architect-update/) — fix issues surfaced by tester
