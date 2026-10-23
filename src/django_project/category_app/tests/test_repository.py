import uuid

import pytest

from src.core.category.domain.category import Category
from src.django_project.category_app.models import Category as CategoryModel


@pytest.mark.django_db
class TestSave:
    def test_save_category_in_database(
        self,
        category_repository,
    ):
        category = Category(
            name="Filme",
            description="Categoria de filmes"
        )
        assert CategoryModel.objects.count() == 0

        category_repository.save(category=category)
        assert CategoryModel.objects.count() == 1

        category_db = CategoryModel.objects.get()
        assert category_db.id == category.id
        assert category_db.name == category.name
        assert category_db.description == category.description
        assert category_db.is_active == category.is_active


@pytest.mark.django_db
class TestGet:
    def test_get_by_id_return_none_when_not_existing_category(
        self,
        category_repository,
    ):
        category_db = category_repository.get_by_id(id=uuid.uuid4())
        assert category_db is None

    def test_get_by_id(
        self,
        category_repository,
    ):
        category_id = uuid.uuid4()

        dados_category = {
            "id": category_id,
            "name": "Filme",
            "description": "Categoria de filmes",
            "is_active": True,
        }
        CategoryModel.objects.create(
            **dados_category
        )
        assert CategoryModel.objects.count() == 1

        category_db = category_repository.get_by_id(id=category_id)
        assert category_db.id == category_id
        assert category_db.name == dados_category["name"]
        assert category_db.description == dados_category["description"]
        assert category_db.is_active == dados_category["is_active"]


@pytest.mark.django_db
class TestDelete:
    def test_delete(
        self,
        category_repository,
    ):
        category_id = uuid.uuid4()

        dados_category = {
            "id": category_id,
            "name": "Filme",
            "description": "Categoria de filmes",
            "is_active": True,
        }
        CategoryModel.objects.create(
            **dados_category
        )
        assert CategoryModel.objects.count() == 1

        category_repository.delete(id=category_id)
        assert CategoryModel.objects.count() == 0


@pytest.mark.django_db
class TestList:
    def test_return_empty_list_when_no_categories(
        self,
        category_repository,
    ):
        categories_db = category_repository.list()
        assert categories_db == []

    def test_list(
        self,
        category_repository,
    ):
        category_id_filme = uuid.uuid4()
        category_id_serie = uuid.uuid4()

        dados_category_filme = {
            "id": category_id_filme,
            "name": "Filme",
            "description": "Categoria de filmes",
            "is_active": True,
        }
        CategoryModel.objects.create(
            **dados_category_filme
        )
        
        dados_category_serie = {
            "id": category_id_serie,
            "name": "Série",
            "description": "Categoria de séries",
            "is_active": True,
        }
        CategoryModel.objects.create(
            **dados_category_serie
        )
        assert CategoryModel.objects.count() == 2

        categories_db = category_repository.list()
        assert len(categories_db) == 2
        assert categories_db == [
            Category(
                id=category_id_filme,
                name=dados_category_filme["name"],
                description=dados_category_filme["description"],
                is_active=dados_category_filme["is_active"],
            ),
            Category(
                id=category_id_serie,
                name=dados_category_serie["name"],
                description=dados_category_serie["description"],
                is_active=dados_category_serie["is_active"],
            )
        ]


@pytest.mark.django_db
class TestUpdate:
    def test_update(
        self,
        category_repository,
    ):
        category_id = uuid.uuid4()

        CategoryModel.objects.create(
            id=category_id,
            name="Filme",
            description="Categoria de filmes",
            is_active=True,
        )
        assert CategoryModel.objects.count() == 1

        category_to_update = Category(
            id=category_id,
            name="Série",
            description="Categoria de séries",
            is_active=True,
        )
        category_repository.update(category=category_to_update)
        assert CategoryModel.objects.count() == 1

        category_db = CategoryModel.objects.get(id=category_id)
        assert category_db.id == category_id
        assert category_db.name == category_to_update.name
        assert category_db.description == category_to_update.description
        assert category_db.is_active == category_to_update.is_active
