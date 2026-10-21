from uuid import UUID

from django.db import transaction

from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository
from src.django_project.genre_app.models import Genre as GenreORM


class DjangoORMGenreRepository(GenreRepository):
    def save(self, genre: Genre) -> None:
        with transaction.atomic():
            genre_model = GenreModelMapper.to_model(genre)
            genre_model.save()
            genre_model.categories.set(genre.categories)

    def get_by_id(self, id: UUID) -> Genre | None:
        try:
            genre_model = GenreORM.objects.get(id=id)
            return GenreModelMapper.to_entity(genre_model)
        except GenreORM.DoesNotExist:
            return None

    def delete(self, id: UUID) -> None:
        GenreORM.objects.filter(id=id).delete()

    def list(self) -> list[Genre]:
        return [
            GenreModelMapper.to_entity(genre_model)
            for genre_model in GenreORM.objects.all()
        ]

    def update(self, genre: Genre) -> None:
        try:
            genre_model = GenreORM.objects.get(id=genre.id)
        except GenreORM.DoesNotExist:
            return None

        with transaction.atomic():
            GenreORM.objects.filter(id=genre.id).update(
                name=genre.name,
                is_active=genre.is_active,
            )
            genre_model.categories.set(genre.categories)


class GenreModelMapper:
    @staticmethod
    def to_model(genre: Genre) -> GenreORM:
        return GenreORM(
            id=genre.id,
            name=genre.name,
            is_active=genre.is_active,
        )

    @staticmethod
    def to_entity(model: GenreORM) -> Genre:
        return Genre(
            id=model.id,
            name=model.name,
            is_active=model.is_active,
            categories={category.id for category in model.categories.all()}
        )
