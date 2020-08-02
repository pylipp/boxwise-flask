from test.auth_override import patch_auth
from test.database_for_testing import with_test_db

import pytest

from boxwise_flask.app import db
from boxwise_flask.models import Camps, Cms_Usergroups_Camps, Cms_Users, Person
from boxwise_flask.routes import app

patch_auth()


MODELS = (Person, Camps, Cms_Usergroups_Camps, Cms_Users)


@pytest.fixture
def client():
    """test client to setup app"""
    app.config["DATABASE"] = "sqlite:///:memory:"

    db.init_app(app)

    with app.test_client() as client:
        yield client


def test_index(client):
    """Verify valid app setup by getting the landing page."""
    rv = client.get("/")
    assert b"This is a landing page" == rv.data


def test_private_endpoint(client):
    """example test for private endpoint"""
    response_data = client.get("/api/private").json
    assert (
        "Hello from a private endpoint! You need to be authenticated to see this."
        == response_data["message"]
    )


@with_test_db(db.database, MODELS)
def test_graphql_endpoint(client):
    """example test for graphql endpoint"""

    Camps.create(id=1, organisation_id=1, name="some text1", currencyname="hello")
    Camps.create(id=2, organisation_id=1, name="some text1", currencyname="hello")
    Camps.create(id=3, organisation_id=1, name="some text1", currencyname="hello")
    Camps.create(id=4, organisation_id=1, name="some text1", currencyname="hello")
    Camps.create(id=5, organisation_id=1, name="some text1", currencyname="hello")

    graph_ql_query_string = """query { \
        allBases { \
            id \
            organisation_id \
            name \
        } \
    }"""

    data = {"query": graph_ql_query_string}
    response_data = client.post("/graphql", json=data).json
    assert response_data["data"]["allBases"][0]["id"] == 1
