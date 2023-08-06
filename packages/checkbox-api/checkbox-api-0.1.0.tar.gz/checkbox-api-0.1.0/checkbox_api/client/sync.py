import logging
import time
from typing import Any, Dict, List, Optional, Set

from checkbox_api.client.base import BaseCheckBoxClient
from checkbox_api.consts import DEFAULT_REQUESTS_RELAX
from checkbox_api.exceptions import CheckBoxError, StatusException
from checkbox_api.methods import cashier, receipts, shifts
from checkbox_api.methods.base import AbstractMethod, BaseMethod
from checkbox_api.storage.simple import SessionStorage
from httpx import Client, HTTPError

logger = logging.getLogger(__name__)


class CheckBoxClient(BaseCheckBoxClient):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._session = Client()

    def emit(self, call: AbstractMethod, storage: Optional[SessionStorage] = None):
        storage = storage or self.storage

        url = f"{self.base_url}/api/v{self.api_version}/{call.uri}"
        try:
            response = self._session.request(
                method=call.method.name,
                url=url,
                timeout=self.timeout,
                params=call.query,
                headers={**storage.headers, **call.headers},
                json=call.payload,
            )
        except HTTPError as e:
            raise CheckBoxError(e)

        self._check_response(response=response)
        result = call.parse_response(storage=storage, response=response)

        return result

    def __call__(self, *args, **kwargs):
        return self.emit(*args, **kwargs)

    def refresh_info(self, storage: Optional[SessionStorage] = None):
        self(cashier.GetMe(), storage=storage)
        self(cashier.GetActiveShift(), storage=storage)

    def authenticate(self, login: str, password: str, storage: Optional[SessionStorage] = None):
        self(cashier.SignIn(login=login, password=password), storage=storage)
        self.refresh_info(storage=storage)

    def authenticate_signature(self, signature: bytes, storage: Optional[SessionStorage] = None):
        self(cashier.SignInSignature(signature=signature), storage=storage)
        self.refresh_info(storage=storage)

    def authenticate_pin_code(self, pin_code: str, storage: Optional[SessionStorage] = None):
        self(cashier.SignInPinCode(pin_code=pin_code), storage=storage)
        self.refresh_info(storage=storage)

    def get_shifts(
        self,
        statuses: Optional[List[str]] = None,
        limit: int = 10,
        storage: Optional[SessionStorage] = None,
    ):
        get_shift = shifts.GetShifts(statuses=statuses, limit=limit)
        while (shifts_result := self(get_shift, storage=storage))["results"]:
            get_shift.resolve_pagination(shifts_result).shift_next_page()
            yield from shifts_result["results"]

    def _wait_status(
        self,
        method: BaseMethod,
        expected_value: Set[Any],
        field: str = "status",
        relax: int = DEFAULT_REQUESTS_RELAX,
        timeout: Optional[int] = None,
        storage: Optional[SessionStorage] = None,
    ):
        logger.info("Wait until %r will be changed to one of %s", field, expected_value)
        initial = time.monotonic()
        while (result := self(method, storage=storage))[field] not in expected_value:
            if timeout is not None and time.monotonic() > initial + timeout:
                logger.error("Status did not changed in required time")
                break
            time.sleep(relax)

        if result[field] not in expected_value:
            raise ValueError(
                f"Object did not change field {field!r} "
                f"to one of expected values {expected_value} (actually {result[field]!r}) "
                f"in {time.monotonic() - initial} seconds"
            )

        logger.info(
            "Status changed in %s seconds to %r", time.monotonic() - initial, result[field],
        )
        return result

    def create_shift(
        self,
        relax: int = DEFAULT_REQUESTS_RELAX,
        timeout: Optional[int] = None,
        storage: Optional[SessionStorage] = None,
    ):
        storage = storage or self.storage
        self.refresh_info(storage=storage)
        if storage.shift is not None:
            logger.info("Shift is already opened %s", storage.shift["id"])
            return storage.shift

        shift = self(shifts.CreateShift(), storage=storage)
        logger.info("Created shift %s", shift["id"])

        shift = self._wait_status(
            shifts.GetShift(shift_id=shift["id"]),
            storage=storage,
            relax=relax,
            field="status",
            expected_value={"OPENED", "CLOSED"},
            timeout=timeout,
        )
        if shift["status"] == "CLOSED":
            initial_transaction = shift["initial_transaction"]
            raise StatusException(
                "Shift can not be opened in due to transaction status moved to "
                f"{initial_transaction['status']!r}: {initial_transaction['response_status']!r} "
                f"{initial_transaction['response_error_message']!r}"
            )
        return shift

    def close_shift(
        self,
        relax: int = DEFAULT_REQUESTS_RELAX,
        timeout: Optional[int] = None,
        storage: Optional[SessionStorage] = None,
    ):
        storage = storage or self.storage
        self.refresh_info(storage=storage)
        if storage.shift is None:
            logger.info("Shift is already closed")
            return storage.shift

        shift = self(shifts.CloseShift(), storage=storage)
        logger.info("Trying to close shift %s", shift["id"])

        shift = self._wait_status(
            shifts.GetShift(shift_id=shift["id"]),
            storage=storage,
            relax=relax,
            field="status",
            expected_value={"OPENED", "CLOSED"},
            timeout=timeout,
        )
        if shift["status"] == "OPENED":
            initial_transaction = shift["initial_transaction"]
            raise StatusException(
                "Shift can not be closed in due to transaction status moved to "
                f"{initial_transaction['status']!r}: {initial_transaction['response_status']!r} "
                f"{initial_transaction['response_error_message']!r}"
            )
        return shift["z_report"]

    def create_receipt(
        self,
        goods: List[Dict[str, Any]],
        payments: List[Dict[str, Any]],
        delivery: Optional[Dict[str, Any]] = None,
        relax: int = DEFAULT_REQUESTS_RELAX,
        timeout: Optional[int] = None,
        storage: Optional[SessionStorage] = None,
    ):
        receipt = self(
            receipts.CreateReceipt(goods=goods, payments=payments, delivery=delivery),
            storage=storage,
        )
        logger.info("Trying create receipt %s", receipt["id"])

        shift = self._wait_status(
            receipts.GetReceipt(receipt_id=receipt["id"]),
            storage=storage,
            relax=relax,
            field="status",
            expected_value={"DONE", "ERROR"},
            timeout=timeout,
        )
        if shift["status"] == "ERROR":
            initial_transaction = shift["transaction"]
            raise StatusException(
                "Receipt can not be created in due to transaction status moved to "
                f"{initial_transaction['status']!r}: {initial_transaction['response_status']!r} "
                f"{initial_transaction['response_error_message']!r}"
            )
        return shift
