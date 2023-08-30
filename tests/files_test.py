from __future__ import annotations

import os
from pathlib import Path

from testing.logging import CapturedLogger
from write_config_files.files import FileSystem


class TestFileSystem:
    def test_write_new_file(self, tmp_path: Path):
        logger = CapturedLogger()

        output_file = tmp_path / 'output'

        writer = FileSystem(logger)
        writer.write_file(str(output_file), 'some content', is_executable=False)

        with open(output_file) as f:
            assert f.read() == 'some content'

        assert logger.captured == {
            'debug': [],
            'info': [f'writing {output_file}'],
            'warn': [],
        }

    def test_overwrite_existing_file(self, tmp_path: Path):
        logger = CapturedLogger()

        output_file = tmp_path / 'output'

        with open(output_file, 'w') as f:
            f.write('pre-existing content')

        writer = FileSystem(logger)
        writer.write_file(str(output_file), 'new content', is_executable=False)

        with open(output_file) as f:
            assert f.read() == 'new content'

        assert logger.captured == {
            'debug': [],
            'info': [],
            'warn': [f'overwriting {output_file}'],
        }

    def test_make_file_executable(self, tmp_path: Path):
        logger = CapturedLogger()

        output_file = tmp_path / 'output'

        writer = FileSystem(logger)
        writer.write_file(str(output_file), 'some content', is_executable=True)

        # check the fiel is executable
        status = os.stat(output_file)
        assert status.st_mode & 0o744 == 0o744
