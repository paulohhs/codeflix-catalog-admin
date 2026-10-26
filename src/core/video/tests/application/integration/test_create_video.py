import uuid
from decimal import Decimal

from src.core.video.domain.value_objects import Rating
from src.core.video.application.use_cases.create_video_without_media import CreateVideoWithoutMedia


class TestCreateVideoWithoutMedia:
    def test_create_video_without_media(
        self,
        mock_im_video_repository,
        mock_im_category_repository_with_data,
        mock_im_genre_repository_with_data,
        mock_im_cast_member_repository_with_data,
    ):
        (
            movie_category,
            documentary_category,
            category_repository,
        ) = mock_im_category_repository_with_data
        category_ids = {movie_category.id, documentary_category.id}

        (
            comedy_genre,
            drama_genre,
            genre_repository,
        ) = mock_im_genre_repository_with_data
        genre_ids = {comedy_genre.id, drama_genre.id}

        (
            actor_member,
            director_member,
            cast_member_repository,
        ) = mock_im_cast_member_repository_with_data
        cast_member_ids = {actor_member.id, director_member.id}

        use_case = CreateVideoWithoutMedia(
            video_repository=mock_im_video_repository,
            category_repository=category_repository,
            genre_repository=genre_repository,
            cast_member_repository=cast_member_repository,
        )

        input = CreateVideoWithoutMedia.Input(
            title="Test Video Title",
            description="Test Description",
            launch_year=2021,
            duration=Decimal(100),
            rating=Rating.L.value,
            opened=True,
            categories=category_ids,
            genres=genre_ids,
            cast_members=cast_member_ids,
        )

        output = use_case.execute(input=input)
        assert isinstance(output.id, uuid.UUID)

        saved_video = mock_im_video_repository.get_by_id(output.id)
        assert saved_video.title == "Test Video Title"
        assert saved_video.description == "Test Description"
        assert saved_video.published == False
        assert saved_video.categories == category_ids
        assert saved_video.genres == genre_ids
        assert saved_video.cast_members == cast_member_ids
