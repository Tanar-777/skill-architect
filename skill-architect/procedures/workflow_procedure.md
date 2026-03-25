# Workflow Procedure — skill-architect (full orchestration loop)

This procedure runs after Step 6 file generation is complete. It orchestrates the full
create → proof → update → validate → ultimate proof → done cycle.

## Resume

If a session was interrupted mid-workflow, ask: "Which phase did we stop at? (1 / 1.5 / 2 / 3 / 3.5 / 4 / 5 / 6)" — then resume from that phase. If uncertain, restart from Phase 1 (proofing is idempotent).

## Phase 1 — Initial Proofing

1. Run `skill-architect-proofing` on the output directory (Branch 1 — pass `skill_path` directly).
2. Display the full ❌/⚠️/ℹ️/✅ report.
3. If all ✅ → proceed to Phase 1.5.
4. If ❌ failures or ⚠️ warnings → proceed to Phase 2 first, then Phase 1.5 after fixes.

## Phase 1.5 — Code Testing (conditional)

**Trigger condition:** Use Glob to check if any `scripts/*.py` OR `tests/test_*.py` files exist in `[skill_path]/`. If none found: skip this phase silently (agent-only test stubs like `test_skill.md` are handled by proofing, not here).

If Python code files are present:
1. Check that `~/.claude/skills/skill-architect-tester/SKILL.md` exists. If not: warn and skip.
2. Run `skill-architect-tester` on the output directory with `caller: workflow`.
3. Display the `code-test-report.md` badge and summary.
4. If ❌ tests failed: surface failures and ask:
   "Tests failed. Fix these issues now? [yes / skip]"
   - `yes` → load `skill-architect-update` (patch mode) with `skill_path`. Re-run tester after fixes.
   - `skip` → proceed to Phase 3 with current state.
5. If ✅ or ⚠️ → proceed to Phase 3.

## Phase 2 — Update Loop (proof → fix → re-proof)

Repeat until clean or user explicitly accepts:

### Iteration start
- Display current proofing issues clearly.
- Ask: "Fix these issues now? [yes / accept-warnings / done]"
  - `accept-warnings` (only if no ❌) → skip to Phase 3.
  - `done` → skip to Phase 3 with current state.
  - `yes` → continue below.

### Fix cycle
- Load `skill-architect-update` procedures in `proof` mode, passing `skill_path` directly.
- skill-architect-update applies fixes with user validation.
- After fixes applied → re-run `skill-architect-proofing` (Branch 1).
- Display updated report.
- Loop back to Iteration start.

**Loop guard:** After 3 consecutive fix cycles with remaining ❌ failures, warn:
"Persistent failures after 3 fix cycles. Recommend a manual major update or accepting current state."
Then ask: [continue / accept / exit]

## Phase 3 — User Validation

Ask the user:
```
Skill generation complete. Does this skill match your intent?

Review checklist:
- [ ] Skill name and description are correct
- [ ] All 6 design steps were validated
- [ ] Behaviour matches the dry-run simulation from Step 5
- [ ] Proofing result is acceptable

Confirm? [yes / no — needs changes]
```

- `yes` → proceed to Phase 4.
- `no — needs changes` → ask what needs changing, then load the appropriate
  skill-architect-update mode (patch/minor/major) and loop back to Phase 1 after changes.

## Phase 3.5 — Behavioral Trial (optional)

Ask:
```
Would you like to run the skill on a real example before final proofing?
This catches behavioral issues that static checks cannot detect.
  (yes)   Invoke the skill now on a real task
  (skip)  Proceed to final proofing
```

- `yes` → Ask the user for a real example input, then invoke the skill on it. After the trial:
  - Ask: "Did the skill behave as expected? [yes / no — needs changes]"
  - `yes` → proceed to Phase 4.
  - `no — needs changes` → load `skill-architect-update` (patch or minor mode) and return to Phase 3.5 after fixes.
- `skip` → proceed to Phase 4 directly.

## Phase 4 — Ultimate Proofing

- Run `skill-architect-proofing` one final time (Branch 1).
- Display the final report and badge.
- State the final readiness verdict:
  - ✅ all pass → **"Skill is ready to share on Git."**
  - ⚠️ warnings → **"Skill can be shared but improvements are recommended."**
  - ❌ failures → **"Skill has unresolved issues — not recommended for sharing."**

## Phase 5 — Post-completion Offer

Ask:
```
Skill complete. Would you like any further updates?
(patch)  Small fix or correction
(minor)  Add a feature or section
(major)  Architectural change
(done)   Exit
```

- `patch` / `minor` / `major` → load skill-architect-update with the chosen mode and `skill_path`.
  After update completes, return to Phase 4 (ultimate proofing).
- `done` → proceed to Phase 6.

## Phase 6 — Git Upload Offer

Ask:
```
Would you like to publish this skill to Git now?
  (yes)  Invoke skill-architect-git-upload
  (no)   Exit
```

- `yes` → invoke `skill-architect-git-upload`, passing `skill_name` and `caller: skill-architect`. Exit when upload completes.
- `no`  → exit. Display final skill path and proofing badge.
