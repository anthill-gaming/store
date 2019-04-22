class BasePaymentBackend:
    def __init__(self, sandbox=False):
        self.sandbox = sandbox

    async def create_order(self, order: "store.model.Order", **kwargs) -> dict:
        raise NotImplementedError
