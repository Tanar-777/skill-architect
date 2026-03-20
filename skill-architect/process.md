# Skill Architect — 6-Step Protocol

---

## STEP 0 — Brainstorm (OPTIONAL — argument-triggered only)

> Only run this step if `-brainstorm` was passed as an argument. Skip entirely otherwise.

- Load `~/.claude/skills/skill-architect-brainstorm/SKILL.md`.
- Pass `caller: skill-architect` and `mode: intent`.
- Run the full brainstorm protocol (6 blocks).
- On return, inject the structured brainstorm summary as prefill context into Step 1.
- Set session brainstorm flag — do not trigger brainstorm again this session.

If `skill-architect-brainstorm` is missing: warn the user and proceed directly to Step 1.

> **Brainstorm completes → proceed immediately to Step 1 with context injected.**

---

## STEP 1 — Definition, Critique & Research (MANDATORY PAUSE)

- **Action 1:** Ask the user for their skill idea.
- **Action 2:** Use WebSearch to check if open-source tools, Python libraries, or APIs already do exactly this. Present the nuances.
- **Action 3:** Be critical. Evaluate trade-offs:
  - Token consumption
  - Execution time
  - Precision vs creativity
  - Output rendering format
- **Action 4:** If the task is complex, list prerequisites or information/tests needed before committing to the design.
- **Action 5:** Propose a definitive skill name (lowercase, hyphens only, max 64 chars) and a clear description (max 1024 chars).
- **Action 6 (Complexity Check):** If the analysis above has identified **2 or more major edge cases** OR **3 or more important trade-offs** with architectural implications — AND the brainstorm session flag is not set — pause and offer:
  > "This skill has significant complexity. Run brainstorm mode before continuing? [yes / skip]"
  - `yes` → load `skill-architect-brainstorm` (`caller: skill-architect`, `mode: intent`), inject result as context, set session flag, then continue to Step 2.
  - `skip` → proceed to Step 2 directly.

> **STOP — Wait for explicit user validation before proceeding.**

---

## STEP 2 — Tooling & Architecture (MANDATORY PAUSE)

Based on Step 1, list the required components:
- Specific Python scripts (e.g. scraper, API connector)
- Configuration files or environment variables
- Regex patterns or utilities
- Potential sub-skills if the task is too complex for one skill

> **STOP — Wait for explicit user validation before proceeding.**

---

## STEP 3 — Storage & Data Strategy (MANDATORY PAUSE)

Define how inputs and outputs will be handled to minimize hallucinations and optimize context:
- Input format? (plain text, strict JSON, file path?)
- Output format? (Markdown for reading, JSON/SQLite for structured data, XML for system parsing?)
- Temporary vs final save structure

> **STOP — Wait for explicit user validation before proceeding.**

---

## STEP 4 — Skill File Structure (MANDATORY PAUSE)

Propose the complete folder structure for the skill:

```
~/.claude/skills/[skill-name]/
├── SKILL.md
├── schema.json      (if tool use required)
├── scripts/
│   └── main.py
└── tests/
    └── test_main.py
```

Specify the content outline of `SKILL.md` using the mandatory sections:
`# DESCRIPTION`, `# OBJECTIVES`, `# STRICT INSTRUCTIONS`, `# AVAILABLE TOOLS`, `# EXPECTED FORMAT (I/O)`

> **STOP — Wait for explicit user validation before proceeding.**

---

## STEP 5 — Dry Run & Logic Verification (MANDATORY PAUSE)

- Walk through a step-by-step simulation of how the skill will execute on a fictional example.
- Draft the Python script architecture with a unit test function:

```python
def run(input: str) -> str:
    # core logic
    ...

def test_run():
    result = run("sample input")
    assert result is not None
    print("OK:", result)

if __name__ == "__main__":
    test_run()
```

> **STOP — Wait for explicit user validation before proceeding.**

---

## STEP 6 — Final Critique & Generation (END)

- Perform a final self-critique of the complete architecture:
  - Security flaws? (hardcoded credentials, API keys, tokens, passwords, or personal config paths?)
  - Risk of infinite loops?
  - Context leaks?
  - Edge cases unhandled?

- **Run the Pre-generation Checklist** (defined in `SKILL.md` under `## Pre-generation Checklist`):
  - Confirm every item is satisfied before writing any file.
  - Fill in any missing items (version, allowed-tools, sections, schema, tests, README) now.

- **If validated by the user:**
  - Generate the complete `SKILL.md`, `schema.json`, `README.md`, `tests/test_*.py`, and any small utilities using the `Write` tool.
  - **Exception:** If Python code in `scripts/` is too large or complex, do NOT generate it here. Instead, provide detailed technical specifications that the user can use in a dedicated new conversation for that script.

- **Post-generation Lifecycle:**
  Load and follow `procedures/workflow_procedure.md` which orchestrates:
  1. Initial proofing via `skill-architect-proofing` (Branch 1).
  2. Update loop via `skill-architect-update` if issues found.
  3. User validation — explicit confirmation that skill matches intent.
  4. Ultimate proofing — final clean run via `skill-architect-proofing`.
  5. Post-completion offer — further updates if wanted.

> **END — Skill generation complete.**
