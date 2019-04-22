from .base import BasePaymentBackend


class XsollaBackend(BasePaymentBackend):
    def __init__(self, project_id, sandbox=False):
        super().__init__(sandbox)
        self.project_id = project_id

    async def create_order(self, order: "store.model.Order", **kwargs) -> dict:
        pass
