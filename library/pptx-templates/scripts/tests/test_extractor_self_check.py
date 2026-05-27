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


def test_yaml_list_at_top_level_exits_3(tmp_path):
    """YAML list (not dict) at template level → exit 3, no traceback."""
    fix = tmp_path / "yaml_list"
    fix.mkdir()
    (fix / "meta.yaml.draft").write_text("- item1\n- item2\n")
    pages = fix / "pages" / "01-cover"
    pages.mkdir(parents=True)
    (pages / "meta.yaml.draft").write_text("status: draft\nlayout_type: cover\n")
    code, out = run("yaml_list", tmp_path)
    assert code == 3, f"{code}\n{out}"
    assert "YAML_NOT_A_DICT" in out


def test_null_provenance_does_not_crash(tmp_path):
    """provenance: null → caught as EMBEDDING_DIM_WRONG, not AttributeError."""
    fix = tmp_path / "null_prov"
    fix.mkdir()
    # Build minimal template with provenance: null
    (fix / "meta.yaml.draft").write_text(
        "status: draft\nid: null_prov\nname: x\ncategory: test\n"
        "content_intent: [x]\nwhen_to_use: [x]\nkeywords: [x]\n"
        "recommended_for: [x]\nvisual_signature: [x]\n"
        "provenance: null\nextraction: null\n"
    )
    pages = fix / "pages" / "01-cover"
    pages.mkdir(parents=True)
    (pages / "meta.yaml.draft").write_text(
        "status: draft\nconfidence: 0.9\nid: null_prov__01-cover\n"
        "name: x\nlayout_type: cover\ncontent_intent: [x]\nwhen_to_use: [x]\n"
        "keywords: [x]\nnative_elements: [x]\n"
    )
    code, out = run("null_prov", tmp_path)
    assert code == 1, f"{code}\n{out}"
    assert "Traceback" not in out
    assert "EMBEDDING_DIM_WRONG" in out


def test_null_layout_type_does_not_pass(tmp_path):
    """layout_type: null → LAYOUT_TYPE_INVALID, exit 1, not silent pass."""
    import shutil
    src = FIXTURES / "minimal_template_ok"
    dst = tmp_path / "null_layout"
    shutil.copytree(src, dst)
    page = dst / "pages" / "01-cover" / "meta.yaml.draft"
    page.write_text(page.read_text().replace("layout_type: cover", "layout_type: null"))
    code, out = run("null_layout", tmp_path)
    assert code == 1
    assert "LAYOUT_TYPE_INVALID" in out


def test_provenance_as_list_does_not_crash(tmp_path):
    """provenance: [a, b] (non-null non-dict) → no AttributeError, EMBEDDING_DIM_WRONG fires."""
    fix = tmp_path / "prov_list"
    fix.mkdir()
    (fix / "meta.yaml.draft").write_text(
        "status: draft\nid: prov_list\nname: x\ncategory: test\n"
        "content_intent: [x]\nwhen_to_use: [x]\nkeywords: [x]\n"
        "recommended_for: [x]\nvisual_signature: [x]\n"
        "provenance: [a, b]\nextraction: [c, d]\n"
    )
    pages = fix / "pages" / "01-cover"
    pages.mkdir(parents=True)
    (pages / "meta.yaml.draft").write_text(
        "status: draft\nconfidence: 0.9\nid: prov_list__01-cover\n"
        "name: x\nlayout_type: cover\ncontent_intent: [x]\nwhen_to_use: [x]\n"
        "keywords: [x]\nnative_elements: [x]\n"
    )
    code, out = run("prov_list", tmp_path)
    assert code == 1, f"{code}\n{out}"
    assert "Traceback" not in out
    assert "EMBEDDING_DIM_WRONG" in out


