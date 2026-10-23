import uuid

import pytest

from src.core.cast_member.application.use_cases.delete_cast_member import DeleteCastMember
from src.core.cast_member.application.use_cases.exceptions import CastMemberNotFound


class TestDeleteCastMember:
    def test_delete_cast_member_from_repository(
        self,
        mock_im_cast_member_repository_with_data,
    ):
        (
            cast_member,
            _,
            mock_cast_member_repository
        ) = mock_im_cast_member_repository_with_data

        use_case = DeleteCastMember(repository=mock_cast_member_repository)
        use_case.execute(input=DeleteCastMember.Input(id=cast_member.id))

        assert mock_cast_member_repository.get_by_id(cast_member.id) is None

    def test_when_cast_member_doesnt_exist_then_raise_not_found_exception(
        self,
        mock_im_cast_member_repository,
    ):
        use_case = DeleteCastMember(repository=mock_im_cast_member_repository)

        with pytest.raises(CastMemberNotFound, match="Cast member not found"):
            use_case.execute(input=DeleteCastMember.Input(id=uuid.uuid4()))
