from unittest.mock import create_autospec

import pytest

from src.core.cast_member.domain.cast_member import (
    CastMemberType,
    CastMember,
)
from src.core.cast_member.application.use_cases.list_cast_member import (
    ListCastMember,
    CastMemberOutput,
)
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
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
        order_by: str,
        current_page: int,
    ):
        cast_member_repository = create_autospec(CastMemberRepository)

        member_1 = CastMember(
            name="Member 1",
            type=CastMemberType.DIRECTOR,
        )
        member_2 = CastMember(
            name="Member 2",
            type=CastMemberType.ACTOR,
        )
        member_3 = CastMember(
            name="Member 3",
            type=CastMemberType.DIRECTOR,
        )
        member_4 = CastMember(
            name="Member 4",
            type=CastMemberType.ACTOR,
        )

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

    def test_when_cast_mesmber_doesnt_exist_return_empty_data(self):
        cast_member_repository = create_autospec(CastMemberRepository)
        cast_member_repository.list.return_value = []

        use_case = ListCastMember(repository=cast_member_repository)
        output = use_case.execute(input=ListCastMember.Input())

        assert len(output.data) == 0
        assert output == ListCastMember.Output(data=[])
