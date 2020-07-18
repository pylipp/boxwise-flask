"""Functionality for common test setups.
See https://docs.pytest.org/en/stable/fixture.html#conftest-py-sharing-fixture-functions

In general, pass fixtures as arguments to a pytest test function in order to base the
test function on those fixtures. No additional import in the test module is required if
the fixture is defined in the 'conftest' module.

More details about the mechanism behind fixtures, and predefined fixtures at
https://docs.pytest.org/en/stable/fixture.html#pytest-fixtures-explicit-modular-scalable
"""
import functools
import os
import tempfile

import pytest
from playhouse.flask_utils import FlaskDB

from boxwise_flask import auth_helper


@pytest.fixture
def client(monkeypatch):
    """Fixture providing a baseline for unit tests that rely on database operations via
    the Flask app. The fixture simulates a client sending requests to the app. Adapted
    from https://flask.palletsprojects.com/en/1.1.x/testing/#the-testing-skeleton.
    """

    def null_decorator(f):
        """Decorator that has no effect."""

        @functools.wraps(f)
        def decorated(*args, **kwargs):
            return f(*args, **kwargs)

        return decorated

    # Patch the 'requires_auth' decorator using a built-in pytest fixture
    monkeypatch.setattr(auth_helper, "requires_auth", null_decorator)

    # Import the app *after* the patching such that it becomes effective
    from boxwise_flask.routes import app

    # Create a temporary Sqlite database and configure the Flask app to use it
    db_fd, db_filepath = tempfile.mkstemp(suffix=".sqlite3")
    app.config["DATABASE"] = {
        "name": db_filepath,
        "engine": "peewee.SqliteDatabase",
    }
    # Use the same mechanism as in main.py instead of 'db = FlaskDB(app)'
    db = FlaskDB()
    db.init_app(app)

    # Create and provide the test client. The yield-statement blocks until the test
    # function has finished
    with app.test_client() as client:
        yield client

    # Test teardown
    db.close_db(None)
    app.before_request_funcs = {}
    app.teardown_request_funcs = {}
    os.close(db_fd)
    os.remove(db_filepath)
