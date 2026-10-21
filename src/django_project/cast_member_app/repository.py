from uuid import UUID

from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.django_project.cast_member_app.models import CastMember as CastMemberORM


class DjangoORMCastMemberRepository(CastMemberRepository):
    def save(self, cast_member: CastMember) -> None:
        CastMemberORM.objects.create(
            id=cast_member.id,
            name=cast_member.name,
            type=cast_member.type,
        )

    def get_by_id(self, id: UUID) -> CastMember | None:
        try:
            cast_member_model = CastMemberORM.objects.get(id=id)
        except CastMemberORM.DoesNotExist:
            return None

        return CastMember(
            id=cast_member_model.id,
            name=cast_member_model.name,
            type=CastMemberType(cast_member_model.type),
        )

    def delete(self, id: UUID) -> None:
        CastMemberORM.objects.filter(id=id).delete()

    def list(self) -> list[CastMember]:
        return [
            CastMember(
                id=cast_member_model.id,
                name=cast_member_model.name,
                type=CastMemberType(cast_member_model.type),
            ) for cast_member_model in CastMemberORM.objects.all()
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
