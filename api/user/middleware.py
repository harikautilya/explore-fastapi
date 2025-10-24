from typing import Annotated
from fastapi import Header
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from .adapter import TokenAdapter
from .adapter.token import TokenDbAdpater
from .models import TokenModel
from .exceptions import MissingHeaderException, InvalidAuthToken

from contextlib import asynccontextmanager
from typing import AsyncGenerator


class Authentication(BaseHTTPMiddleware):

    def __init__(self, app, db_session, dispatch=None):
        super().__init__(app, dispatch)
        self.db_session = db_session

    @asynccontextmanager
    async def _getTokenAdapter(self) -> AsyncGenerator[TokenAdapter, None]:
        async for db_session in self.db_session():
            token_adapter: TokenAdapter = TokenDbAdpater(db=db_session)
            yield token_adapter

    # since dependecies are something that are resolved
    async def dispatch(self, request, call_next) -> Response:
        # Read the path and ignore the login endpoint

        path = request.url.path
        method = request.method
        ignore_paths = {
            "/api/docs": {"*"},
            "/api/user/login": {"*"},
            "/api/user/": {"POST"},
            "/api/openapi.json": {"*"},
        }
        if path in ignore_paths.keys():
            if bool(ignore_paths[path] & {"*", method}):
                response = await call_next(request)
                return response

        # Read the path for the rest of the endpoints
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            raise MissingHeaderException()
        token = auth_header.split(" ")[1]

        # Read if the token  is correct or not
        async with self._getTokenAdapter() as token_adapter:
            token = await token_adapter.get_user(
                token=TokenModel(token=token, user=None)
            )
            if token is None:
                raise InvalidAuthToken()
            request.state.token = token

        response = await call_next(request)
        return response
