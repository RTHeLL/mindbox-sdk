import csv
from io import StringIO
from typing import Any, Dict, Optional, List

from mindbox.services.base import BaseMindboxAPIService
from mindbox.types.operations import RegistrationResponse


class MindboxOperationsService(BaseMindboxAPIService):
    def __init__(
        self,
        endpoint_id: str,
        secret_key: Optional[str] = None,
        device_uuid: Optional[str] = None,
        type_: str = "sync",
    ) -> None:
        """
        Initializes a new instance of the class.

        Args:
            secret_key (str): The secret key used for authentication.
            type_ (str, optional): The type of the operation (sync or async). Defaults to 'sync'.

        Returns:
            None
        """

        super().__init__(endpoint_id, secret_key, device_uuid, type_)
        self.uri = f"operations/{type_}"

    def register_client(self, operation: str, **payload) -> RegistrationResponse:
        return RegistrationResponse(**self.request("POST", self.uri, operation=operation, payload=payload))

    def update_client(self, operation: str, **payload) -> None:
        return self.request("POST", self.uri, operation=operation, payload=payload)

    def get_client(self, operation: str, **payload) -> Dict[str, Any]:
        return self.request("POST", self.uri, operation=operation, payload=payload)
