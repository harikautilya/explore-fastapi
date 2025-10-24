from fastapi import FastAPI


def register_router(app: FastAPI):
    """
    Register routers
    """

    from .routes import router

    app.include_router(router)


def setup_middleware(app: FastAPI):
    """
    Register middleware
    """
    from api.db.base import get_db_session
    from .middleware import Authentication

    app.add_middleware(Authentication, db_session=get_db_session)


def setup_excepttion_handling(app: FastAPI):
    """
    Register exception handling
    """
    from .exceptions import (
        InvalidCredentialsException,
        MissingHeaderException,
        handle_invalid_creds_exception,
        handle_missing_header_exception,
    )

    app.add_exception_handler(MissingHeaderException, handle_missing_header_exception)
    app.add_exception_handler(
        InvalidCredentialsException, handle_invalid_creds_exception
    )


