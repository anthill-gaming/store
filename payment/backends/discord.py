from .base import BasePaymentBackend
import os


class DiscordBackend(BasePaymentBackend):
    def __init__(self, client_id, client_secret, sandbox=False):
        super().__init__(sandbox)
        self.client_id = os.getenv('DISCORD_CLIENT_ID', client_id)
        self.client_secret = os.getenv('DISCORD_CLIENT_SECRET', client_secret)

    async def create_order(self, order, **kwargs) -> dict:
        pass
