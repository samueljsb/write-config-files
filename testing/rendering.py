from __future__ import annotations

import attrs


@attrs.frozen
class FakeRenderer:
    output: str

    def render(self, template_name: str) -> str:
        return self.output
