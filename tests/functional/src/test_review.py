from http import HTTPStatus
from settings import test_settings
import pytest
import json


pytestmark = pytest.mark.asyncio

url = test_settings.SERVICE_URL + '/api/v1/reviews'
headers = {'Content-Type': 'application/json'}


async def test_create(client_session):
    query_data = {
        "review_id": "1",
        "user_id": "1",
        "film_id": "1",
        "review": "string",
        "date": "2023-06-21T17:32:42.912Z",
        "like": "10"
    }
    async with client_session.post(url+"/reviews", data=json.dumps(query_data), headers=headers) as response:
        pass

    assert response.status == HTTPStatus.OK


async def test_read(client_session):
    query_data = {
        "review_id": "2",
        "user_id": "2",
        "film_id": "2",
        "review": "string",
        "date": "2023-06-21T17:32:42.912Z",
        "like": "10"
    }
    async with client_session.post(url+"/reviews", data=json.dumps(query_data), headers=headers) as response:
        pass

    assert response.status == HTTPStatus.OK

    async with client_session.get(url+f"/reviews?key=user_id&value={query_data['user_id']}") as response:
        result = await response.json()

    assert response.status == HTTPStatus.OK
    assert result == [query_data]


async def test_update(client_session):
    query_data = {
        "review_id": "3",
        "user_id": "3",
        "film_id": "3",
        "review": "string",
        "date": "2023-06-21T17:32:42.912Z",
        "like": "10"
    }
    async with client_session.post(url+"/reviews", data=json.dumps(query_data), headers=headers) as response:
        pass

    assert response.status == HTTPStatus.OK

    async with client_session.get(url+f"/reviews?key=user_id&value={query_data['user_id']}") as response:
        result = await response.json()

    assert response.status == HTTPStatus.OK
    assert result == [query_data]

    update_query_data = {
        "review_id": "3",
        "user_id": "3",
        "film_id": "3",
        "review": "string",
        "date": "2023-06-21T17:32:42.912Z",
        "like": "0"
    }
    async with client_session.put(url+"/reviews", data=json.dumps(update_query_data), headers=headers) as response:
        pass

    assert response.status == HTTPStatus.OK

    async with client_session.get(url+f"/reviews?key=user_id&value={update_query_data['user_id']}") as response:
        result = await response.json()

    assert response.status == HTTPStatus.OK
    assert result == [update_query_data]
