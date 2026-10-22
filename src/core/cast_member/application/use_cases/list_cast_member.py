from dataclasses import dataclass
from uuid import UUID

from src.core.cast_member.domain.cast_member import CastMemberType
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.core._shared.application.list_response import ListOutput, ListOutputMeta, ListInput


@dataclass
class CastMemberOutput:
    id: UUID
    name: str
    type: CastMemberType


class ListCastMember:
    def __init__(self, repository: CastMemberRepository):
        self.repository = repository

    @dataclass
    class Input(ListInput):
        pass

    @dataclass
    class Output(ListOutput[CastMemberOutput]):
        pass

    def execute(self, input: Input) -> Output:
        cast_members = self.repository.list()

        sorted_cast_members = sorted(
            [
                CastMemberOutput(
                    id=cast_member.id,
                    name=cast_member.name,
                    type=cast_member.type,
                ) for cast_member in cast_members
            ],
            key = lambda cast_member: getattr(cast_member, input.order_by)
        )

        DEFAULT_PAGE_SIZE = 2
        page_offset = (input.current_page - 1) * DEFAULT_PAGE_SIZE
        cast_members_page = sorted_cast_members[page_offset:page_offset + DEFAULT_PAGE_SIZE]

        return self.Output(
            data=cast_members_page,
            meta=ListOutputMeta(
                current_page=input.current_page,
                per_page=DEFAULT_PAGE_SIZE,
                total=len(sorted_cast_members)
            )
        )