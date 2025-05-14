import uuid

from fastapi_pagination import Page, Params

from taskify.core.exception import TaskifyException, status
from taskify.schemas.cards import CardCreate, CardUpdate
from taskify.schemas.filters import CardFilter
from .base import BaseService
from taskify.repositories.card import CardRepository
from taskify.models.board import Card, List


class CardService(BaseService[CardRepository, Card, uuid.UUID, CardCreate, CardUpdate]):
    async def get_list_cards(self, list_id: uuid.UUID, params: Params) -> Page[Card]:
        filter = CardFilter(list_id=list_id)
        return await self.repo.get_many(params, filter)

    async def create(self, payload: CardCreate, **kwargs) -> Card:
        list: List = kwargs.get("list", None)

        dump = payload.model_dump()

        if "position" not in dump or dump["position"] is None:
            dump["position"] = len(list.cards)
        dump["list_id"] = list.id

        return await self.repo.create(dump)

    async def move_card(self, card_id: uuid.UUID, list: List, position: int):
        instance = await self.get(card_id)
        instance = await self.repo.update(
            instance, {"list_id": list.id, "position": position}
        )
        return instance

    async def reorder_cards(
        self, list: List, card_order: list[uuid.UUID], params: Params
    ):
        list_id = list.id
        id_map = {item.id: item for item in list.cards}
        card_dict = {id_map[i].id: id_map[i] for i in card_order if i in id_map}

        for card_id in card_order:
            if card_id not in card_dict or card_dict[card_id].list_id != list.id:
                raise TaskifyException(
                    status.HTTP_400_BAD_REQUEST,
                    "Incorrect list",
                    f"Card {card_id} does not belong to list {list.id}",
                )

        await self.repo.reorder_cards(card_dict, card_order)
        return await self.get_list_cards(list_id, params)
