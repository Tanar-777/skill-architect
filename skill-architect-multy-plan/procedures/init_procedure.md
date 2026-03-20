# Init Procedure — Input Mode Detection

## Purpose
Determine the input mode and route to the correct procedure.

## Steps

### 1. Detect input mode

Check in order:

**A. Delegated mode** — `prefill` object is present in arguments:
- Display the received context to the user:
  > "skill-architect passed me this context:
  > - Suite name candidate: `[name_candidate]`
  > - Idea: [idea]
  > - Step 1 notes: [step1_notes]
  >
  > Does this look right, or do you want to adjust the suite name or overview?"
- Wait for user confirmation or correction.
- Store confirmed suite name as `suite_name`, overview as `suite_overview`.
- Proceed to `gather_procedure.md` (per-skill section only — skip suite overview questions).

**B. File mode** — `reference_file` argument is present:
- Verify the file exists. If not found:
  > "Reference file not found at [path]. Falling back to conversational mode."
  → proceed to step C.
- Run credential scan (see Credential Scan Rule in SKILL.md).
- Read the file.
- Attempt to extract:
  - **Suite name:** top-level heading, `name:` field, or filename stem.
  - **Skill list:** numbered/bulleted lists, `###` headings, entries prefixed with `skill-`.
  - **Per-skill fields:** purpose, inputs, outputs, dependencies from structured blocks near each skill entry.
- For each unresolvable field: mark as `[TO DEFINE]`.
- Display a parse summary:
  > "Parsed [N] skills from [filename]: [skill-a], [skill-b], ...
  > Fields marked [TO DEFINE]: [list]
  >
  > Correct? [yes / adjust]"
- If fewer than 2 skills found: warn and fall through to conversational supplement.
- If user confirms: proceed to `plan_procedure.md` with extracted data.
- If fields remain `[TO DEFINE]`: proceed to `gather_procedure.md` (supplement only).

**C. Cold start** — no prefill, no reference file:
- Proceed to `gather_procedure.md` (full flow).

### 2. Check for existing plan file

If `output_path/[suite-name]-plan.md` already exists:
> "A plan file already exists at [path] (plan_version: [X]).
> Update existing plan or start fresh? [update / fresh / cancel]"
- `update` → read existing plan, load into context, proceed to `plan_procedure.md` in revision mode (bump `plan_version` by 0.1 on save).
- `fresh` → continue with current mode, will overwrite on approval.
- `cancel` → exit.
