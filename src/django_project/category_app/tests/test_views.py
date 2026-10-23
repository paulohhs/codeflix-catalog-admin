import uuid

from rest_framework.test import APIClient
from rest_framework import status
import pytest

from src.core.category.domain.category import Category
from src.django_project.category_app.repository import DjangoORMCategoryRepository


@pytest.mark.django_db
class TestListAPI:
    def test_list_categories(
        self,
        mock_movie_category: Category,
        mock_documentary_category: Category,
        category_repository: DjangoORMCategoryRepository,
    ):
        category_repository.save(mock_movie_category)
        category_repository.save(mock_documentary_category)

        url = "/api/categories/"
        response = APIClient().get(url)

        expected_data = {
            "data": [
                {
                    "id": str(mock_documentary_category.id),
                    "name": mock_documentary_category.name,
                    "description": mock_documentary_category.description,
                    "is_active": mock_documentary_category.is_active,
                },
                {
                    "id": str(mock_movie_category.id),
                    "name": mock_movie_category.name,
                    "description": mock_movie_category.description,
                    "is_active": mock_movie_category.is_active,
                },
            ],
            "meta": {
                "current_page": 1,
                "per_page": 2,
                "total": 2,
            }
        }

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["data"]) == 2
        assert response.data == expected_data

    @pytest.mark.parametrize(
        "order_by, current_page",
        [
            ("name", 1),
            ("name", 2),
            ("description", 1),
            ("description", 2),
        ]
    )
    def test_list_categories_with_sorting_and_pagination(
        self,
        category_repository: DjangoORMCategoryRepository,
        mock_category: callable,
        order_by: str,
        current_page: int,
    ):
        category_a = mock_category(name="A", description="B")
        category_repository.save(category_a)

        category_b = mock_category(name="B", description="C")
        category_repository.save(category_b)

        category_c = mock_category(name="C", description="A")
        category_repository.save(category_c)

        if order_by == "name":
            expected_data_per_page = {
                1: [category_a, category_b],
                2: [category_c],
            }
        else:
            expected_data_per_page = {
                1: [category_c, category_a],
                2: [category_b],
            }

        expected_data = {
            "data": [
                {
                    "id": str(category.id),
                    "name": category.name,
                    "description": category.description,
                    "is_active": category.is_active,
                }
                for category in expected_data_per_page[current_page]
            ],
            "meta": {
                "current_page": current_page,
                "per_page": 2,
                "total": 3,
            }
        }

        url = f"/api/categories/?order_by={order_by}&current_page={current_page}"
        response = APIClient().get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["data"]) == len(expected_data_per_page[current_page])
        assert response.data == expected_data


