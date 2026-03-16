"""
infer_skill.py — Parse a source file and extract skill metadata.
Extracts functions, classes, docstrings, parameters, return types, and infers a skill name/description.
"""

import ast
import os
import re
import sys
import json


def slugify(name: str) -> str:
    """Convert a name to a valid skill slug (lowercase, hyphens, max 64 chars)."""
    name = name.lower()
    name = re.sub(r'[_\s]+', '-', name)
    name = re.sub(r'[^a-z0-9-]', '', name)
    name = re.sub(r'-+', '-', name).strip('-')
    return name[:64]


def infer_python(file_path: str, source: str) -> dict:
    """Parse a Python file using AST and extract structured metadata."""
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        return {"error": f"Python syntax error: {e}"}

    functions = []
    classes = []
    imports = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            else:
                module = node.module or ''
                imports.append(module)

    for node in tree.body:
        if isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
            params = []
            for arg in node.args.args:
                if arg.arg == 'self':
                    continue
                annotation = ''
                if arg.annotation:
                    try:
                        annotation = ast.unparse(arg.annotation)
                    except Exception:
                        annotation = ''
                params.append({"name": arg.arg, "type": annotation})

            returns = ''
            if node.returns:
                try:
                    returns = ast.unparse(node.returns)
                except Exception:
                    returns = ''

            docstring = ast.get_docstring(node) or ''

            functions.append({
                "name": node.name,
                "params": params,
                "returns": returns,
                "docstring": docstring[:256]
            })

        elif isinstance(node, ast.ClassDef):
            methods = []
            class_docstring = ast.get_docstring(node) or ''

            for item in node.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    method_params = []
                    for arg in item.args.args:
                        if arg.arg == 'self':
                            continue
                        annotation = ''
                        if arg.annotation:
                            try:
                                annotation = ast.unparse(arg.annotation)
                            except Exception:
                                annotation = ''
                        method_params.append({"name": arg.arg, "type": annotation})

                    method_returns = ''
                    if item.returns:
                        try:
                            method_returns = ast.unparse(item.returns)
                        except Exception:
                            method_returns = ''

                    methods.append({
                        "name": item.name,
                        "params": method_params,
                        "returns": method_returns,
                        "docstring": (ast.get_docstring(item) or '')[:256]
                    })

            classes.append({
                "name": node.name,
                "methods": methods,
                "docstring": class_docstring[:256]
            })

    return {
        "functions": functions,
        "classes": classes,
        "imports": list(set(imports))[:20]
    }


def infer_generic(source: str, language: str) -> dict:
    """Basic regex-based extraction for non-Python files."""
    patterns = {
        'javascript': r'(?:function\s+(\w+)|const\s+(\w+)\s*=\s*(?:async\s*)?\(?)',
        'typescript': r'(?:function\s+(\w+)|const\s+(\w+)\s*=\s*(?:async\s*)?\(?|(?:export\s+)?(?:async\s+)?function\s+(\w+))',
        'go': r'func\s+(?:\(\w+\s+\*?\w+\)\s+)?(\w+)\s*\(',
        'ruby': r'def\s+(\w+)',
        'java': r'(?:public|private|protected|static|\s)+[\w<>\[\]]+\s+(\w+)\s*\(',
        'rust': r'fn\s+(\w+)\s*[<(]',
        'shell': r'^(?:function\s+)?(\w+)\s*\(\)',
    }

    pattern = patterns.get(language, r'(?:function|def|fn)\s+(\w+)')
    functions = []

    for match in re.finditer(pattern, source, re.MULTILINE):
        name = next((g for g in match.groups() if g), None)
        if name and not name.startswith('_'):
            functions.append({"name": name, "params": [], "returns": "", "docstring": ""})

    return {"functions": functions, "classes": [], "imports": []}


def detect_language(file_path: str) -> str:
    ext_map = {
        '.py': 'python', '.js': 'javascript', '.ts': 'typescript',
        '.jsx': 'javascript', '.tsx': 'typescript', '.rb': 'ruby',
        '.go': 'go', '.java': 'java', '.rs': 'rust', '.sh': 'shell',
        '.bash': 'shell', '.php': 'php', '.cs': 'csharp',
    }
    ext = os.path.splitext(file_path)[1].lower()
    return ext_map.get(ext, 'unknown')


def infer(file_path: str) -> dict:
    """
    Parse a source file and return extracted skill metadata.

    Args:
        file_path: Path to the source file.

    Returns:
        Dict with: suggested_name, description, language, functions, classes, imports, side_effects
    """
    file_path = os.path.abspath(file_path)

    if not os.path.exists(file_path):
        return {"error": f"File not found: {file_path}"}

    with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
        source = f.read()

    language = detect_language(file_path)
    base_name = os.path.splitext(os.path.basename(file_path))[0]

    if language == 'python':
        extracted = infer_python(file_path, source)
    else:
        extracted = infer_generic(source, language)

    if "error" in extracted:
        return extracted

    functions = extracted.get("functions", [])
    classes = extracted.get("classes", [])
    imports = extracted.get("imports", [])

    # Infer description from module-level docstring or first function docstring
    description = ""
    if language == 'python':
        try:
            tree = ast.parse(source)
            description = ast.get_docstring(tree) or ""
        except Exception:
            pass

    if not description and functions:
        description = functions[0].get("docstring", "")

    if not description:
        description = f"Skill generated from {os.path.basename(file_path)}"

    # Detect side effects heuristically
    side_effects = []
    side_effect_signals = {
        'file write': ['open(', 'write(', 'os.remove', 'shutil.', 'Path('],
        'network': ['requests.', 'urllib', 'httpx', 'aiohttp', 'socket'],
        'database': ['sqlite3', 'psycopg2', 'sqlalchemy', 'cursor.execute'],
        'subprocess': ['subprocess', 'os.system', 'os.popen'],
    }
    for effect, signals in side_effect_signals.items():
        if any(s in source for s in signals):
            side_effects.append(effect)

    suggested_name = slugify(base_name)

    return {
        "suggested_name": suggested_name,
        "description": description[:1024],
        "language": language,
        "functions": functions,
        "classes": classes,
        "imports": imports,
        "side_effects": ', '.join(side_effects) if side_effects else "none detected"
    }


def test_infer():
    result = infer(__file__)
    assert "suggested_name" in result, "Missing 'suggested_name'"
    assert "functions" in result, "Missing 'functions'"
    assert isinstance(result["functions"], list), "'functions' must be a list"
    assert len(result["functions"]) > 0, "Should find at least one function in this file"
    print(f"OK: inferred '{result['suggested_name']}' — {len(result['functions'])} functions")
    print(f"    Description: {result['description'][:80]}...")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        test_infer()
    else:
        try:
            result = infer(sys.argv[1])
            print(json.dumps(result, indent=2))
        except Exception as e:
            print(json.dumps({"error": str(e)}))
            sys.exit(1)
