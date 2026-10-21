from dataclasses import dataclass
from uuid import UUID

from src.core.cast_member.domain.cast_member import CastMemberType
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


@dataclass
class CastMemberOutput:
    id: UUID
    name: str
    type: CastMemberType


class ListCastMember:
    def __init__(self, repository: CastMemberRepository):
        self.repository = repository

    @dataclass
    class Input:
        pass

    @dataclass
    class Output:
        data: list[CastMemberOutput]

    def execute(self, input: Input) -> Output:
        cast_members = self.repository.list()

        mapped_cast_members = [
            CastMemberOutput(
                id=cast_member.id,
                name=cast_member.name,
                type=cast_member.type,
            ) for cast_member in cast_members
        ]

        return self.Output(data=mapped_cast_members)