def test_pmap_tree_path_unresolvable_returns_2(tmp_path):
    """Construct a placeholder_map.draft with bad tree_path, verify exit code 2."""
    import shutil
    # Set up items/ root structure
    items_root = tmp_path / "items"
    items_root.mkdir()
    src = FIXTURES / "minimal_template_ok"
    dst = items_root / "minimal_template_ok"
    shutil.copytree(src, dst)
    # Place sample.pptx as _source/
    source_dir = tmp_path / "_source"
    source_dir.mkdir()
    shutil.copy(
        FIXTURES / "sample.pptx",
        source_dir / "minimal_template_ok.pptx",
    )
    # Write bad placeholder_map.draft (tree_path 99 doesn't exist)
    pmap_path = dst / "pages" / "01-cover" / "placeholder_map.yaml.draft"
    pmap_path.write_text(
        "template_page_index: 0\n"
        "layout_class: cover\n"
        "slots:\n"
        "  - id: title\n"
        "    tree_path: '99'\n"
        "    capacity_chars: 24\n"
    )
    code, out = run("minimal_template_ok", items_root)
    assert code == 2, f"{code}\n{out}"
    assert "PMAP_TREE_PATH_UNRESOLVABLE" in out


def test_pmap_valid_tree_path_passes(tmp_path):
    """A valid tree_path should not trigger PMAP error."""
    import shutil
    items_root = tmp_path / "items"
    items_root.mkdir()
    src = FIXTURES / "minimal_template_ok"
    dst = items_root / "minimal_template_ok"
    shutil.copytree(src, dst)
    source_dir = tmp_path / "_source"
    source_dir.mkdir()
    shutil.copy(
        FIXTURES / "sample.pptx",
        source_dir / "minimal_template_ok.pptx",
    )
    # tree_path '0' is the first shape on page 0 of sample.pptx (the title textbox)
    pmap_path = dst / "pages" / "01-cover" / "placeholder_map.yaml.draft"
    pmap_path.write_text(
        "template_page_index: 0\n"
        "layout_class: cover\n"
        "slots:\n"
        "  - id: title\n"
        "    tree_path: '0'\n"
        "    capacity_chars: 24\n"
    )
    code, out = run("minimal_template_ok", items_root)
    assert code == 0, f"{code}\n{out}"


def test_pmap_check_skipped_when_no_source(tmp_path):
    """If _source/<name>.pptx doesn't exist, PMAP check is skipped (no false positive)."""
    import shutil
    items_root = tmp_path / "items"
    items_root.mkdir()
    src = FIXTURES / "minimal_template_ok"
    dst = items_root / "minimal_template_ok"
    shutil.copytree(src, dst)
    # No _source/ dir created
    # Write a placeholder_map.draft with bad tree_path
    pmap_path = dst / "pages" / "01-cover" / "placeholder_map.yaml.draft"
    pmap_path.write_text(
        "template_page_index: 0\n"
        "layout_class: cover\n"
        "slots:\n"
        "  - id: title\n"
        "    tree_path: '99'\n"
        "    capacity_chars: 24\n"
    )
    code, out = run("minimal_template_ok", items_root)
    # Should pass (no source = check skipped)
    assert code == 0, f"{code}\n{out}"


def test_extraction_bool_rejected_as_non_int(tmp_path):
    """declared_pages: true / rendered_pages: false → EXTRACTION_TYPE_INVALID, not silent pass."""
    import shutil
    src = FIXTURES / "minimal_template_ok"
    dst = tmp_path / "ext_bool"
    shutil.copytree(src, dst)
    tpl = dst / "meta.yaml.draft"
    tpl.write_text(
        tpl.read_text()
        .replace("declared_pages: 1", "declared_pages: true")
        .replace("rendered_pages: 1", "rendered_pages: false")
        .replace("discrepancy: 0", "discrepancy: true")
    )
    code, out = run("ext_bool", tmp_path)
    assert code == 1, f"{code}\n{out}"
    assert "EXTRACTION_TYPE_INVALID" in out
