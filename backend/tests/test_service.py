import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.service import InvalidNumber, analyze

client = TestClient(app)


def test_formats_are_normalised():
    data = analyze("+14155552671", with_map=False)
    assert data["formats"]["e164"] == "+14155552671"
    assert data["country_code"] == 1
    assert data["region"] == "US"


def test_local_number_needs_region():
    assert analyze("0821234567", region="ZA", with_map=False)["formats"]["e164"] == "+27821234567"


def test_garbage_is_rejected():
    with pytest.raises(InvalidNumber):
        analyze("not a number", with_map=False)


def test_api_returns_422_for_garbage():
    assert client.get("/api/lookup", params={"number": "hello"}).status_code == 422


def test_health():
    assert client.get("/health").json() == {"status": "ok"}
