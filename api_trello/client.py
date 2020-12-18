import asyncio
from typing import List
from aiohttp import ClientSession, ClientResponse
from .trello_json_client import TrelloJson
from typing import List
from .pydantic_model import TrelloWebHook, TrelloCard, TrelloList, Member
from datetime import datetime
from loguru import logger as log
import re

class TrelloException(Exception):
    pass


class Client:
    def __init__(self, api_key: str = None, token: str = None, board_id: str = None):
        assert re.match(r'^[0-9a-fA-F]{32}$', api_key)
        assert re.match(r'^[0-9a-fA-F]{64}$', token)
        assert re.match(r'^[0-9a-fA-F]+$', board_id)

        self.token = token
        self.board_id = board_id
        self._json_client = TrelloJson(api_key=api_key, token=token, board_id=board_id)


    # # TODO: get_card_in_list
    # async def get_card(self, card_id, card_list_id):
    #     card_list = await self.loop.run_in_executor(None, self.board.get_list, card_list_id)
    #     json_obj = await self.loop.run_in_executor(None, self.client.fetch_json,
    #                                                '/boards/' + self.board_id + '/cards/' + str(card_id))
    #     return await self.loop.run_in_executor(None, Card.from_json, card_list, json_obj)

    async def get_webhooks(self) -> List[TrelloWebHook]:
        """
        Get Webhooks for Token
        """
        response = await self._json_client.get_webhooks()
        return [TrelloWebHook.parse_obj(wh) for wh in response]

    async def del_webhook(self, wh_id: str) -> bool:
        """
        :param wh_id: ID of the webhook to retrieve. Pattern: ^[0-9a-fA-F]{32}$
        """
        assert re.match(r'^[0-9a-fA-F]+$', wh_id)
        response = await self._json_client.del_webhook(wh_id)
        if "error" in response:
            return False
        return True

    async def set_webhook(self, callback_url: str, description: str = "", id_model: str = None) -> TrelloWebHook:
        """
        :param callback_url: A valid URL that is reachable with a HEAD and POST request.
        :param description: A string with a length from 0 to 16384.
        :param id_model: ID of the model to be monitored. Pattern: ^[0-9a-fA-F]{32}$
        """
        response = await self._json_client.set_webhook(callback_url, description, id_model)

        if "error" in response:
            raise TrelloException(response["message"])

        return TrelloWebHook.parse_obj(response)


    async def create_card(self, id_list, name: str = "", desc: str = "", due: str = None, pos = "top", **kwargs) -> TrelloCard:
        """
        :param id_list: The ID of the list the card should be created in. Pattern: ^[0-9a-fA-F]{32}$
        :param name: The name for the card
        :param desc: The description for the card
        :param due: A due date for the card. Format: date
        :param pos: The position of the new card. top, bottom, or a positive float
        :param kwargs:
        """
        # assert re.match(r'^[0-9a-fA-F]+$', id_list)
        assert pos in ["top", "bottom"] or type(pos) == float
        if not due:
            due = str(datetime.today())

        response = await self._json_client.create_card(id_list, name, desc, due, pos, **kwargs)

        if "error" in response:
            raise TrelloException(response["message"])

        return TrelloCard.parse_obj(response)


    async def get_card(self, card_id: str) -> TrelloCard:
        """
        :param card_id: The ID of the Card. Pattern: ^[0-9a-fA-F]{32}$
        """
        # assert re.match(r'^[0-9a-fA-F]+$', card_id)

        response = await self._json_client.get_card(card_id)

        if "error" in response:
            raise TrelloException(response["message"])

        return TrelloCard.parse_obj(response)

    async def update_card(self, card_id, **kwagrs) -> TrelloCard:
        """
        :param card_id: The ID of the Card. Pattern: ^[0-9a-fA-F]{32}$
        """
        # assert re.match(r'^[0-9a-fA-F]+$', card_id)
        response = await self._json_client.update_card(card_id)

        if "error" in response:
            raise TrelloException(response["message"])

        return TrelloCard.parse_obj(response)

        # new_title = "🔄 " + str(card_short_id) + " " + title
        # card = await self.get_card(card_id)
        #
        # if card:
        #     await self.loop.run_in_executor(None, card.set_name, new_title)
        #     await self.loop.run_in_executor(None, card.set_description, txt)
        #
        #     if card.labels and len(card.labels) > 0:
        #         for la in card.labels:
        #             await self.loop.run_in_executor(None, card.remove_label, la)
        #     if lab:
        #         await self.loop.run_in_executor(None, card.add_label, lab)
        #
        # return card, lab

    async def get_lists(self, **kwargs) -> List[TrelloList]:

        response = await self._json_client.get_lists(**kwargs)

        if "error" in response:
            raise TrelloException(response["message"])

        return [TrelloList.parse_obj(lst) for lst in response]

    async def add_member(self, card_id, value) -> List[Member]:
        """
        :param card_id: The ID of the Card. Pattern: ^[0-9a-fA-F]{32}$
        :param value: The ID of the Member to add to the card. Pattern: ^[0-9a-fA-F]{32}$
        :return:
        """
        response = await self._json_client.add_member(card_id, value)

        if "error" in response:
            raise TrelloException(response["message"])

        return [Member.parse_obj(m) for m in response]



    # async def update_card_status(self, obj: Display):
    #     # TODO: лишний запрос в трелло
    #     card = await self.get_card(obj.entities.card.id)
    #
    #     if obj.entities.member_creator.id not in card.id_members:
    #         await self.add_member(card.id, obj.entities.member_creator.id)
    #
    #     if obj.entities.list_after.id == Const_Trello_Lists.DONE:
    #         new_title = "✅" + re.sub("[" + re.escape("🆘✅🔄" + "]"), "", card.name)
    #         await self.update_card(card.id, due_complete=True, title=new_title)
    #
    #     if obj.entities.list_before.id == Const_Trello_Lists.DONE:
    #         new_title = "🔄" + re.sub("[" + re.escape("🆘✅🔄" + "]"), "", card.name)
    #         await self.update_card(card.id, due_complete=False, title=new_title)

