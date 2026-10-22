import uuid

from rest_framework.test import APIClient
from rest_framework import status
import pytest

from src.core.category.domain.category import Category
from src.django_project.category_app.repository import DjangoORMCategoryRepository


@pytest.fixture
def category_movie() -> Category:
    return Category(
        name="Movie",
        description="Movie description",
    )


@pytest.fixture
def category_documentary() -> Category:
    return Category(
        name="Documentary",
        description="Documentary description",
    )


@pytest.fixture
def category_repository() -> DjangoORMCategoryRepository:
    return DjangoORMCategoryRepository()


@pytest.mark.django_db
class TestListAPI:
    def test_list_categories(
        self,
        category_movie: Category,
        category_documentary: Category,
        category_repository: DjangoORMCategoryRepository,
    ):
        category_repository.save(category_movie)
        category_repository.save(category_documentary)

        url = "/api/categories/"
        response = APIClient().get(url)

        expected_data = {
            "data": [
                {
                    "id": str(category_documentary.id),
                    "name": category_documentary.name,
                    "description": category_documentary.description,
                    "is_active": category_documentary.is_active,
                },
                {
                    "id": str(category_movie.id),
                    "name": category_movie.name,
                    "description": category_movie.description,
                    "is_active": category_movie.is_active,
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
        order_by: str,
        current_page: int,
    ):
        category_a = Category(name="A", description="B")
        category_repository.save(category_a)

        category_b = Category(name="B", description="C")
        category_repository.save(category_b)

        category_c = Category(name="C", description="A")
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
        category_movie: Category,
        category_documentary: Category,
        category_repository: DjangoORMCategoryRepository,
    ):
        category_repository.save(category_movie)
        category_repository.save(category_documentary)

        url = f"/api/categories/{category_documentary.id}/"
        response = APIClient().get(url)

        expected_data = {
            "data": {
                "id": str(category_documentary.id),
                "name": category_documentary.name,
                "description": category_documentary.description,
                "is_active": category_documentary.is_active,
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
        category_movie: Category,
        category_repository: DjangoORMCategoryRepository,
    ):
        category_repository.save(category_movie)
        
        url = f'/api/categories/{category_movie.id}/'        
        response = APIClient().put(
            url,
            data={
                "name": "Docs",
                "description": "Docs description",
                "is_active": True,
            }
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

        updated_category = category_repository.get_by_id(category_movie.id)

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
        category_movie: Category,
        category_repository: DjangoORMCategoryRepository,
    ):
        category_repository.save(category_movie)

        url = f"/api/categories/{category_movie.id}/"
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
        category_movie: Category,
        category_repository: DjangoORMCategoryRepository,
    ):
        category_repository.save(category_movie)
        
        url = f'/api/categories/{category_movie.id}/'        
        response = APIClient().patch(
            url,
            data={
                "name": "Docs",
            }
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

        updated_category = category_repository.get_by_id(category_movie.id)

        assert updated_category.name != category_movie.name
        assert updated_category.name == "Docs"

        assert updated_category.description == category_movie.description
        assert updated_category.description == "Movie description"

        assert updated_category.is_active == category_movie.is_active
        assert updated_category.is_active is True

    def test_update_category_description_and_return_204(
        self,
        category_movie: Category,
        category_repository: DjangoORMCategoryRepository,
    ):
        category_repository.save(category_movie)
        
        url = f'/api/categories/{category_movie.id}/'        
        response = APIClient().patch(
            url,
            data={
                "description": "Docs description",
            }
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

        updated_category = category_repository.get_by_id(category_movie.id)

        assert updated_category.name == category_movie.name
        assert updated_category.name == "Movie"

        assert updated_category.description != category_movie.description
        assert updated_category.description == "Docs description"

        assert updated_category.is_active == category_movie.is_active
        assert updated_category.is_active is True

    def test_activate_category_and_return_204(
        self,
        category_movie: Category,
        category_repository: DjangoORMCategoryRepository,
    ):
        category_movie.is_active = False
        category_repository.save(category_movie)
        
        url = f'/api/categories/{category_movie.id}/'        
        response = APIClient().patch(
            url,
            data={
                "is_active": True,
            }
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

        updated_category = category_repository.get_by_id(category_movie.id)

        assert updated_category.name == category_movie.name
        assert updated_category.name == "Movie"

        assert updated_category.description == category_movie.description
        assert updated_category.description == "Movie description"

        assert updated_category.is_active != category_movie.is_active
        assert updated_category.is_active is True

    def test_deactivate_category_and_return_204(
        self,
        category_movie: Category,
        category_repository: DjangoORMCategoryRepository,
    ):
        assert category_movie.is_active is True
        category_repository.save(category_movie)
        
        url = f'/api/categories/{category_movie.id}/'        
        response = APIClient().patch(
            url,
            data={
                "is_active": False,
            }
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

        updated_category = category_repository.get_by_id(category_movie.id)

        assert updated_category.name == category_movie.name
        assert updated_category.name == "Movie"

        assert updated_category.description == category_movie.description
        assert updated_category.description == "Movie description"

        assert updated_category.is_active != category_movie.is_active
        assert updated_category.is_active is False
