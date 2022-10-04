# From https://pgjones.gitlab.io/quart/how_to_guides/testing.html

import pytest
from quart import Quart

@pytest.fixture()
def app():

    app = Quart(__name__)
    app.config.update({
        "TESTING": True,
    })

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()