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
    from app1.api.db.base import get_db_session
    from .middleware import Authentication
    from app1.api.db.session import AsyncSessionManagedDB
    from app1.api.db.user import Token
    from app1.api.db.base import SessionLocal

    session = AsyncSessionManagedDB[Token, int](
        session_manager=SessionLocal,
        model_class=Token,
    )

    app.add_middleware(Authentication, db_session=session)


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
