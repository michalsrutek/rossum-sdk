import pytest
from rossum_ng.models.user import User
from rossum_ng.elis_api_client import ElisAPIClient
from rossum_ng.api_client import APIClient


@pytest.fixture
def dummy_user():
    return {
        "id": 10775,
        "url": "https://elis.rossum.ai/api/v1/users/10775",
        "first_name": "John",
        "last_name": "Doe",
        "email": "john-doe@east-west-trading.com",
        "date_joined": "2018-09-19T13:44:56.000000Z",
        "username": "john-doe@east-west-trading.com",
        "groups": ["https://elis.rossum.ai/api/v1/groups/3"],
        "organization": "https://elis.rossum.ai/api/v1/organizations/406",
        "queues": ["https://elis.rossum.ai/api/v1/queues/8199"],
        "is_active": True,
        "last_login": "2019-02-07T16:20:18.652253Z",
        "ui_settings": {},
        "metadata": {},
        "oidc_id": None,
    }


@pytest.mark.asyncio
class TestUsers:
    async def test_get_users(self, http_client: APIClient, dummy_user, mock_generator):
        http_client.fetch_all.return_value = mock_generator(dummy_user)

        client = ElisAPIClient(http_client=http_client)
        users = client.get_users()

        async for u in users:
            assert u == User(**dummy_user)

        http_client.fetch_all.assert_called()
        http_client.fetch_all.assert_called_with("users")

    async def test_get_user(self, http_client: APIClient, dummy_user):
        http_client.fetch_one.return_value = dummy_user

        client = ElisAPIClient(http_client=http_client)
        uid = dummy_user["id"]
        user = await client.get_user(uid)

        assert user == User(**dummy_user)

        http_client.fetch_one.assert_called()
        http_client.fetch_one.assert_called_with("users", uid)