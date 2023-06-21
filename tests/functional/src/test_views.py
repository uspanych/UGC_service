from http import HTTPStatus
from settings import test_settings
import pytest
import json
import asyncio


pytestmark = pytest.mark.asyncio

url = test_settings.SERVICE_URL + '/api/v1/views'
headers = {'Content-Type': 'application/json'}


async def test_create(client_session):
    query_data = {
        "key": "test_key",
        "value": "test_value"
    }
    async with client_session.post(url+"/views", data=json.dumps(query_data), headers=headers) as response:
        pass

    assert response.status == HTTPStatus.OK


async def test_read(client_session):
    query_data = {
        "key": "second_test_key",
        "value": "second_test_value"
    }
    async with client_session.post(url+"/views", data=json.dumps(query_data), headers=headers) as response:
        pass

    assert response.status == HTTPStatus.OK

    await asyncio.sleep(1)

    async with client_session.get(url+f"/views?key={query_data['key']}") as response:
        result = await response.json()

    assert response.status == HTTPStatus.OK
    assert result == {"value": query_data["value"]}
