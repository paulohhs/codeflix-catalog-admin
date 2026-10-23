import pytest

from src.core.cast_member.application.use_cases.list_cast_member import (
    ListCastMember,
    CastMemberOutput,
)
from src.core._shared.application.list_response import ListOutputMeta


class TestListCastMember:
    @pytest.mark.parametrize(
        "order_by, current_page",
        [
            ("name", 1),
            ("name", 2),
            ("type", 1),
            ("type", 2),
        ]
    )
    def test_list_cast_members(
        self,
        mock_cast_member_repository,
        mock_actor_member,
        mock_director_member,
        order_by: str,
        current_page: int,
    ):
        cast_member_repository = mock_cast_member_repository

        member_1 = mock_director_member(name="Member 1")
        member_2 = mock_actor_member(name="Member 2")
        member_3 = mock_director_member(name="Member 3")
        member_4 = mock_actor_member(name="Member 4")

        cast_member_repository.list.return_value = [
            member_1,
            member_2,
            member_3,
            member_4,
        ]

        if order_by == "name":
            expected_data_per_page = {
                1: [member_1, member_2],
                2: [member_3, member_4],
            }
        else:
            expected_data_per_page = {
                1: [member_2, member_4],
                2: [member_1, member_3],
            }

        expected_data = [
            CastMemberOutput(
                id=cast_member.id,
                name=cast_member.name,
                type=cast_member.type,
            ) for cast_member in expected_data_per_page[current_page]
        ]

        use_case = ListCastMember(repository=cast_member_repository)
        output = use_case.execute(input=ListCastMember.Input(
            order_by=order_by,
            current_page=current_page,
        ))

        assert output == ListCastMember.Output(
            data=expected_data,
            meta=ListOutputMeta(
                current_page=current_page,
                per_page=2,
                total=4
            )
        )

    def test_when_cast_mesmber_doesnt_exist_return_empty_data(
        self,
        mock_cast_member_repository,
    ):
        cast_member_repository = mock_cast_member_repository
        cast_member_repository.list.return_value = []

        use_case = ListCastMember(repository=cast_member_repository)
        output = use_case.execute(input=ListCastMember.Input())

        assert len(output.data) == 0
        assert output == ListCastMember.Output(data=[])
