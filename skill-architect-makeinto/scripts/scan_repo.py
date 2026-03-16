"""
scan_repo.py — Walk a directory and return relevant source files for skill inference.
Filters out non-source files, binaries, and common noise directories.
"""

import os
import sys
import json

IGNORE_DIRS = {
    '.git', 'node_modules', '__pycache__', 'dist', 'build',
    'venv', '.venv', '.tox', '.mypy_cache', '.pytest_cache',
    'coverage', '.next', '.nuxt', 'out', 'target'
}

IGNORE_EXTENSIONS = {
    '.lock', '.log', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico',
    '.bin', '.exe', '.whl', '.zip', '.tar', '.gz', '.env',
    '.DS_Store', '.pyc', '.pyo', '.class', '.o', '.so', '.dll',
    '.pdf', '.docx', '.xlsx', '.mov', '.mp4', '.mp3'
}

SOURCE_EXTENSIONS = {
    '.py': 'python',
    '.js': 'javascript',
    '.ts': 'typescript',
    '.jsx': 'javascript',
    '.tsx': 'typescript',
    '.rb': 'ruby',
    '.go': 'go',
    '.java': 'java',
    '.cs': 'csharp',
    '.cpp': 'cpp',
    '.c': 'c',
    '.rs': 'rust',
    '.sh': 'shell',
    '.bash': 'shell',
    '.php': 'php',
    '.swift': 'swift',
    '.kt': 'kotlin',
}

IGNORE_FILES = {
    'package-lock.json', 'yarn.lock', 'poetry.lock', 'Pipfile.lock',
    '.gitignore', '.gitattributes', '.editorconfig', 'LICENSE', 'CHANGELOG.md'
}


def scan(path: str) -> list:
    """
    Walk the given path and return a list of relevant source file metadata.

    Args:
        path: Absolute or relative path to a file or directory.

    Returns:
        List of dicts: [{"path": str, "language": str, "size": int, "name": str}]
    """
    path = os.path.abspath(path)

    if not os.path.exists(path):
        raise FileNotFoundError(f"Path does not exist: {path}")

    # Single file
    if os.path.isfile(path):
        ext = os.path.splitext(path)[1].lower()
        language = SOURCE_EXTENSIONS.get(ext, 'unknown')
        return [{
            "path": path,
            "name": os.path.basename(path),
            "language": language,
            "size": os.path.getsize(path)
        }]

    # Directory walk
    results = []
    for root, dirs, files in os.walk(path, followlinks=False):
        # Prune ignored directories in-place
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS and not d.startswith('.')]

        for fname in files:
            if fname in IGNORE_FILES:
                continue

            ext = os.path.splitext(fname)[1].lower()

            if ext in IGNORE_EXTENSIONS:
                continue

            if ext not in SOURCE_EXTENSIONS:
                continue

            full_path = os.path.join(root, fname)
            results.append({
                "path": full_path,
                "name": fname,
                "language": SOURCE_EXTENSIONS[ext],
                "size": os.path.getsize(full_path)
            })

    return results


def test_scan():
    result = scan(".")
    assert isinstance(result, list), "scan() must return a list"
    assert all("path" in f for f in result), "Each entry must have 'path'"
    assert all("language" in f for f in result), "Each entry must have 'language'"
    print(f"OK: {len(result)} source files found")
    for f in result[:5]:
        print(f"  {f['language']:12} {f['name']}")
    if len(result) > 5:
        print(f"  ... and {len(result) - 5} more")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        test_scan()
    else:
        try:
            files = scan(sys.argv[1])
            print(json.dumps(files, indent=2))
        except FileNotFoundError as e:
            print(json.dumps({"error": str(e)}))
            sys.exit(1)
