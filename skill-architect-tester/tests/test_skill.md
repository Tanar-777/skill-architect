# Behavioural Tests — skill-architect-tester

## Test 1 — No runnable code
**Input:** `skill_path` pointing to a skill with no `tests/` or `scripts/` directories.
**Expected:** `code-test-report.md` created noting "No runnable code found", badge ⚠️. No crash.

## Test 2 — Pytest passes
**Input:** `skill_path` with `tests/test_main.py` where all assertions pass.
**Expected:** `code-test-report.md` shows ✅ all passed, stdout from pytest -v captured.

## Test 3 — Pytest fails
**Input:** `skill_path` with `tests/test_main.py` containing a failing assertion.
**Expected:** `code-test-report.md` shows ❌, FAILED lines and short traceback captured.

## Test 4 — Python not available
**Input:** `skill_path` on a system where `python` is not in PATH.
**Expected:** Report notes "Python not available in environment". No crash. Badge ⚠️.

## Test 5 — Script execution skipped by default
**Input:** `skill_path` with `scripts/main.py`, `run_scripts` not provided.
**Expected:** scripts section shows ⏭️ skipped in report. pytest still runs if tests exist.

## Test 6 — Security gate triggered on script
**Input:** `skill_path` with `scripts/main.py` containing `os.system(user_input)`.
**Expected:** User warned before execution. Script skipped if user answers "skip".

## Test 7 — Called from workflow (caller: skill-architect)
**Input:** `skill_path` + `caller: skill-architect`.
**Expected:** No interactive skill discovery prompt. Report written. Badge returned to caller.

## Test 8 — pytest not installed
**Input:** `skill_path` with test files, but pytest not installed in the environment.
**Expected:** Report notes "pytest not installed — run `pip install pytest`". Badge ⚠️.
