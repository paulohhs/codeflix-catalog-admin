from unittest.mock import create_autospec

import pytest

from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.django_project.cast_member_app.repository import DjangoORMCastMemberRepository
from src.core.cast_member.infra.in_memory_cast_member_repository import InMemoryCastMemberRepository
from src.core.cast_member.domain.cast_member import (
    CastMember,
    CastMemberType
)


@pytest.fixture(scope="function")
def mock_actor_member() -> callable:
    def make_mock(name: str = "Test Actor Member") -> CastMember:
        return CastMember(name=name, type=CastMemberType.ACTOR)

    yield make_mock


@pytest.fixture(scope="function")
def mock_director_member() -> callable:
    def make_mock(name: str = "Test Director Member") -> CastMember:
        return CastMember(name=name, type=CastMemberType.DIRECTOR)

    yield make_mock


@pytest.fixture(scope="function")
def mock_cast_member() -> callable:
    def make_mock(name: str, type: CastMemberType) -> CastMember:
        return CastMember(name=name, type=type)

    yield make_mock


@pytest.fixture
def mock_cast_member_repository() -> CastMemberRepository:
    return create_autospec(CastMemberRepository)


@pytest.fixture
def mock_cast_member_repository_with_data(
    mock_actor_member,
    mock_director_member,
) -> tuple[CastMember, CastMember, CastMemberRepository]:
    repository = create_autospec(CastMemberRepository)
    actor_member = mock_actor_member()
    director_member = mock_director_member()

    repository.list.return_value = [actor_member, director_member]

    return actor_member, director_member, repository


@pytest.fixture
def mock_im_cast_member_repository() -> InMemoryCastMemberRepository:
    return InMemoryCastMemberRepository()


@pytest.fixture
def mock_im_cast_member_repository_with_data(
    mock_actor_member,
    mock_director_member,
) -> tuple[CastMember, CastMember, InMemoryCastMemberRepository]:
    actor_member = mock_actor_member()
    director_member = mock_director_member()

    repository = InMemoryCastMemberRepository(
        cast_members=[actor_member, director_member]
    )

    return actor_member, director_member, repository


@pytest.fixture
def cast_member_repository() -> DjangoORMCastMemberRepository:
    return DjangoORMCastMemberRepository()
