import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_text_process_ok():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        payload = {"input_id":"t1","text":"hello world"}
        headers = {"X-API-KEY":"demo-secret-key"}
        r = await ac.post("/v1/process/text", json=payload, headers=headers)
        assert r.status_code == 200
        j = r.json()
        assert j["status"] == "success"
