"""Every Python example in README.md must run against the current code.

README.md is the project page on PyPI. Its quickstart once called ``TaskReporter`` with
arguments that no longer existed and showed two operations whose outputs each left the
other field in clear text; nothing noticed. Each ```python block is executed here as-is,
in its own namespace, inside a temporary working directory.
"""

import re
from pathlib import Path

import pytest

README = Path(__file__).resolve().parents[1] / "README.md"
BLOCKS = re.findall(r"```python\n(.*?)```", README.read_text(encoding="utf-8"), re.S)


def test_readme_has_python_examples():
    assert len(BLOCKS) >= 3


@pytest.mark.parametrize("code", BLOCKS, ids=[f"block{i}" for i in range(len(BLOCKS))])
def test_readme_python_block_runs(code, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    exec(compile(code, f"README.md:{code[:40]!r}", "exec"), {"__name__": "__readme__"})
