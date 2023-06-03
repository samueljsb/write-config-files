from __future__ import annotations

import attrs

from ..config import TemplateConfig
from ..files import FileWriter
from ..logging import Logger
from ..rendering import TemplateRenderer


@attrs.frozen
class Writer:
    renderer: TemplateRenderer
    file_writer: FileWriter
    logger: Logger

    def write(self, templates: TemplateConfig, skip_if_exists: bool) -> None:
        for file in templates.files:
            rendered = self.renderer.render(file.template_name)

            if skip_if_exists and self.file_writer.file_exists(file.destination_path):
                self.logger.debug(
                    f'skipping {file.destination_path} because it already exists',
                )
                continue

            self.file_writer.write_file(
                file.destination_path,
                rendered,
                file.is_executable,
            )