@pytest.mark.django_db
class TestRetrieveAPI:
    def test_when_id_is_invalid_return_400(self):
        url = '/api/categories/1234567/'

        response = APIClient().get(url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_return_category_when_exists(
        self,
        mock_movie_category: Category,
        mock_documentary_category: Category,
        category_repository: DjangoORMCategoryRepository,
    ):
        category_repository.save(mock_movie_category)
        category_repository.save(mock_documentary_category)

        url = f"/api/categories/{mock_documentary_category.id}/"
        response = APIClient().get(url)

        expected_data = {
            "data": {
                "id": str(mock_documentary_category.id),
                "name": mock_documentary_category.name,
                "description": mock_documentary_category.description,
                "is_active": mock_documentary_category.is_active,
            }
        }

        assert response.status_code == status.HTTP_200_OK
        assert response.data == expected_data

    def test_return_404_when_category_not_exists(self):
        url = f"/api/categories/{uuid.uuid4()}/"
        response = APIClient().get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestCreateAPI:
    def test_when_payload_is_invalid_then_return_400(self):
        url = '/api/categories/'

        response = APIClient().post(
            url,
            data={
                "name": "",
                "description": "Movie description",
            }
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_when_payload_is_valid_then_create_category_and_return_201(
        self,
        category_repository: DjangoORMCategoryRepository,
    ):
        url = '/api/categories/'
        
        response = APIClient().post(
            url,
            data={
                "name": "Movie",
                "description": "Movie description",
            }
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert category_repository.list() == [
            Category(
                id=uuid.UUID(response.data["id"]),
                name="Movie",
                description="Movie description",
                is_active=True,
            )
        ]


@pytest.mark.django_db
class TestUpdateAPI:
    def test_when_payload_is_invalid_then_return_400(self):
        url = '/api/categories/12345678/'
        
        response = APIClient().put(
            url,
            data={
                "name": "",
                "description": "Movie description",
            }
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {
            "name": ["This field may not be blank."],
            "id": ["Must be a valid UUID."],
            "is_active": ["This field is required."]
        }

    def test_when_payload_is_valid_update_category_and_return_204(
        self,
        mock_movie_category: Category,
        category_repository: DjangoORMCategoryRepository,
    ):
        category_repository.save(mock_movie_category)
        
        url = f'/api/categories/{mock_movie_category.id}/'
        response = APIClient().put(
            url,
            data={
                "name": "Docs",
                "description": "Docs description",
                "is_active": True,
            }
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

        updated_category = category_repository.get_by_id(mock_movie_category.id)

        assert updated_category.name == "Docs"
        assert updated_category.description == "Docs description"
        assert updated_category.is_active is True

    def test_when_category_doesnt_exist_then_return_404(self):
        url = f"/api/categories/{uuid.uuid4()}/"
        response = APIClient().put(
            url,
            data={
                "name": "Docs",
                "description": "Docs description",
                "is_active": True,
            },
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestDeleteAPI:
    def test_when_id_is_invalid_then_return_400(self):
        url = f"/api/categories/12345678/"
        response = APIClient().delete(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_when_category_doesnt_exist_then_return_404(self):
        url = f"/api/categories/{uuid.uuid4()}/"
        response = APIClient().delete(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_when_category_does_exist_then_delete_and_return_204(
        self,
        mock_movie_category: Category,
        category_repository: DjangoORMCategoryRepository,
    ):
        category_repository.save(mock_movie_category)

        url = f"/api/categories/{mock_movie_category.id}/"
        response = APIClient().delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert category_repository.list() == []


@pytest.mark.django_db
class TestPartialUpdateAPI:
    def test_when_id_is_invalid_then_return_400(self):
        url = '/api/categories/12345678/'
        
        response = APIClient().patch(
            url,
            data={"name": "Movie"}
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {
            "id": ["Must be a valid UUID."],
        }

    def test_when_category_doesnt_exist_then_return_404(self):
        url = f"/api/categories/{uuid.uuid4()}/"
        response = APIClient().patch(
            url,
            data={
                "name": "Docs",
            },
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_category_name_and_return_204(
        self,
        mock_movie_category: Category,
        category_repository: DjangoORMCategoryRepository,
    ):
        category_repository.save(mock_movie_category)
        
        url = f'/api/categories/{mock_movie_category.id}/'
        response = APIClient().patch(
            url,
            data={
                "name": "Docs",
            }
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

        updated_category = category_repository.get_by_id(mock_movie_category.id)

        assert updated_category.name != mock_movie_category.name
        assert updated_category.name == "Docs"

        assert updated_category.description == mock_movie_category.description
        assert updated_category.description == "Movie description"

        assert updated_category.is_active == mock_movie_category.is_active
        assert updated_category.is_active is True

    def test_update_category_description_and_return_204(
        self,
        mock_movie_category: Category,
        category_repository: DjangoORMCategoryRepository,
    ):
        category_repository.save(mock_movie_category)
        
        url = f'/api/categories/{mock_movie_category.id}/'
        response = APIClient().patch(
            url,
            data={
                "description": "Docs description",
            }
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

        updated_category = category_repository.get_by_id(mock_movie_category.id)

        assert updated_category.name == mock_movie_category.name
        assert updated_category.name == "Movie"

        assert updated_category.description != mock_movie_category.description
        assert updated_category.description == "Docs description"

        assert updated_category.is_active == mock_movie_category.is_active
        assert updated_category.is_active is True

    def test_activate_category_and_return_204(
        self,
        mock_movie_category: Category,
        category_repository: DjangoORMCategoryRepository,
    ):
        mock_movie_category.is_active = False
        category_repository.save(mock_movie_category)
        
        url = f'/api/categories/{mock_movie_category.id}/'
        response = APIClient().patch(
            url,
            data={
                "is_active": True,
            }
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

        updated_category = category_repository.get_by_id(mock_movie_category.id)

        assert updated_category.name == mock_movie_category.name
        assert updated_category.name == "Movie"

        assert updated_category.description == mock_movie_category.description
        assert updated_category.description == "Movie description"

        assert updated_category.is_active != mock_movie_category.is_active
        assert updated_category.is_active is True

    def test_deactivate_category_and_return_204(
        self,
        mock_movie_category: Category,
        category_repository: DjangoORMCategoryRepository,
    ):
        assert mock_movie_category.is_active is True
        category_repository.save(mock_movie_category)
        
        url = f'/api/categories/{mock_movie_category.id}/'
        response = APIClient().patch(
            url,
            data={
                "is_active": False,
            }
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

        updated_category = category_repository.get_by_id(mock_movie_category.id)

        assert updated_category.name == mock_movie_category.name
        assert updated_category.name == "Movie"

        assert updated_category.description == mock_movie_category.description
        assert updated_category.description == "Movie description"

        assert updated_category.is_active != mock_movie_category.is_active
        assert updated_category.is_active is False
