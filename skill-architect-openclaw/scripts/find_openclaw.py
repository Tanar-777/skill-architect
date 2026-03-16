"""
find_openclaw.py
Scans for OpenClaw repository directories on the local filesystem.
Used by the skill-architect-openclaw skill during first-run path resolution.
"""

from pathlib import Path

SEARCH_PATTERNS = ["openclaw", "OpenClaw", "open-claw"]
MAX_DEPTH = 6


def _within_depth(path: Path, base: Path, max_depth: int) -> bool:
    try:
        relative = path.relative_to(base)
        return len(relative.parts) <= max_depth
    except ValueError:
        return False


def find_openclaw_repo(start_path: str = None, machine_wide: bool = False) -> list[str]:
    """
    Scan for OpenClaw repo directories containing a 'skills/' subdirectory.

    Args:
        start_path: Directory to start scanning from. Defaults to user home.
        machine_wide: If True, scan from filesystem root (requires user permission).

    Returns:
        List of confirmed 'skills/' paths inside OpenClaw repos.
    """
    base = Path(start_path) if start_path else Path.home()
    search_root = Path("/") if machine_wide else base
    results = []

    for pattern in SEARCH_PATTERNS:
        try:
            for match in search_root.rglob(f"*{pattern}*"):
                if not _within_depth(match, search_root, MAX_DEPTH):
                    continue
                if match.is_dir() and (match / "skills").exists():
                    skills_path = str(match / "skills")
                    if skills_path not in results:
                        results.append(skills_path)
        except PermissionError:
            continue

    return results


def test_find_openclaw():
    results = find_openclaw_repo()
    assert isinstance(results, list)
    print("OK:", results if results else "No OpenClaw repo found (expected in test env)")


if __name__ == "__main__":
    test_find_openclaw()
