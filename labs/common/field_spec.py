"""Declarative TShark field specification used by the streaming reader."""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Any
import yaml

@dataclass(frozen=True)
class FieldDefinition:
    name: str
    attribute: str
    type: str

@dataclass(frozen=True)
class FieldSpec:
    display_filter: str
    fields: tuple[FieldDefinition, ...]

    @classmethod
    def from_yaml(cls, path: str | Path) -> "FieldSpec":
        data: dict[str, Any] = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
        return cls(
            display_filter=str(data["display_filter"]),
            fields=tuple(FieldDefinition(**item) for item in data["fields"]),
        )

    @property
    def tshark_fields(self) -> tuple[str, ...]:
        return tuple(field.name for field in self.fields)
