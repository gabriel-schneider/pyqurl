import pytest
from .fixtures import app, client
from pyqurl.web.quart import use_query_filters


@pytest.mark.asyncio
async def test_quart_decorator(app, client):

    @app.get("/noop")
    @use_query_filters()
    async def _(query):
        assert query.sort is not None

        assert query.sort[0].prop == "id"
        assert query.sort[0].descending == True

        assert query.sort[1].prop == "name"
        assert query.sort[1].descending == False

        return "OK!"

    response = await client.get("/noop?sort=-id,+name")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_quart_decorator_pagination(app, client):

    @app.get("/noop")
    @use_query_filters()
    async def _(query):
        assert query.pagination is not None

        assert query.pagination.offset == 10
        assert query.pagination.limit == 20

        return "OK!"

    response = await client.get("/noop?offset=10&limit=20")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_quart_decorator_pagination_with_string_offset(app, client):

    @app.get("/noop")
    @use_query_filters()
    async def _(query):
        assert query.pagination is not None

        assert query.pagination.offset == "abc"
        assert query.pagination.limit == 20

        return "OK!"

    response = await client.get("/noop?offset=abc&limit=20")
    assert response.status_code == 200
