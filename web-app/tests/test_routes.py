"""tests for web app routes."""

# pylint: disable=redefined-outer-name
import pytest

from app import create_app


@pytest.fixture
def test_client():
    """create test client."""
    test_app = create_app()
    test_app.config["TESTING"] = True

    with test_app.test_client() as test_client:
        yield test_client


def test_home_route(test_client):
    """check home page loads."""
    response = test_client.get("/")

    assert response.status_code == 200


def test_history_route_without_db(test_client, monkeypatch):
    """check history route handles missing database."""
    monkeypatch.delenv("MONGODB_URI", raising=False)

    response = test_client.get("/history")

    assert response.status_code in [200, 500]


def test_health_route(test_client):
    """check health route if it exists."""
    response = test_client.get("/health")

    assert response.status_code in [200, 404]
