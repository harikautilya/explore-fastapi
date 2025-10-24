from fastapi import FastAPI, HTTPException, status, Request
from fastapi.responses import JSONResponse


class InvalidUserDetails(Exception):

    def __init__(self, *args):
        super().__init__(*args)


class InvalidAuthToken(Exception):

    def __init__(self, message="Auth token is wrong"):
        super().__init__(message)

class InvalidCredentialsException(Exception):

    def __init__(self, message="Invalid credentails"):
        super().__init__(message)


class MissingHeaderException(Exception):

    def __init__(self, message="Missing header with value, Bearer <your_token>"):
        super().__init__(message)


def handle_invalid_creds_exception(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "message" : str(exc)
        }
    )

def handle_missing_header_exception(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "message" : str(exc)
        }
    )

def handle_auth_token_exception(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "message" : str(exc)
        }
    )