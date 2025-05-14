from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool = True
    TITLE: str = "Taskify Backend"
    VERSION: str = "1.0.0"

    # # ============= Routers ==========================================

    GLOBAL_ROUTER_PREFIX: str = "/api"

    # ============= Database ==========================================

    DATABASE_URL: str = ""

    # ============= JWT ==========================================
    JWT_ALGORITHM: str = "HS256"
    JWT_SECRET_KEY: str = ""
    JWT_AUTH_TOKEN_MAX_AGE: int = 60 * 60 * 24
    JWT_AUTH_TOKEN_AUDIENCE: list[str] = ["taskify:auth"]
    JWT_STATE_TOKEN_MAX_AGE: int = 60 * 10
    JWT_STATE_TOKEN_AUDIENCE: list[str] = ["taskify:oauth"]
    JWT_RESET_TOKEN_MAX_AGE: int = 60 * 10
    JWT_RESET_TOKEN_AUDIENCE: list[str] = ["taskify:reset"]
    AUTH_COOKIE_NAME: str = "taskify_auth"

    # ============= OAuth ==========================================

    GITHUB_CLIENT_ID: str = ""
    GITHUB_SECRET_KEY: str = ""
    GITHUB_CALLBACK_URL: str | None = ""

    DEFAULT_ROLE_ID: int = 1

    # ============= FS ==========================================

    APP_DIR: Path = Path(__file__).parent.absolute()

    # ============ STORAGE =====================================

    BUCKET_NAME: str = "taskifybucket"
    AWS_ACCESS_KEY_ID: str = ''
    AWS_SECRET_ACCESS_KEY: str = ''
    AWS_REGION_NAME: str | None = None
    AWS_ENDPOINT_URL: str | None = ''
    


settings = Settings()
