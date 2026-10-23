import pytest

from src.django_project.genre_app.models import Genre as GenreORM


@pytest.mark.django_db
class TestSave:
    def test_save_genre_in_database(
        self,
        mock_comedy_genre,
        genre_repository,
    ):
        assert GenreORM.objects.count() == 0
        genre_repository.save(genre=mock_comedy_genre)

        assert GenreORM.objects.count() == 1
        genre_model = GenreORM.objects.first()

        assert genre_model.id == mock_comedy_genre.id
        assert genre_model.name == mock_comedy_genre.name
        assert genre_model.is_active

    def test_save_genre_with_categories(
        self,
        mock_comedy_genre,
        genre_repository,
        mock_movie_category,
        category_repository,
    ):
        category_repository.save(category=mock_movie_category)
        mock_comedy_genre.add_category(category_id=mock_movie_category.id)
        assert GenreORM.objects.count() == 0

        genre_repository.save(genre=mock_comedy_genre)
        assert GenreORM.objects.count() == 1

        genre_model = GenreORM.objects.get(id=mock_comedy_genre.id)
        related_category = genre_model.categories.get()
        assert related_category.id == mock_movie_category.id
        assert related_category.name == mock_movie_category.name


@pytest.mark.django_db
class TestGet:
    def test_get_genre(
        self,
        mock_comedy_genre,
        genre_repository,
    ):
        genre_repository.save(genre=mock_comedy_genre)
        assert GenreORM.objects.count() == 1

        genre_model = genre_repository.get_by_id(id=mock_comedy_genre.id)
        assert genre_model is not None
        assert genre_model.name == mock_comedy_genre.name
        assert genre_model.is_active
                

    def test_get_genre_with_categories(
        self,
        mock_movie_category,
        mock_genre_with_categories,
        category_repository,
        genre_repository,
    ):
        category_repository.save(category=mock_movie_category)
        
        genre = mock_genre_with_categories(name="Comedy", categories={mock_movie_category.id})
        genre_repository.save(genre=genre)

        assert GenreORM.objects.count() == 1

        genre_model = genre_repository.get_by_id(id=genre.id)
        assert genre_model is not None
        assert genre_model.categories == {mock_movie_category.id}


@pytest.mark.django_db
class TestDelete:
    def test_delete_genre(
        self,
        mock_comedy_genre,
        genre_repository,
    ):
        genre_repository.save(genre=mock_comedy_genre)

        assert GenreORM.objects.count() == 1

        genre_repository.delete(id=mock_comedy_genre.id)
        assert GenreORM.objects.count() == 0


@pytest.mark.django_db
class TestList:
    def test_list_genre(
        self,
        mock_comedy_genre,
        mock_drama_genre,
        genre_repository,
    ):
        genre_repository.save(genre=mock_comedy_genre)
        genre_repository.save(genre=mock_drama_genre)

        assert GenreORM.objects.count() == 2

        genries_model = genre_repository.list()
        assert len(genries_model) == 2
        assert genries_model == [
            mock_comedy_genre,
            mock_drama_genre,
        ]

    def test_list_genre_with_category(
        self,
        mock_genre_with_categories,
        mock_movie_category,
        genre_repository,
        category_repository,
    ):
        category_repository.save(category=mock_movie_category)

        comedy_genre = mock_genre_with_categories(
            name="Comedy",
            categories={mock_movie_category.id}
        )
        genre_repository.save(genre=comedy_genre)

        action_genre = mock_genre_with_categories(
            name="Action",
            categories={mock_movie_category.id}
        )
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
    def test_update_genre(
        self,
        mock_comedy_genre,
        genre_repository,
    ):
        genre_repository.save(genre=mock_comedy_genre)

        mock_comedy_genre.change_name(name="Action")
        mock_comedy_genre.deactivate()
        genre_repository.update(genre=mock_comedy_genre)

        updated_genre = GenreORM.objects.get(id=mock_comedy_genre.id)
        assert updated_genre.id == mock_comedy_genre.id
        assert updated_genre.name == "Action"
        assert not updated_genre.is_active

    def test_update_associated_categories_genre(
        self,
        mock_movie_category,
        mock_documentary_category,
        mock_genre_with_categories,
        genre_repository,
        category_repository,
    ):
        category_repository.save(category=mock_movie_category)
        category_repository.save(category=mock_documentary_category)

        genre = mock_genre_with_categories(name="Comedy", categories={mock_movie_category.id})
        genre_repository.save(genre=genre)
        
        genre.categories = {mock_documentary_category.id}
        genre_repository.update(genre=genre)

        updated_genre = genre_repository.get_by_id(id=genre.id)
        assert updated_genre.id == genre.id
        assert updated_genre.categories == genre.categories
        assert updated_genre.categories == {mock_documentary_category.id}
