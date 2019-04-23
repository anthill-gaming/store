from .base import BasePaymentBackend
import os


class XsollaBackend(BasePaymentBackend):
    def __init__(self, project_id, project_key, merchant_id, api_key, sandbox=False):
        super().__init__(sandbox)
        self.project_id = project_id
        self.project_key = os.getenv('XSOLLA_PROJECT_KEY', project_key)
        self.merchant_id = os.getenv('XSOLLA_MERCHANT_ID', merchant_id)
        self.api_key = os.getenv('XSOLLA_API_KEY', api_key)

    async def create_order(self, order, **kwargs) -> dict:
        pass
