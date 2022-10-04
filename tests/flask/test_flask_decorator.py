from fixtures import app, client
from pyqurl.web.flask import use_query_filters


def test_decorator(app, client):


    @app.route("/noop")
    @use_query_filters()
    def _(query):
        assert query.sort is not None

        assert query.sort[0].prop == "id"
        assert query.sort[0].descending == True

        assert query.sort[1].prop == "name"
        assert query.sort[1].descending == False

        return "OK!"

    response = client.get("/noop?sort=-id,+name")
    assert response.status_code == 200

