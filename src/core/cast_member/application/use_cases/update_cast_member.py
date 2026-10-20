from dataclasses import dataclass
from uuid import UUID

from src.core.cast_member.application.use_cases.exceptions import (
    CastMemberNotFound, InvalidCastMember
)
from src.core.cast_member.domain.cast_member import TypeCastMember
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


class UpdateCastMember:
    def __init__(self, repository: CastMemberRepository) -> None:
        self.repository = repository

    @dataclass
    class Input:
        id: UUID
        name: str
        type: TypeCastMember

    def execute(self, input: UpdateCastMember.Input) -> None:
        cast_member = self.repository.get_by_id(input.id)

        if not cast_member:
            raise CastMemberNotFound("Cast member not found")

        try:
            cast_member.change_name(name=input.name)
            cast_member.change_type(type=input.type)
        except ValueError as e:
            raise InvalidCastMember(e)

        self.repository.update(cast_member=cast_member)