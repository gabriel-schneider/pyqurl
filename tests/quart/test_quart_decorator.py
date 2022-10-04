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

