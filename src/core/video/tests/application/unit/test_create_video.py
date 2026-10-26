import uuid
from decimal import Decimal

import pytest

from src.core.video.application.use_cases.exceptions import (
    InvalidVideo,
    RelatedEntitiesNotFound,
)
from src.core.video.domain.value_objects import Rating
from src.core.video.application.use_cases.create_video_without_media import CreateVideoWithoutMedia
from src.core.video.domain.video import Video


class TestCreateVideoWithoutMedia:
    @pytest.mark.parametrize(
        "invalid_entity, match_error",
        [
            ("categories", "Categories with provided IDs not found"),
            ("genres", "Genres with provided IDs not found"),
            ("cast_members", "Cast Members with provided IDs not found"),
            # Todos os erros devem aparecer de uma única vez
            ("all", "")
        ]
    )
    def test_when_some_entity_does_not_exist_then_raise_related_entities_not_found(
        self,
        mock_video_repository,
        mock_category_repository_with_data,
        mock_genre_repository_with_data,
        mock_cast_member_repository_with_data,
        invalid_entity,
        match_error,
    ):
        (
            movie_category,
            documentary_category,
            category_repository,
        ) = mock_category_repository_with_data
        category_ids = {movie_category.id, documentary_category.id}

        (
            comedy_genre,
            drama_genre,
            genre_repository,
        ) = mock_genre_repository_with_data
        genre_ids = {comedy_genre.id, drama_genre.id}

        (
            actor_member,
            director_member,
            cast_member_repository,
        ) = mock_cast_member_repository_with_data
        cast_member_ids = {actor_member.id, director_member.id}

        use_case = CreateVideoWithoutMedia(
            video_repository=mock_video_repository,
            category_repository=category_repository,
            genre_repository=genre_repository,
            cast_member_repository=cast_member_repository,
        )

        entities_data = {
            "categories": category_ids,
            "genres": genre_ids,
            "cast_members": cast_member_ids,
        }

        inexist_entities = {uuid.uuid4(), uuid.uuid4()}
        if invalid_entity == "categories":
            entities_data["categories"] = inexist_entities
        elif invalid_entity == "genres":
            entities_data["genres"] = inexist_entities
        elif invalid_entity == "cast_members":
            entities_data["cast_members"] = inexist_entities
        elif invalid_entity == "all":
            entities_data["categories"] = inexist_entities
            entities_data["genres"] = inexist_entities
            entities_data["cast_members"] = inexist_entities

            match_error  = (
                "Categories with provided IDs not found, "
                "Genres with provided IDs not found, "
                "Cast Members with provided IDs not found"
            )

        input_data = dict(
            title="Test Video",
            description="Test Description",
            launched_year=2021,
            duration=Decimal(100),
            rating=Rating.L,
            opened=True,
            **entities_data,
        )

        input = CreateVideoWithoutMedia.Input(**input_data)
        with pytest.raises(RelatedEntitiesNotFound, match=match_error):
            use_case.execute(input=input)

    @pytest.mark.parametrize(
        "invalid_title, match_error",
        [
            ("", "title cannot be empty"),
            ("a" * 256, "title cannot be longer than 255"),
        ]
    )
    def test_when_title_is_invalid_then_return_invalid_video(
        self,
        mock_video_repository,
        mock_category_repository_with_data,
        mock_genre_repository_with_data,
        mock_cast_member_repository_with_data,
        invalid_title,
        match_error,
    ):
        (
            movie_category,
            documentary_category,
            category_repository,
        ) = mock_category_repository_with_data
        category_ids = {movie_category.id, documentary_category.id}

        (
            comedy_genre,
            drama_genre,
            genre_repository,
        ) = mock_genre_repository_with_data
        genre_ids = {comedy_genre.id, drama_genre.id}

        (
            actor_member,
            director_member,
            cast_member_repository,
        ) = mock_cast_member_repository_with_data
        cast_member_ids = {actor_member.id, director_member.id}

        use_case = CreateVideoWithoutMedia(
            video_repository=mock_video_repository,
            category_repository=category_repository,
            genre_repository=genre_repository,
            cast_member_repository=cast_member_repository,
        )

        input = CreateVideoWithoutMedia.Input(
            title=invalid_title,
            description="Test Description",
            launched_year=2021,
            duration=Decimal(100),
            rating=Rating.L.value,
            opened=True,
            categories=category_ids,
            genres=genre_ids,
            cast_members=cast_member_ids,
        )
        with pytest.raises(InvalidVideo, match=match_error):
            use_case.execute(input=input)

    def test_create_video_without_media(
        self,
        mock_video_repository,
        mock_category_repository_with_data,
        mock_genre_repository_with_data,
        mock_cast_member_repository_with_data,
    ):
        (
            movie_category,
            documentary_category,
            category_repository,
        ) = mock_category_repository_with_data
        category_ids = {movie_category.id, documentary_category.id}

        (
            comedy_genre,
            drama_genre,
            genre_repository,
        ) = mock_genre_repository_with_data
        genre_ids = {comedy_genre.id, drama_genre.id}

        (
            actor_member,
            director_member,
            cast_member_repository,
        ) = mock_cast_member_repository_with_data
        cast_member_ids = {actor_member.id, director_member.id}

        use_case = CreateVideoWithoutMedia(
            video_repository=mock_video_repository,
            category_repository=category_repository,
            genre_repository=genre_repository,
            cast_member_repository=cast_member_repository,
        )

        input = CreateVideoWithoutMedia.Input(
            title="Test Video Title",
            description="Test Description",
            launched_year=2021,
            duration=Decimal(100),
            rating=Rating.L.value,
            opened=True,
            categories=category_ids,
            genres=genre_ids,
            cast_members=cast_member_ids,
        )

        output = use_case.execute(input=input)
        assert isinstance(output.id, uuid.UUID)
        mock_video_repository.save.assert_called_once_with(
            Video(
                id=output.id,
                title="Test Video Title",
                description="Test Description",
                launched_year=2021,
                duration=Decimal(100),
                published=False,
                rating=Rating.L,
                opened=True,
                categories=category_ids,
                genres=genre_ids,
                cast_members=cast_member_ids,
            )
        )
