import pytest
from uuid import UUID
import uuid
from category import Category

class TestCategory:
    def test_name_is_required(self):
        with pytest.raises(TypeError, match="missing 1 required positional argument: 'name'"):
            Category()

    def test_name_must_have_less_than_256_characters(self):
        with pytest.raises(ValueError, match="name must have less than 256 characters"):
            Category(name="a" * 256)

    def test_category_must_be_created_with_id_as_uuid(self):
        category = Category(name="Test Category")
        assert isinstance(category.id, UUID)

    def test_created_category_with_default_values(self):
        category = Category(name="Test Category")
        assert category.name == "Test Category"
        assert category.description == ""
        assert category.is_active == True

    def test_category_is_created_as_active_by_default(self):
        category = Category(name="Test Category")
        assert category.is_active == True

    def test_category_is_created_with_provided_values(self):
        category_id = uuid.uuid4()
        category = Category(
            id=category_id,
            name="Test Category", 
            description="A test category", 
            is_active=False
        )
        assert category.id == category_id
        assert category.name == "Test Category"
        assert category.description == "A test category"
        assert category.is_active == False

    def test_category_str_representation(self):
        category = Category(name="Test Category", description="A test category", is_active=True)
        assert str(category) == "Test Category - A test category (True)"

    def test_category_repr_representation(self):
        category_id = uuid.uuid4()
        category = Category(
            id=category_id,
            name="Test Category",
            description="A test category",
            is_active=True
        )
        assert repr(category) == f"<Category Test Category ({category_id})>"
