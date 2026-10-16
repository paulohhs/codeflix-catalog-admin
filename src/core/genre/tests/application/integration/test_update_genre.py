from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository
from src.core.genre.application.use_cases.update_genre import UpdateGenre
from src.core.genre.domain.genre import Genre
from src.core.genre.infra.in_memory_genre_repository import InMemoryGenreRepository


class TestUpdateGenre:
    def test_can_update_genre_attributes(self):
        movie_category = Category(name="Movie")
        documentary_category = Category(name="Documentary")
        category_repository = InMemoryCategoryRepository()
        category_repository.save(movie_category)
        category_repository.save(documentary_category)

        genre = Genre(name="Comedy", is_active=False)
        genre_repository = InMemoryGenreRepository()
        genre_repository.save(genre)

        use_case = UpdateGenre(
            repository=genre_repository,
            category_repository=category_repository
        )

        input = UpdateGenre.Input(
            id=genre.id,
            name="Terror",
            is_active=True,
            category_ids={movie_category.id, documentary_category.id}
        )
        use_case.execute(input=input)

        updated_genre = genre_repository.get_by_id(id=genre.id)
        assert updated_genre.id == genre.id
        assert updated_genre.name == input.name
        assert updated_genre.is_active == input.is_active
        assert updated_genre.categories == input.category_ids
