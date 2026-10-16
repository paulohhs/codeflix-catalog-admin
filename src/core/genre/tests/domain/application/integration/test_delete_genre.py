from unittest.mock import create_autospec
import uuid

import pytest

from src.core.genre.application.use_cases.delete_genre import DeleteGenre
from src.core.genre.application.use_cases.exceptions import GenreNotFound
from src.core.genre.domain.genre import Genre
from src.core.genre.infra.in_memory_genre_repository import InMemoryGenreRepository



class TestDeleteGenre:
    def test_delete_genre_from_repository(self):
        genre_repository = InMemoryGenreRepository()

        genre = Genre(name="Comedy")
        genre_repository.save(genre=genre)

        use_case = DeleteGenre(repository=genre_repository)

        assert len(genre_repository.list()) == 1

        use_case.execute(input=DeleteGenre.Input(id=genre.id))
        assert len(genre_repository.list()) == 0

    def test_when_genre_doesnt_exist_then_raise_not_found_exception(
        self,
    ):
        genre_repository = InMemoryGenreRepository()

        use_case = DeleteGenre(repository=genre_repository)

        with pytest.raises(GenreNotFound, match="Genre not found"):
            use_case.execute(input=DeleteGenre.Input(id=uuid.uuid4()))
        