import uuid

from rest_framework import status
from rest_framework.test import APIClient

import pytest

from src.core.category.domain.category import Category
from src.core.genre.domain.genre import Genre
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.genre_app.repository import DjangoORMGenreRepository
from src.django_project.genre_app.models import Genre as GenreORM


@pytest.fixture
def category_movie():
    return Category(
        name="Movie",
        description="Movie description",
    )

@pytest.fixture
def category_documentary():
    return Category(
        name="Documentary",
        description="Documentary description",
    )


@pytest.fixture
def category_repository(category_documentary, category_movie) -> DjangoORMCategoryRepository:
    repo = DjangoORMCategoryRepository()
    repo.save(category=category_movie)
    repo.save(category=category_documentary)

    return repo


@pytest.fixture
def genre_romance(category_documentary, category_movie) -> Genre:
    return Genre(
        name="Romance",
        is_active=True,
        categories={category_movie.id, category_documentary.id}
    )


@pytest.fixture
def genre_drama() -> Genre:
    return Genre(
        name="Drama",
        is_active=True,
        categories=set()
    )

@pytest.fixture
def genre_repository() -> DjangoORMGenreRepository:
    return DjangoORMGenreRepository()


@pytest.mark.django_db
class TestListAPI:
    def test_list_genres_and_categories(
        self,
        genre_drama,
        genre_romance,
        genre_repository,
        category_documentary,
        category_movie,
        category_repository,
    ):
        genre_repository.save(genre=genre_romance)
        genre_repository.save(genre=genre_drama)

        # expected_response = {
        #     "data": [
        #         {
        #             "id": str(genre_romance.id),
        #             "name": genre_romance.name,
        #             "is_active": genre_romance.is_active,
        #             "categories": [
        #                 str(category_movie.id),
        #                 str(category_documentary.id),
        #             ],
        #         },
        #         {
        #             "id": str(genre_drama.id),
        #             "name": genre_drama.name,
        #             "is_active": genre_drama.is_active,
        #             "categories": [],
        #         }
        #     ]
        # }

        url = "/api/genres/"

        response = APIClient().get(url)
        assert response.status_code == status.HTTP_200_OK
        # assert response.data == expected_response

        assert response.data["data"]
        assert response.data["data"][0]["id"] == str(genre_drama.id)
        assert response.data["data"][0]["name"] == genre_drama.name
        assert response.data["data"][0]["is_active"] == genre_drama.is_active
        assert set(response.data["data"][0]["categories"]) == set()

        assert response.data["data"][1]["id"] == str(genre_romance.id)
        assert response.data["data"][1]["name"] == genre_romance.name
        assert response.data["data"][1]["is_active"] == genre_romance.is_active
        assert len(response.data["data"][1]["categories"]) == 2


@pytest.mark.django_db
class TestCreateAPI:
    def test_create_genre_with_associated_categories(
        self,
        category_movie,
        category_documentary,
        category_repository,
        genre_repository: DjangoORMGenreRepository,
    ):
        url = "/api/genres/"
        data = {
            "name": "Drama",
            "categories": [
                str(category_movie.id),
                str(category_documentary.id),
            ],
        }

        response = APIClient().post(url, data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["id"]
        created_genre_id = response.data["id"]

        saved_genre = genre_repository.get_by_id(id=created_genre_id)
        assert saved_genre.name == "Drama"
        assert saved_genre.categories == {
            category_movie.id,
            category_documentary.id,
        }


@pytest.mark.django_db
class TestDeleteAPI:
    def test_when_genre_doesnt_exist_then_raise_404(self):
        url = f"/api/genres/{uuid.uuid4()}/"
        response = APIClient().delete(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_when_id_is_invalid_then_return_400(self):
        url = f"/api/genres/1/"
        response = APIClient().delete(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_delete_genre_from_repository(
        self,
        genre_drama,
        genre_repository,
    ):
        genre_repository.save(genre=genre_drama)
        assert GenreORM.objects.count() == 1

        url = f"/api/genres/{genre_drama.id}/"
        response = APIClient().delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert genre_repository.get_by_id(genre_drama.id) is None
        assert GenreORM.objects.count() == 0


@pytest.mark.django_db
class TestUpdateAPI:
    def test_when_request_data_is_valid_then_update_genre(
        self,
        category_repository: DjangoORMCategoryRepository,
        category_movie: Category,
        category_documentary: Category,
        genre_repository: DjangoORMGenreRepository,
        genre_romance: Genre,
    ) -> None:
        genre_repository.save(genre_romance)

        url = f"/api/genres/{str(genre_romance.id)}/"
        data = {
            "name": "Drama",
            "is_active": True,
            "categories": [category_documentary.id],
        }
        response = APIClient().put(url, data=data)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        updated_genre = genre_repository.get_by_id(genre_romance.id)
        assert updated_genre.name == "Drama"
        assert updated_genre.is_active is True
        assert updated_genre.categories == {category_documentary.id}

    def test_when_request_data_is_invalid_then_return_400(
        self,
        genre_drama: Genre,
    ) -> None:
        url = f"/api/genres/{str(genre_drama.id)}/"
        data = {
            "name": "",
            "is_active": True,
            "categories": [],
        }
        response = APIClient().put(url, data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {"name": ["This field may not be blank."]}

    def test_when_related_categories_do_not_exist_then_return_400(
        self,
        category_repository: DjangoORMCategoryRepository,
        category_movie: Category,
        category_documentary: Category,
        genre_repository: DjangoORMGenreRepository,
        genre_romance: Genre,
    ) -> None:
        genre_repository.save(genre_romance)

        url = f"/api/genres/{str(genre_romance.id)}/"
        data = {
            "name": "Romance",
            "is_active": True,
            "categories": [uuid.uuid4()],  # non-existent category
        }
        response = APIClient().put(url, data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Categories not found" in response.data["error"]

    def test_when_genre_does_not_exist_then_return_404(self) -> None:
        url = f"/api/genres/{str(uuid.uuid4())}/"
        data = {
            "name": "Romance",
            "is_active": True,
            "categories": [],
        }
        response = APIClient().put(url, data=data)

        assert response.status_code == status.HTTP_404_NOT_FOUND
