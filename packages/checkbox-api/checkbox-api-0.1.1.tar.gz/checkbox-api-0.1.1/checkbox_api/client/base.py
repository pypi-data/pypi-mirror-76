import logging
from abc import ABC, abstractmethod
from typing import Optional

from httpx import Response

from checkbox_api.consts import API_VERSION, BASE_API_URL, DEFAULT_REQUEST_TIMEOUT
from checkbox_api.exceptions import CheckBoxAPIError, CheckBoxAPIValidationError, CheckBoxError
from checkbox_api.methods.base import AbstractMethod
from checkbox_api.storage.simple import SessionStorage

logger = logging.getLogger(__name__)


class BaseCheckBoxClient(ABC):
    def __init__(
        self,
        base_url: str = BASE_API_URL,
        requests_timeout: int = DEFAULT_REQUEST_TIMEOUT,
        api_version: str = API_VERSION,
        storage: Optional[SessionStorage] = None,
    ) -> None:
        self.base_url = base_url
        self.api_version = api_version
        self.timeout = requests_timeout
        self.storage = storage or SessionStorage()

    @abstractmethod
    def emit(self, storage: SessionStorage, method: AbstractMethod):
        pass

    @classmethod
    def _check_response(cls, response: Response):
        if response.status_code >= 500:
            raise CheckBoxError(
                f"Failed to make request [status={response.status_code}, text={response.text!r}]"
            )
        if response.status_code == 422:
            raise CheckBoxAPIValidationError(status=response.status_code, content=response.json())
        if response.status_code >= 400:
            raise CheckBoxAPIError(status=response.status_code, content=response.json())
