import uvicorn
from taskify.core.asgi import create_app
from taskify.config import settings
from pathlib import Path

app = create_app()

if __name__ == "__main__":
    if settings.DEBUG:
        asgi_path = (
            settings.APP_DIR.joinpath("main.py")
            .relative_to(Path.cwd())
            .as_posix()
            .replace("/", ".")
            .strip(".py")
            .split(".")
        )
        asgi_path = ".".join(asgi_path[1:]) + ":app"
        uvicorn.run(asgi_path, reload=True)
    else:
        uvicorn.run(app, host="0.0.0.0")
