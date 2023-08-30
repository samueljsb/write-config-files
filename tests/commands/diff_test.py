from __future__ import annotations

from testing.files import FakeFileSystem
from testing.printing import CapturedPrinter
from testing.rendering import FakeRenderer
from write_config_files.commands.diff import Differ
from write_config_files.config import TemplateConfig
from write_config_files.config import TemplateFile


def test_diff_when_no_change():
    reader = FakeFileSystem(files={'no-change': 'file content\n'})
    printer = CapturedPrinter()

    templates = TemplateConfig(
        root_dir='',
        files=(TemplateFile('', 'no-change', False),),
    )

    differ = Differ(
        reader=reader,
        renderer=FakeRenderer('file content\n'),
        printer=printer,
    )
    differ.print_diff(templates=templates)

    assert printer.diffs == []


def test_diff_when_file_changed():
    reader = FakeFileSystem(files={'has-change': 'different content\n'})
    printer = CapturedPrinter()

    templates = TemplateConfig(
        root_dir='',
        files=(TemplateFile('', 'has-change', False),),
    )

    differ = Differ(
        reader=reader,
        renderer=FakeRenderer('file content\n'),
        printer=printer,
    )
    differ.print_diff(templates=templates)

    assert printer.diffs == [
        [
            '--- has-change\n',
            '+++ has-change\n',
            '@@ -1 +1 @@\n',
            '-different content\n',
            '+file content\n',
        ],
    ]


def test_diff_for_new_file():
    reader = FakeFileSystem(files={})
    printer = CapturedPrinter()

    templates = TemplateConfig(
        root_dir='',
        files=(TemplateFile('', 'new-file', False),),
    )

    differ = Differ(
        reader=reader,
        renderer=FakeRenderer('file content\n'),
        printer=printer,
    )
    differ.print_diff(templates=templates)

    assert printer.diffs == [
        [
            '--- new-file\n',
            '+++ new-file\n',
            '@@ -0,0 +1 @@\n',
            '+file content\n',
        ],
    ]
