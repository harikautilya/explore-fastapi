from fastapi.routing import APIRouter
from fastapi import Path, Body, Depends, Request, status, Response
from typing import Annotated, List
from pydantic import BaseModel

from .deps import get_note_service
from .service import NoteService


router = APIRouter(
    prefix="/notes",
    tags=["notes"],
    dependencies=[],
)


class NoteGetResponse(BaseModel):
    id: int
    title: str
    content: str


class NoteUpdateRequest(BaseModel):
    title: str
    content: str


class NoteUpdateResponse(BaseModel):
    message: str


class NoteCreateRequest(BaseModel):
    title: str
    content: str


class NoteCreateResponse(BaseModel):
    id: int
    title: str
    content: str


@router.get("/", response_model=List[NoteGetResponse])
async def get_notes(
    request: Request,
    note_service: Annotated[NoteService, Depends(get_note_service)],
) -> List[NoteGetResponse]:
    """
    API end point to get all the notes for the user
    """
    user_id = request.state.token.user.id
    notes = await note_service.get_notes(user_id=user_id)
    return notes


@router.post(
    "/", response_model=NoteCreateResponse, status_code=status.HTTP_201_CREATED
)
async def create_note(
    request: Request,
    request_body: Annotated[
        NoteCreateRequest, Body(description="Body for the note creation")
    ],
    note_service: Annotated[NoteService, Depends(get_note_service)],
) -> NoteCreateResponse:
    """
    API to created note
    """
    user_id = request.state.token.user.id
    created_note = await note_service.create_note(
        title=request_body.title, content=request_body.content, user_id=user_id
    )
    return created_note


@router.put("/{note_id}", response_model=NoteUpdateResponse)
async def update_note(
    request: Request,
    note_id: Annotated[int, Path(title="Id of the note")],
    request_body: Annotated[
        NoteUpdateRequest, Body(description="Body for the note update")
    ],
    note_service: Annotated[NoteService, Depends(get_note_service)],
    response: Response,
) -> NoteUpdateResponse:
    """
    Update description and title in the notes
    """
    user_id = request.state.token.user.id
    updated_note = await note_service.update_note(
        note_id=note_id,
        title=request_body.title,
        content=request_body.content,
        user_id=user_id,
    )
    if updated_note is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return NoteUpdateResponse(message="Note not present")
    return NoteUpdateResponse(message="Noted Updated")


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(
    note_id: Annotated[int, Path(title="Id of the note")],
    note_service: Annotated[NoteService, Depends(get_note_service)],
    request: Request,
    response: Response,
):
    """
    Delete a particular note
    """
    user_id = request.state.token.user.id
    result = await note_service.delete_note(note_id=note_id, user_id=user_id)
    if not result:
        response.status_code = status.HTTP_404_NOT_FOUND
    else:
        response.status_code = status.HTTP_204_NO_CONTENT
    return
