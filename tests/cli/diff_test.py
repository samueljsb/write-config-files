from __future__ import annotations

from pathlib import Path

import pytest
from pytest import CaptureFixture

from write_config_files import cli


def _setup(template_dir: Path, output_dir: Path, tmp_path: Path) -> tuple[Path, Path]:
    unchanged_template = template_dir / 'unchanged_file.txt'
    unchanged_template.write_text(
        """\
some text and a newline
""",
    )
    unchanged_file = output_dir / 'unchanged_file.txt'
    unchanged_file.write_text(
        """\
some text and a newline
""",
    )

    changed_template = template_dir / 'changed_file.txt'
    changed_template.write_text(
        """\
some text and a newline
""",
    )
    changed_file = output_dir / 'changed_file.txt'
    changed_file.write_text(
        """\
different text and a newline
""",
    )

    new_template = template_dir / 'new_file.txt'
    new_template.write_text(
        """\
some text and a newline
""",
    )

    templates_file = tmp_path / 'templates.yaml'
    templates_file.write_text(
        f"""\
root_template_dir: {template_dir}
config_files:
-   output_dir: {output_dir}
    templates:
    -   template: unchanged_file.txt
    -   template: changed_file.txt
    -   template: new_file.txt
""",
    )

    context_file = tmp_path / 'context.yaml'
    context_file.write_text('{}')

    return templates_file, context_file


@pytest.mark.parametrize(
    'args', (
        (),
        ('-p', 'cat'),
    ),
)
def test_diff(
    args: tuple[str, ...],
    template_dir: Path,
    output_dir: Path,
    tmp_path: Path,
    capfd: CaptureFixture[str],
):
    templates_file, context_file = _setup(template_dir, output_dir, tmp_path)

    ret = cli.main(
        ['diff', '-t', str(templates_file), '-c', str(context_file), *args],
    )

    assert ret == 0

    captured = capfd.readouterr()
    assert captured.out == f"""\
--- {output_dir}/changed_file.txt
+++ {output_dir}/changed_file.txt
@@ -1 +1 @@
-different text and a newline
+some text and a newline
--- {output_dir}/new_file.txt
+++ {output_dir}/new_file.txt
@@ -0,0 +1 @@
+some text and a newline
"""
