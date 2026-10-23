import uuid

from rest_framework import status
from rest_framework.test import APIClient

import pytest

from shared.tests.mocks.mock_category import mock_documentary_category, mock_movie_category
from src.django_project.genre_app.models import Genre as GenreORM


@pytest.mark.django_db
class TestListAPI:
    @pytest.mark.parametrize(
        "current_page",
        [1, 2, 3]
    )
    def test_list_genres_and_categories(
        self,
        mock_genre,
        mock_drama_genre,
        mock_comedy_genre,
        genre_repository,
        category_repository_with_data,
        current_page,
    ):
        genre_novel = mock_genre(name="Novel", is_active=False)
        genre_cartoon = mock_genre(name="Carton", is_active=False)
        genre_romance = mock_genre(name="Romance", is_active=False)
        genre_repository.save(genre=mock_drama_genre)
        genre_repository.save(genre=genre_romance)
        genre_repository.save(genre=mock_comedy_genre)
        genre_repository.save(genre=genre_novel)
        genre_repository.save(genre=genre_cartoon)

        expected_data_per_page = {
            1: [genre_cartoon, mock_comedy_genre],
            2: [mock_drama_genre, genre_novel],
            3: [genre_romance]
        }

        expected_response = {
            "data": [
                {
                    "id": str(genre.id),
                    "name": genre.name,
                    "is_active": genre.is_active,
                    "categories": [
                        str(category) for category in genre.categories
                    ] if len(genre.categories) > 0 else [],
                } for genre in expected_data_per_page[current_page]
            ],
            "meta": {
                "current_page": current_page,
                "per_page": 2,
                "total": 5,
            }
        }

        url = f"/api/genres/?current_page={current_page}"

        response = APIClient().get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == expected_response


@pytest.mark.django_db
class TestCreateAPI:
    def test_create_genre_with_associated_categories(
        self,
        mock_movie_category,
        mock_documentary_category,
        category_repository_with_data,
        genre_repository,
    ):
        url = "/api/genres/"
        data = {
            "name": "Drama",
            "categories": [
                str(mock_movie_category.id),
                str(mock_documentary_category.id),
            ],
        }

        response = APIClient().post(url, data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["id"]
        created_genre_id = response.data["id"]

        saved_genre = genre_repository.get_by_id(id=created_genre_id)
        assert saved_genre.name == "Drama"
        assert saved_genre.categories == {
            mock_movie_category.id,
            mock_documentary_category.id,
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
        mock_drama_genre,
        genre_repository,
    ):
        genre_repository.save(genre=mock_drama_genre)
        assert GenreORM.objects.count() == 1

        url = f"/api/genres/{mock_drama_genre.id}/"
        response = APIClient().delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert genre_repository.get_by_id(mock_drama_genre.id) is None
        assert GenreORM.objects.count() == 0


@pytest.mark.django_db
class TestUpdateAPI:
    def test_when_request_data_is_valid_then_update_genre(
        self,
        mock_documentary_category,
        mock_drama_genre,
        genre_repository,
        category_repository_with_data,
    ) -> None:
        genre_repository.save(mock_drama_genre)

        url = f"/api/genres/{str(mock_drama_genre.id)}/"
        data = {
            "name": "Drama",
            "is_active": True,
            "categories": [mock_documentary_category.id],
        }
        response = APIClient().put(url, data=data)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        updated_genre = genre_repository.get_by_id(mock_drama_genre.id)
        assert updated_genre.name == "Drama"
        assert updated_genre.is_active is True
        assert updated_genre.categories == {mock_documentary_category.id}

    def test_when_request_data_is_invalid_then_return_400(
        self,
        mock_drama_genre,
    ) -> None:
        url = f"/api/genres/{str(mock_drama_genre.id)}/"
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
        mock_drama_genre,
        genre_repository,
        category_repository_with_data,
    ) -> None:
        genre_repository.save(mock_drama_genre)

        url = f"/api/genres/{str(mock_drama_genre.id)}/"
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
