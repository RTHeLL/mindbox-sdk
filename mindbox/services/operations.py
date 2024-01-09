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
        self.uri = self.__get_uri(type_)

    @staticmethod
    def __get_uri(type_):
        return f"operations/{type_}"

    def register_client(self, operation: str, **payload) -> RegistrationResponse:
        return RegistrationResponse(**self.request("POST", self.uri, operation=operation, payload=payload))

    def update_client(self, operation: str, **payload) -> None:
        return self.request("POST", self.uri, operation=operation, payload=payload)

    def get_client(self, operation: str, **payload) -> Dict[str, Any]:
        return self.request("POST", self.uri, operation=operation, payload=payload)

    def bulk_import_client(
        self,
        operation: str,
        clients: List[Dict[str, Any]],
        source_action_template: str,
        edit_action_template: str,
        csv_code_page: str = "65001",
        csv_column_delimiter: str = ";",
        csv_text_qualifier: str = '"',
        params: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Метод для пакетного импорта клиентов.

        Параметры:
         - operation (str): Тип операции для импорта клиентов.
         - clients (List[Dict[str, Any]]): Список словарей, каждый словарь представляет данные одного клиента.
         - source_action_template (str): Шаблон действия регистрации клиента.
         - edit_action_template (str): Шаблон действия редактирования клиента.
         - csv_code_page (str, опционально): Идентификатор кодовой страницы Windows для CSV-файла.
           По умолчанию '65001' (UTF-8).
         - csv_column_delimiter (str, опционально): Символ, используемый для разделения колонок в CSV-файле.
           По умолчанию ';'.
         - csv_text_qualifier (str, опционально): Символ, опционально добавляемый в начале и в конце значения колонки
           в CSV-файле.
         - params (Optional[Dict[str, Any]], опционально): Дополнительные параметры запроса.

        Возвращает:
         - None

        Примечания:
         - Максимальный размер принимаемого файла - 200 МБ. При необходимости загрузки большего объема данных,
           данные нужно разбить на несколько файлов.
         - Поддерживается формат gzip для передачи данных.
           Для использования необходимо, чтобы веб-сервер вернул заголовок Content-Encoding: gzip.
           Файл должен быть прикреплен в бинарном виде.

        Подробнее: https://developers.mindbox.ru/docs/customers-import-v3
        """

        base_params = {
            "csvCodePage": csv_code_page,
            "csvColumnDelimiter": csv_column_delimiter,
            "csvTextQualifier": csv_text_qualifier,
            "SourceActionTemplate": source_action_template,
            "editActionTemplate": edit_action_template,
        }

        if params:
            base_params.update(params)

        keys = clients[0].keys()

        f = StringIO()
        dict_writer = csv.DictWriter(f, keys, delimiter=';')
        dict_writer.writeheader()
        dict_writer.writerows(clients)

        return self.request(
            "POST",
            self.__get_uri("bulk"),
            operation=operation,
            params=base_params,
            headers={
                "Accept": "application/json",
                "Content-Type": "text/csv;charset=utf-8",
            },
            data=f.getvalue(),
        )
