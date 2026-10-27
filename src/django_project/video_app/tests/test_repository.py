import pytest

from src.core.cast_member.domain.cast_member import CastMemberType
from src.django_project.video_app.models import Video as VideoORM


@pytest.mark.django_db
class TestSave:
    def test_save_video_without_media(
        self,
        mock_video_without_media,
        video_repository,
    ):
        assert VideoORM.objects.count() == 0

        video_repository.save(mock_video_without_media)
        assert VideoORM.objects.count() == 1

        video_model = VideoORM.objects.first()
        assert video_model.id == mock_video_without_media.id
        assert video_model.title == mock_video_without_media.title
        assert not video_model.published


@pytest.mark.django_db
class TestGet:
    def test_get_video(
        self,
        mock_video_without_media,
        video_repository,
    ):
        video_repository.save(mock_video_without_media)
        assert VideoORM.objects.count() == 1

        video_model = video_repository.get_by_id(id=mock_video_without_media.id)
        assert video_model is not None
        assert video_model.id == mock_video_without_media.id
        assert video_model.title == mock_video_without_media.title
        assert video_model.categories == mock_video_without_media.categories
        assert video_model.genres == mock_video_without_media.genres
        assert video_model.cast_members == mock_video_without_media.cast_members
        assert not video_model.published


@pytest.mark.django_db
class TestDelete:
    def test_delete_video(
        self,
        mock_video_without_media,
        video_repository,
    ):
        video_repository.save(mock_video_without_media)
        assert VideoORM.objects.count() == 1

        video_repository.delete(id=mock_video_without_media.id)
        assert VideoORM.objects.count() == 0
        assert video_repository.get_by_id(id=mock_video_without_media.id) is None


@pytest.mark.django_db
class TestList:
    def test_list_video(
        self,
        mock_video_without_media,
        video_repository,
    ):
        video_repository.save(mock_video_without_media)
        assert VideoORM.objects.count() == 1

        videos_model = video_repository.list()
        assert len(videos_model) == 1
        assert videos_model == [
            mock_video_without_media
        ]


@pytest.mark.django_db
class TestUpdate:
    def test_update_video(
        self,
        mock_category,
        category_repository,
        mock_genre,
        genre_repository,
        mock_cast_member,
        cast_member_repository,
        mock_video_without_media,
        video_repository,
    ):
        video_repository.save(mock_video_without_media)
        assert VideoORM.objects.count() == 1

        category = mock_category(name="New Category")
        category_repository.save(category)
        new_categories = {category.id}

        genre = mock_genre(name="New Genre")
        genre_repository.save(genre)
        new_genres = {genre.id}

        cast_member = mock_cast_member(name="New Cast Member", type=CastMemberType.ACTOR)
        cast_member_repository.save(cast_member)
        new_cast_members = {cast_member.id}

        mock_video_without_media.title = "Title updated"
        mock_video_without_media.description = "Description updated"
        mock_video_without_media.genres = new_genres
        mock_video_without_media.cast_members = new_cast_members
        mock_video_without_media.categories = new_categories

        video_repository.update(mock_video_without_media)
        updated_video = video_repository.get_by_id(id=mock_video_without_media.id)

        assert updated_video.id == mock_video_without_media.id
        assert updated_video.title == "Title updated"
        assert updated_video.description == "Description updated"
        assert updated_video.genres == new_genres
        assert updated_video.cast_members == new_cast_members
        assert updated_video.categories == new_categories
