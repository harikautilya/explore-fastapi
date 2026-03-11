from fastapi.testclient import TestClient
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict
import pytest


@pytest.mark.asyncio
async def test_login_user_route(test_app: FastAPI, test_request: Dict[str, Dict]):
    with TestClient(app=test_app) as client:
        payload = {"username": "testuser", "password": "password"}
        resp = client.post("/api/user/login", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert "token" in data and isinstance(data["token"], str)


@pytest.mark.asyncio
async def test_create_user_route_success(test_app: FastAPI):
    with TestClient(app=test_app) as client:
        payload = {"username": "newuser", "password": "pw", "name": "New"}
        resp = client.post("/api/user/", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert data.get("message") == "User Created"


@pytest.mark.asyncio
async def test_get_user_route(test_app: FastAPI, test_request: Dict[str, Dict]):
    with TestClient(app=test_app) as client:
        resp = client.get("/api/user/", headers=test_request["headers"])
        assert resp.status_code == 200
        data = resp.json()
        assert "name" in data
