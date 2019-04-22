from .base import BasePaymentBackend


class AppstoreBackend(BasePaymentBackend):
    def __init__(self, sandbox=False):
        super().__init__(sandbox)

    async def create_order(self, order: "store.model.Order", **kwargs) -> dict:
        pass
