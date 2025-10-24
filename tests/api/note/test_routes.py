from fastapi.testclient import TestClient
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict
import pytest
from api.note.deps import get_note_service
from api.note.adapter import NoteDbAdapter
from api.note.service import NoteService
from utils.lists import compare

def _overide_deps(app: FastAPI, inmemory_db_session: AsyncSession) -> FastAPI:

    # override the service dependency to use the test DB-backed adapter
    def _override_get_note_service():
        return NoteService.get_instance(
            note_adapter=NoteDbAdapter(db=inmemory_db_session)
        )

    app.dependency_overrides[get_note_service] = _override_get_note_service

    return app


@pytest.mark.asyncio
async def test_create_note_routes(
    test_app: FastAPI,
    inmemory_db_session: AsyncSession,
    test_request: Dict[str, Dict],
):
    test_app = _overide_deps(test_app, inmemory_db_session)

    with TestClient(app=test_app) as client:
        # create
        payload = {"title": "T", "content": "C"}

        resp = client.post("/api/notes/", json=payload, headers=test_request["headers"])
        assert resp.status_code == 201

        # ensure response body exists and has expected fields
        data = resp.json()
        assert data is not None
        assert isinstance(data, dict)
        assert data.get("title") == payload["title"]
        assert data.get("content") == payload["content"]
        assert "id" in data and data["id"] is not None


@pytest.mark.asyncio
async def test_update_note_route(
    test_app: FastAPI,
    inmemory_db_session: AsyncSession,
    test_request: Dict[str, Dict],
):
    test_app = _overide_deps(test_app, inmemory_db_session)

    with TestClient(app=test_app) as client:
        # create
        payload = {"title": "T", "content": "C"}
        # Create a sample note
        resp = client.post("/api/notes/", json=payload, headers=test_request["headers"])
        assert resp.status_code == 201

        # Get id from response
        data = resp.json()
        note_id = data.get("id")

        # Full note change
        payload = {"title": "T2", "content": "C2"}
        resp = client.put(
            f"/api/notes/{note_id}", json=payload, headers=test_request["headers"]
        )
        assert resp.status_code == 200

        # Title note change, parital update not allowed
        payload = {"title": "T3"}
        resp = client.put(
            f"/api/notes/{note_id}", json=payload, headers=test_request["headers"]
        )
        assert resp.status_code == 422

        # Title note change, parital update not allowed
        payload = {"content": "C3"}
        resp = client.put(
            f"/api/notes/{note_id}", json=payload, headers=test_request["headers"]
        )
        assert resp.status_code == 422


@pytest.mark.asyncio
async def test_delete_note_route(
    test_app: FastAPI,
    inmemory_db_session: AsyncSession,
    test_request: Dict[str, Dict],
):
    test_app = _overide_deps(test_app, inmemory_db_session)

    with TestClient(app=test_app) as client:
        # create
        payload = {"title": "T", "content": "C"}
        # Create a sample note
        resp = client.post("/api/notes/", json=payload, headers=test_request["headers"])
        assert resp.status_code == 201

        # Get id from response
        data = resp.json()
        note_id = data.get("id")

        # Note delete
        resp = client.delete(f"/api/notes/{note_id}", headers=test_request["headers"])
        assert resp.status_code == 204


@pytest.mark.asyncio
async def test_get_note_routes(
    test_app: FastAPI,
    inmemory_db_session: AsyncSession,
    test_request: Dict[str, Dict],
    test_request_two: Dict[str, Dict],
):
    test_app = _overide_deps(test_app, inmemory_db_session)

    with TestClient(app=test_app) as client:

        user_one_payload = []
        user_two_payload = []
        
        # create for user 1
        payload = {"title": "T", "content": "C"}
        resp = client.post("/api/notes/", json=payload, headers=test_request["headers"])
        assert resp.status_code == 201
        data = resp.json()
        note_id = data.get("id")
        user_one_payload.append({
            "id" : note_id,
            **payload
        })


        payload = {"title": "T2", "content": "C2"}
        resp = client.post("/api/notes/", json=payload, headers=test_request["headers"])
        assert resp.status_code == 201
        data = resp.json()
        note_id = data.get("id")
        user_one_payload.append({
            "id" : note_id,
            **payload
        })


        # create for user 2
        payload = {"title": "T2_other", "content": "C2_other"}
        resp = client.post("/api/notes/", json=payload, headers=test_request_two["headers"])
        assert resp.status_code == 201
        data = resp.json()
        note_id = data.get("id")
        user_two_payload.append({
            "id" : note_id,
            **payload
        })

        # Read for user 1 and check if user 2 data is present
        resp = client.get("/api/notes",  headers=test_request["headers"])
        assert resp.status_code == 200
        data = resp.json()
        
        assert len(user_one_payload) == len(data)
        assert compare(user_one_payload, data) == True


        # Read for user 2 and check if user 1 data is present
        resp = client.get("/api/notes",  headers=test_request_two["headers"])
        assert resp.status_code == 200
        data = resp.json()

        assert len(user_two_payload) == len(data)
        assert compare(user_two_payload, data) == True


        