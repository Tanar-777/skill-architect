"""
Tests for skill-architect-multy-plan utilities.
Covers YAML frontmatter parsing, skill name validation,
dependency cycle detection, and plan status transitions.
"""

import re
import yaml


def parse_frontmatter(content: str) -> dict:
    """Extract and parse YAML frontmatter from a plan file."""
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return {}
    return yaml.safe_load(match.group(1))


def validate_skill_name(name: str) -> bool:
    """Validate skill name: lowercase, hyphens only, max 64 chars."""
    return bool(re.match(r'^[a-z][a-z0-9-]{0,63}$', name))


def detect_cycles(skills: list) -> list:
    """
    Detect circular dependencies in a skill list.
    Returns list of cycle paths, empty list if acyclic.
    """
    graph = {s['name']: s.get('depends_on', []) for s in skills}
    visited, stack, cycles = set(), [], []

    def dfs(node, path):
        if node in stack:
            cycle_start = path.index(node)
            cycles.append(path[cycle_start:] + [node])
            return
        if node in visited:
            return
        visited.add(node)
        stack.append(node)
        for dep in graph.get(node, []):
            dfs(dep, path + [node])
        stack.pop()

    for node in graph:
        if node not in visited:
            dfs(node, [])
    return cycles


def topological_sort(skills: list) -> list:
    """
    Return skills in dependency order (no dependencies first).
    Raises ValueError if cycles are detected.
    """
    cycles = detect_cycles(skills)
    if cycles:
        raise ValueError(f"Circular dependency detected: {cycles[0]}")

    graph = {s['name']: s.get('depends_on', []) for s in skills}
    skill_map = {s['name']: s for s in skills}
    visited, result = set(), []

    def visit(name):
        if name in visited:
            return
        for dep in graph.get(name, []):
            visit(dep)
        visited.add(name)
        result.append(skill_map[name])

    for s in skills:
        visit(s['name'])
    return result


def validate_status_transition(current: str, next_status: str) -> bool:
    """
    Validate allowed plan status transitions.
    draft → approved → in_progress → complete
    """
    allowed = {
        'draft': ['approved'],
        'approved': ['in_progress', 'draft'],
        'in_progress': ['complete', 'approved'],
        'complete': [],
    }
    return next_status in allowed.get(current, [])


# --- Tests ---

def test_parse_frontmatter():
    sample = "---\nsuite: my-suite\nplan_version: 1.0\nstatus: draft\n---\n# Body"
    result = parse_frontmatter(sample)
    assert result['suite'] == 'my-suite'
    assert result['plan_version'] == 1.0
    assert result['status'] == 'draft'
    print("OK: parse_frontmatter")


def test_parse_frontmatter_missing():
    result = parse_frontmatter("# No frontmatter here")
    assert result == {}
    print("OK: parse_frontmatter_missing")


def test_validate_skill_name_valid():
    assert validate_skill_name("my-skill") is True
    assert validate_skill_name("data-pipeline-ingest") is True
    assert validate_skill_name("a") is True
    print("OK: validate_skill_name_valid")


def test_validate_skill_name_invalid():
    assert validate_skill_name("My-Skill") is False       # uppercase
    assert validate_skill_name("my skill") is False       # space
    assert validate_skill_name("a" * 65) is False         # too long
    assert validate_skill_name("123-skill") is False      # starts with digit
    print("OK: validate_skill_name_invalid")


def test_detect_cycles_clean():
    skills = [
        {'name': 'a', 'depends_on': []},
        {'name': 'b', 'depends_on': ['a']},
        {'name': 'c', 'depends_on': ['b']},
    ]
    assert detect_cycles(skills) == []
    print("OK: detect_cycles_clean")


def test_detect_cycles_with_cycle():
    skills = [
        {'name': 'a', 'depends_on': ['b']},
        {'name': 'b', 'depends_on': ['a']},
    ]
    cycles = detect_cycles(skills)
    assert len(cycles) > 0
    print("OK: detect_cycles_with_cycle")


def test_topological_sort():
    skills = [
        {'name': 'c', 'depends_on': ['b']},
        {'name': 'a', 'depends_on': []},
        {'name': 'b', 'depends_on': ['a']},
    ]
    result = topological_sort(skills)
    names = [s['name'] for s in result]
    assert names.index('a') < names.index('b')
    assert names.index('b') < names.index('c')
    print("OK: topological_sort")


def test_validate_status_transition():
    assert validate_status_transition('draft', 'approved') is True
    assert validate_status_transition('approved', 'in_progress') is True
    assert validate_status_transition('in_progress', 'complete') is True
    assert validate_status_transition('complete', 'draft') is False
    assert validate_status_transition('draft', 'complete') is False
    print("OK: validate_status_transition")


if __name__ == "__main__":
    test_parse_frontmatter()
    test_parse_frontmatter_missing()
    test_validate_skill_name_valid()
    test_validate_skill_name_invalid()
    test_detect_cycles_clean()
    test_detect_cycles_with_cycle()
    test_topological_sort()
    test_validate_status_transition()
    print("\nAll tests passed.")
