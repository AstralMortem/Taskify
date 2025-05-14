import uvicorn
from taskify.core.asgi import create_app
from taskify.config import settings
from pathlib import Path

app = create_app()


def migrate():
    from alembic.command import upgrade
    from alembic.config import Config

    cfg = Config(Path(__file__).parent.parent.joinpath("alembic.ini").absolute())
    cfg.set_main_option("script_location", "./src/migrations/")
    upgrade(cfg, "heads")


def main():
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
        migrate()
        uvicorn.run(app, host="0.0.0.0")


if __name__ == "__main__":
    main()
