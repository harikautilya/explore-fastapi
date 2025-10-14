from fastapi import FastAPI


def register_router(app: FastAPI):
    """
    Everything to registered during runtime to avoid circular dependency during startup
    and limit the startup only and if the router is registered
    """
    from .middleware import Authentication
    from .routes import router
    from .exceptions import (
        InvalidCredentialsException,
        MissingHeaderException,
        handle_invalid_creds_exception,
        handle_missing_header_exception,
    )
    app.add_middleware(Authentication)
    app.include_router(router)

    app.add_exception_handler(MissingHeaderException, handle_missing_header_exception)
    app.add_exception_handler(
        InvalidCredentialsException, handle_invalid_creds_exception
    )
