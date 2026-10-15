import pytest
from uuid import UUID
import uuid
from src.core.category.domain.category import Category

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

    def test_cannot_create_category_with_empty_name(self):
        with pytest.raises(ValueError, match="name cannot be empty"):
            Category(name="")

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


class TestUpdateCategory:
    def test_update_category_with_name_and_description(self):
        category = Category(name="Old Name", description="Old Description")

        category.update_category(name="New Name", description="New Description")

        assert category.name == "New Name"
        assert category.description == "New Description"

    def test_update_category_with_invalid_name(self):
        category = Category(name="Old Name", description="Old Description")

        with pytest.raises(ValueError, match="name must have less than 256 characters"):
            category.update_category(name="a" * 256, description="New Description")


class TestActivateCategory:
    def test_activate_inactive_category(self):
        category = Category(name="Test Category", is_active=False)

        category.activate()

        assert category.is_active == True

    def test_activate_active_category(self):
        category = Category(name="Test Category", is_active=True)

        category.activate()

        assert category.is_active == True


class TestDeactivateCategory:
    def test_deactivate_inactive_category(self):
        category = Category(name="Test Category", is_active=False)

        category.deactivate()

        assert category.is_active == False

    def test_deactivate_active_category(self):
        category = Category(name="Test Category", is_active=True)

        category.deactivate()

        assert category.is_active == False


class TestEquality:
    def test_when_categories_have_same_id_they_are_equal(self):
        category_id = uuid.uuid4()
        category_1 = Category(id=category_id, name="Category")
        category_2 = Category(id=category_id, name="Category")

        assert category_1 == category_2

    def test_equality_different_classes(self):
        class Dummy:
            pass

        category_id = uuid.uuid4()
        category = Category(id=category_id, name="Category")
        dummy = Dummy()
        dummy.id = category_id

        assert category != dummy
