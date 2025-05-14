from taskify.models.oauth import OAuthAccount
from .base import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .board import Card, Board


class PermissionRoleRel(BaseModel):
    __tablename__ = "permission_role_rel"
    __exclude_default_id__ = True
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True)
    permission_id: Mapped[int] = mapped_column(
        ForeignKey("permissions.id", ondelete="CASCADE"), primary_key=True
    )


class Role(BaseModel):
    __tablename__ = "roles"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    permissions: Mapped[list["Permission"]] = relationship(
        back_populates="roles", secondary=PermissionRoleRel.__table__, lazy="selectin", passive_deletes=True
    )


class Permission(BaseModel):
    __tablename__ = "permissions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    resource: Mapped[str] = mapped_column(String(255))
    action: Mapped[str] = mapped_column(String(255))

    roles: Mapped[list[Role]] = relationship(
        back_populates="permissions", secondary=PermissionRoleRel.__table__, passive_deletes=True
    )


class User(BaseModel):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    username: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    full_name: Mapped[str | None]
    avatar: Mapped[str | None]
    hashed_password: Mapped[str]
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))
    is_active: Mapped[bool] = mapped_column(default=True)

    role: Mapped[Role] = relationship(lazy="joined")
    boards: Mapped[list["Board"]] = relationship(back_populates="owner", lazy="selectin")
    cards: Mapped[list["Card"]] = relationship(back_populates="assigned_to")
    oauth_accounts: Mapped[list[OAuthAccount]] = relationship(lazy="joined", cascade="all, delete-orphan")
