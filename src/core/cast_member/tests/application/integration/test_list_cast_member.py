from core.cast_member.domain.cast_member import (
    CastMemberType,
    CastMember,
)
from core.cast_member.infra.in_memory_cast_member_repository import InMemoryCastMemberRepository
from src.core.cast_member.application.use_cases.list_cast_member import (
    ListCastMember,
    CastMemberOutput,
)


class TestListCastMember:
    def test_list_cast_members(self):
        cast_member_repository = InMemoryCastMemberRepository()

        actor_member = CastMember(
            name="Actor Member",
            type=CastMemberType.ACTOR,
        )
        director_member = CastMember(
            name="Director Member",
            type=CastMemberType.DIRECTOR,
        )
        cast_member_repository.save(actor_member)
        cast_member_repository.save(director_member)

        use_case = ListCastMember(repository=cast_member_repository)
        output = use_case.execute(input=ListCastMember.Input())

        assert output == ListCastMember.Output(
            data=[
                CastMemberOutput(
                    id=actor_member.id,
                    name=actor_member.name,
                    type=actor_member.type,
                ),
                CastMemberOutput(
                    id=director_member.id,
                    name=director_member.name,
                    type=director_member.type,
                )
            ]
        )

    def test_when_cast_mesmber_doesnt_exist_return_empty_data(self):
        cast_member_repository = InMemoryCastMemberRepository()

        use_case = ListCastMember(repository=cast_member_repository)
        output = use_case.execute(input=ListCastMember.Input())

        assert len(output.data) == 0
        assert output == ListCastMember.Output(data=[])
