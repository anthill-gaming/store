from .base import BasePaymentBackend


class MailruBackend(BasePaymentBackend):
    def __init__(self, sandbox=False):
        super().__init__(sandbox)

    async def create_order(self, order, **kwargs) -> dict:
        pass
