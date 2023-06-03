from __future__ import annotations

from collections.abc import Sequence

import attrs


@attrs.frozen
class CapturedPrinter:
    diffs: list[Sequence[str]] = attrs.field(factory=list)

    def print(self, diff_lines: Sequence[str]) -> None:
        self.diffs.append(diff_lines)
