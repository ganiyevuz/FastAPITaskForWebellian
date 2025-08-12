import pytest


@pytest.mark.asyncio
async def test_get_catalogs(async_client):
    response = await async_client.get("/api/v1/catalogs")
    assert response.status_code == 200
    data = response.json()
    assert "count" in data
    assert "items" in data
    assert isinstance(data["count"], int)
    assert isinstance(data["items"], list)


@pytest.mark.asyncio
async def test_create_catalogs(async_client):
    response = await async_client.post(
        "/api/v1/catalogs", json={"name": "Test Catalog"}
    )
    assert response.status_code == 200
    product = response.json()
    assert "catalog_id" in product
    assert product["name"] == "Test Catalog"
