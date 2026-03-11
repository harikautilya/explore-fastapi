import uvicorn

from fastapi.security import HTTPBearer
from fastapi import FastAPI
from app1.docs import custom_openapi

from app1.api import user, note


def init_main_app():
    """
    This is the main application to the fastapi
    """
    app = FastAPI()

    return app


def init_api_app():
    """
    This is the sub application mounted on the main app that only handle the apis
    """
    api_app = FastAPI()
    
    user.register_router(api_app)
    user.setup_excepttion_handling(api_app)
    user.setup_middleware(api_app)
    note.register_router(api_app)
    # open_api_schema = api_app.openapi()
    # Doc update to include the auth header
    api_app.openapi = lambda: custom_openapi(api_app)
    return api_app


app = init_main_app()
app.mount("/api", init_api_app())
def start():
    # Crucial: Use the full module path so uvicorn can reload from root
    uvicorn.run("app1.main:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    start()