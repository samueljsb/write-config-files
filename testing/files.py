from __future__ import annotations

import attrs


@attrs.frozen
class FakeFileSystem:
    files: dict[str, str] = attrs.field(factory=dict)
    executables: list[str] = attrs.field(factory=list)

    def file_exists(self, path: str) -> bool:
        return path in self.files

    def read_lines(self, file_path: str) -> list[str]:
        try:
            return self.files[file_path].splitlines(keepends=True)
        except KeyError:
            return []

    def write_file(self, path: str, content: str, is_executable: bool) -> None:
        self.files[path] = content
        if is_executable:
            self.executables.append(path)
