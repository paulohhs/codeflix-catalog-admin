from unittest.mock import create_autospec
import uuid

import pytest

from src.core.cast_member.domain.cast_member import CastMemberType
from src.core.cast_member.application.use_cases.exceptions import (
    CastMemberNotFound,
    InvalidCastMember,
)
from src.core.cast_member.application.use_cases.update_cast_member import UpdateCastMember
from src.core.cast_member.domain.cast_member import CastMember
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


@pytest.fixture
def mock_cast_member_repository() -> CastMemberRepository:
    return create_autospec(CastMemberRepository)


class TestUpdateGenre:
    def test_when_cast_member_doesnt_exist_then_raise_cast_member_not_found(
        self,
        mock_cast_member_repository,
    ):
        mock_cast_member_repository.get_by_id.return_value = None

        use_case = UpdateCastMember(
            repository=mock_cast_member_repository,
        )
        input = UpdateCastMember.Input(
            id=uuid.uuid4(),
            name="Actor Member",
            type=CastMemberType.ACTOR
        )

        with pytest.raises(CastMemberNotFound):
            use_case.execute(input=input)

    def test_when_attributes_is_invalid_then_raise_invalid_genre(
        self,
        mock_cast_member_repository,
    ):
        cast_member = CastMember(name="Actor Member", type=CastMemberType.ACTOR)
        mock_cast_member_repository.get_by_id.return_value = cast_member

        use_case = UpdateCastMember(
            repository=mock_cast_member_repository,
        )

        # Nome vazio não é permitido
        input = UpdateCastMember.Input(
            id=cast_member.id,
            name="",
            type=cast_member.type,
        )
        with pytest.raises(InvalidCastMember):
            use_case.execute(input=input)

        # type deve ser do tipo TypeCastMember
        input.name = "Actor Member"
        input.type = "Invalid type"
        with pytest.raises(InvalidCastMember):
            use_case.execute(input=input)

    def test_attributes_is_valid_then_update_cast_member(
        self,
        mock_cast_member_repository,
    ):
        cast_member = CastMember(name="Member", type=CastMemberType.ACTOR)
        mock_cast_member_repository.get_by_id.return_value = cast_member

        use_case = UpdateCastMember(
            repository=mock_cast_member_repository,
        )

        input = UpdateCastMember.Input(
            id=cast_member.id,
            name="Member updated",
            type=CastMemberType.DIRECTOR,
        )

        assert cast_member.name == "Member"
        assert cast_member.type == CastMemberType.ACTOR

        use_case.execute(input=input)

        assert cast_member.name == "Member updated"
        assert cast_member.type == CastMemberType.DIRECTOR
