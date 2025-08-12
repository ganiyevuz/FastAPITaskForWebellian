import pytest


@pytest.mark.asyncio
async def test_root(async_client):
    response = await async_client.get("/")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_products(async_client):
    response = await async_client.get("/api/v1/products")
    assert response.status_code == 200
    data = response.json()
    assert "count" in data
    assert "items" in data
    assert isinstance(data["count"], int)
    assert isinstance(data["items"], list)


@pytest.mark.asyncio
async def test_create_product(async_client):
    response = await async_client.post(
        "/api/v1/products", json={"name": "Test Product", "price": 9.9, "catalog_id": 1}
    )
    assert response.status_code == 200
    product = response.json()
    assert "product_id" in product
    assert product["name"] == "Test Product"
    assert product["price"] == 9.9
    assert product["catalog_id"] == 1


@pytest.mark.asyncio
async def test_delete_product(async_client):
    # First, create a product to delete
    create_response = await async_client.post(
        "/api/v1/products", json={"name": "Test Product", "price": 9.9, "catalog_id": 1}
    )
    assert create_response.status_code == 200
    product = create_response.json()

    # Now, delete the created product
    delete_response = await async_client.delete(
        f"/api/v1/products/{product['product_id']}"
    )
    assert delete_response.status_code == 200

    # Verify the product is deleted
    get_response = await async_client.get(f"/api/v1/products/{product['product_id']}")
    assert get_response.status_code == 404
