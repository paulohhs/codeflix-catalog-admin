import pytest
from uuid import UUID
import uuid

from src.core.cast_member.domain.cast_member import CastMember, CastMemberType


class TestCastMember:
    def test_attributes_is_required(self):
        # Name é obrigatório
        with pytest.raises(TypeError, match="missing 1 required positional argument: 'name'"):
            CastMember(type=CastMemberType.ACTOR)

        with pytest.raises(TypeError, match="missing 1 required positional argument: 'type'"):
            CastMember(name="Member 1")

    def test_name_must_have_less_than_256_characters(self):
        with pytest.raises(ValueError, match="name must have less than 256 characters"):
            CastMember(name="a" * 256, type=CastMemberType.ACTOR)

    def test_cannot_create_cast_member_with_empty_name(self):
        with pytest.raises(ValueError, match="name cannot be empty"):
            CastMember(name="", type=CastMemberType.ACTOR)

    def test_cannot_create_cast_member_with_different_type(self):
        with pytest.raises(ValueError, match="type must be a CastMemberType"):
            cast_member = CastMember(name="Member 1", type="Invalid type")

    def test_cast_member_must_be_created_with_id_as_uuid(self):
        cast_member = CastMember(name="Member 1", type=CastMemberType.ACTOR)

        assert isinstance(cast_member.id, UUID)

    def test_genre_str_representation(self):
        cast_member = CastMember(name="Member 1", type=CastMemberType.ACTOR)

        assert str(cast_member) == "Member 1 - (ACTOR)"

    def test_genre_repr_representation(self):
        cast_member_id = uuid.uuid4()
        cast_member = CastMember(
            id=cast_member_id,
            name="Member 1",
            type=CastMemberType.ACTOR
        )

        assert repr(cast_member) == f"<CastMember Member 1 ({cast_member_id})>"


class TestEquality:
    def test_when_genres_have_same_id_they_are_equal(self):
        cast_member_id = uuid.uuid4()
        cast_member_1 = CastMember(id=cast_member_id, name="Actor member", type=CastMemberType.ACTOR)
        cast_member_2 = CastMember(id=cast_member_id, name="Director member", type=CastMemberType.DIRECTOR)

        assert cast_member_1 == cast_member_2

    def test_equality_different_classes(self):
        class Dummy:
            pass

        cast_member_id = uuid.uuid4()
        cast_member = CastMember(id=cast_member_id, name="Actor member", type=CastMemberType.ACTOR)
        dummy = Dummy()
        dummy.id = cast_member_id

        assert cast_member != dummy


class TestChangeName:
    def test_change_name(self):
        cast_member = CastMember(name="Actor member", type=CastMemberType.ACTOR)

        cast_member.change_name("Actor name edited")
        assert cast_member.name == "Actor name edited"

    def test_when_name_is_empty(self):
        cast_member = CastMember(name="Actor member", type=CastMemberType.ACTOR)

        with pytest.raises(ValueError, match="name cannot be empty"):
            cast_member.change_name("")


class TestChangeType:
    def test_change_type(self):
        cast_member = CastMember(name="Member Test", type=CastMemberType.ACTOR)

        cast_member.change_type(CastMemberType.DIRECTOR)
        assert cast_member.type == CastMemberType.DIRECTOR

    def test_when_type_is_invalid(self):
        cast_member = CastMember(name="Actor member", type=CastMemberType.ACTOR)

        with pytest.raises(ValueError, match="type must be a CastMemberType"):
            cast_member.change_type("Invalid type")
