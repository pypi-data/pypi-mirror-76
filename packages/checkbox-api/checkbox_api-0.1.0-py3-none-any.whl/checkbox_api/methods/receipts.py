from typing import Any, Dict, List, Optional

from checkbox_api.methods.base import BaseMethod, HTTPMethod, PaginationMixin
from checkbox_api.storage.simple import SessionStorage
from httpx import Response


class GetReceipts(PaginationMixin, BaseMethod):
    uri = "receipts"


class GetReceipt(BaseMethod):
    def __init__(self, receipt_id: str):
        self.receipt_id = receipt_id

    @property
    def uri(self) -> str:
        return f"receipts/{self.receipt_id}"


class CreateReceipt(BaseMethod):
    method = HTTPMethod.POST
    uri = "receipts/sell"

    def __init__(
        self,
        goods: List[Dict[str, Any]],
        payments: List[Dict[str, Any]],
        delivery: Optional[Dict[str, Any]] = None,
    ):
        self.goods = goods
        self.payments = payments
        self.delivery = delivery

    @property
    def payload(self):
        payload = super().payload
        payload["goods"] = self.goods
        payload["payments"] = self.payments
        if self.delivery:
            payload["delivery"] = self.delivery
        return payload

    def parse_response(self, storage: SessionStorage, response: Response):
        result = super().parse_response(storage=storage, response=response)
        storage.shift = result["shift"]
        return result


class GetReceiptVisualization(GetReceipt):
    def __init__(self, receipt_id: str, fmt: str = "text", **query):
        super().__init__(receipt_id=receipt_id)
        self.format = fmt
        self.params = query

    @property
    def query(self):
        query = super().query
        query.update(self.params)
        return query

    @property
    def uri(self) -> str:
        uri = super().uri
        return f"{uri}/{self.format}"

    def parse_response(self, storage: SessionStorage, response: Response):
        return response.content
