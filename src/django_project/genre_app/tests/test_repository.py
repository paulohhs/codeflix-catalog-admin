import pytest

from src.core.category.domain.category import Category
from src.core.genre.domain.genre import Genre
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.genre_app.repository import DjangoORMGenreRepository
from src.django_project.genre_app.models import Genre as GenreORM


@pytest.mark.django_db
class TestSave:
    def test_save_genre_in_database(self):
        genre = Genre(name="Comedy")
        genre_repository = DjangoORMGenreRepository()

        assert GenreORM.objects.count() == 0
        genre_repository.save(genre=genre)

        assert GenreORM.objects.count() == 1
        genre_model = GenreORM.objects.first()

        assert genre_model.id == genre.id
        assert genre_model.name == genre.name
        assert genre_model.is_active

    def test_save_genre_with_categories(self):
        genre_repository = DjangoORMGenreRepository()
        category_repository = DjangoORMCategoryRepository()

        category = Category(name="Movie")
        category_repository.save(category=category)

        genre = Genre(name="Comedy")
        genre.add_category(category_id=category.id)

        assert GenreORM.objects.count() == 0
        genre_repository.save(genre=genre)
        assert GenreORM.objects.count() == 1

        genre_model = GenreORM.objects.get(id=genre.id)
        related_category = genre_model.categories.get()
        assert related_category.id == category.id
        assert related_category.name == category.name


@pytest.mark.django_db
class TestGet:
    def test_get_genre(self):
        genre = Genre(name="Comedy")
        genre_repository = DjangoORMGenreRepository()
        genre_repository.save(genre=genre)

        assert GenreORM.objects.count() == 1

        genre_model = genre_repository.get_by_id(id=genre.id)
        assert genre_model is not None
        assert genre_model.name == genre.name
        assert genre_model.is_active
                

    def test_get_genre_with_categories(self):
        category_repository = DjangoORMCategoryRepository()
        category = Category(name="Movie")
        category_repository.save(category=category)
        
        genre = Genre(name="Comedy", categories={category.id})
        genre_repository = DjangoORMGenreRepository()
        genre_repository.save(genre=genre)

        assert GenreORM.objects.count() == 1

        genre_model = genre_repository.get_by_id(id=genre.id)
        assert genre_model is not None
        assert genre_model.categories == {category.id}


@pytest.mark.django_db
class TestDelete:
    def test_delete_genre(self):
        genre = Genre(name="Comedy")
        genre_repository = DjangoORMGenreRepository()
        genre_repository.save(genre=genre)

        assert GenreORM.objects.count() == 1

        genre_repository.delete(id=genre.id)
        assert GenreORM.objects.count() == 0


@pytest.mark.django_db
class TestList:
    def test_list_genre(self):
        genre_repository = DjangoORMGenreRepository()

        comedy_genre = Genre(name="Comedy")
        genre_repository.save(genre=comedy_genre)

        action_genre = Genre(name="Action")
        genre_repository.save(genre=action_genre)

        assert GenreORM.objects.count() == 2

        genries_model = genre_repository.list()
        assert len(genries_model) == 2
        assert genries_model == [
            comedy_genre,
            action_genre,
        ]

    def test_list_genre_with_category(self):
        genre_repository = DjangoORMGenreRepository()

        category_repository = DjangoORMCategoryRepository()
        category = Category(name="Movie")
        category_repository.save(category=category)

        comedy_genre = Genre(name="Comedy", categories={category.id})
        genre_repository.save(genre=comedy_genre)

        action_genre = Genre(name="Action", categories={category.id})
        genre_repository.save(genre=action_genre)

        assert GenreORM.objects.count() == 2

        genries_model = genre_repository.list()
        assert len(genries_model) == 2
        assert genries_model == [
            comedy_genre,
            action_genre,
        ]


@pytest.mark.django_db
class TestUpdate:
    def test_update_genre(self):
        genre_repository = DjangoORMGenreRepository()
        genre = Genre(name="Comedy")
        genre_repository.save(genre=genre)

        genre.change_name(name="Action")
        genre.deactivate()
        genre_repository.update(genre=genre)

        updated_genre = GenreORM.objects.get(id=genre.id)
        assert updated_genre.id == genre.id
        assert updated_genre.name == "Action"
        assert not updated_genre.is_active

    def test_update_associated_categories_genre(self):
        genre_repository = DjangoORMGenreRepository()
        
        category_repository = DjangoORMCategoryRepository()
        category = Category(name="Movie")
        category_repository.save(category=category)

        genre = Genre(name="Comedy", categories={category.id})
        genre_repository.save(genre=genre)

        doc_category = Category(name="Documentary")
        category_repository.save(category=doc_category)
        
        genre.categories = {doc_category.id}
        genre_repository.update(genre=genre)

        updated_genre = genre_repository.get_by_id(id=genre.id)
        assert updated_genre.id == genre.id
        assert updated_genre.categories == genre.categories
        assert updated_genre.categories == {doc_category.id}
