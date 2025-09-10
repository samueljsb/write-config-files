from __future__ import annotations

from testing.files import FakeFileSystem
from testing.logging import CapturedLogger
from testing.rendering import FakeRenderer
from write_config_files.commands.write import Writer
from write_config_files.config import TemplateConfig
from write_config_files.config import TemplateFile


def test_write_file() -> None:
    file_system = FakeFileSystem()
    logger = CapturedLogger()

    templates = TemplateConfig(
        root_dir='',
        files=(
            TemplateFile('templates/config-file', 'output/config-file', False),
            TemplateFile('templates/settings-file', 'output/settings-file', False),
        ),
    )

    writer = Writer(
        renderer=FakeRenderer('some content'),
        file_system=file_system,
        logger=logger,
    )
    writer.write(templates=templates, skip_if_exists=False)

    assert file_system.files == {
        'output/config-file': 'some content',
        'output/settings-file': 'some content',
    }
    assert file_system.executables == []

    assert logger.captured == {
        'debug': [],
        'info': ['writing output/config-file', 'writing output/settings-file'],
        'warn': [],
    }


def test_write_executable_file() -> None:
    file_system = FakeFileSystem()
    logger = CapturedLogger()

    templates = TemplateConfig(
        root_dir='',
        files=(
            TemplateFile('templates/a-script', 'output/a-script', True),
        ),
    )

    writer = Writer(
        renderer=FakeRenderer('some content'),
        file_system=file_system,
        logger=logger,
    )
    writer.write(templates=templates, skip_if_exists=False)

    assert file_system.files == {
        'output/a-script': 'some content',
    }
    assert file_system.executables == ['output/a-script']

    assert logger.captured == {
        'debug': [],
        'info': ['writing output/a-script'],
        'warn': [],
    }


def test_overwrite_existing_file() -> None:
    file_system = FakeFileSystem(files={'output/existing-file': ''})
    logger = CapturedLogger()

    templates = TemplateConfig(
        root_dir='',
        files=(
            TemplateFile('templates/existing-file', 'output/existing-file', False),
        ),
    )

    writer = Writer(
        renderer=FakeRenderer('new content'),
        file_system=file_system,
        logger=logger,
    )
    writer.write(templates=templates, skip_if_exists=False)

    assert file_system.files == {
        'output/existing-file': 'new content',  # new content written
    }

    assert logger.captured == {
        'debug': [],
        'info': [],
        'warn': ['overwriting output/existing-file'],
    }


def test_skip_unchanged_file() -> None:
    file_system = FakeFileSystem(files={'output/existing-file': 'some content'})
    logger = CapturedLogger()

    templates = TemplateConfig(
        root_dir='',
        files=(
            TemplateFile('templates/existing-file', 'output/existing-file', False),
        ),
    )

    writer = Writer(
        renderer=FakeRenderer('some content'),
        file_system=file_system,
        logger=logger,
    )
    writer.write(templates=templates, skip_if_exists=False)

    assert file_system.files == {
        'output/existing-file': 'some content',  # same content
    }

    assert logger.captured == {
        'debug': ['skipping output/existing-file because there are no changes'],
        'info': [],
        'warn': [],
    }


def test_skip_existing_file() -> None:
    file_system = FakeFileSystem(files={'output/existing-file': ''})
    logger = CapturedLogger()

    templates = TemplateConfig(
        root_dir='',
        files=(
            TemplateFile('templates/existing-file', 'output/existing-file', False),
        ),
    )

    writer = Writer(
        renderer=FakeRenderer('some content'),
        file_system=file_system,
        logger=logger,
    )
    writer.write(templates=templates, skip_if_exists=True)

    assert file_system.files == {
        'output/existing-file': '',  # not changed
    }

    assert logger.captured == {
        'debug': ['skipping output/existing-file because it already exists'],
        'info': [],
        'warn': [],
    }
