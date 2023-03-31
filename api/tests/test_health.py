import pytest
from app import APP


def test_index_route():
    response = APP.test_client().get("/api/v1.0/siteprofiling/health")

    assert response.status_code == 200
    assert response.json == {"message": "healty"}
