from __future__ import annotations

import attrs


@attrs.frozen
class CapturedLogger:  # pragma: no cover
    debugs: list[str] = attrs.field(factory=list)
    infos: list[str] = attrs.field(factory=list)
    warns: list[str] = attrs.field(factory=list)

    @property
    def captured(self) -> dict[str, list[str]]:
        return {
            'debug': self.debugs,
            'info': self.infos,
            'warn': self.warns,
        }

    def debug(self, msg: str) -> None:
        self.debugs.append(msg)

    def info(self, msg: str) -> None:
        self.infos.append(msg)

    def warn(self, msg: str) -> None:
        self.warns.append(msg)
