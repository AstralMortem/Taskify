import uuid

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from taskify.core.db import get_session
from taskify.models.board import Card
from .base import BaseRepository


class CardRepository(BaseRepository[Card, uuid.UUID]):
    model = Card

    async def reorder_cards(
        self, card_dict: dict[uuid.UUID, Card], card_order: list[uuid.UUID]
    ):
        for index, card_id in enumerate(card_order):
            card = card_dict[card_id]
            card.position = index
            self.session.add(card)
        await self.session.commit()


async def get_card_repository(session: AsyncSession = Depends(get_session)):
    return CardRepository(session)
