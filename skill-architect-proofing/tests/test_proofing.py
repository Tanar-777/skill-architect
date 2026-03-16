# tests/test_proofing.py
# Delegates to the proofing.py self-test which creates a temp skill and validates the full run.

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from proofing import run
import tempfile
from pathlib import Path

def test_run():
    """Smoke test: proofing runs on a minimal valid skill and returns a report."""
    with tempfile.TemporaryDirectory() as tmp:
        skill_dir = Path(tmp)
        (skill_dir / "SKILL.md").write_text(
            "---\nname: test-skill\nversion: 1.0.0\nallowed-tools: [Read]\n---\n"
            "# DESCRIPTION\nTest.\n# OBJECTIVES\nTest.\n"
            "# STRICT INSTRUCTIONS\nTest.\n# AVAILABLE TOOLS\nRead\n"
            "# EXPECTED FORMAT (I/O)\nInput: string\nOutput: string\n",
            encoding="utf-8",
        )
        (skill_dir / "schema.json").write_text(
            '{"name": "test-skill", "parameters": {}}', encoding="utf-8"
        )
        tests_dir = skill_dir / "tests"
        tests_dir.mkdir()
        (tests_dir / "test_main.py").write_text("def test_run(): assert True\n", encoding="utf-8")

        result = run(str(skill_dir))
        assert "skill-proofing report" in result
        assert (skill_dir / "proofing-report.md").exists()
        print("OK:", result[:80])

if __name__ == "__main__":
    test_run()
