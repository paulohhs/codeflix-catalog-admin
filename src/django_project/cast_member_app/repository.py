from uuid import UUID

from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.django_project.cast_member_app.models import CastMember as CastMemberORM


class DjangoORMCastMemberRepository(CastMemberRepository):
    def save(self, cast_member: CastMember) -> None:
        cast_member_model = CastMemberModelMapper.to_model(cast_member)
        cast_member_model.save()

    def get_by_id(self, id: UUID) -> CastMember | None:
        try:
            cast_member_model = CastMemberORM.objects.get(id=id)
            return CastMemberModelMapper.to_entity(cast_member_model)
        except CastMemberORM.DoesNotExist:
            return None

    def delete(self, id: UUID) -> None:
        CastMemberORM.objects.filter(id=id).delete()

    def list(self) -> list[CastMember]:
        return [
            CastMemberModelMapper.to_entity(cast_member_model)
            for cast_member_model in CastMemberORM.objects.all()
        ]

    def update(self, cast_member: CastMember) -> None:
        try:
            cast_member_model = CastMemberORM.objects.get(id=cast_member.id)
        except CastMemberORM.DoesNotExist:
            return None

        CastMemberORM.objects.filter(id=cast_member.id).update(
            name=cast_member.name,
            type=cast_member.type,
        )


class CastMemberModelMapper:
    @staticmethod
    def to_model(cast_member: CastMember) -> CastMemberORM:
        return CastMemberORM(
            id=cast_member.id,
            name=cast_member.name,
            type=cast_member.type,
        )

    @staticmethod
    def to_entity(model: CastMemberORM) -> CastMember:
        return CastMember(
            id=model.id,
            name=model.name,
            type=CastMemberType(model.type),
        )
