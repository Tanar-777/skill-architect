# noscan
"""
proofing.py
Core quality gate script for Claude Code skills.
Runs a full checklist on a skill directory and writes proofing-report.md.
"""

import re
import json
from pathlib import Path
from datetime import date

# --- Constants ---

MANDATORY_SECTIONS = [
    "# DESCRIPTION",
    "# OBJECTIVES",
    "# STRICT INSTRUCTIONS",
    "# AVAILABLE TOOLS",
    "# EXPECTED FORMAT",
]

TEXT_EXTENSIONS = {".md", ".py", ".sh", ".json", ".txt", ".yaml", ".yml"}

CREDENTIAL_PATTERNS = [
    (r"sk-[a-zA-Z0-9]{20,}", "API key pattern (sk-...)"),
    (r"Bearer\s+[a-zA-Z0-9\-_\.]{20,}", "Bearer token"),
    (r"(?i)api[_\-]?key\s*[=:]\s*['\"][^'\"]{8,}['\"]", "Hardcoded API key"),
    (r"-----BEGIN .{0,30}PRIVATE KEY-----", "Private key block"),
    (r"(?i)password\s*[=:]\s*['\"][^'\"]{4,}['\"]", "Hardcoded password"),
    (r"(?i)secret\s*[=:]\s*['\"][^'\"]{8,}['\"]", "Hardcoded secret"),
    (r"ghp_[a-zA-Z0-9]{36}", "GitHub personal access token"),
    (r"xox[baprs]-[a-zA-Z0-9\-]+", "Slack token"),
]

UNSAFE_BASH_PATTERNS = [
    (r"rm\s+-rf", "rm -rf (destructive delete)"),
    (r"curl\s+.*\|\s*bash", "curl | bash (arbitrary code execution)"),
    (r"\beval\s*\(", "eval() (arbitrary code execution)"),
    (r"\bsudo\s+", "sudo (privilege escalation)"),
    (r"os\.system\s*\(", "os.system() (unsafe shell execution)"),
    (r"subprocess\.call\s*\(\s*['\"]", "subprocess with string arg (injection risk)"),
]

SENSITIVE_PATH_PATTERNS = [
    (r"~/\.ssh", "~/.ssh (SSH keys directory)"),
    (r"~/\.aws", "~/.aws (AWS credentials)"),
    (r"/etc/passwd", "/etc/passwd (system users)"),
    (r"/etc/shadow", "/etc/shadow (system passwords)"),
    (r"~/\.env\b", "~/.env (environment variables file)"),
]

INTERNAL_IP_PATTERN = (
    r"\b(192\.168\.\d{1,3}\.\d{1,3}"
    r"|10\.\d{1,3}\.\d{1,3}\.\d{1,3}"
    r"|172\.(1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3})\b"
)

EMAIL_PATTERN = r"\b[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}\b"
IGNORED_EMAIL_DOMAINS = {"example.com", "test.com", "noreply.com", "anthropic.com"}

EXFILTRATION_PATTERNS = [
    (r"requests\.(post|put|patch)\s*\(['\"]https?://(?!localhost)", "Outbound POST/PUT to external URL"),
    (r"urllib.*urlopen.*https?://(?!localhost)", "urllib outbound request"),
]


# --- Helpers ---

def _read_text_files(skill_path: Path) -> list[tuple[Path, str]]:
    """Read all text files in a skill directory, skipping binaries."""
    results = []
    for f in skill_path.rglob("*"):
        if f.is_file() and f.suffix in TEXT_EXTENSIONS and f.name != "proofing-report.md":
            try:
                content = f.read_text(encoding="utf-8", errors="ignore")
                if content.lstrip().startswith("# noscan"):
                    continue
                results.append((f, content))
            except Exception:
                continue
    return results


def _issue(severity: str, code: str, message: str) -> dict:
    return {"severity": severity, "code": code, "message": message}


# --- Check functions ---

