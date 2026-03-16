# Tests — skill-architect

## test_invocation
- Invoke `/skill-architect` with no arguments.
- Expected: agent reads `process.md` and asks the user for their skill idea (Step 1).

## test_step_gate
- Provide a skill idea at Step 1.
- Expected: agent completes Step 1 analysis and stops, waiting for explicit user validation before proceeding to Step 2.

## test_no_skip
- Validate Steps 1 through 4, then say "skip to Step 6".
- Expected: agent refuses and states Step 5 must be validated first.

## test_output_location
- Complete all 6 steps for a simple skill idea.
- Expected: all generated files are written to `~/.claude/skills/[skill-name]/`.

## test_proofing_handoff
- Complete Step 6 generation.
- Expected: agent automatically invokes `skill-proofing` on the output directory and presents the report.
