"""Unit tests for top-level Flask app behavior."""


def test_index(client):
    """Verify valid app setup by getting the landing page."""
    rv = client.get("/")
    assert b"This is a landing page" == rv.data
