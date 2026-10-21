import pytest

from src.core.cast_member.domain.cast_member import TypeCastMember
from src.core.cast_member.domain.cast_member import CastMember
from src.django_project.cast_member_app.repository import DjangoORMCastMemberRepository
from src.django_project.cast_member_app.models import CastMember as CastMemberORM


@pytest.mark.django_db
class TestSave:
    def test_save_cast_member_in_database(self):
        cast_member = CastMember(name="Test Member", type=TypeCastMember.ACTOR)
        cast_member_repository = DjangoORMCastMemberRepository()

        assert CastMemberORM.objects.count() == 0
        cast_member_repository.save(cast_member=cast_member)

        assert CastMemberORM.objects.count() == 1
        cast_member_model = CastMemberORM.objects.first()

        assert cast_member_model.id == cast_member.id
        assert cast_member_model.name == cast_member.name
        assert cast_member_model.type == cast_member.type


@pytest.mark.django_db
class TestGet:
    def test_get_cast_member(self):
        cast_member = CastMember(name="Test Member", type=TypeCastMember.ACTOR)
        cast_member_repository = DjangoORMCastMemberRepository()
        cast_member_repository.save(cast_member=cast_member)

        assert CastMemberORM.objects.count() == 1

        cast_member_model = cast_member_repository.get_by_id(id=cast_member.id)
        assert cast_member_model is not None
        assert cast_member_model.name == cast_member.name
        assert cast_member_model.type == cast_member.type


@pytest.mark.django_db
class TestDelete:
    def test_delete_cast_member(self):
        cast_member = CastMember(name="Test Member", type=TypeCastMember.ACTOR)
        cast_member_repository = DjangoORMCastMemberRepository()
        cast_member_repository.save(cast_member=cast_member)

        assert CastMemberORM.objects.count() == 1

        cast_member_repository.delete(id=cast_member.id)
        assert CastMemberORM.objects.count() == 0


@pytest.mark.django_db
class TestList:
    def test_list_cast_member(self):
        cast_member_repository = DjangoORMCastMemberRepository()

        cast_member_1 = CastMember(name="Test Member", type=TypeCastMember.ACTOR)
        cast_member_repository.save(cast_member=cast_member_1)

        cast_member_2 = CastMember(name="Test Member", type=TypeCastMember.DIRECTOR)
        cast_member_repository.save(cast_member=cast_member_2)

        assert CastMemberORM.objects.count() == 2

        cast_members_model = cast_member_repository.list()
        assert len(cast_members_model) == 2
        assert cast_members_model == [
            cast_member_1,
            cast_member_2,
        ]


@pytest.mark.django_db
class TestUpdate:
    def test_update_cast_member(self):
        cast_member_repository = DjangoORMCastMemberRepository()
        cast_member = CastMember(name="Test Member", type=TypeCastMember.ACTOR)
        cast_member_repository.save(cast_member=cast_member)

        cast_member.change_name(name="Member updated")
        cast_member.change_type(type=TypeCastMember.DIRECTOR)
        cast_member_repository.update(cast_member=cast_member)

        updated_cast_member = CastMemberORM.objects.get(id=cast_member.id)
        assert updated_cast_member.id == cast_member.id
        assert updated_cast_member.name == "Member updated"
        assert updated_cast_member.type == TypeCastMember.DIRECTOR
