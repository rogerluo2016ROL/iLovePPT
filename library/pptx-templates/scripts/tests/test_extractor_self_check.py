import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).parent.parent / "extractor_self_check.py"
FIXTURES = Path(__file__).parent / "fixtures"


def run(name: str, fixture_root: Path) -> tuple[int, str]:
    """运行 self_check 脚本,返回 (exit_code, stdout+stderr)."""
    r = subprocess.run(
        [sys.executable, str(SCRIPT), name, "--items-root", str(fixture_root)],
        capture_output=True, text=True,
    )
    return r.returncode, r.stdout + r.stderr


def test_ok_fixture_passes():
    code, out = run("minimal_template_ok", FIXTURES)
    assert code == 0, f"expected exit 0, got {code}\n{out}"


def test_bad_enum_fails_with_code_1():
    code, out = run("bad_enum", FIXTURES)
    assert code == 1, f"expected exit 1, got {code}\n{out}"
    assert "ENUM_VIOLATION" in out
    assert "comparison_venn" in out


def test_bad_yaml_fails_with_code_3():
    code, out = run("bad_yaml", FIXTURES)
    assert code == 3, f"expected exit 3, got {code}\n{out}"
    assert "YAML_SYNTAX_ERROR" in out


def test_missing_fields_fails_with_code_1():
    code, out = run("missing_fields", FIXTURES)
    assert code == 1, f"expected exit 1, got {code}\n{out}"
    assert "MISSING_PAGE_FIELD" in out
    assert "keywords" in out


def test_nonexistent_template_fails_with_code_4():
    code, out = run("does_not_exist", FIXTURES)
    assert code == 4
    assert "TEMPLATE_NOT_FOUND" in out
