from __future__ import annotations

from typing import Protocol

import attrs

from ..config import TemplateConfig
from ..logging import Logger
from ..rendering import TemplateRenderer


class FileSystem(Protocol):
    def file_exists(self, path: str) -> bool: ...
    def write_file(self, path: str, content: str, is_executable: bool) -> None: ...


@attrs.frozen
class Writer:
    renderer: TemplateRenderer
    file_system: FileSystem
    logger: Logger

    def write(self, templates: TemplateConfig, skip_if_exists: bool) -> None:
        for file in templates.files:
            rendered = self.renderer.render(file.template_name)

            if skip_if_exists and self.file_system.file_exists(file.destination_path):
                self.logger.debug(
                    f'skipping {file.destination_path} because it already exists',
                )
                continue

            self.file_system.write_file(
                file.destination_path,
                rendered,
                file.is_executable,
            )
