import uuid
import pytest

from src.core.genre.application.use_cases.delete_genre import DeleteGenre
from src.core.genre.application.use_cases.exceptions import GenreNotFound



class TestDeleteGenre:
    def test_delete_genre_from_repository(
        self,
        mock_im_genre_repository_with_data,
    ):
        genre, _, genre_repository = mock_im_genre_repository_with_data
        use_case = DeleteGenre(repository=genre_repository)

        assert len(genre_repository.list()) == 2
        use_case.execute(input=DeleteGenre.Input(id=genre.id))

        assert len(genre_repository.list()) == 1
        assert genre_repository.get_by_id(genre.id) is None

    def test_when_genre_doesnt_exist_then_raise_not_found_exception(
        self,
        mock_im_genre_repository,
    ):
        use_case = DeleteGenre(repository=mock_im_genre_repository)

        with pytest.raises(GenreNotFound, match="Genre not found"):
            use_case.execute(input=DeleteGenre.Input(id=uuid.uuid4()))
        