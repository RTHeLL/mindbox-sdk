from typing import Optional

from mindbox.services.operations import MindboxOperationsService


class MindboxClient:
    def __init__(
        self,
        endpoint_id: str,
        secret_key: Optional[str] = None,
        device_uuid: Optional[str] = None,
        type_: str = "sync",
    ) -> None:
        self.operations = MindboxOperationsService(endpoint_id, secret_key, device_uuid, type_)
