import pytest
from fastapi import status
from fastapi.testclient import TestClient

from main import app


pytest_plugins = ("pytest_asyncio",)


@pytest.mark.asyncio
async def test_health_check():
    """Tests health check endpoint"""
    client = TestClient(app)
    url = client.app.url_path_for("common_health_check")

    response = client.get(url, headers={"Authorization": "Bearer test"})
    assert response.status_code == status.HTTP_200_OK

    response = client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    response = client.get(url, headers={"Authorization": "Bearer wrong"})
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_info():
    """Tests info endpoint"""
    client = TestClient(app)
    url = client.app.url_path_for("info_get_app_version")

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
