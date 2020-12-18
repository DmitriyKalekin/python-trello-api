import asyncio
import pytest
from aioresponses import aioresponses
from api_trello import TrelloJson, Client


@pytest.fixture(scope="module")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop


@pytest.fixture
def mock_aioresponse():
    with aioresponses() as m:
        yield m

@pytest.fixture(scope="module")
def client_trello_json():
    client = TrelloJson(
        api_key="aaaaaaaaaa1234567890AAAAAAAAAA00",
        token="cccccccccc1234567890CCCCCCCCCC11cccccccccc1234567890CCCCCCCCCC11",
        board_id="bbbbbbbbbb1234567890BBBBBBBBBB00")
    yield client

@pytest.fixture(scope="module")
def client():
    client = Client(
        api_key="aaaaaaaaaa1234567890AAAAAAAAAA00",
        token="cccccccccc1234567890CCCCCCCCCC11cccccccccc1234567890CCCCCCCCCC11",
        board_id="bbbbbbbbbb1234567890BBBBBBBBBB00")
    yield client