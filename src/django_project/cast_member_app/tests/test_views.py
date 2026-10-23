import uuid

from rest_framework import status
from rest_framework.test import APIClient

import pytest

from src.core.cast_member.domain.cast_member import CastMemberType
from src.django_project.cast_member_app.repository import DjangoORMCastMemberRepository
from src.django_project.cast_member_app.models import CastMember as CastMemberORM


@pytest.mark.django_db
class TestCreateAPI:
    def test_create_cast_member(
        self,
        cast_member_repository,
    ):
        url = "/api/cast_members/"
        data = {
            "name": "Actor Member",
            "type": "ACTOR",
        }

        response = APIClient().post(url, data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["id"]
        created_cast_member_id = response.data["id"]

        saved_cast_member = cast_member_repository.get_by_id(id=created_cast_member_id)
        assert saved_cast_member.name == "Actor Member"
        assert saved_cast_member.type == CastMemberType.ACTOR

    def test_when_request_data_is_invalid_then_return_400(self):
        url = "/api/cast_members/"
        data = {
            "name": "",
            "type": "ACTOR",
        }
        response = APIClient().post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        data["name"] = "Test Member"
        data["type"] = "Invalid type"
        response = APIClient().post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestListAPI:
    def test_when_does_not_exist_cast_member_return_empty_list(self):
        url = "/api/cast_members/"

        response = APIClient().get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["data"] == []

    @pytest.mark.parametrize(
        "order_by, current_page",
        [
            ("name", 1),
            ("name", 2),
            ("type", 1),
            ("type", 2),
        ]
    )
    def test_list_cast_members(
        self,
        mock_actor_member,
        mock_director_member,
        cast_member_repository,
        order_by: str,
        current_page: int,
    ):
        member_1 = mock_director_member(name="Member 1")
        member_2 = mock_actor_member(name="Member 2")
        member_3 = mock_director_member(name="Member 3")
        member_4 = mock_actor_member(name="Member 4")
        cast_member_repository.save(member_1)
        cast_member_repository.save(member_2)
        cast_member_repository.save(member_3)
        cast_member_repository.save(member_4)

        if order_by == "name":
            expected_data_per_page = {
                1: [member_1, member_2],
                2: [member_3, member_4],
            }
        else:
            expected_data_per_page = {
                1: [member_2, member_4],
                2: [member_1, member_3],
            }

        expected_data = {
            "data": [
                {
                    "id": str(cast_member.id),
                    "name": cast_member.name,
                    "type": cast_member.type,
                } for cast_member in expected_data_per_page[current_page]
            ],
            "meta": {
                "current_page": current_page,
                "per_page": 2,
                "total": 4,
            }
        }

        url = f"/api/cast_members/?order_by={order_by}&current_page={current_page}"
        response = APIClient().get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == expected_data


@pytest.mark.django_db
class TestUpdateAPI:
    def test_when_request_data_is_valid_then_update_cast_member(
        self,
        mock_actor_member,
        cast_member_repository: DjangoORMCastMemberRepository,
    ) -> None:
        actor_member = mock_actor_member()
        cast_member_repository.save(actor_member)

        url = f"/api/cast_members/{str(actor_member.id)}/"
        data = {
            "name": "Member Updated",
            "type": "DIRECTOR",
        }
        response = APIClient().put(url, data=data)
        assert response.status_code == status.HTTP_204_NO_CONTENT

        updated_cast_member = cast_member_repository.get_by_id(actor_member.id)
        assert updated_cast_member.name == "Member Updated"
        assert updated_cast_member.type == CastMemberType.DIRECTOR

    def test_when_request_data_is_invalid_then_return_400(
        self,
        mock_actor_member,
    ) -> None:
        actor_member = mock_actor_member()
        url = f"/api/cast_members/{str(actor_member.id)}/"
        data = {
            "name": "",
            "type": "DIRECTOR",
        }
        response = APIClient().put(url, data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {"name": ["This field may not be blank."]}

        data["name"] = "Test Member"
        data["type"] = "Invalid type"
        response = APIClient().put(url, data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_when_cast_member_does_not_exist_then_return_404(self) -> None:
        url = f"/api/cast_members/{str(uuid.uuid4())}/"
        data = {
            "name": "Member Does Not Exist",
            "type": CastMemberType.DIRECTOR
        }
        response = APIClient().put(url, data=data)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestDeleteAPI:
    def test_when_cast_member_doesnt_exist_then_raise_404(self):
        url = f"/api/cast_members/{uuid.uuid4()}/"
        response = APIClient().delete(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_when_id_is_invalid_then_return_400(self):
        url = f"/api/cast_members/1/"
        response = APIClient().delete(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_delete_cast_member_from_repository(
        self,
        mock_actor_member,
        cast_member_repository,
    ):
        actor_member = mock_actor_member()
        cast_member_repository.save(cast_member=actor_member)
        assert CastMemberORM.objects.count() == 1

        url = f"/api/cast_members/{actor_member.id}/"
        response = APIClient().delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert cast_member_repository.get_by_id(actor_member.id) is None
        assert CastMemberORM.objects.count() == 0
