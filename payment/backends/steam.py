from .base import BasePaymentBackend
import os


class SteamBackend(BasePaymentBackend):
    def __init__(self, game_id, app_ticket_key, sandbox=False):
        super().__init__(sandbox)
        self.game_id = os.getenv('STEAM_GAME_ID', game_id)
        self.app_ticket_key = os.getenv('STEAM_APP_TICKET_KEY', app_ticket_key)

    async def create_order(self, order, **kwargs) -> dict:
        pass
