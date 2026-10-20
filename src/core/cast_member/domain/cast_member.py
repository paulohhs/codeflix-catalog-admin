from dataclasses import dataclass, field
import uuid
from enum import StrEnum
from uuid import UUID


class TypeCastMember(StrEnum):
    ACTOR = "ACTOR"
    DIRECTOR = "DIRECTOR"


@dataclass
class CastMember:
    name: str
    type: TypeCastMember
    id: UUID = field(default_factory=uuid.uuid4)

    def __post_init__(self):
        self.validate()

    def __str__(self):
        return f"{self.name} - ({self.type})"

    def __repr__(self):
        return f"<CastMember {self.name} ({self.id})>"

    def __eq__(self, other):
        if not isinstance(other, CastMember):
            return False
        return self.id == other.id

    def validate(self):
        if not self.name:
            raise ValueError("name cannot be empty")

        if len(self.name) > 255:
            raise ValueError("name must have less than 256 characters")

        if not isinstance(self.type, TypeCastMember):
            raise ValueError("type must be a TypeCastMember")

    def change_name(self, name: str) -> None:
        self.name = name
        self.validate()

    def change_type(self, type: TypeCastMember) -> None:
        self.type = type
        self.validate()