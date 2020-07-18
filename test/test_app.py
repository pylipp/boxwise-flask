"""Unit tests for top-level Flask app behavior."""


def test_index(client):
    """Verify valid app setup by getting the landing page."""
    rv = client.get("/")
    assert b"This is a landing page" == rv.data


def test_private_route(client):
    rv = client.get("/api/private")
    assert rv.status_code == 200
    assert (
        rv.json["message"]
        == "Hello from a private endpoint! You need to be authenticated to see this."
    )
