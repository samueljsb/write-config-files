from __future__ import annotations

import os
from pathlib import Path
from unittest import mock

from pytest import CaptureFixture

from write_config_files import cli

PLAIN_FILE_CONTENT = """\
some text and a newline
"""


def _setup(template_dir: Path, output_dir: Path, tmp_path: Path) -> tuple[Path, Path]:
    new_template = template_dir / 'new_file.txt'
    new_template.write_text(PLAIN_FILE_CONTENT)

    existing_template = template_dir / 'existing_file.txt'
    existing_template.write_text(PLAIN_FILE_CONTENT)
    existing_file = output_dir / 'existing_file.txt'
    existing_file.write_text(PLAIN_FILE_CONTENT)

    custom_subdir_template = template_dir / 'file_in_custom_subdir.txt'
    custom_subdir_template.write_text(PLAIN_FILE_CONTENT)

    abs_path_template = template_dir / 'file_with_abs_path.txt'
    abs_path_template.write_text(PLAIN_FILE_CONTENT)

    templates_file = tmp_path / 'templates.yaml'
    templates_file.write_text(
        f"""\
root_template_dir: {template_dir}
config_files:
-   output_dir: {output_dir}
    templates:
    -   template: new_file.txt
    -   template: existing_file.txt
    -   template: file_in_custom_subdir.txt
        destination: subdir/custom.txt
    -   template: file_with_abs_path.txt
        destination: /{template_dir}/elsewhere/absolute.txt
context:
""",
    )

    context_file = tmp_path / 'context.yaml'
    context_file.write_text('{}')

    return templates_file, context_file


def test_write(
    template_dir: Path,
    output_dir: Path,
    tmp_path: Path,
    capfd: CaptureFixture[str],
):
    templates_file, context_file = _setup(template_dir, output_dir, tmp_path)

    ret = cli.main(['write', '-t', str(templates_file), '-c', str(context_file)])

    assert ret == 0

    captured = capfd.readouterr()
    assert captured.out == ''
    assert (
        captured.err
        == f"""\
\033[0mwriting {output_dir}/new_file.txt\033[0m
\033[2mskipping {output_dir}/existing_file.txt because it already exists\033[0m
\033[0mwriting {output_dir}/subdir/custom.txt\033[0m
\033[0mwriting /{template_dir}/elsewhere/absolute.txt\033[0m
"""
    )


def test_write_no_color(
    template_dir: Path,
    output_dir: Path,
    tmp_path: Path,
    capfd: CaptureFixture[str],
):
    templates_file, context_file = _setup(template_dir, output_dir, tmp_path)

    with mock.patch.dict(os.environ, {'NO_COLOR': '1'}):
        ret = cli.main(['write', '-t', str(templates_file), '-c', str(context_file)])

    assert ret == 0

    captured = capfd.readouterr()
    assert captured.out == ''
    assert (
        captured.err
        == f"""\
writing {output_dir}/new_file.txt
skipping {output_dir}/existing_file.txt because it already exists
writing {output_dir}/subdir/custom.txt
writing /{template_dir}/elsewhere/absolute.txt
"""
    )


def test_write_force(
    template_dir: Path,
    output_dir: Path,
    tmp_path: Path,
    capfd: CaptureFixture[str],
):
    templates_file, context_file = _setup(template_dir, output_dir, tmp_path)

    ret = cli.main(
        ['write', '-t', str(templates_file), '-c', str(context_file), '-f'],
    )

    assert ret == 0

    captured = capfd.readouterr()
    assert captured.out == ''
    assert (
        captured.err
        == f"""\
\033[0mwriting {output_dir}/new_file.txt\033[0m
\033[93moverwriting {output_dir}/existing_file.txt\033[0m
\033[0mwriting {output_dir}/subdir/custom.txt\033[0m
\033[0mwriting /{template_dir}/elsewhere/absolute.txt\033[0m
"""
    )


def test_write_dry_run(
    template_dir: Path,
    output_dir: Path,
    tmp_path: Path,
    capfd: CaptureFixture[str],
):
    templates_file, context_file = _setup(template_dir, output_dir, tmp_path)

    ret = cli.main(
        ['write', '-t', str(templates_file), '-c', str(context_file), '-d'],
    )

    assert ret == 0

    captured = capfd.readouterr()
    assert captured.out == ''
    assert (
        captured.err
        == f"""\
\033[0mwould write {output_dir}/new_file.txt\033[0m
\033[2mskipping {output_dir}/existing_file.txt because it already exists\033[0m
\033[0mwould write {output_dir}/subdir/custom.txt\033[0m
\033[0mwould write /{template_dir}/elsewhere/absolute.txt\033[0m
"""
    )


def test_write_force_dry_run(
    template_dir: Path,
    output_dir: Path,
    tmp_path: Path,
    capfd: CaptureFixture[str],
):
    templates_file, context_file = _setup(template_dir, output_dir, tmp_path)

    ret = cli.main(
        ['write', '-t', str(templates_file), '-c', str(context_file), '-fd'],
    )

    assert ret == 0

    captured = capfd.readouterr()
    assert captured.out == ''
    assert (
        captured.err
        == f"""\
\033[0mwould write {output_dir}/new_file.txt\033[0m
\033[93mwould overwrite {output_dir}/existing_file.txt\033[0m
\033[0mwould write {output_dir}/subdir/custom.txt\033[0m
\033[0mwould write /{template_dir}/elsewhere/absolute.txt\033[0m
"""
    )
