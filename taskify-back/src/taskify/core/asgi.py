from fastapi import FastAPI, Request
from taskify.config import settings
from fastapi.middleware.cors import CORSMiddleware


def init_router(app: FastAPI):
    from taskify.api import global_router

    app.include_router(global_router)


def set_exception(app: FastAPI):
    from taskify.core.exception import TaskifyException

    @app.exception_handler(TaskifyException)
    async def _(request: Request, exc: TaskifyException):
        return exc.to_response()

def set_origins(app: FastAPI):
    app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.ORIGIN, 'http://localhost:3000'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )


async def default_lifespan(app: FastAPI):
    yield


def create_app(lifespan=default_lifespan):
    app = FastAPI(
        debug=settings.DEBUG,
        title=settings.TITLE,
        version=settings.VERSION,
        lifespan=lifespan,
    )

    init_router(app)
    set_exception(app)
    set_origins(app)

    return app
