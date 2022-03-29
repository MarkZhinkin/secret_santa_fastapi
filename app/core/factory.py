from typing import Union

from fastapi import FastAPI
from fastapi.routing import APIRoute
from fastapi.staticfiles import StaticFiles
from fastapi_users import FastAPIUsers
from starlette.middleware.cors import CORSMiddleware

from app.api import router
from app.core.config import settings


class Application:

    def __init__(self):
        self.settings = settings
        self.app: Union[FastAPI, None] = None

    def create_app(self):
        self.app = FastAPI(
            title=settings.PROJECT_NAME,
            # openapi_url=f"{settings.API_PATH}/openapi.json",
            description=f"{settings.PROJECT_NAME} API",
            # docs_url="/docs",
            redoc_url=None,
        )

        # ToDo Add static if it need.
        # app.mount("/static", StaticFiles(directory=os.path.join('static', 'public')), name="static")

        self.setup_routers()
        self.init_db_hooks()
        self.setup_middleware()
        return self.app

    def setup_routers(self) -> None:
        self.app.include_router(router, prefix=settings.API_PATH)

        # The following operation needs to be at the end of this function
        self.use_route_names_as_operation_ids()

    def use_route_names_as_operation_ids(self) -> None:
        """
        Simplify operation IDs so that generated API clients have simpler function
        names.

        Should be called only after all routes have been added.
        """
        route_names = set()
        for route in self.app.routes:
            if isinstance(route, APIRoute):
                if route.name in route_names:
                    raise Exception("Route function names should be unique")
                unique_name = '_'.join([route.name, *list(route.methods)])
                route.operation_id = unique_name
                route_names.add(unique_name)

    def init_db_hooks(self) -> None:
        from app.core.db import engine, database

        app = self.app

        @app.on_event("startup")
        async def startup():
            await database.connect()

        @app.on_event("shutdown")
        async def shutdown():
            await database.disconnect()

    def setup_middleware(self):
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["GET", "POST"],
            expose_headers=["Content-Range", "Range"],
            allow_headers=["*"]
            # allow_headers=["Authorization", "Range", "Content-Range"],
        )
