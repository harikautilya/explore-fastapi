from fastapi.routing import APIRouter
from fastapi import Body, Query, Header, Cookie, Depends, status, Response, Request
from typing import Annotated
from pydantic import BaseModel, Field
from .deps import get_token_service, get_user_service
from .service import TokenService, UserService
from .exceptions import InvalidUserDetails


router = APIRouter(
    prefix="/user",
    dependencies=[],
    tags=["users"],
)

class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    token: str


class CreateUserRequest(BaseModel):
    username: str
    password: str
    name: str


class CreateUserResponse(BaseModel):
    message: str


class GetUserResponse(BaseModel):
    name: str


@router.post("/login", response_model=LoginResponse)
async def login_user(
    request_body: Annotated[LoginRequest, Body()],
    service: Annotated[TokenService, Depends(get_token_service)],
) -> LoginResponse:
    """
    Endpoint to login user using username and password
    """

    token = await service.generate_token(
        username=request_body.username,
        password=request_body.password,
    )
    return LoginResponse(token=token)


@router.post(
    "/",
    response_model=CreateUserResponse,
    responses={
        status.HTTP_200_OK: {
            "model": CreateUserResponse,
            "description": "User created",
        },
        status.HTTP_400_BAD_REQUEST: {
            "model": CreateUserResponse,
            "description": "Invalid informaiton",
        },
    },
)
async def create_user(
    request_body: Annotated[CreateUserRequest, Body()],
    service: Annotated[UserService, Depends(get_user_service)],
    response: Response,
) -> CreateUserResponse:
    """
    Endpoint to create user of the application
    """
    try:
        await service.create_user(
            username=request_body.username,
            password=request_body.password,
            name=request_body.name,
        )
        response.status_code = status.HTTP_200_OK
        return CreateUserResponse(message="User Created")
    except InvalidUserDetails as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return CreateUserResponse(message="Invalid information")


@router.get("/")
async def get_user(
    request : Request,
    service: Annotated[UserService, Depends(get_user_service)],
) -> GetUserResponse:
    """
    Endpoint to collect the user details based on the user token
    """
    user = await service.get_user_by_id(id=request.state.token.user.id)
    return GetUserResponse(
        name=user.name
    )
