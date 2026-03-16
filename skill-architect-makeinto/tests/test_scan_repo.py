"""
Tests for scan_repo.py
"""

import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
from scan_repo import scan


def test_scan_single_file():
    """scan() on a single .py file should return exactly 1 result."""
    result = scan(__file__)
    assert isinstance(result, list), "Result must be a list"
    assert len(result) == 1, f"Expected 1 file, got {len(result)}"
    assert result[0]["language"] == "python"
    assert result[0]["name"] == os.path.basename(__file__)
    print("OK: test_scan_single_file")


def test_scan_directory():
    """scan() on a directory with known source files should return them."""
    scripts_dir = os.path.join(os.path.dirname(__file__), '..', 'scripts')
    result = scan(scripts_dir)
    assert isinstance(result, list)
    assert len(result) >= 2, f"Expected at least 2 scripts, got {len(result)}"
    names = [f["name"] for f in result]
    assert "scan_repo.py" in names, "scan_repo.py should be found"
    assert "infer_skill.py" in names, "infer_skill.py should be found"
    print(f"OK: test_scan_directory — {len(result)} files found")


def test_scan_filters_noise():
    """scan() should skip .log, .png, and lock files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create noise files
        for fname in ["package-lock.json", "debug.log", "image.png", "data.bin"]:
            open(os.path.join(tmpdir, fname), 'w').close()
        # Create one real source file
        with open(os.path.join(tmpdir, "main.py"), 'w') as f:
            f.write("def hello(): pass\n")

        result = scan(tmpdir)
        names = [f["name"] for f in result]
        assert "main.py" in names, "main.py should be included"
        assert "package-lock.json" not in names
        assert "debug.log" not in names
        assert "image.png" not in names
        print("OK: test_scan_filters_noise")


def test_scan_nonexistent_path():
    """scan() on a non-existent path should raise FileNotFoundError."""
    try:
        scan("/nonexistent/path/that/does/not/exist")
        assert False, "Should have raised FileNotFoundError"
    except FileNotFoundError:
        print("OK: test_scan_nonexistent_path")


if __name__ == "__main__":
    test_scan_single_file()
    test_scan_directory()
    test_scan_filters_noise()
    test_scan_nonexistent_path()
    print("\nAll scan_repo tests passed.")
