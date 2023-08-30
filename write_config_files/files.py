from __future__ import annotations

import os.path

import attrs

from .logging import Logger


class FileSystemReader:
    def load_file(self, file_path: str) -> list[str]:
        try:
            with open(file_path) as f:
                return f.readlines()
        except FileNotFoundError:
            return []


@attrs.frozen
class OsFileWriter:
    logger: Logger

    def file_exists(self, path: str) -> bool:
        return os.path.exists(path)

    def write_file(
            self,
            path: str, content: str,
            is_executable: bool,
    ) -> None:
        if self.file_exists(path):
            self.logger.warn(f'overwriting {path}')
        else:
            self.logger.info(f'writing {path}')

        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            f.write(content)

        if is_executable:
            os.chmod(path, 0o744)


@attrs.frozen
class DryRunFileWriter:
    logger: Logger

    def file_exists(self, path: str) -> bool:
        return os.path.exists(path)

    def write_file(self, path: str, content: str, is_executable: bool) -> None:
        if self.file_exists(path):
            self.logger.warn(f'would overwrite {path}')
        else:
            self.logger.info(f'would write {path}')
