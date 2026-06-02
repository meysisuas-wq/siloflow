import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
class TestHealth:
    async def test_health(self, client: AsyncClient):
        r = await client.get("/health")
        assert r.status_code == 200
        assert r.json()["service"] == "siloflow"

@pytest.mark.asyncio
class TestFields:
    async def test_create_validation(self, client: AsyncClient):
        r = await client.post("/api/v1/fields", json={})
        assert r.status_code == 422

    async def test_list(self, client: AsyncClient):
        r = await client.get("/api/v1/fields")
        assert r.status_code == 501
