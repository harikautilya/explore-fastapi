from fastapi import FastAPI
from fastapi.testclient import TestClient
from api import note
from types import SimpleNamespace

from api.note.deps import get_note_service
from api.note.adapter import NoteDbAdapter
from api.note.service import NoteService


def _make_test_app(db_session):
    """Create a new FastAPI app for testing with dependency overrides and
    a small middleware to set request.state.token (so routes can read
    request.state.token.user.id).
    """
    app = FastAPI()
    note.register_router(app=app)

    # override the service dependency to use the test DB-backed adapter
    def _override_get_note_service():
        return NoteService.get_instance(note_adapter=NoteDbAdapter(db=db_session))

    app.dependency_overrides[get_note_service] = _override_get_note_service

    return app


def test_create_get_update_delete_note_routes(inmemory_db_session):
    app = _make_test_app(inmemory_db_session)

    with TestClient(app=app) as client:
        # create
        resp = client.post("/notes/", json={"title": "t", "content": "C"})
        assert resp.status_code == 201