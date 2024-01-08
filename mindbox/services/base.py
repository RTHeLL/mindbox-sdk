from abc import ABC
from typing import Dict, Any, Optional

import requests

from mindbox.exceptions import ErrorDetail, ValidationError


class BaseMindboxAPIService(ABC):
    BASE_URI = "https://api.mindbox.ru/v3/"

    def __init__(
        self,
        endpoint_id: str,
        secret_key: Optional[str] = None,
        device_uuid: Optional[str] = None,
        type_: str = "sync",
    ) -> None:
        if not isinstance(type_, str) or type_ not in ["sync", "async"]:
            raise ValueError('type_ must be "sync" or "async"')

        self.client = requests.Session()

        self.endpoint_id = endpoint_id

        if secret_key:
            self.client.headers.update(
                {
                    "Authorization": f'Mindbox secretKey="{secret_key}"',
                },
            )

        self.device_uuid = device_uuid

    def request(
        self,
        method: str,
        uri: str,
        operation: str,
        params: Optional[Dict[str, Any]] = None,
        payload: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        base_params = {
            "operation": operation,
            "endpointId": self.endpoint_id,
        }

        if self.device_uuid:
            params["deviceUUID"] = self.device_uuid

        if payload is None:
            payload = {}

        if params:
            base_params.update(params)

        response = self.client.request(method, self.BASE_URI + uri, params=base_params, json=payload, **kwargs)

        if response.status_code == 404:
            raise ValueError(*response)

        return response.json()

    def validate_payload(self, payload: Dict[str, Any], types) -> bool:
        errors = list()

        if isinstance(payload, list):
            for i in payload:
                self.validate_payload(i, types)
        else:
            for field, value in payload.items():
                _type = types[field]

                if not isinstance(value, _type):
                    errors.append(ErrorDetail(f"must be of type {_type}", field))

        if errors:
            raise ValidationError(errors)

        return True
