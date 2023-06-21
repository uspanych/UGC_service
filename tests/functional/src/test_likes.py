from http import HTTPStatus
from settings import test_settings
import pytest
import json


pytestmark = pytest.mark.asyncio

url = test_settings.SERVICE_URL + '/api/v1/likes'
headers = {'Content-Type': 'application/json'}


async def test_create(client_session):
    query_data = {
        "user_id": "1",
        "film_id": "1",
        "point": 10
    }
    async with client_session.post(url+"/like", data=json.dumps(query_data), headers=headers) as response:
        pass

    assert response.status == HTTPStatus.OK


async def test_count(client_session):
    query_data = {
        "user_id": "2",
        "film_id": "2",
        "point": 10
    }
    async with client_session.post(url+f"/like", data=json.dumps(query_data), headers=headers) as response:
        pass

    assert response.status == HTTPStatus.OK

    async with client_session.get(url+f"/likes/film?film_id={query_data['film_id']}") as response:
        result = await response.json()

    assert response.status == HTTPStatus.OK
    assert result == {
            "film_id": query_data["film_id"],
            "positive_vote": 1,
            "negative_vote": 0
        }


async def test_avg(client_session):
    query_data = {
        "user_id": "3",
        "film_id": "3",
        "point": 5
    }
    async with client_session.post(url+f"/like", data=json.dumps(query_data), headers=headers) as response:
        pass

    assert response.status == HTTPStatus.OK

    async with client_session.get(url+f"/likes/avg?film_id={query_data['film_id']}") as response:
        result = await response.json()

    assert response.status == HTTPStatus.OK
    assert result == {
            "film_id": query_data["film_id"],
            "avg_vote": query_data["point"]
        }
    

async def test_update(client_session):
    query_data = {
        "user_id": "4",
        "film_id": "4",
        "point": 10
    }
    async with client_session.post(url+f"/like", data=json.dumps(query_data), headers=headers) as response:
        pass

    assert response.status == HTTPStatus.OK

    async with client_session.get(url+f"/likes/film?film_id={query_data['film_id']}") as response:
        result = await response.json()

    assert response.status == HTTPStatus.OK
    assert result == {
            "film_id": query_data["film_id"],
            "positive_vote": 1,
            "negative_vote": 0
        }

    update_query_data = {
        "user_id": "4",
        "film_id": "4",
        "point": 0
    }

    async with client_session.put(url+"/update", data=json.dumps(update_query_data), headers=headers) as response:
        pass

    assert response.status == HTTPStatus.OK

    async with client_session.get(url+f"/likes/film?film_id={query_data['film_id']}") as response:
        result = await response.json()

    assert response.status == HTTPStatus.OK
    assert result == {
            "film_id": update_query_data["film_id"],
            "positive_vote": 0,
            "negative_vote": 1
        }


async def test_delete(client_session):
    query_data = {
        "user_id": "5",
        "film_id": "5",
        "point": 10
    }

    async with client_session.post(url+"/like", data=json.dumps(query_data), headers=headers) as response:
        pass

    assert response.status == HTTPStatus.OK

    async with client_session.get(url+f"/likes/film?film_id={query_data['film_id']}") as response:
        result = await response.json()

    assert response.status == HTTPStatus.OK
    assert result == {
            "film_id": query_data["film_id"],
            "positive_vote": 1,
            "negative_vote": 0
        }
    
    async with client_session.delete(url+f"/like/delete?film_id={query_data['film_id']}") as response:
        pass

    assert response.status == HTTPStatus.OK
