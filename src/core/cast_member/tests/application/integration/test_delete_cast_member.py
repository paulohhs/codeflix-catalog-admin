import uuid

import pytest

from src.core.cast_member.domain.cast_member import CastMemberType
from src.core.cast_member.application.use_cases.delete_cast_member import DeleteCastMember
from src.core.cast_member.application.use_cases.exceptions import CastMemberNotFound
from src.core.cast_member.domain.cast_member import CastMember
from src.core.cast_member.infra.in_memory_cast_member_repository import InMemoryCastMemberRepository


class TestDeleteCastMember:
    def test_delete_cast_member_from_repository(
        self,
    ):
        cast_member = CastMember(name="Test Member", type=CastMemberType.ACTOR)
        mock_cast_member_repository = InMemoryCastMemberRepository(cast_members=[cast_member])

        use_case = DeleteCastMember(repository=mock_cast_member_repository)
        use_case.execute(input=DeleteCastMember.Input(id=cast_member.id))

        assert mock_cast_member_repository.get_by_id(cast_member.id) is None

    def test_when_cast_member_doesnt_exist_then_raise_not_found_exception(
        self,
    ):
        use_case = DeleteCastMember(repository=InMemoryCastMemberRepository())

        with pytest.raises(CastMemberNotFound, match="Cast member not found"):
            use_case.execute(input=DeleteCastMember.Input(id=uuid.uuid4()))
