import pytest
from fastapi.testclient import TestClient
from src.api.main import app
from src.api.routes.forecast import get_redis

# Dependency override to mock Redis
def mock_get_redis():
    class MockRedis:
        def __init__(self):
            self.cache = {}
        def get(self, key):
            return self.cache.get(key)
        def setex(self, key, time, value):
            self.cache[key] = value
    return MockRedis()

app.dependency_overrides[get_redis] = mock_get_redis

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_get_latest_forecast():
    response = client.get("/api/v1/forecast/latest?bidding_zone=DE_LU&horizon_hours=24")
    assert response.status_code == 200
    data = response.json()
    assert "points" in data
    assert len(data["points"]) == 24
    assert data["metadata"]["bidding_zone"] == "DE_LU"

def test_simulate_forecast():
    payload = {
        "bidding_zone": "DE_LU",
        "horizon_hours": 12,
        "wind_speed_delta": 5.0,
        "solar_radiation_delta": 100.0
    }
    response = client.post("/api/v1/forecast/simulate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert len(data["points"]) == 12
    assert data["metadata"]["weather_deltas"]["wind"] == 5.0
    assert data["metadata"]["weather_deltas"]["solar"] == 100.0
