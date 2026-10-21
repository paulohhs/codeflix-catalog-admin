import uuid

import pytest

from src.core.cast_member.domain.cast_member import CastMemberType, CastMember
from src.core.cast_member.infra.in_memory_cast_member_repository import InMemoryCastMemberRepository

from src.core.cast_member.application.use_cases.create_cast_member import CreateCastMember
from src.core.cast_member.application.use_cases.exceptions import InvalidCastMember


class TestCreateCastMember:
    def test_when_created_cast_member_is_invalid_then_raise_invalid_cast_member(
        self,
    ):
        use_case = CreateCastMember(repository=InMemoryCastMemberRepository())
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

    def test_create_cast_member(self):
        cast_member_repository = InMemoryCastMemberRepository()
        use_case = CreateCastMember(
            repository=cast_member_repository,
        )
        input = CreateCastMember.Input(
            name="Test Member",
            type=CastMemberType.ACTOR,
        )

        output = use_case.execute(input=input)
        assert isinstance(output.id, uuid.UUID)

        created_cast_member = cast_member_repository.get_by_id(output.id)
        assert isinstance(created_cast_member, CastMember)
        assert created_cast_member.name == input.name
        assert created_cast_member.type == input.type
