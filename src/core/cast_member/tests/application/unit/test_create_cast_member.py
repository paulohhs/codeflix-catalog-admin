import uuid
from unittest.mock import create_autospec

import pytest

from src.core.cast_member.domain.cast_member import CastMemberType, CastMember
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository

from src.core.cast_member.application.use_cases.create_cast_member import CreateCastMember
from src.core.cast_member.application.use_cases.exceptions import InvalidCastMember


@pytest.fixture
def mock_cast_member_repository() -> CastMemberRepository:
    return create_autospec(CastMemberRepository)


class TestCreateCastMember:
    def test_when_created_cast_member_is_invalid_then_raise_invalid_cast_member(
            self,
            mock_cast_member_repository,
    ):
        use_case = CreateCastMember(repository=mock_cast_member_repository)
        input = CreateCastMember.Input(
            name="",
            type=CastMemberType.ACTOR,
        )

        with pytest.raises(InvalidCastMember, match="name cannot be empty"):
            use_case.execute(input=input)

        input.name = "a" * 256
        with pytest.raises(InvalidCastMember, match="name must have less than 256 characters"):
            use_case.execute(input=input)

        input.name = "Test Member"
        input.type = "Invalid Type"
        with pytest.raises(InvalidCastMember, match="type must be a CastMemberType"):
            use_case.execute(input=input)

    def test_create_cast_member(
        self,
        mock_cast_member_repository,
    ):
        use_case = CreateCastMember(
            repository=mock_cast_member_repository,
        )
        input = CreateCastMember.Input(
            name="Test Member",
            type=CastMemberType.ACTOR,
        )

        output = use_case.execute(input=input)

        assert isinstance(output.id, uuid.UUID)
        mock_cast_member_repository.save.assert_called_once_with(
            CastMember(
                id=output.id,
                name="Test Member",
                type=CastMemberType.ACTOR
            )
        )
