from tkinter import NO
from .base import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Text, Integer, DateTime
from datetime import datetime
from .auth import User
import uuid
from typing import List as PYList

class BoardMemberRel(BaseModel):
    __tablename__ = "board_members"
    __exclude_default_id__ = True
    board_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("boards.id"), primary_key=True
    )
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), primary_key=True)


class Board(BaseModel):
    __tablename__ = "boards"

    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None]
    background: Mapped[str | None]
    is_stared: Mapped[bool] = mapped_column(default=False)
    owner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))

    public_hash: Mapped[str | None] = mapped_column(unique=True, index=True)
    is_public: Mapped[bool | None] = mapped_column(default=False)


    owner: Mapped[User] = relationship(lazy="joined")  # TODO: add back_populates
    lists: Mapped[list["List"]] = relationship(
        back_populates="board", cascade="all, delete-orphan",
        lazy="selectin"
    )
    members: Mapped[list[User]] = relationship(secondary=BoardMemberRel.__table__, lazy="joined")


class List(BaseModel):
    __tablename__ = "lists"

    title: Mapped[str] = mapped_column(String(255))
    position: Mapped[int] = mapped_column(default=0)
    board_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("boards.id"))

    board: Mapped[Board] = relationship(back_populates="lists")
    cards: Mapped[list["Card"]] = relationship(back_populates="list", lazy="selectin", cascade="all, delete-orphan")


class CardLabelRel(BaseModel):
    __tablename__ = "card_label_rel"
    __exclude_default_id__ = True
    card_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("cards.id"), primary_key=True)
    label_id: Mapped[int] = mapped_column(ForeignKey("labels.id"), primary_key=True)


class Card(BaseModel):
    __tablename__ = "cards"

    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    position: Mapped[int] = mapped_column(Integer, default=0)
    list_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("lists.id"))
    assigned_to_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )
    due_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=False))
    is_completed: Mapped[bool] = mapped_column(default=False)

    list: Mapped[List] = relationship(back_populates="cards")
    assigned_to: Mapped[User] = relationship(back_populates="cards")
    # labels: Mapped[PYList["Card"]] = relationship(
    #     back_populates="cards", secondary=CardLabelRel.__table__
    # )  # type: ignore


class Label(BaseModel):
    __tablename__ = "labels"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str]
    color: Mapped[str] = mapped_column(default="#61BD4F")

    # cards: Mapped[list[Card]] = relationship(
    #     back_populates="labels", secondary=CardLabelRel.__table__
    # )
