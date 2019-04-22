from .base import BasePaymentBackend


class SteamBackend(BasePaymentBackend):
    def __init__(self, sandbox=False):
        super().__init__(sandbox)

    async def create_order(self, order: "store.model.Order", **kwargs) -> dict:
        pass
