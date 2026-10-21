from dataclasses import dataclass
from uuid import UUID

from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.core.cast_member.application.use_cases.exceptions import CastMemberNotFound


class DeleteCastMember:
    def __init__(self, repository: CastMemberRepository) -> None:
        self.repository = repository

    @dataclass
    class Input:
        id: UUID

    def execute(self, input: Input) -> None:
        cast_member = self.repository.get_by_id(id=input.id)

        if not cast_member:
            raise CastMemberNotFound("Cast member not found")

        self.repository.delete(id=input.id)
