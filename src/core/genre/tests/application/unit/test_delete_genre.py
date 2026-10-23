import uuid
import pytest

from src.core.genre.application.use_cases.delete_genre import DeleteGenre
from src.core.genre.application.use_cases.exceptions import GenreNotFound
from src.core.genre.domain.genre import Genre


class TestDeleteGenre:
    def test_delete_genre_from_repository(
        self,
        mock_genre_repository,
    ):
        genre = Genre(name="Comedy")
        mock_genre_repository.get_by_id.return_value = genre

        use_case = DeleteGenre(repository=mock_genre_repository)
        use_case.execute(input=DeleteGenre.Input(id=genre.id))

        mock_genre_repository.delete.assert_called_once_with(genre.id)

    def test_when_genre_doesnt_exist_then_raise_not_found_exception(
        self,
        mock_genre_repository,
    ):
        mock_genre_repository.get_by_id.return_value = None

        use_case = DeleteGenre(repository=mock_genre_repository)

        with pytest.raises(GenreNotFound, match="Genre not found"):
            use_case.execute(input=DeleteGenre.Input(id=uuid.uuid4()))

        mock_genre_repository.delete.assert_not_called
        