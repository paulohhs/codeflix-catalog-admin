from dataclasses import dataclass
from uuid import UUID

from src.core.cast_member.application.use_cases.exceptions import InvalidCastMember
from src.core.cast_member.domain.cast_member import CastMember
from src.core.cast_member.domain.cast_member import CastMemberType
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


class CreateCastMember:
    def __init__(self, repository: CastMemberRepository):
        self.repository = repository

    @dataclass
    class Input:
        name: str
        type: CastMemberType

    @dataclass
    class Output:
        id: UUID

    def execute(self, input: Input):
        try:
            cast_member = CastMember(
                name=input.name,
                type=input.type
            )
        except ValueError as e:
            raise InvalidCastMember(e)

        self.repository.save(cast_member)

        return self.Output(id=cast_member.id)
