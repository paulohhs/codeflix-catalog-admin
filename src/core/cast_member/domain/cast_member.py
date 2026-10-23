from dataclasses import dataclass
from enum import StrEnum

from core._shared.domain.entity import Entity


class CastMemberType(StrEnum):
    ACTOR = "ACTOR"
    DIRECTOR = "DIRECTOR"


@dataclass
class CastMember(Entity):
    name: str
    type: CastMemberType

    def __post_init__(self):
        self.validate()

    def __str__(self):
        return f"{self.name} - ({self.type})"

    def __repr__(self):
        return f"<CastMember {self.name} ({self.id})>"

    def validate(self):
        if not self.name:
            self.notification.add_error("name cannot be empty")

        if len(self.name) > 255:
            self.notification.add_error("name must have less than 256 characters")

        if not isinstance(self.type, CastMemberType):
            self.notification.add_error("type must be a CastMemberType")

        if self.notification.has_errors:
            raise ValueError(self.notification.messages)

    def change_name(self, name: str) -> None:
        self.name = name
        self.validate()

    def change_type(self, type: CastMemberType) -> None:
        self.type = type
        self.validate()