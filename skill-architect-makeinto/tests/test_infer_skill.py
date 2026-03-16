"""
Tests for infer_skill.py
"""

import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
from infer_skill import infer, slugify


def test_infer_self():
    """infer() on infer_skill.py itself should find known functions."""
    script_path = os.path.join(os.path.dirname(__file__), '..', 'scripts', 'infer_skill.py')
    result = infer(script_path)
    assert "error" not in result, f"Unexpected error: {result.get('error')}"
    assert "suggested_name" in result
    assert "functions" in result
    function_names = [f["name"] for f in result["functions"]]
    assert "infer" in function_names, f"Expected 'infer' in functions, got: {function_names}"
    assert result["language"] == "python"
    print(f"OK: test_infer_self — found {len(result['functions'])} functions")


def test_infer_simple_python():
    """infer() on a simple Python file should extract function metadata."""
    with tempfile.NamedTemporaryFile(suffix='.py', mode='w', delete=False) as f:
        f.write('''"""A simple math utility."""

def add(x: int, y: int) -> int:
    """Add two numbers."""
    return x + y

def multiply(x: int, y: int) -> int:
    """Multiply two numbers."""
    return x * y
''')
        tmp_path = f.name

    try:
        result = infer(tmp_path)
        assert "error" not in result
        assert result["language"] == "python"
        function_names = [f["name"] for f in result["functions"]]
        assert "add" in function_names
        assert "multiply" in function_names
        assert result["description"] == "A simple math utility."
        print(f"OK: test_infer_simple_python — {result['suggested_name']}, {len(result['functions'])} functions")
    finally:
        os.unlink(tmp_path)


def test_infer_nonexistent_file():
    """infer() on a non-existent file should return an error dict."""
    result = infer("/nonexistent/file.py")
    assert "error" in result, "Expected error for missing file"
    print("OK: test_infer_nonexistent_file")


def test_slugify():
    """slugify() should produce valid skill name slugs."""
    assert slugify("MyScript") == "myscript"
    assert slugify("my_script") == "my-script"
    assert slugify("My Script Here") == "my-script-here"
    assert slugify("foo--bar") == "foo-bar"
    assert len(slugify("a" * 100)) <= 64
    print("OK: test_slugify")


def test_infer_side_effects():
    """infer() should detect file write side effects."""
    with tempfile.NamedTemporaryFile(suffix='.py', mode='w', delete=False) as f:
        f.write('''def save_data(path):
    with open(path, "w") as f:
        f.write("data")
''')
        tmp_path = f.name

    try:
        result = infer(tmp_path)
        assert "file write" in result.get("side_effects", ""), \
            f"Expected 'file write' in side_effects, got: {result.get('side_effects')}"
        print("OK: test_infer_side_effects")
    finally:
        os.unlink(tmp_path)


if __name__ == "__main__":
    test_infer_self()
    test_infer_simple_python()
    test_infer_nonexistent_file()
    test_slugify()
    test_infer_side_effects()
    print("\nAll infer_skill tests passed.")
