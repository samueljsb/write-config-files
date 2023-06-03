from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture
def output_dir(tmp_path: Path) -> Path:
    output_dir = tmp_path / 'output'
    output_dir.mkdir()
    return output_dir


@pytest.fixture
def template_dir(tmp_path: Path) -> Path:
    template_dir = tmp_path / 'templates'
    template_dir.mkdir()
    return template_dir
