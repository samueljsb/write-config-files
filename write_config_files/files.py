from __future__ import annotations

import os.path

import attrs


class FileSystemReader:
    def read_lines(self, file_path: str) -> list[str]:
        try:
            with open(file_path) as f:
                return f.readlines()
        except FileNotFoundError:
            return []


@attrs.frozen
class FileSystem:
    def file_exists(self, path: str) -> bool:
        return os.path.exists(path)

    def read_content(self, path: str) -> str:
        try:
            with open(path) as f:
                return f.read()
        except FileNotFoundError:
            return ''

    def write_file(
            self,
            path: str, content: str,
            is_executable: bool,
    ) -> None:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            f.write(content)

        if is_executable:
            os.chmod(path, 0o744)


@attrs.frozen
class DryRunFileWriter:
    def file_exists(self, path: str) -> bool:
        return os.path.exists(path)

    def read_content(self, path: str) -> str:
        try:
            with open(path) as f:
                return f.read()
        except FileNotFoundError:
            return ''

    def write_file(self, path: str, content: str, is_executable: bool) -> None:
        pass
