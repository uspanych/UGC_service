from http import HTTPStatus
from settings import test_settings
import pytest
import json


pytestmark = pytest.mark.asyncio

url = test_settings.SERVICE_URL + '/api/v1/bookmarks'
headers = {'Content-Type': 'application/json'}


async def test_create(client_session):
    query_data = {
        "user_id": "1",
        "film_id": "1"
    }
    async with client_session.post(url+"/bookmarks", data=json.dumps(query_data), headers=headers) as response:
        pass

    assert response.status == HTTPStatus.OK


async def test_read(client_session):
    query_data = {
        "user_id": "2",
        "film_id": "2"
    }
    async with client_session.post(url+"/bookmarks", data=json.dumps(query_data), headers=headers) as response:
        pass

    assert response.status == HTTPStatus.OK

    async with client_session.get(url+f"/bookmarks?user_id={query_data['user_id']}") as response:
        result = await response.json()

    assert response.status == HTTPStatus.OK
    assert result == [query_data]


async def test_delete(client_session):
    query_data = {
        "user_id": "3",
        "film_id": "3"
    }
    async with client_session.post(url+"/bookmarks", data=json.dumps(query_data), headers=headers) as response:
        pass

    assert response.status == HTTPStatus.OK

    async with client_session.get(url+f"/bookmarks?user_id={query_data['user_id']}") as response:
        result = await response.json()

    assert response.status == HTTPStatus.OK
    assert result == [query_data]


    async with client_session.delete(url+f"/bookmarks?user_id={query_data['user_id']}") as response:
        pass

    assert response.status == HTTPStatus.OK

    async with client_session.get(url+f"/bookmarks?user_id={query_data['user_id']}") as response:
        result = await response.json()

    assert response.status == HTTPStatus.OK
    assert result == []
