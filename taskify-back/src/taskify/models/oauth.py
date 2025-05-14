import uuid
from .base import BaseModel
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, String


class OAuthAccount(BaseModel):
    __tablename__ = "oauth_accounts"
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    oauth_name: Mapped[str] = mapped_column(String(255), index=True)
    access_token: Mapped[str]
    expires_at: Mapped[int | None]
    refresh_token: Mapped[str | None]
    account_id: Mapped[str] = mapped_column(String(200), index=True)
    account_email: Mapped[str] = mapped_column(String(255), index=True)