def check_frontmatter(skill_md: str) -> list[dict]:
    issues = []
    if "version:" not in skill_md:
        issues.append(_issue("warning", "VERSIONING", "No `version` field in YAML frontmatter"))
    if "allowed-tools:" not in skill_md:
        issues.append(_issue("warning", "TOOL_SCOPE", "No `allowed-tools` declared in frontmatter"))
    elif re.search(r"allowed-tools:\s*\[\s*\*\s*\]", skill_md):
        issues.append(_issue("warning", "TOOL_SCOPE", "`allowed-tools: [*]` — overly permissive, violates least-privilege"))
    return issues


def check_sections(skill_md: str) -> list[dict]:
    issues = []
    for section in MANDATORY_SECTIONS:
        if section not in skill_md:
            issues.append(_issue("fail", "MISSING_SECTION", f"Mandatory section `{section}` not found in SKILL.md"))
    return issues


def check_structure(skill_path: Path) -> list[dict]:
    issues = []
    schema_path = skill_path / "schema.json"
    if not schema_path.exists():
        issues.append(_issue("warning", "STRUCTURE", "No `schema.json` found"))
    else:
        try:
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
            if "parameters" not in schema:
                issues.append(_issue("info", "STRUCTURE", "`schema.json` has no `parameters` defined"))
        except json.JSONDecodeError:
            issues.append(_issue("fail", "STRUCTURE", "`schema.json` is not valid JSON"))

    tests = list(skill_path.glob("tests/test_*.py"))
    if not tests:
        issues.append(_issue("warning", "STRUCTURE", "No test files found in `tests/` — add at least one `test_*.py`"))

    if not (skill_path / "README.md").exists():
        issues.append(_issue("info", "STRUCTURE", "No `README.md` found — recommended for Git sharing"))

    return issues


def check_credentials(files: list[tuple[Path, str]]) -> list[dict]:
    issues = []
    for path, content in files:
        for pattern, label in CREDENTIAL_PATTERNS:
            if re.search(pattern, content):
                issues.append(_issue("fail", "CREDENTIALS", f"{label} detected in `{path.name}`"))
    return issues


def check_paths(files: list[tuple[Path, str]]) -> list[dict]:
    issues = []
    for path, content in files:
        for pattern, label in SENSITIVE_PATH_PATTERNS:
            if re.search(pattern, content):
                issues.append(_issue("fail", "SENSITIVE_PATH", f"{label} reference found in `{path.name}`"))

        if re.search(INTERNAL_IP_PATTERN, content):
            issues.append(_issue("warning", "INTERNAL_IP",
                f"Internal IP address found in `{path.name}` — may reveal private infrastructure"))

        emails = re.findall(EMAIL_PATTERN, content)
        public_emails = [e for e in emails if e.split("@")[-1] not in IGNORED_EMAIL_DOMAINS]
        if public_emails:
            preview = ", ".join(public_emails[:3])
            issues.append(_issue("warning", "PERSONAL_DATA",
                f"Email address(es) found in `{path.name}`: {preview}"))

    return issues


def check_bash_safety(scripts: list[tuple[Path, str]]) -> list[dict]:
    issues = []
    for path, content in scripts:
        for pattern, label in UNSAFE_BASH_PATTERNS:
            if re.search(pattern, content):
                issues.append(_issue("fail", "UNSAFE_BASH", f"`{label}` found in `{path.name}`"))
    return issues


def check_exfiltration(scripts: list[tuple[Path, str]]) -> list[dict]:
    issues = []
    for path, content in scripts:
        for pattern, label in EXFILTRATION_PATTERNS:
            if re.search(pattern, content):
                issues.append(_issue("warning", "EXFILTRATION",
                    f"{label} in `{path.name}` — ensure user is aware of outbound requests"))
    return issues


# --- Report generation ---

