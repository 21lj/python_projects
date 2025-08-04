import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app')))

from app.main import app, url_store


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        url_store.clear()
        yield client

def test_health_check(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.get_json()["message"] == "URL Shortener running"

def test_shorten_valid_url(client):
    response = client.post("/api/shorten", json={"url": "https://example.com"})
    assert response.status_code == 201
    assert "short_url" in response.get_json()

def test_shorten_invalid_url(client):
    response = client.post("/api/shorten", json={"url": "invalid-url"})
    assert response.status_code == 400
    assert "error" in response.get_json()

def test_redirect_and_click_count(client):
    # Create short URL
    shorten = client.post("/api/shorten", json={"url": "https://example.com"})
    short_url = shorten.get_json()["short_url"]
    code = short_url.split("/")[-1]

    # Check initial click count
    stats = client.get(f"/api/stats/{code}")
    assert stats.status_code == 200
    assert stats.get_json()["clicks"] == 0

    # Hit redirect endpoint
    redirect = client.get(f"/{code}")
    assert redirect.status_code == 302
    assert redirect.headers["Location"] == "https://example.com"

    # Click count should increase
    stats_after = client.get(f"/api/stats/{code}")
    assert stats_after.get_json()["clicks"] == 1

def test_stats_nonexistent_code(client):
    response = client.get("/api/stats/abcdef")
    assert response.status_code == 404

def test_redirect_nonexistent_code(client):
    response = client.get("/abcdef")
    assert response.status_code == 404
