import pytest
from uuid import UUID
import uuid
from src.core.genre.domain.genre import Genre

class TestGenre:
    def test_name_is_required(self):
        with pytest.raises(TypeError, match="missing 1 required positional argument: 'name'"):
            Genre()

    def test_name_must_have_less_than_256_characters(self):
        with pytest.raises(ValueError, match="name must have less than 256 characters"):
            Genre(name="a" * 256)

    def test_cannot_create_genre_with_empty_name(self):
        with pytest.raises(ValueError, match="name cannot be empty"):
            Genre(name="")

    def test_genre_must_be_created_with_id_as_uuid(self):
        category = Genre(name="Comedy")

        assert isinstance(category.id, UUID)

    def test_created_genre_with_default_values(self):
        genre = Genre(name="Comedy")

        assert genre.name == "Comedy"
        assert genre.is_active == True
        assert isinstance(genre.id, UUID)
        assert genre.categories == set()

    def test_genre_is_created_as_active_by_default(self):
        genre = Genre(name="Comedy")

        assert genre.is_active == True

    def test_genre_is_created_with_provided_values(self):
        genre_id = uuid.uuid4()
        categories = {uuid.uuid4(), uuid.uuid4()}

        genre = Genre(
            id=genre_id,
            name="Comedy", 
            is_active=False,
            categories=categories,
        )

        assert genre.id == genre_id
        assert genre.name == "Comedy"
        assert genre.is_active == False
        assert genre.categories == categories

    def test_genre_str_representation(self):
        genre = Genre(name="Comedy", is_active=True)

        assert str(genre) == "Comedy - (True)"

    def test_genre_repr_representation(self):
        genre_id = uuid.uuid4()
        genre = Genre(
            id=genre_id,
            name="Comedy",
            is_active=True
        )

        assert repr(genre) == f"<Genre Comedy ({genre_id})>"


class TestActivateGenre:
    def test_activate_inactive_genre(self):
        genre = Genre(name="Comedy", is_active=False)

        genre.activate()

        assert genre.is_active == True

    def test_activate_active_genre(self):
        genre = Genre(name="Comedy", is_active=True)

        genre.activate()

        assert genre.is_active == True


class TestDeactivateGenre:
    def test_deactivate_inactive_genre(self):
        genre = Genre(name="Comedy", is_active=False)

        genre.deactivate()

        assert genre.is_active == False

    def test_deactivate_active_genre(self):
        genre = Genre(name="Comedy", is_active=True)

        genre.deactivate()

        assert genre.is_active == False


class TestEquality:
    def test_when_genres_have_same_id_they_are_equal(self):
        genre_id = uuid.uuid4()
        genre_1 = Genre(id=genre_id, name="Comedy")
        genre_2 = Genre(id=genre_id, name="Comedy")

        assert genre_1 == genre_2

    def test_equality_different_classes(self):
        class Dummy:
            pass

        genre_id = uuid.uuid4()
        genre = Genre(id=genre_id, name="Comedy")
        dummy = Dummy()
        dummy.id = genre_id

        assert genre != dummy


class TestChangeName:
    def test_change_name(self):
        genre = Genre(name="Comedy")

        genre.change_name("Terror")
        assert genre.name == "Terror"

    def test_when_name_is_empty(self):
        genre = Genre(name="Comedy")

        with pytest.raises(ValueError, match="name cannot be empty"):
            genre.change_name("")


class TestAddCategory:
    def test_add_category_to_genre(self):
        genre = Genre(name="Comedy")
        category_id = uuid.uuid4()

        assert category_id not in genre.categories
        genre.add_category(category_id=category_id)
        assert category_id in genre.categories

    def test_add_multiples_category_to_genre(self):
        genre = Genre(name="Comedy")
        category_1 = uuid.uuid4()
        category_2 = uuid.uuid4()

        assert category_1 not in genre.categories
        assert category_2 not in genre.categories

        genre.add_category(category_id=category_1)
        genre.add_category(category_id=category_2)
        assert category_1 in genre.categories
        assert category_2 in genre.categories


class TestRemoveCategory:
    def test_remove_category_to_genre(self):
        category_id = uuid.uuid4()
        genre = Genre(name="Comedy", categories=[category_id])

        assert category_id in genre.categories
        genre.remove_category(category_id=category_id)
        assert category_id not in genre.categories
