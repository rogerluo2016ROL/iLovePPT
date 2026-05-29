"""组件 A(P0-3)· builder 静默吞错 → fail-loud 可见性测试。"""
import importlib

base = importlib.import_module("builder.base")


def test_warn_appends_and_prints(capsys):
    base.BUILD_WARNINGS.clear()
    base._warn("builder.token-extract", "示例消息")
    captured = capsys.readouterr()
    assert base.BUILD_WARNINGS == ["[builder.token-extract] WARN 示例消息"]
    assert "[builder.token-extract] WARN 示例消息" in captured.err
    assert captured.out == ""  # 必须走 stderr 不污染 stdout