def generate_report(results: list[dict], skill_path: Path) -> str:
    skill_name = skill_path.name
    today = date.today().isoformat()

    fails = [r for r in results if r["severity"] == "fail"]
    warnings = [r for r in results if r["severity"] == "warning"]
    infos = [r for r in results if r["severity"] == "info"]

    total_categories = 7
    failed_categories = len(set(r["code"] for r in fails))
    warned_categories = len(set(r["code"] for r in warnings))
    passed = total_categories - failed_categories - warned_categories

    if fails:
        badge_color = "red"
        badge_label = "%E2%9D%8C+failed"
        status_message = "This skill is **not ready to share on Git**."
    elif warnings:
        badge_color = "yellow"
        badge_label = "%E2%9A%A0%EF%B8%8F+warnings"
        status_message = "This skill can be shared but improvements are recommended."
    else:
        badge_color = "brightgreen"
        badge_label = "%E2%9C%85+passed"
        status_message = "This skill is **ready to share on Git**."

    lines = [
        f"<!-- skill-proofing -->",
        f"![skill-proofing](https://img.shields.io/badge/skill--proofing-{badge_label}-{badge_color})",
        f"**Last checked:** {today} | **Score:** {passed}/{total_categories} categories passed",
        f"<!-- end skill-proofing -->",
        f"",
        f"## skill-proofing report — {skill_name}",
        f"",
        f"> {status_message}",
        f"",
    ]

    if fails:
        lines += ["### ❌ Hard Failures (must fix before sharing)", ""]
        for r in fails:
            lines.append(f"- [{r['code']}] {r['message']}")
        lines.append("")

    if warnings:
        lines += ["### ⚠️ Warnings (should fix)", ""]
        for r in warnings:
            lines.append(f"- [{r['code']}] {r['message']}")
        lines.append("")

    if infos:
        lines += ["### ℹ️ Info (nice to fix)", ""]
        for r in infos:
            lines.append(f"- [{r['code']}] {r['message']}")
        lines.append("")

    if not fails and not warnings and not infos:
        lines += ["### ✅ All checks passed — ready to share!", ""]

    report = "\n".join(lines)
    (skill_path / "proofing-report.md").write_text(report, encoding="utf-8")
    return report


# --- Entry point ---

def run(skill_path: str) -> str:
    path = Path(skill_path).expanduser().resolve()

    if not path.exists():
        return f"❌ Path not found: {path}"

    skill_md_path = path / "SKILL.md"
    if not skill_md_path.exists():
        return f"❌ No SKILL.md found in {path} — is this a valid skill directory?"

    skill_md = skill_md_path.read_text(encoding="utf-8", errors="ignore")
    all_files = _read_text_files(path)
    scripts = [(p, c) for p, c in all_files if p.suffix in (".py", ".sh")]

    results = (
        check_frontmatter(skill_md)
        + check_sections(skill_md)
        + check_structure(path)
        + check_credentials(all_files)
        + check_paths(all_files)
        + check_bash_safety(scripts)
        + check_exfiltration(scripts)
    )

    return generate_report(results, path)


def test_run():
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        skill_dir = Path(tmp) / "test-skill"
        skill_dir.mkdir()

        (skill_dir / "SKILL.md").write_text(
            "---\nname: test-skill\nversion: 1.0.0\nallowed-tools: [Read, Write]\n---\n"
            "# DESCRIPTION\nTest.\n# OBJECTIVES\nTest.\n"
            "# STRICT INSTRUCTIONS\nTest.\n# AVAILABLE TOOLS\nRead\n"
            "# EXPECTED FORMAT (I/O)\nInput: string\nOutput: string\n",
            encoding="utf-8",
        )
        (skill_dir / "schema.json").write_text(
            '{"name": "test-skill", "parameters": {"input": {"type": "string"}}}',
            encoding="utf-8",
        )
        tests_dir = skill_dir / "tests"
        tests_dir.mkdir()
        (tests_dir / "test_main.py").write_text("def test_run(): assert True\n", encoding="utf-8")

        result = run(str(skill_dir))
        assert "skill-proofing report" in result
        assert (skill_dir / "proofing-report.md").exists()
        print("OK:\n", result)


if __name__ == "__main__":
    test_run()
