import os
from unittest.mock import patch

from fastapi.testclient import TestClient

os.environ.setdefault("ETL_API_KEY", "test-etl-key")

from main import app

client = TestClient(app)


def test_quality_report_is_public():
    with patch("routers.etl.query_df") as mock_query:
        mock_query.return_value.to_dict.return_value = [
            {
                "total_rows": 100,
                "null_price": 0,
                "null_sqft": 0,
                "null_lat": 100,
                "null_state": 0,
                "min_price": 100000,
                "max_price": 2000000,
                "avg_price": 500000,
            }
        ]
        response = client.get("/etl/quality-report")

    assert response.status_code == 200
    assert response.json()["total_rows"] == 100


def test_clean_properties_rejects_missing_api_key():
    response = client.post("/etl/clean/properties")
    assert response.status_code == 401


def test_clean_properties_rejects_wrong_api_key():
    response = client.post(
        "/etl/clean/properties",
        headers={"X-API-Key": "wrong-key"},
    )
    assert response.status_code == 401


def test_clean_properties_accepts_valid_api_key():
    with patch("routers.etl.query_df") as mock_query:
        mock_query.return_value = None
        response = client.post(
            "/etl/clean/properties",
            headers={"X-API-Key": "test-etl-key"},
        )

    assert response.status_code == 200
    assert response.json()["message"] == "Data cleaned successfully"
    assert mock_query.call_count == 2
