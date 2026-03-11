from fastapi import FastAPI


def register_router(app: FastAPI):
    """
    Registers the note router with the FastAPI application.
    """
    from .routes import router

    app.include_router(router)